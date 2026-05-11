# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
import FreeCAD as App
import FreeCADGui as Gui
import os
from PySide import QtGui, QtWidgets
from collections import deque
from .._resources import get_command_icon

from ..furniture_design.order import Order
from ..furniture_design.cabinets.cabinet import Cabinet
from ..furniture_design.cabinets.features import FEATURES
from ..furniture_design.cabinets.architectures import CABINETS
from .cmd_make_element import get_elements_registry
from ..furniture_design.design_engine import load_default_rules, DEFAULT_RULES_PATH
from ..manufacturing.generate_files import generate_manufacturing_files


_ROT_STEPS_TABLE = None


def _mat_mul3(a, b):
    return (
        a[0] * b[0] + a[1] * b[3] + a[2] * b[6],
        a[0] * b[1] + a[1] * b[4] + a[2] * b[7],
        a[0] * b[2] + a[1] * b[5] + a[2] * b[8],
        a[3] * b[0] + a[4] * b[3] + a[5] * b[6],
        a[3] * b[1] + a[4] * b[4] + a[5] * b[7],
        a[3] * b[2] + a[4] * b[5] + a[5] * b[8],
        a[6] * b[0] + a[7] * b[3] + a[8] * b[6],
        a[6] * b[1] + a[7] * b[4] + a[8] * b[7],
        a[6] * b[2] + a[7] * b[5] + a[8] * b[8],
    )


def _step_rot_matrix(axis):
    # Matches placement_from_position_list() semantics in cmd_explode_cabinet.py:
    # one recorded "rotate axis" corresponds to +90° in FreeCAD placement space.
    if axis == "x":
        return (
            1, 0, 0,
            0, 0, -1,
            0, 1, 0,
        )
    if axis == "y":
        return (
            0, 0, 1,
            0, 1, 0,
            -1, 0, 0,
        )
    if axis == "z":
        return (
            0, -1, 0,
            1, 0, 0,
            0, 0, 1,
        )
    raise ValueError(f"Unsupported axis: {axis}")


def _build_rot_steps_table():
    identity = (
        1, 0, 0,
        0, 1, 0,
        0, 0, 1,
    )
    table = {identity: []}
    queue = deque([identity])
    axes = ("x", "y", "z")

    while queue and len(table) < 24:
        current = queue.popleft()
        current_steps = table[current]
        for axis in axes:
            nxt = _mat_mul3(_step_rot_matrix(axis), current)
            if nxt not in table:
                table[nxt] = current_steps + [["rotate", axis]]
                queue.append(nxt)

    return table


def _snap_axis_vector(v, tol=1e-5):
    coords = (v.x, v.y, v.z)
    idx = max(range(3), key=lambda i: abs(coords[i]))
    if abs(abs(coords[idx]) - 1.0) > tol:
        return None
    if any(abs(coords[i]) > tol for i in range(3) if i != idx):
        return None

    out = [0, 0, 0]
    out[idx] = 1 if coords[idx] >= 0 else -1
    return tuple(out)


def _rotation_to_discrete_matrix(rot):
    ex = _snap_axis_vector(rot.multVec(App.Vector(1, 0, 0)))
    ey = _snap_axis_vector(rot.multVec(App.Vector(0, 1, 0)))
    ez = _snap_axis_vector(rot.multVec(App.Vector(0, 0, 1)))
    if not ex or not ey or not ez:
        return None

    # Columns are rotated basis vectors.
    return (
        ex[0], ey[0], ez[0],
        ex[1], ey[1], ez[1],
        ex[2], ey[2], ez[2],
    )


def freecad_placement_to_position_list(placement):
    """Convert FreeCAD Placement to position_list format used by elements."""
    position_list = []
    base = placement.Base
    rot = placement.Rotation
    global _ROT_STEPS_TABLE
    if _ROT_STEPS_TABLE is None:
        _ROT_STEPS_TABLE = _build_rot_steps_table()

    discrete_rot = _rotation_to_discrete_matrix(rot)
    if discrete_rot in _ROT_STEPS_TABLE:
        position_list.extend(_ROT_STEPS_TABLE[discrete_rot])
    else:
        App.Console.PrintWarning(
            "[WARN] cmd_generate_from_geometry.py: "
            "could not map placement rotation to 90-degree steps exactly; using Euler fallback.\n"
        )
        # Fallback keeps behavior for non-orthogonal placements.
        try:
            yaw, pitch, roll = rot.toEuler()
            for axis, angle in [("z", yaw), ("y", pitch), ("x", roll)]:
                steps = int(round(angle / 90.0)) % 4
                for _ in range(abs(steps)):
                    position_list.append(["rotate", axis])
        except Exception:
            pass

    # Extract translations
    if abs(base.x) > 1e-9:
        position_list.append(["move", "x", base.x])
    if abs(base.y) > 1e-9:
        position_list.append(["move", "y", base.y])
    if abs(base.z) > 1e-9:
        position_list.append(["move", "z", base.z])

    return position_list


