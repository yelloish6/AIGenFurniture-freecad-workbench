import os
import FreeCAD as App
import FreeCADGui as Gui

class CabinetWorkbench (Gui.Workbench):
    """Cabinet Generator Workbench"""
    def __init__(self):

        current_file = inspect.getfile(inspect.currentframe())
        base_dir = os.path.dirname(os.path.abspath(current_file))
        icon_path = os.path.join(base_dir, "Resources", "icons", "convert_cabinet.svg")
        
        self.__class__.MenuText = "Cabinet Generator"
        self.__class__.ToolTip = "Tools for generating cabinets from boxes"
        self.__class__.Icon = icon_path

        # Save for later use when registering commands
        self.icon_path = icon_path

    def Initialize(self):

        # Convert to cabinet command
        # import ConvertCommand
        # ConvertCommand.ICON_PATH = self.icon_path
        # Gui.addCommand('Convert_Box_To_Cabinet', ConvertCommand.ConvertBoxCommand())
        # self.appendToolbar("Cabinet Tools", ["Convert_Box_To_Cabinet"])
        # self.appendMenu("Cabinet Tools", ["Convert_Box_To_Cabinet"])

        from commands import cmd_make_box, cmd_add_shelf

        # # Toolbars
        # self.appendToolbar("Cabinets", ["Cmd_Base_Box"])
        # self.appendToolbar("Features", ["Cmd_Add_Shelf"])

        # Menus
        # self.appendMenu("CabinetGenerator", ["Cmd_Base_Box", "Cmd_Add_Shelf"])

        # features
        import commands.cmd_make_feature
        import commands.cmd_make_cabinet
        import commands.cmd_make_element
        import commands.cmd_json_export
        import commands.cmd_aigenfurniture
        import commands.cmd_make_ordervar
        import commands.cmd_explode_cabinet

        self.appendToolbar("Features", [f"Cmd_Add_{f}" for f in commands.cmd_make_feature.FEATURES])
        self.appendToolbar("Cabinets", [f"Cmd_Add_{c}" for c in commands.cmd_make_cabinet.CABINETS])
        self.appendToolbar("Elements", [f"Cmd_Add_{e}" for e in commands.cmd_make_element.ELEMENTS])
        self.appendToolbar("Cabinet Tools", [
                                    "Export_JSON",
                                    "Create_Globals_Spreadsheet",
                                    "Explode_Box_To_Cabinet",
                                    "AIGenFurniture"
                                    ]
                           )

    def Activated(self):
        pass

    def Deactivated(self):
        pass

    def ContextMenu(self, recipient):
        self.appendContextMenu("Cabinets", ["Cmd_Base_Box"])
        self.appendContextMenu("Features", ["Cmd_Add_Shelf"])

    def GetClassName(self):
        return "Gui::PythonWorkbench"

Gui.addWorkbench(CabinetWorkbench())

