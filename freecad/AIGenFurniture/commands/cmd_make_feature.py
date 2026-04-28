# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
import FreeCAD as App
import FreeCADGui as Gui
from ..furniture_design.cabinets.features import get_enabled_features


def make_feature_command(feature_name, data):
    class FeatureCommand:

        def GetResources(self):
            return {
                'MenuText': data.get("label", f'{feature_name}'),
                'ToolTip': data.get("tooltip", f'{feature_name}'),
            }

        def IsActive(self):
            sel = Gui.Selection.getSelection()
            if len(sel) != 1:
                return False
            obj = sel[0]
            return obj.TypeId == "Part::Box" and hasattr(obj, "CabinetType")

        def Activated(self):
            sel = Gui.Selection.getSelection()
            if not sel:
                App.Console.PrintError("Please select a valid Cabinet first.\n")
                return
            obj = sel[0]

            # Find next available group name
            idx = 1
            while True:
                group = f"Feature_{feature_name}_{idx}"
                if not any(obj.getGroupOfProperty(p) == group for p in obj.PropertiesList):
                    break
                idx += 1

            doc = App.ActiveDocument
            doc.openTransaction(f"Add Feature {feature_name}")
            try:
                params = data.get("params", feature_name)
                for pname, (ptype, default, desc) in params.items():
                    if not hasattr(obj, pname):
                        property_name = str(group + "_" + pname)
                        obj.addProperty(ptype, property_name, group, desc)
                        setattr(obj, property_name, default)

                doc.recompute()
                doc.commitTransaction()
                App.Console.PrintMessage(f"{feature_name} properties added to {obj.Name}\n")
            except Exception as e:
                doc.abortTransaction()
                App.Console.PrintError(str(e) + "\n")

    return FeatureCommand()

REGISTERED_FEATURES = get_enabled_features()

def register_feature_commands(features_registry):
    registered = []
    for feature_name, feature_data in features_registry.items():
        Gui.addCommand(f"Cmd_Add_{feature_name}", make_feature_command(feature_name, feature_data))
        registered.append(feature_name)
    return registered


# for feature_name, feature_data in get_enabled_features().items():
#     Gui.addCommand(f"Cmd_Add_{feature_name}", make_feature_command(feature_name, feature_data))
#     REGISTERED_FEATURES.append(feature_name)
