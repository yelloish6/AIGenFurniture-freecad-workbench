# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
import FreeCAD as App
import FreeCADGui as Gui
import os
from .._resources import get_command_icon

from . import resources
from ..furniture_design.design_engine import load_default_rules, DEFAULT_RULES_PATH
from ..furniture_design.cabinets.architectures import get_cabinet_factory

def is_valid_cabinet_object(obj):
    if obj is None:
        return False
    if getattr(obj, "TypeId", "") != "Part::Box":
        return False
    if not hasattr(obj, "CabinetType"):
        return False
    cab_type = getattr(obj, "CabinetType", "")
    return bool(cab_type) and get_cabinet_factory(cab_type) is not None

def apply_movements_to_part(part, position_list):
    pl = App.Placement()  # identity
    for movement in position_list:
        if movement[0] == "move":
            axis, offset = movement[1], movement[2]
            if axis == "x":
                step = App.Placement(App.Vector(offset, 0, 0), App.Rotation())
            elif axis == "y":
                step = App.Placement(App.Vector(0, offset, 0), App.Rotation())
            elif axis == "z":
                step = App.Placement(App.Vector(0, 0, offset), App.Rotation())
        elif movement[0] == "rotate":
            axis = movement[1]
            if axis == "x":
                step = App.Placement(App.Vector(), App.Rotation(App.Vector(1, 0, 0), -90))
            elif axis == "y":
                step = App.Placement(App.Vector(), App.Rotation(App.Vector(0, 1, 0), -90))
            elif axis == "z":
                step = App.Placement(App.Vector(), App.Rotation(App.Vector(0, 0, 1), -90))
        else:
            continue

        pl = pl.multiply(step)  # sequential like STL
    part.Placement = pl

def placement_from_position_list(position_list):
    """
    Build a Placement that exactly matches STL's imperative transform:
    - moves add to a translation vector t (in global coords at that moment)
    - rotates are about global origin and also spin the accumulated t
    Resulting transform: x' = R x + t
    """
    t = App.Vector(0, 0, 0)          # accumulated translation
    R = App.Rotation()               # accumulated rotation (identity)

    for op, axis, *rest in position_list:
        if op == "move":
            offset = rest[0]
            if axis == "x":
                t = t.add(App.Vector(offset, 0, 0))
            elif axis == "y":
                t = t.add(App.Vector(0, offset, 0))
            elif axis == "z":
                t = t.add(App.Vector(0, 0, offset))

        elif op == "rotate":
            # build rotation matching STL (-90°)
            if axis == "x":
                Rstep = App.Rotation(App.Vector(1,0,0), 90)
            elif axis == "y":
                Rstep = App.Rotation(App.Vector(0,1,0), 90)
            elif axis == "z":
                Rstep = App.Rotation(App.Vector(0,0,1), 90)
            else:
                continue

            # IMPORTANT: rotate both the rotation and the already-accumulated translation
            t = Rstep.multVec(t)
            R = Rstep.multiply(R)

    return App.Placement(t, R)

def explode_box_to_cabinet(box):
    doc = App.ActiveDocument
    if not box:
        App.Console.PrintError("[WARNING] cmd_explode_cabinet.py: No box selected.\n")
        return

    # Get box dimensions
    height = int(box.Height.Value)
    width  = int(box.Length.Value)
    depth  = int(box.Width.Value)

    # Cabinet type property
    cab_type = getattr(box, "CabinetType", "BaseBox")

    # Rules (normally from spreadsheet / OrderVar)
    rules = load_default_rules(DEFAULT_RULES_PATH)

    factory = get_cabinet_factory(cab_type)
    if not factory:
        App.Console.PrintError(
            f"[ERROR] Unknown or inactive CabinetType '{cab_type}'. Falling back to BaseBox.\n"
        )
        factory = get_cabinet_factory("BaseBox")

    cabinet = factory(box.Label, height, width, depth, rules, box=box)

    import re
    from collections import defaultdict

# TODO rewrite the section below to use the get_feature_handler() method defined in the __init__.py for features.
    # === AUTO-APPLY BOX FEATURES ===
    feature_pattern = re.compile(r"^Feature_(\w+)_([0-9]+)_(\w+)$")
    features = defaultdict(lambda: defaultdict(dict))

    # Collect features grouped by (feature_name, index)
    for prop in box.PropertiesList:
        match = feature_pattern.match(prop)
        if not match:
            continue
        feature_name, index, param = match.groups()
        value = getattr(box, prop)
        features[feature_name][index][param] = value

    # Execute feature methods dynamically
    for feature_name, instances in features.items():
        if not hasattr(cabinet, feature_name):
            App.Console.PrintWarning(f"[WARNING] cmd_explode_cabinet.py: Cabinet has no method '{feature_name}' (skipping)\n")
            continue
        method = getattr(cabinet, feature_name)
        for index, params in instances.items():
            try:
                method(**params)
                App.Console.PrintMessage(f"[OK] Applied feature '{feature_name}' #{index} with {params}\n")
            except TypeError as e:
                App.Console.PrintError(f"[ERROR] cmd_explode_cabinet.py: Error applying feature '{feature_name}' #{index}: {e}\n")

    # ── UNDO TRANSACTION ──────────────────────────────────────────────────────
    # Open a named transaction BEFORE any document mutations so that a single
    # Ctrl+Z reverses the entire cabinet generation as one atomic undo step.
    doc.openTransaction("Generate Cabinet")
    try:
        _do_explode(doc, box, cabinet, cab_type, height, width, depth)
        doc.commitTransaction()
    except Exception as e:
        doc.abortTransaction()   # rolls back every addObject / property change
        import traceback
        App.Console.PrintError(
            f"[ERROR] cmd_explode_cabinet.py: Generation failed, changes rolled back.\n"
            f"{traceback.format_exc()}"
        )
        raise
    # ─────────────────────────────────────────────────────────────────────────


