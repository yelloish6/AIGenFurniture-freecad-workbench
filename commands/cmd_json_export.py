import FreeCAD
import FreeCADGui
import json
import os

# def serialize_property_value(val):
#     """Convert FreeCAD property values into JSON-safe formats."""
#     # Distances, Angles, etc. (they have .Value)
#     if hasattr(val, "Value") and isinstance(val.Value, (int, float)):
#         return val.Value
#
#     # Quantity types (e.g. Units like 'mm', 'deg')
#     if hasattr(val, "UserString") and hasattr(val, "Value"):
#         return float(val.Value)
#
#     # Lists of numbers (PropertyIntegerList, PropertyFloatList, PropertyVectorList, etc.)
#     if isinstance(val, (list, tuple)):
#         return [serialize_property_value(v) for v in val]
#
#     # Simple native types
#     if isinstance(val, (str, int, float, bool)):
#         return val
#
#     # Fallback: stringify anything else
#     return str(val)

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

    # ✅ Load global variables from spreadsheet aliases
    global_aliases = [
        "client", "Client Proficut", "Tel Proficut", "Transport", "Adresa",
        "h_bucatarie", "h_faianta_top", "h_faianta_base", "depth_base",
        "top_height", "top_height_2", "top_depth", "top_depth_2",
        "blat_height", "cuptor_height", "MsV_height_min", "MsV_height_max",
        "material_pal", "material_front", "material_blat", "material_pfl",
        "h_rate", "h_proiect", "discount", "nr_electrocasnice"
    ]

    globals_dict = {}
    for alias in global_aliases:
        try:
            val = spreadsheet.get(alias)
            if val != "":
                try:
                    val = float(val) if "." in str(val) else int(val)
                except:
                    pass
                globals_dict[alias] = val
        except:
            pass
    # Extract elements
    elements = []
    for obj in doc.Objects:
        if obj.TypeId in ["Part::Box"]:
            if not hasattr(obj, "ElementType"):
                continue

            placement = obj.Placement
            base = placement.Base
            rot = placement.Rotation

            # Dimensions
            width, depth, height = obj.Length.Value, obj.Width.Value, obj.Height.Value
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
            z_rot_steps = round(yaw / 90)
            if z_rot_steps % 4 != 0:
                for _ in range(abs(z_rot_steps)):
                    positioning.append({"rotate": "z"})

            if base.y != 0:
                positioning.append({"move": ["y", base.y]})
            if base.x != 0:
                positioning.append({"move": ["x", base.x]})
            if base.z != 0:
                positioning.append({"move": ["z", base.z]})

            element["positioning"] = positioning

            # ➕ Export all "Element" group properties (generic, any type)
            element_props = {}
            for prop in obj.PropertiesList:
                group = obj.getGroupOfProperty(prop)
                if group == "Element":
                    val = getattr(obj, prop)
                    element_props[prop] = serialize_property_value(val)

            if element_props:
                element.update(element_props)

            elements.append(element)

    # ✅ Extract cabinets
    cabinets = []
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
            z_rot_steps = round(yaw / 90)
            if z_rot_steps % 4 != 0:
                for _ in range(abs(z_rot_steps)):
                    positioning.append({"rotate": "z"})

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

    # fc_path = doc.FileName or os.path.expanduser("~/kitchen_layout.json")
    # output_path = os.path.join(os.path.dirname(fc_path), "kitchen_layout.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    FreeCAD.Console.PrintMessage(f"✅ Exported {len(cabinets)} cabinets to: {output_path}\n")


class ExportJSONCommand:
    def GetResources(self):
        return {
            "Pixmap": "path/to/icon_json_export.svg",  # replace with actual icon path
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

        fc_path = doc.FileName or os.path.expanduser("~/kitchen_layout.json")
        output_path = os.path.join(os.path.dirname(fc_path), "kitchen_layout.json")
        try:
            export(doc, output_path)
        except Exception as e:
            FreeCAD.Console.PrintError(str(e) + "\n")

# Register command
FreeCADGui.addCommand("Export_JSON", ExportJSONCommand())
