import FreeCAD as App
import FreeCADGui as Gui

from AIGenFurniture.furniture_design.cabinets.Kitchen.base_box import BaseBox
from AIGenFurniture.furniture_design.cabinets.elements.accessory import Accessory
from AIGenFurniture.furniture_design.cabinets.elements.board import BoardPal, Blat, Front, Pfl

def explode_box_to_cabinet(box):
    doc = App.ActiveDocument
    if not box:
        App.Console.PrintError("⚠ No box selected.\n")
        return

    # Get box dimensions
    height = int(box.Height.Value)
    width  = int(box.Length.Value)
    depth  = int(box.Width.Value)

    # Cabinet type property
    cab_type = getattr(box, "CabinetType", "BaseBox")

    # Rules (normally from spreadsheet / OrderVar)
    rules = {
        "thick_pal": 18,
        "thick_front": 18,
        "thick_blat": 40,
        "width_blat": 600,
        "cant_general": 2,
        "gap_front": 3,
        "pol_depth": 500,
        "cant_pol": 2,
        "cant_separator": 2,
        "gap_fata": 20
    }

    # Build cabinet
    if cab_type == "BaseBox":
        cabinet = BaseBox(box.Label, height, width, depth, rules)
    else:
        App.Console.PrintError(f"⚠ Unknown CabinetType '{cab_type}', defaulting to BaseBox.\n")
        cabinet = BaseBox(box.Label, height, width, depth, rules)

    # Create container group
    cab_group = doc.addObject("App::DocumentObjectGroup", cabinet.label)

    # Add an "Accessories" property group
    cab_group.addProperty("App::PropertyStringList", "Accessories", "Cabinet",
                          "List of accessories for this cabinet")
    accessories_list = []

    # Place elements
    for elem in cabinet.elements_list:
        if elem.type in ("pal", "front", "pfl", "blat"):
            part = doc.addObject("Part::Box", elem.label)
            part.Length = elem.position[0]
            part.Width  = elem.position[1]
            part.Height = elem.position[2]
            # Position
            part.Placement.Base.x = elem.position[3]
            part.Placement.Base.y = elem.position[4]
            part.Placement.Base.z = elem.position[5]
            cab_group.addObject(part)

        elif elem.type == "accessory":
            accessories_list.append(f"{elem.label} x {elem.price if hasattr(elem,'price') else '?'}")

        else:
            App.Console.PrintError(f"❌ Unknown element type: {elem.type}\n")

    # Store accessories as a property
    cab_group.Accessories = accessories_list

    # Hide original box
    box.ViewObject.Visibility = False

    doc.recompute()
    App.Console.PrintMessage(f"✅ Replaced {box.Label} with cabinet {cabinet.label}\n")


class ExplodeBoxCommand:
    def GetResources(self):
        return {
            "Pixmap": "path/to/icon_convert_box.svg",
            "MenuText": "Convert Box to Cabinet",
            "ToolTip": "Replace a simple box with a Cabinet architecture"
        }

    def IsActive(self):
        return App.ActiveDocument is not None

    def Activated(self):
        sel = Gui.Selection.getSelection()
        if not sel:
            App.Console.PrintError("⚠ Please select a box first.\n")
            return
        explode_box_to_cabinet(sel[0])


# Register command
Gui.addCommand("Explode_Box_To_Cabinet", ExplodeBoxCommand())