def _do_explode(doc, box, cabinet, cab_type, height, width, depth):
    """
    Performs all FreeCAD document mutations for one cabinet generation.
    Must be called inside an open transaction so that errors can be aborted.
    """
    # Create container group
    cab_group = doc.addObject("App::Part", f'Assy_{cabinet.label}')

    # Transfer cabinet properties to part
    cab_group.addProperty("App::PropertyString", "CabinetType", "Cabinet", "Type of cabinet").CabinetType = cab_type
    cab_group.addProperty("App::PropertyFloat", "Height", "Box", "Cabinet Height").Height = height
    cab_group.addProperty("App::PropertyFloat", "Width", "Box", "Cabinet Height").Width = width
    cab_group.addProperty("App::PropertyFloat", "Depth", "Box", "Cabinet Height").Depth = depth

    # Add accessories properties (parallel arrays: names + counts)
    cab_group.addProperty("App::PropertyStringList", "AccessoryTypes", "Cabinet",
                          "List of accessory types")
    cab_group.addProperty("App::PropertyIntegerList", "AccessoryCounts", "Cabinet",
                          "List of accessory counts")

    accessory_types = []
    accessory_counts = []

    # Place elements
    for elem in cabinet.elements_list:
        if elem.type in ("pal", "front", "pfl", "blat"):
            part = doc.addObject("Part::Box", elem.label)
            part.Length = elem.length
            part.Width  = elem.width
            part.Height = elem.thick

            part.addProperty("App::PropertyString", "ElementType", "Element", "Type of element")

            # Map legacy code elem.type to FreeCAD ElementType definitions
            element_type_map = {
                "pal": "BoardPal",
                "pfl": "Pfl",
                "front": "Front",
                "blat": "Countertop"
            }

            try:
                part.ElementType = element_type_map[elem.type]
            except KeyError:
                App.Console.PrintError(f"[ERROR] cmd_explode_cabinet.py: Unknown board type '{elem.type}' in cabinet {cabinet.label}\n")
                continue

            # --- Specific parameters for "pal" boards ---
            if elem.type == "pal":
                cant_names = ["cant_L1", "cant_L2", "cant_l1", "cant_l2"]
                for name, value in zip(cant_names, elem.cant_list):
                    part.addProperty("App::PropertyString", name, "Element", f"Edge {name} flag")
                    setattr(part, name, str(value))

            # Apply recorded transformations of the element (match STL)
            part.Placement = placement_from_position_list(elem.position_list)
            cab_group.addObject(part)   # ← single call (duplicate removed)

        elif elem.type == "accessory":
            accessory_types.append(elem.label)
            accessory_counts.append(int(elem.pieces))

        else:
            App.Console.PrintError(f"[ERROR] cmd_explode_cabinet.py: Unknown element type: {elem.type}\n")

    # Store accessories
    cab_group.AccessoryTypes = accessory_types
    cab_group.AccessoryCounts = accessory_counts
    cab_group.Placement = box.Placement.multiply(placement_from_position_list(cabinet.position_list))

    # Hide original box
    box.ViewObject.Visibility = False

    doc.recompute()
    App.Console.PrintMessage(f"[OK] Generated {cabinet.label} from {box.Label}.\n")


class ExplodeBoxCommand:

    def GetResources(self):
        return {
            "Pixmap": get_command_icon("icon_explode_box"),
            "MenuText": "Generate Cabinet",
            "ToolTip": "Generate cabinet structure based on the parameters of the cabinet box"
        }

    def IsActive(self):
        if App.ActiveDocument is None:
            return False
        sel = Gui.Selection.getSelection()
        if len(sel) != 1:
            return False
        return is_valid_cabinet_object(sel[0])

    def Activated(self):
        sel = Gui.Selection.getSelection()
        if len(sel) != 1 or not is_valid_cabinet_object(sel[0]):
            App.Console.PrintError(
                "[WARNING] cmd_explode_cabinet.py: Please select one valid cabinet box first.\n"
            )
            return
        explode_box_to_cabinet(sel[0])


# Register command
Gui.addCommand("Explode_Box_To_Cabinet", ExplodeBoxCommand())