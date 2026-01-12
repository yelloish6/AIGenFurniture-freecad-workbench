import FreeCAD
import FreeCADGui
import json
import os

def serialize_property_value(value):
    """Convert FreeCAD property values into JSON-serializable Python types."""

    # If it's a string, try to parse as JSON
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            return parsed
        except Exception:
            return value  # keep as plain string if not JSON

    # If it's a FreeCAD Quantity (e.g. Distance), use its Value (in mm)
    if hasattr(value, "Value"):
        return value.Value

    # Convert list/tuple to normal list
    if isinstance(value, (list, tuple)):
        return [serialize_property_value(v) for v in value]

    # For everything else, return as is (int, float, bool, etc.)
    return value

def export(doc, output_path):
    # ✅ Find the spreadsheet with Label "OrderVar"
    spreadsheet = None
    for obj in doc.Objects:
        if obj.TypeId == "Spreadsheet::Sheet" and obj.Label == "OrderVar":
            spreadsheet = obj
            break

    if not spreadsheet:
        FreeCAD.Console.PrintError("Spreadsheet with label 'OrderVar' not found.\n")
        return

    # ✅ Load global variables from spreadsheet aliases using centralized definition
    globals_dict = {}
    
    # Prefer dynamic alias enumeration if available; otherwise use centralized list
    try:
        alias_names = list(getattr(spreadsheet, "Aliases", {}).keys())
        # Import here to avoid circular imports at module level
        from AIGenFurniture.furniture_design.order import get_order_param_names
        # Use centralized list to ensure consistent ordering if dynamic enumeration fails
        alias_iter = alias_names if alias_names else get_order_param_names()
    except Exception:
        from AIGenFurniture.furniture_design.order import get_order_param_names
        alias_iter = get_order_param_names()

    for alias_name in alias_iter:
        try:
            val = spreadsheet.get(alias_name)
        except Exception:
            val = None
        # Always serialize; include empty/None as-is
        globals_dict[alias_name] = serialize_property_value(val)

    # ✅ Collect elements and group them by Std_Part parent
    part_groups = {}   # {part_obj: [element_dicts]}
    root_elements = [] # elements not inside any Std_Part

    for obj in doc.Objects:
        if obj.TypeId not in ["Part::Box"]:
            continue
        if not hasattr(obj, "ElementType"):
            continue

        # Determine parent Std_Part
        parent_part = None
        for parent in doc.Objects:
            if parent.TypeId == "App::Part" and obj in getattr(parent, "Group", []):
                parent_part = parent
                break

        placement = obj.Placement
        base = placement.Base
        rot = placement.Rotation

        # Dimensions
        if obj.TypeId == "Part::Cut":
            bb = obj.Shape.BoundBox
            width, depth, height = bb.XLength, bb.YLength, bb.ZLength
        else:
            width, depth, height = obj.Length.Value, obj.Width.Value, obj.Height.Value

        try:
            yaw, pitch, roll = rot.toEuler()
        except Exception:
            yaw = pitch = roll = 0.0

        element_type = getattr(obj, "ElementType", "Unknown")

        element = {
            "label": obj.Label,
            "element_type": element_type,
            "thick": height,
            "length": width,
            "width": depth,
        }

        # 👉 Positioning
        positioning = []
        def add_rot(axis, angle_deg):
            try:
                steps = int(round(angle_deg / 90.0)) % 4
            except Exception:
                steps = 0
            for _ in range(abs(steps)):
                positioning.append({"rotate": axis})

        add_rot("x", roll)
        add_rot("y", pitch)
        add_rot("z", yaw)

        if base.y != 0:
            positioning.append({"move": ["y", base.y]})
        if base.x != 0:
            positioning.append({"move": ["x", base.x]})
        if base.z != 0:
            positioning.append({"move": ["z", base.z]})

        element["positioning"] = positioning

        # ➕ Export all "Element" group properties
        element_props = {}
        for prop in obj.PropertiesList:
            group = obj.getGroupOfProperty(prop)
            if group == "Element":
                val = getattr(obj, prop)
                element_props[prop] = serialize_property_value(val)

        if element_props:
            element.update(element_props)

        # ➕ Add to proper group
        if parent_part:
            part_groups.setdefault(parent_part, []).append(element)
        else:
            root_elements.append(element)

    # ✅ Convert part_groups into cabinet-like entries
    part_cabinets = []
    for part, elems in part_groups.items():
        # Try to read the CabinetType property from the "Cabinet" group
        if hasattr(part, "PropertiesList"):
            cabinet_type = None
            for prop in part.PropertiesList:
                group = part.getGroupOfProperty(prop)
                if group == "Cabinet" and prop == "CabinetType":
                    cabinet_type = getattr(part, prop)
                    break
            if not cabinet_type:
                cabinet_type = getattr(part, "CabinetType", "Unknown")
        else:
            cabinet_type = getattr(part, "CabinetType", "Unknown")

        width = getattr(part, "Width", None)
        depth = getattr(part, "Depth", None)
        height = getattr(part, "Height", None)

        cabinet = {
            "label": part.Label,
            "cabinet_type": cabinet_type,
            "height": height,
            "width": width,
            "depth": depth,
            "elements": elems
        }
        # optional: record Part placement if needed
        try:
            placement = part.Placement
            base = placement.Base
            rot = placement.Rotation
            yaw, pitch, roll = rot.toEuler()
            positioning = []
            for axis, angle in zip(["x","y","z"], [roll, pitch, yaw]):
                steps = int(round(angle / 90.0)) % 4
                for _ in range(abs(steps)):
                    positioning.append({"rotate": axis})
            if base.x or base.y or base.z:
                for axis, val in zip(["x","y","z"], [base.x, base.y, base.z]):
                    if val != 0:
                        positioning.append({"move": [axis, val]})
            if positioning:
                cabinet["positioning"] = positioning
        except Exception:
            pass

        part_cabinets.append(cabinet)

    # ✅ Final elements and cabinets
    elements = root_elements
    cabinets = part_cabinets

    # elements = []
    # for obj in doc.Objects:

        # if obj.TypeId in ["Part::Box"]:
        #     if not hasattr(obj, "ElementType"):
        #         continue
        #
        #     placement = obj.Placement
        #     base = placement.Base
        #     rot = placement.Rotation
        #
        #     # Dimensions
        #     width, depth, height = obj.Length.Value, obj.Width.Value, obj.Height.Value
        #     if obj.TypeId == "Part::Cut":
        #         bb = obj.Shape.BoundBox
        #         width, depth, height = bb.XLength, bb.YLength, bb.ZLength
        #     else:
        #         width, depth, height = obj.Length.Value, obj.Width.Value, obj.Height.Value
        #
        #     try:
        #         yaw, pitch, roll = rot.toEuler()
        #     except Exception:
        #         yaw = pitch = roll = 0.0
        #
        #     element_type = getattr(obj, "ElementType", "Unknown")
        #
        #     element = {
        #         "label": obj.Label,
        #         "element_type": element_type,
        #         "thick": height,
        #         "length": width,
        #         "width": depth,
        #     }
        #
        #     # 👉 Positioning
        #     positioning = []
        #     # Include rotation for all axes (roll=X, pitch=Y, yaw=Z), in 90° steps
        #     def add_rot(axis, angle_deg):
        #         try:
        #             # invert direction: FreeCAD +90 (CW) -> 3 CCW steps; -90 (CCW) -> 1 CCW step
        #             #steps = (-int(round(angle_deg / 90.0))) % 4
        #             steps = int(round(angle_deg / 90.0)) % 4
        #         except Exception:
        #             steps = 0
        #         for _ in range(abs(steps)):
        #             positioning.append({"rotate": axis})
        #
        #     add_rot("x", roll)
        #     add_rot("y", pitch)
        #     add_rot("z", yaw)
        #
        #     if base.y != 0:
        #         positioning.append({"move": ["y", base.y]})
        #     if base.x != 0:
        #         positioning.append({"move": ["x", base.x]})
        #     if base.z != 0:
        #         positioning.append({"move": ["z", base.z]})
        #
        #     element["positioning"] = positioning
        #
        #     # ➕ Export all "Element" group properties (generic, any type)
        #     element_props = {}
        #     for prop in obj.PropertiesList:
        #         group = obj.getGroupOfProperty(prop)
        #         if group == "Element":
        #             val = getattr(obj, prop)
        #             element_props[prop] = serialize_property_value(val)
        #
        #     if element_props:
        #         element.update(element_props)
        #
        #     elements.append(element)

    # ✅ Extract cabinets
    # cabinets = []
    for obj in doc.Objects:
        if obj.TypeId in ["Part::Box", "Part::Cut"]:
            if not hasattr(obj, "CabinetType"):
                continue

            placement = obj.Placement
            base = placement.Base
            rot = placement.Rotation

            # Dimensions
            if obj.TypeId == "Part::Cut":
                bb = obj.Shape.BoundBox
                width, depth, height = bb.XLength, bb.YLength, bb.ZLength
            else:
                width, depth, height = obj.Length.Value, obj.Width.Value, obj.Height.Value

            try:
                yaw, pitch, roll = rot.toEuler()
            except Exception:
                yaw = pitch = roll = 0.0

            cabinet_type = getattr(obj, "CabinetType", "Unknown")

            cabinet = {
                "label": obj.Label,
                "cabinet_type": cabinet_type,
                "height": height,
                "width": width,
                "depth": depth,
            }

            # 👉 Positioning
            positioning = []
            # z_rot_steps = round(yaw / 90)
            # if z_rot_steps % 4 != 0:
            #     for _ in range(abs(z_rot_steps)):
            #         positioning.append({"rotate": "z"})

            def add_rot(axis, angle_deg):
                try:
                    steps = (int(round(angle_deg / 90.0))) % 4
                except Exception:
                    steps = 0
                for _ in range(abs(steps)):
                    positioning.append({"rotate": axis})

            add_rot("x", roll)
            add_rot("y", pitch)
            add_rot("z", yaw)

            if base.y != 0:
                positioning.append({"move": ["y", base.y]})
            if base.x != 0:
                positioning.append({"move": ["x", base.x]})
            if base.z != 0:
                positioning.append({"move": ["z", base.z]})

            cabinet["positioning"] = positioning

            # ➕ Export all "Cabinet" group properties (generic, any type)
            cabinet_props = {}
            for prop in obj.PropertiesList:
                group = obj.getGroupOfProperty(prop)
                if group == "Cabinet":
                    val = getattr(obj, prop)
                    cabinet_props[prop] = serialize_property_value(val)

            if cabinet_props:
                cabinet.update(cabinet_props)

            # ➕ Features
            features = []
            feature_groups = set()
            for prop in obj.PropertiesList:
                group = obj.getGroupOfProperty(prop)
                if group and group.startswith("Feature_"):
                    feature_groups.add(group)

            for group in feature_groups:
                gname = group[len("Feature_"):]
                if "_" in gname:
                    feature_name, index = gname.rsplit("_", 1)
                else:
                    feature_name, index = gname, "1"

                feature_data = {"feature": feature_name}
                for p in obj.PropertiesList:
                    if obj.getGroupOfProperty(p) == group:
                        val = getattr(obj, p)
                        prefix = group + "_"
                        pname = p[len(prefix):] if p.startswith(prefix) else p
                        feature_data[pname] = serialize_property_value(val)
                        # if hasattr(val, "Value") and isinstance(val.Value, (int, float)):
                        #     feature_data[pname] = val.Value
                        # elif isinstance(val, (str, int, float, bool)):
                        #     feature_data[pname] = val
                features.append(feature_data)

            if features:
                cabinet["additional_features"] = features

            cabinets.append(cabinet)

    # ✅ Combine and export
    export_data = globals_dict
    export_data["cabinets"] = cabinets
    export_data["elements"] = elements

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    # FreeCAD.Console.PrintMessage(f"✅ Exported {len(cabinets)} cabinets to: {output_path}\n")


class ExportJSONCommand:
    def GetResources(self):
        base_dir = os.path.dirname(os.path.dirname(__file__))
        return {
            "Pixmap": os.path.join(base_dir, "Resources", "icons", "icon_json_export.png"),  # replace with actual icon path
            "MenuText": "Export Cabinets JSON",
            "ToolTip": "Export all cabinets and global parameters to a JSON file"
        }

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None

    def Activated(self):
        doc = FreeCAD.ActiveDocument
        if not doc:
            FreeCAD.Console.PrintError("No active document open.\n")
            return

        fc_path = doc.FileName or os.path.expanduser("~/layout.json")
        output_path = os.path.join(os.path.dirname(fc_path), "layout.json")
        try:
            export(doc, output_path)
        except Exception as e:
            FreeCAD.Console.PrintError(str(e) + "\n")

# Register command
FreeCADGui.addCommand("Export_JSON", ExportJSONCommand())
