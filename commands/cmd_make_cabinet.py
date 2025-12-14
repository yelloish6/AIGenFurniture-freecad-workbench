import FreeCAD as App
import FreeCADGui as Gui
from AIGenFurniture.furniture_design.cabinets.architectures import UI_CABINETS, META_KEYS

# -------------------------
# Command class generator
# -------------------------
def make_cabinet_command(cabinet_name, params):
    class CabinetCommand:
        def GetResources(self):
            display_name = params.get("label", cabinet_name)
            return {
                "Pixmap": "",  # put path to icon if you have one
                "MenuText": f"{display_name}",
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
                # skip META_KEYS from creating parameters
                if pname in META_KEYS:
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
REGISTERED_CABINETS = []
for cab_name, cab_data in UI_CABINETS.items():
    if not cab_data.get("active", True):
        continue # skip inactive cabinets
    Gui.addCommand(f"Cmd_Add_{cab_name}", make_cabinet_command(cab_name, cab_data))
    REGISTERED_CABINETS.append(cab_name)