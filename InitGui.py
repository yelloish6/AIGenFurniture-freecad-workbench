import os
import inspect
import FreeCAD as App
import FreeCADGui as Gui
# import DraftGui



class CabinetWorkbench (Gui.Workbench):
    """Cabinet Generator Workbench"""
    def __init__(self):

        current_file = inspect.getfile(inspect.currentframe())
        base_dir = os.path.dirname(os.path.abspath(current_file))
        icon_path = os.path.join(base_dir, "Resources", "icons", "AIGenFurniture_logo_noBG.png")
        
        from AIGenFurniture import __version__

        self.__class__.MenuText = "Cabinet Generator"
        self.__class__.ToolTip = "Tools for generating cabinets from boxes (v{__version__})"
        self.__class__.Icon = icon_path

        # Save for later use when registering commands
        self.icon_path = icon_path

    def Initialize(self):

        # features
        import commands.cmd_make_feature
        import commands.cmd_make_cabinet
        import commands.cmd_make_element
        import commands.cmd_json_export
        import commands.cmd_aigenfurniture
        import commands.cmd_make_ordervar
        import commands.cmd_explode_cabinet
        import commands.cmd_generate_from_geometry
        import Draft
        import DraftTools
        import DraftGui

        # Gui.activateWorkbench("DraftWorkbench")
        # Gui.activateWorkbench("CabinetWorkbench")

        self.appendToolbar("Features", [f"Cmd_Add_{f}" for f in commands.cmd_make_feature.REGISTERED_FEATURES])
        self.appendToolbar("Cabinets", [f"Cmd_Add_{c}" for c in commands.cmd_make_cabinet.REGISTERED_CABINETS])
        self.appendToolbar("Elements", [f"Cmd_Add_{e}" for e in commands.cmd_make_element.ELEMENTS])
        self.appendToolbar("Cabinet Tools", [
                                    # "Export_JSON",
                                    "Create_Globals_Spreadsheet",
                                    "Explode_Box_To_Cabinet",
                                    # "AIGenFurniture",
                                    "Generate_From_Geometry"
                                    ]
                           )
        self.appendToolbar("Manipulation", ["Draft_Move", "Draft_Rotate"])
        snap_cmds = [
            "Draft_Snap_Lock",
            "Draft_Snap_Endpoint",
            "Draft_Snap_Midpoint",
            "Draft_Snap_Center",
            "Draft_Snap_Perpendicular",
            "Draft_Snap_Intersection",
            "Draft_Snap_Parallel",
            "Draft_Snap_Grid",
            "Draft_Snap_Near",
            "Draft_Snap_Extension",
            "Draft_Snap_Angle",
            "Draft_Snap_Dimensions",
            "Draft_ToggleGrid",
        ]
        self.appendToolbar("Snap tools", snap_cmds)

    def Activated(self):
        pass

    def Deactivated(self):
        pass

    def ContextMenu(self, recipient):
        # self.appendContextMenu("Cabinets", ["Cmd_Base_Box"])
        # self.appendContextMenu("Features", ["Cmd_Add_Shelf"])
        pass

    def GetClassName(self):
        return "Gui::PythonWorkbench"

Gui.addWorkbench(CabinetWorkbench())

