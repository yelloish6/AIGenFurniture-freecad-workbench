import FreeCAD as App
import FreeCADGui as Gui

# -------------------------
# Define the CABINETS dict
# -------------------------
CABINETS = {
    "BaseBox": {
        "tooltip": "Add a base box cabinet",
    },
    "BaseCorner": {
        "tooltip": "Add a base corner cabinet",
        "cut_width": ("App::PropertyDistance", "", "Cut Width"),
        "cut_depth": ("App::PropertyDistance", "", "Cut Depth"),
        "l_r": ("App::PropertyString", "", "Left or Right Corner"),
        "with_polita": ("App::PropertyBool", "false", "Has a shelf")
    },
    "TopCorner": {
        "tooltip": "Add a top corner cabinet",
        "cut_width": ("App::PropertyDistance", "", "Cut Width"),
        "cut_depth": ("App::PropertyDistance", "", "Cut Depth"),
        "l_r": ("App::PropertyString", "", "Left or Right Corner"),
        "polite": ("App::PropertyInteger", 1, "Number of shelves included")
    },
    "Raft": {
        "tooltip": "Add a shelf unit (Raft)",
        "shelves": ("App::PropertyInteger", 1, "Number of shelves included")
    },
    "Bar": {
        "tooltip": "Add a bar cabinet",
    },
    "JollyBox": {
        "tooltip": "Add a JollyBox cabinet",
    },
    "TopBox": {
        "tooltip": "Add a top box cabinet",
    },
    "SinkBox": {
        "tooltip": "Add a sink cabinet",
    },
    "TowerBox": {
        "tooltip": "Add a tower cabinet",
        "gap_list": ("App::PropertyIntegerList", [20, 40], "Gap List"),
        "gap_heat": ("App::PropertyInteger", 50, "Gap for heat dissipation on the back of the cabinet"),
        "front_list": ("App::PropertyIntegerList", [0, 0, 0, 0], "List which gaps should be closed by doors")
    },
    "MsVBox": {
        "tooltip": "Add a MsVBox cabinet",
    },
    "BaseCornerShelf": {
        "tooltip": "Add a base corner shelf cabinet",
        "shelves": ("App::PropertyInteger", 1, "Number of shelves included"),
    },
    "Banca": {
        "tooltip": "Add a bench cabinet",
    },
    "Etajera": {
        "tooltip": "Add an Etajera (shelf unit)",
        "shelves": ("App::PropertyInteger", 1, "Number of shelves included"),
    },
    "CorpDressing": {
        "tooltip": "Add a wardrobe cabinet",
        "gap_list": ("App::PropertyString", "", "Gap List"),
        "front_list": ("App::PropertyString", "", "List which gaps should be closed by doors"),
    },
    "Dulap": {
        "tooltip": "Add a simple closet (Dulap)",
    },
    "CorpCuPicioare": {
        "tooltip": "Add a cabinet with legs (CorpCuPicioare)",
        "plinta_height": ("App::PropertyInteger", 100, "Height of legs area"),
    }
}


# -------------------------
# Command class generator
# -------------------------
def make_cabinet_command(cabinet_name, params):
    class CabinetCommand:
        def GetResources(self):
            return {
                "Pixmap": "",  # put path to icon if you have one
                "MenuText": f"{cabinet_name}",
                "ToolTip": params.get("tooltip", f"Add {cabinet_name}"),
            }

        def Activated(self):
            doc = App.ActiveDocument or App.newDocument("Cabinets")

            # Create a box placeholder
            box = doc.addObject("Part::Box", f"{cabinet_name}")
            box.Label = cabinet_name
            box.Length = 600
            box.Width = 500
            box.Height = 720

            # Add a CabinetType property
            box.addProperty("App::PropertyString", "CabinetType", "Cabinet", "Type of cabinet").CabinetType = cabinet_name

            # Add parameters as properties
            for pname, value in params.items():
                if pname == "tooltip":  # skip tooltip
                    continue
                ptype, default, desc = value
                if not hasattr(box, pname):
                    box.addProperty(ptype, pname, "Cabinet", desc)
                    setattr(box, pname, default)

            doc.recompute()
            App.Console.PrintMessage(f"{cabinet_name} created.\n")

    return CabinetCommand()

# -------------------------
# Register commands in FreeCAD
# -------------------------
for cab_name, cab_data in CABINETS.items():
    Gui.addCommand(f"Cmd_Add_{cab_name}", make_cabinet_command(cab_name, cab_data))