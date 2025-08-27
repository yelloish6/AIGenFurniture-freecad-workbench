import FreeCAD as App
import FreeCADGui as Gui

class CmdAddShelf:
    def GetResources(self):
        return {
            'MenuText': 'Add Shelf',
            'ToolTip': 'Adds shelf parameters to the selected cabinet box'
        }

    def IsActive(self):
        sel = Gui.Selection.getSelection()
        if len(sel) != 1:
            return False

        obj = sel[0]

        # Check if it's a Part::Box and has CabinetType attribute
        if obj.TypeId == "Part::Box" and hasattr(obj, "CabinetType"):
            return True

        return False

    def Activated(self):
        sel = Gui.Selection.getSelection()
        if not sel:
            App.Console.PrintError("Please select a valid Cabinet Box first.\n")
            return

        obj = sel[0]

        # Add new shelf properties if not already present
        if not hasattr(obj, "nr"):
            obj.addProperty("App::PropertyInteger", "nr", "Feature_add_pol_1", "Number of shelves")
            obj.nr = 1

        if not hasattr(obj, "cant"):
            obj.addProperty("App::PropertyString", "cant", "Feature_add_pol_1", "Type of edge treatment")
            obj.cant = "2"

        App.ActiveDocument.recompute()
        App.Console.PrintMessage(f"Shelf properties added to {obj.Name}\n")

Gui.addCommand("Cmd_Add_Shelf", CmdAddShelf())