def freecad_box_to_element(fc_box):
    """Convert FreeCAD Part::Box to Element object."""
    if not hasattr(fc_box, "ElementType"):
        return None

    elements_registry = get_elements_registry()
    element_type = fc_box.ElementType
    element_def = elements_registry.get(element_type)

    if not element_def:
        App.Console.PrintWarning(
            f"[WARN] Element type '{element_type}' not found in registry, skipping {fc_box.Label}\n"
        )
        return None

    # Get dimensions from FreeCAD object
    length = fc_box.Length.Value
    width = fc_box.Width.Value
    height = fc_box.Height.Value  # This is thickness

    # Build constructor arguments
    ctor_keys = element_def["constructor"]
    ctor_args = {
        "label": fc_box.Label,
        "length": length,
        "width": width,
    }
    # Only add thick if it's in the constructor keys (Pfl doesn't accept it)
    if "thick" in ctor_keys:
        ctor_args["thick"] = height

    # Add element-specific properties (e.g., cant_L1, cant_L2 for BoardPal)
    for prop in fc_box.PropertiesList:
        if fc_box.getGroupOfProperty(prop) == "Element":
            prop_name = prop
            prop_value = getattr(fc_box, prop)
            # Convert FreeCAD Quantity to float if needed
            if hasattr(prop_value, "Value"):
                prop_value = prop_value.Value
            # Only add if it's in constructor keys
            if prop_name in ctor_keys:
                ctor_args[prop_name] = prop_value

    # Create element object
    element_cls = element_def["class"]
    try:
        element = element_cls(**ctor_args)
    except Exception as e:
        App.Console.PrintError(
            f"[ERROR] Failed to create element {element_type} '{fc_box.Label}': {e}\n"
        )
        return None

    # Apply positioning from FreeCAD Placement
    position_list = freecad_placement_to_position_list(fc_box.Placement)
    element.position_list = position_list

    # Preserve editable element properties that are not constructor arguments.
    for prop in fc_box.PropertiesList:
        if fc_box.getGroupOfProperty(prop) != "Element" or prop == "ElementType":
            continue

        prop_value = getattr(fc_box, prop)
        if hasattr(prop_value, "Value"):
            prop_value = prop_value.Value

        setattr(element, prop, prop_value)
        if prop == "Material":
            element.material = prop_value
        elif prop == "ManufacturingRoute":
            setattr(element, "manufacturing_route", prop_value)

    return element


