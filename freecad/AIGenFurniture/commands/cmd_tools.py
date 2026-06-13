# freecad/AIGenFurniture/commands/cmd_tools.py
import FreeCADGui as Gui

# Import base tool command classes (files unchanged)
from .cmd_about import AboutCommand
from .cmd_explode_cabinet import ExplodeBoxCommand
from .cmd_generate_from_geometry import GenerateFromGeometryCommand
from .cmd_aigenfurniture import AIGenFurnitureCommand
from .cmd_make_ordervar import CreateOrderSpreadsheetCommand
from .cmd_json_export import ExportJSONCommand
from .cmd_design_rules import DesignRulesCommand

# Base tool registry — same schema plugins use
TOOLS = [
    {
        "id": "AIGenFurniture_About",
        "command": AboutCommand(),
        "toolbar": "Cabinet Tools",
        "enabled": True,
    },
    {
        "id": "Design_Rules",
        "command": DesignRulesCommand(),
        "toolbar": "Cabinet Tools",
        "enabled": True,
    },
    {
        "id": "Create_Order_Spreadsheet",
        "command": CreateOrderSpreadsheetCommand(),
        "toolbar": "Cabinet Tools",
        "enabled": True,
    },
    {
        "id": "Explode_Box_To_Cabinet",
        "command": ExplodeBoxCommand(),
        "toolbar": "Cabinet Tools",
        "enabled": True,
    },
    {
        "id": "Generate_From_Geometry",
        "command": GenerateFromGeometryCommand(),
        "toolbar": "Cabinet Tools",
        "enabled": True,
    },
    # Add Export_JSON here with enabled=False to keep parity
    {
        "id": "Export_JSON",
        "command": ExportJSONCommand(),
        "toolbar": "Cabinet Tools",
        "enabled": False,
    },
]


def register_tools(tools_registry):
    """Called after addon_loader merges plugin tools into the registry."""
    registered = []
    for tool in tools_registry:
        if tool.get("enabled", True):
            Gui.addCommand(tool["id"], tool["command"])
            registered.append((tool["id"], tool["toolbar"]))
    return registered  # list of (id, toolbar) for init_gui.py to consume