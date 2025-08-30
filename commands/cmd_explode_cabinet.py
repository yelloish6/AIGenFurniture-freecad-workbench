import FreeCAD as App
import FreeCADGui as Gui

from AIGenFurniture.furniture_design.cabinets.Kitchen.base_box import BaseBox
from AIGenFurniture.furniture_design.cabinets.elements.board import BoardPal, Blat, Front, Pfl
from AIGenFurniture.furniture_design.design_engine import load_default_rules, DEFAULT_RULES_PATH
from AIGenFurniture.furniture_design.cabinets.Kitchen import CABINETS

def apply_movements_to_part(part, position_list):
    """Apply the same sequence of move/rotate operations as STL export."""
    pl = part.Placement
    for movement in position_list:
        if movement[0] == "move":
            axis, offset = movement[1], movement[2]
            if axis == "x":
                pl.Base.x += offset
            elif axis == "y":
                pl.Base.y += offset
            elif axis == "z":
                pl.Base.z += offset
        elif movement[0] == "rotate":
            axis = movement[1]
            if axis == "x":
                pl.Rotation = pl.Rotation.multiply(App.Rotation(App.Vector(1, 0, 0), 90))
            elif axis == "y":
                pl.Rotation = pl.Rotation.multiply(App.Rotation(App.Vector(0, 1, 0), 90))
            elif axis == "z":
                pl.Rotation = pl.Rotation.multiply(App.Rotation(App.Vector(0, 0, 1), 90))
            else:
                App.Console.PrintError(f"❌ Unknown rotation axis {axis}\n")
    part.Placement = pl


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
    rules = load_default_rules(DEFAULT_RULES_PATH)
    # rules = {
    #     "thick_pal": 18,
    #     "thick_front": 18,
    #     "thick_blat": 40,
    #     "width_blat": 600,
    #     "cant_general": 2,
    #     "gap_front": 3,
    #     "pol_depth": 500,
    #     "cant_pol": 2,
    #     "cant_separator": 2,
    #     "gap_fata": 20
    # }

    # Build cabinet
    # if cab_type == "BaseBox":
    #     cabinet = BaseBox(box.Label, height, width, depth, rules)
    # else:
    #     App.Console.PrintError(f"⚠ Unknown CabinetType '{cab_type}', defaulting to BaseBox.\n")
    #     cabinet = BaseBox(box.Label, height, width, depth, rules)



    # Lookup cabinet factory
    if cab_type in CABINETS:
        CabinetFactory = CABINETS[cab_type]

        # Handle special factories (functions) vs normal classes
        if callable(CabinetFactory):
            try:
                cabinet = CabinetFactory(box.Label, height, width, depth, rules, box=box)
            except TypeError:
                # For simple class constructors
                cabinet = CabinetFactory(box.Label, height, width, depth, rules)
        else:
            App.Console.PrintError(f"❌ Invalid cabinet factory for {cab_type}\n")
            return
    else:
        App.Console.PrintError(f"⚠ Unknown CabinetType '{cab_type}', using BaseBox.\n")
        cabinet = CABINETS["BaseBox"](box.Label, height, width, depth, rules)

    # Create container group
    cab_group = doc.addObject("App::DocumentObjectGroup", cabinet.label)

    # Add accessories properties (parallel arrays: names + counts)
    cab_group.addProperty("App::PropertyStringList", "AccessoryTypes", "Cabinet",
                          "List of accessory types")
    cab_group.addProperty("App::PropertyIntegerList", "AccessoryCounts", "Cabinet",
                          "List of accessory counts")

    accessory_types = []
    accessory_counts = []

    # Place elements
    for elem in cabinet.elements_list:
        if elem.type in ("pal", "front", "pfl", "blat"):
            part = doc.addObject("Part::Box", elem.label)
            part.Length = elem.length
            part.Width  = elem.width
            part.Height = elem.thick

            # Apply recorded transformations
            apply_movements_to_part(part, elem.position_list)

            cab_group.addObject(part)

        elif elem.type == "accessory":  # lowercase type
            accessory_types.append(elem.label)
            accessory_counts.append(int(getattr(elem, "count", 1)))

        else:
            App.Console.PrintError(f"❌ Unknown element type: {elem.type}\n")

    # Store accessories
    cab_group.AccessoryTypes = accessory_types
    cab_group.AccessoryCounts = accessory_counts

    # Hide original box
    box.ViewObject.Visibility = False

    doc.recompute()
    App.Console.PrintMessage(f"✅ Exploded {box.Label} into cabinet {cabinet.label}\n")


class ExplodeBoxCommand:
    def GetResources(self):
        return {
            "Pixmap": "path/to/icon_explode_box.svg",
            "MenuText": "Explode Box to Cabinet",
            "ToolTip": "Explode a simple box into a Cabinet architecture"
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