def freecad_document_to_order(doc):
    """Convert FreeCAD document to Order object by reading exploded geometry."""
    # Find OrderVar spreadsheet for global order data
    spreadsheet = None
    for obj in doc.Objects:
        if obj.TypeId == "Spreadsheet::Sheet" and obj.Label == "OrderVar":
            spreadsheet = obj
            break

    # Build customer_data dict from spreadsheet using centralized definition
    customer_data = {}
    if spreadsheet:
        try:
            aliases = getattr(spreadsheet, "Aliases", {})
            # Import here to avoid circular imports at module level
            from ..furniture_design.order import get_order_param_names
            # Prefer dynamic alias enumeration if available; otherwise use centralized list
            alias_names = list(aliases.keys()) if aliases else None
            alias_iter = alias_names if alias_names else get_order_param_names()

            for alias_name in alias_iter:
                try:
                    val = spreadsheet.get(alias_name)
                    if hasattr(val, "Value"):
                        val = val.Value
                    # Convert FreeCAD Quantity to appropriate type
                    if val is not None:
                        customer_data[alias_name] = val
                except Exception as e:
                    pass
        except Exception as e:
            pass

    # Create Order object
    order = Order(customer_data)

    # Load default rules
    rules = load_default_rules(DEFAULT_RULES_PATH)

    # Find all App::Part objects that represent exploded cabinets (Assy_*)
    for obj in doc.Objects:
        if obj.TypeId == "App::Part" and hasattr(obj, "CabinetType"):
            # Get cabinet dimensions from Part properties
            height = getattr(obj, "Height", 0)
            width = getattr(obj, "Width", 0)
            depth = getattr(obj, "Depth", 0)

            # Convert FreeCAD Quantity to float if needed
            if hasattr(height, "Value"):
                height = height.Value
            if hasattr(width, "Value"):
                width = width.Value
            if hasattr(depth, "Value"):
                depth = depth.Value

            # Create a generic Cabinet (not using factory)
            cabinet = Cabinet(obj.Label, height, width, depth, rules)

            # Clear default elements - we'll populate from FreeCAD geometry
            cabinet.elements_list = []

            # Read elements from FreeCAD Part's Group
            if hasattr(obj, "Group"):
                for fc_obj in obj.Group:
                    if fc_obj.TypeId == "Part::Box" and hasattr(fc_obj, "ElementType"):
                        element = freecad_box_to_element(fc_obj)
                        if element:
                            cabinet.append(element)

            # Read accessories from cabinet properties
            if hasattr(obj, "AccessoryTypes") and hasattr(obj, "AccessoryCounts"):
                from ..furniture_design.cabinets.elements.accessory import Accessory
                accessory_types = obj.AccessoryTypes
                accessory_counts = obj.AccessoryCounts
                for acc_type, acc_count in zip(accessory_types, accessory_counts):
                    accessory = Accessory(acc_type, acc_count)
                    cabinet.append(accessory)

            # Apply cabinet positioning from Part Placement
            position_list = freecad_placement_to_position_list(obj.Placement)
            cabinet.position_list = position_list

            # Add cabinet to order
            order.append(cabinet)

    return order


def generate_from_geometry():
    """Main function to generate manufacturing files from FreeCAD geometry."""
    doc = App.ActiveDocument
    if not doc:
        QtGui.QMessageBox.warning(None, "Error", "No active document.")
        return

    # Check if document has exploded cabinets
    has_cabinets = False
    for obj in doc.Objects:
        if obj.TypeId == "App::Part" and hasattr(obj, "CabinetType"):
            has_cabinets = True
            break

    if not has_cabinets:
        QtGui.QMessageBox.warning(
            None,
            "No Cabinets Found",
            "No exploded cabinets found in the document.\n"
            "Please use 'Generate Cabinet' command first."
        )
        return

    if not doc.FileName:
        QtGui.QMessageBox.warning(
            None,
            "Cabinet Generator",
            "Please save the FreeCAD file before running."
        )
        return

    fc_path = doc.FileName
    project_dir = os.path.dirname(fc_path)
    basename = os.path.splitext(os.path.basename(fc_path))[0]

    # Create output folder
    output_dir = os.path.join(project_dir, basename + "_output")
    os.makedirs(output_dir, exist_ok=True)

    try:
        # Read FreeCAD geometry and create Order directly
        App.Console.PrintMessage("Reading exploded cabinets from FreeCAD document...\n")
        order = freecad_document_to_order(doc)

        App.Console.PrintMessage(f"Found {len(order.cabinets_list)} cabinet(s)\n")

        # Generate manufacturing files
        App.Console.PrintMessage(f"Generating manufacturing files to: {output_dir}\n")
        elements_registry = get_elements_registry()
        context = {
            "elements_registry": elements_registry,
            "features_registry": FEATURES,
            "cabinets_registry": CABINETS,
        }
        generate_manufacturing_files(order, output_dir, context["elements_registry"])

        QtGui.QMessageBox.information(
            None,
            "Cabinet Generator",
            f"Generation complete!\n\nFiles saved in:\n{output_dir}"
        )
    except Exception as e:
        App.Console.PrintError(f"Error: {str(e)}\n")
        import traceback
        App.Console.PrintError(traceback.format_exc())
        QtGui.QMessageBox.critical(
            None,
            "Error",
            f"Failed to generate manufacturing files:\n{str(e)}"
        )


class GenerateFromGeometryCommand:
    def GetResources(self):
        return {
            "Pixmap": get_command_icon("icon_AIGenFurniture"),
            "MenuText": "Generate from Geometry",
            "ToolTip": "Generate manufacturing files from exploded cabinets in FreeCAD"
        }

    def IsActive(self):
        return App.ActiveDocument is not None

    def Activated(self):
        generate_from_geometry()


# Register command
Gui.addCommand("Generate_From_Geometry", GenerateFromGeometryCommand())
