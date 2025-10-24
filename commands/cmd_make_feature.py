FEATURES = {
    # direct cabinet features
    "front": {
        "split_list": ("App::PropertyString", "[[100,50],[100,50]]", "Split list of tuples"),
        "front_type": ("App::PropertyString", "", "Front type"),
    },

    "remove_all_pfl": {
        "remove_all_pfl": ("App::PropertyBool", True, "Remove PFL"),
    },

    "remove_element": {
        "type": ("App::PropertyString", "", "Element type"),
        "label": ("App::PropertyString", "", "Element label"),
    },
    "add_pfl": {},

    # drawers
    "add_tandem_box": {
        "type": ("App::PropertyString", "", "Box type"),
        "offset": ("App::PropertyFloat", 0.0, "Offset"),
    },
    "add_drawer": {
        "height": ("App::PropertyFloat", 100.0, "Drawer height"),
        "offset": ("App::PropertyFloat", 0.0, "Offset"),
        "box_type": ("App::PropertyString", "a", "(a) lateral assembles on the edge of the front board, or (b) on the back"),
        "bottom": ("App::PropertyString", "pfl", "material of the bottom. Can be (pal) or (pfl) -> (default and not defined)"),
    },
    # "add_drawer_a_pfl": {
    #     "height": ("App::PropertyFloat", 100.0, "Drawer height"),
    #     "offset": ("App::PropertyFloat", 0.0, "Offset"),
    # },
    # "add_drawer_a_pal": {
    #     "height": ("App::PropertyFloat", 100.0, "Drawer height"),
    #     "offset": ("App::PropertyFloat", 0.0, "Offset"),
    # },
    # "add_drawer_b_pal": {
    #     "height": ("App::PropertyFloat", 100.0, "Drawer height"),
    #     "offset": ("App::PropertyFloat", 0.0, "Offset"),
    # },
    "add_drawer_pal_glass": {
        "height": ("App::PropertyFloat", 100.0, "Drawer height"),
        "offset": ("App::PropertyFloat", 0.0, "Offset"),
    },

    # shelves
    "add_pol": {
        "nr": ("App::PropertyInteger", 1, "Number of shelves"),
        "cant": ("App::PropertyString", "", "Edge type"),
    },
    "add_pol_2": {
        "orient": ("App::PropertyString", "h", "orientation [h or v]"),
        "length": ("App::PropertyFloat", 0.0, "length of the board, 0 for default width"),
        "height": ("App::PropertyFloat", 0.0, "Position offset of the shelf in the cabinet on Z"),
        "offset": ("App::PropertyFloat", 0.0, "Position offset of the shelf in the cabinet on X"),
    },
    "add_separator": {
        "orient": ("App::PropertyString", "V", "Orientation"),
        "sep_cant": ("App::PropertyString", "", "Separator edge type"),
    },
    "add_wine_shelf": {
        "goluri": ("App::PropertyInteger", 4, "Number of slots"),
        "left_right": ("App::PropertyString", "L", "Left or Right"),
        "cant": ("App::PropertyString", "", "Edge type"),
    },
    "add_sep_v": {
        "height": ("App::PropertyFloat", 0.0, "Height"),
        "offset_x": ("App::PropertyFloat", 0.0, "Offset X"),
        "offset_z": ("App::PropertyFloat", 0.0, "Offset Z"),
        "cant": ("App::PropertyString", "", "Edge type"),
    },
    "add_sep_h": {
        "width": ("App::PropertyFloat", 0.0, "Width"),
        "offset_x": ("App::PropertyFloat", 0.0, "Offset X"),
        "offset_z": ("App::PropertyFloat", 0.0, "Offset Z"),
        "sep_edge": ("App::PropertyString", "", "Edge type"),
        "edge_gap": ("App::PropertyFloat", 0.0, "Gap between edge of separator and edge of cabinet"),
    },
}

import FreeCAD as App
import FreeCADGui as Gui

# from .feature_definitions import FEATURES  # put dict above in a separate file

def make_feature_command(feature_name, params):
    class FeatureCommand:
        def GetResources(self):
            return {
                'MenuText': f'{feature_name}',
                'ToolTip': f'Adds {feature_name} parameters to the selected cabinet'
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
                App.Console.PrintError("Please select a valid Cabinet Box first.\n")
                return
            obj = sel[0]

            # find next available group name
            idx = 1
            while True:
                group = f"Feature_{feature_name}_{idx}"
                # check if this group name is already used
                if not any(obj.getGroupOfProperty(p) == group for p in obj.PropertiesList):
                    break
                idx += 1

            # group = f"Feature_{feature_name}_1"

            for pname, (ptype, default, desc) in params.items():
                if not hasattr(obj, pname):
                    # adds the group name and the index to the property name
                    property_name = str(group + "_" + pname)
                    obj.addProperty(ptype, property_name, group, desc)
                    setattr(obj, property_name, default)

            App.ActiveDocument.recompute()
            App.Console.PrintMessage(f"{feature_name} properties added to {obj.Name}\n")

    return FeatureCommand()

# Register all feature commands
for feature, params in FEATURES.items():
    Gui.addCommand(f"Cmd_Add_{feature}", make_feature_command(feature, params))
