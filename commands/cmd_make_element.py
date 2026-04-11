# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
import FreeCAD as App
import FreeCADGui as Gui
from AIGenFurniture.furniture_design.cabinets.elements import ELEMENTS


# -------------------------
# Command class generator
# -------------------------
def make_element_command(element_name, data):
    class ElementCommand:
        def GetResources(self):
            return {
                "Pixmap": "",  # put path to icon if you have one
                "MenuText": data.get("UI_label", f"{element_name}"),
                "ToolTip": data.get("tooltip", f"{element_name}"),
            }

        def Activated(self):
            doc = App.ActiveDocument or App.newDocument("Cabinets")

            # Create a box placeholder
            box = doc.addObject("Part::Box", f"{element_name}")
            defaults = data.get("defaults", {})
            box.Label = defaults.get("label", f"{element_name}")
            box.Length = defaults.get("length", f"{element_name}")
            box.Width = defaults.get("width", f"{element_name}")
            box.Height = defaults.get("thickness", f"{element_name}")
            # if element_name == "PFL":
            #     box.Height = 4
            # elif element_name == "Countertop":
            #     box.Height = 38
            # else:
            #     box.Height = 18

            # Add a ElementType property
            box.addProperty("App::PropertyString", "ElementType", "Element", "Type of element").ElementType = element_name
            # box.addProperty("App::PropertyString", "BoardType", "Board", "Type of board").BoardType = element_name

            # Add parameters as properties
            params = data.get("params", element_name)
            for pname, value in params.items():
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