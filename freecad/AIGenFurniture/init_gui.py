# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
import FreeCAD as App
import FreeCADGui as Gui
from ._resources import get_resource_path
from ._plugin_loader import load_plugins

class CabinetWorkbench (Gui.Workbench):
    """Cabinet Generator Workbench"""
    def __init__(self):

        icon_path = get_resource_path("..", "..", "Resources", "Icons", "AIGenFurniture_logo_noBG.svg")
        
        from freecad.AIGenFurniture import __version__

        self.__class__.MenuText = "Cabinet Generator"
        self.__class__.ToolTip = "Tools for generating cabinets from boxes (v{__version__})"
        self.__class__.Icon = icon_path

        # Save for later use when registering commands
        self.icon_path = icon_path

    def Initialize(self):

        # features
        from freecad.AIGenFurniture.commands.cmd_make_feature import REGISTERED_FEATURES, register_feature_commands
        from freecad.AIGenFurniture.commands.cmd_make_cabinet import REGISTERED_CABINETS, register_cabinet_commands
        from freecad.AIGenFurniture.commands.cmd_make_element import REGISTERED_ELEMENTS, register_element_commands
        from freecad.AIGenFurniture.commands.cmd_tools import TOOLS, register_tools
        from freecad.AIGenFurniture.furniture_design.order import ORDER_PARAMS
        from freecad.AIGenFurniture.commands import cmd_about
        from freecad.AIGenFurniture.commands import cmd_json_export
        from freecad.AIGenFurniture.commands import cmd_aigenfurniture
        from freecad.AIGenFurniture.commands import cmd_make_ordervar
        from freecad.AIGenFurniture.commands import cmd_explode_cabinet
        from freecad.AIGenFurniture.commands import cmd_generate_from_geometry
        import Draft
        import DraftTools
        import DraftGui



        # Gui.activateWorkbench("DraftWorkbench")
        # Gui.activateWorkbench("CabinetWorkbench")

        load_plugins(REGISTERED_FEATURES, REGISTERED_ELEMENTS, REGISTERED_CABINETS, TOOLS, ORDER_PARAMS)
        registered_features = register_feature_commands(REGISTERED_FEATURES)
        registered_cabinets = register_cabinet_commands(REGISTERED_CABINETS)
        registered_elements = register_element_commands(REGISTERED_ELEMENTS)
        registered_tools = register_tools(TOOLS)

        self.appendToolbar("Features", [f"Cmd_Add_{f}" for f in registered_features])
        self.appendToolbar("Cabinets", [f"Cmd_Add_{c}" for c in registered_cabinets])
        self.appendToolbar("Elements", [f"Cmd_Add_{e}" for e in registered_elements])

        # self.appendToolbar("Cabinet Tools", [
        #                             # "Export_JSON",
        #                             "Create_Globals_Spreadsheet",
        #                             "Explode_Box_To_Cabinet",
        #                             # "AIGenFurniture",
        #                             "Generate_From_Geometry",
        #                             "AIGenFurniture_About"
        #                             ]
        #                    )
        # Group tool IDs by toolbar
        from collections import defaultdict
        toolbar_groups = defaultdict(list)
        for tool_id, toolbar in registered_tools:
            toolbar_groups[toolbar].append(tool_id)
        for toolbar_name, tool_ids in toolbar_groups.items():
            self.appendToolbar(toolbar_name, tool_ids)

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
