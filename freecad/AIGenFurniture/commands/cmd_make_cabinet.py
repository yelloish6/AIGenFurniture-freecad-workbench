# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
import FreeCAD as App
import FreeCADGui as Gui
from ..furniture_design.cabinets.architectures import get_enabled_ui_cabinets

# -------------------------
# Command class generator
# -------------------------
def make_cabinet_command(cabinet_name, ui, params):
    class CabinetCommand:
        def GetResources(self):
            display_name = ui.get("label", cabinet_name)
            return {
                "Pixmap": "",  # put path to icon if you have one
                "MenuText": ui.get("label", f"{cabinet_name}"),       # f"{display_name}",
                "ToolTip": ui.get("tooltip", f"Add {cabinet_name}"),
            }

        def Activated(self):
            doc = App.ActiveDocument or App.newDocument("Cabinets")
            doc.openTransaction(f"Add {cabinet_name}")

            # Create a box placeholder
            try:
                box = doc.addObject("Part::Box", f"{cabinet_name}")
                box.Label = cabinet_name
                box.Length = 600
                box.Width = 500
                box.Height = 720

                # Add a CabinetType property
                box.addProperty("App::PropertyString", "CabinetType", "Cabinet", "Type of cabinet").CabinetType = cabinet_name
                doc.recompute()
                doc.commitTransaction()
            except Exception as e:
                doc.abortTransaction()
                raise e

            # Add parameters as properties
            for pname, value in params.items():
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
REGISTERED_CABINETS = []
for cab_name, cab_data in get_enabled_ui_cabinets().items():
    Gui.addCommand(f"Cmd_Add_{cab_name}", make_cabinet_command(cab_name, cab_data["ui"], cab_data["params"]))
    REGISTERED_CABINETS.append(cab_name)