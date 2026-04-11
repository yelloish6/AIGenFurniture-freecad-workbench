# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
import FreeCAD as App
import FreeCADGui as Gui

import os
# Import centralized order parameters - uses deterministic ordering
from AIGenFurniture.furniture_design.order import get_enabled_order_params

def create_globals_spreadsheet(doc):
    """Create a spreadsheet with enabled order parameters prefilled and aliases set.
    
    Uses centralized ORDER_PARAMS definition for consistency.
    Only enabled parameters are included (MVP cleanliness).
    Column A: English label (user-facing)
    Column B: Value (with alias set to parameter key for programmatic access)
    """
    # Check if spreadsheet "OrderVar" already exists
    spreadsheet = None
    for obj in doc.Objects:
        if obj.TypeId == "Spreadsheet::Sheet" and obj.Label == "OrderVar":
            spreadsheet = obj
            break

    if not spreadsheet:
        spreadsheet = doc.addObject("Spreadsheet::Sheet", "OrderVar")

    # Get enabled parameters only
    enabled_params = get_enabled_order_params()

    # Fill spreadsheet from enabled ORDER_PARAMS only
    row = 1
    for param_name, param_def in enabled_params.items():
        # Column A: English label (user-facing, no parameter keys visible)
        label = param_def.get("label", param_name)
        spreadsheet.set(f"A{row}", label)

        # Column B: default value (stored as string in ORDER_PARAMS for spreadsheet)
        default_value = param_def.get("default", "")
        spreadsheet.set(f"B{row}", str(default_value))

        # Set alias of cell in column B to parameter key (for programmatic access, not visible)
        try:
            spreadsheet.setAlias(f"B{row}", param_name)
        except Exception as e:
            App.Console.PrintError(f"⚠ Could not set alias for {param_name}: {e}\n")

        row += 1

    doc.recompute()
    App.Console.PrintMessage(f"✅ Spreadsheet 'OrderVar' created/updated with {len(enabled_params)} enabled parameters.\n")


class CreateGlobalsSpreadsheetCommand:
    def GetResources(self):
        base_dir = os.path.dirname(os.path.dirname(__file__))
        return {
            "Pixmap": os.path.join(base_dir, "Resources", "icons", "icon_create_spreadsheet.jpg"),  # replace with actual icon path
            "MenuText": "Create Globals Spreadsheet",
            "ToolTip": "Create a spreadsheet with all global aliases and default values"
        }

    def IsActive(self):
        return App.ActiveDocument is not None

    def Activated(self):
        doc = App.ActiveDocument
        if not doc:
            App.Console.PrintError("No active document open.\n")
            return

        try:
            create_globals_spreadsheet(doc)
        except Exception as e:
            App.Console.PrintError(str(e) + "\n")


# Register command
Gui.addCommand("Create_Globals_Spreadsheet", CreateGlobalsSpreadsheetCommand())
