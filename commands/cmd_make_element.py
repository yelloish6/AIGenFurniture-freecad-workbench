import FreeCAD as App
import FreeCADGui as Gui

# -------------------------
# Define the ELEMENTS dict
# -------------------------
ELEMENTS = {
    "BoardPal": {
        "tooltip": "Add a standard chipboard",
        "cant_L1": ("App::PropertyString", "", "Edge length 1"),
        "cant_L2": ("App::PropertyString", "", "Edge length 2"),
        "cant_l1": ("App::PropertyString", "", "Edge width 1"),
        "cant_l2": ("App::PropertyString", "", "Edge width 2"),
    },
    "Countertop": {
        "tooltip": "Add a countertop board",
    },
    "Front": {
        "tooltip": "Add a front board",
    }
}

# -------------------------
# Command class generator
# -------------------------
def make_element_command(element_name, params):
    class ElementCommand:
        def GetResources(self):
            return {
                "Pixmap": "",  # put path to icon if you have one
                "MenuText": f"{element_name}",
                "ToolTip": params.get("tooltip", f"Add {element_name}"),
            }

        def Activated(self):
            doc = App.ActiveDocument or App.newDocument("Cabinets")

            # Create a box placeholder
            box = doc.addObject("Part::Box", f"{element_name}")
            box.Label = element_name
            box.Length = 600
            box.Width = 500
            box.Height = 18

            # Add a ElementType property
            box.addProperty("App::PropertyString", "ElementType", "Element", "Type of element").ElementType = element_name

            # Add parameters as properties
            for pname, value in params.items():
                if pname == "tooltip":  # skip tooltip
                    continue
                ptype, default, desc = value
                if not hasattr(box, pname):
                    box.addProperty(ptype, pname, "Element", desc)
                    setattr(box, pname, default)

            doc.recompute()
            App.Console.PrintMessage(f"{element_name} created.\n")

    return ElementCommand()

# -------------------------
# Register commands in FreeCAD
# -------------------------
for ele_name, ele_data in ELEMENTS.items():
    Gui.addCommand(f"Cmd_Add_{ele_name}", make_element_command(ele_name, ele_data))