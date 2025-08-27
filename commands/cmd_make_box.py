import FreeCAD as App
import FreeCADGui as Gui

class CmdBaseBox:
    def GetResources(self):
        return {
            'MenuText': 'Base Box',
            'ToolTip': 'Creates a kitchen base box with predefined cabinet properties'
        }

    def IsActive(self):
        return True

    def Activated(self):
        doc = App.ActiveDocument or App.newDocument("Cabinets")

        # Create a basic box
        box = doc.addObject("Part::Box", "BaseBox")
        box.Length = 600
        box.Width = 500
        box.Height = 720

        # Add some custom properties
        box.addProperty("App::PropertyString", "CabinetType", "Cabinet", "Type of cabinet")
        box.CabinetType = "BaseBox"

        doc.recompute()

Gui.addCommand("Cmd_Base_Box", CmdBaseBox())
