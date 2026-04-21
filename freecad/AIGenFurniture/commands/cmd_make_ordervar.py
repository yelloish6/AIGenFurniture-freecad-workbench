# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
import FreeCAD as App
import FreeCADGui as Gui

import os
# Import centralized order parameters - uses deterministic ordering
from ..furniture_design.order import get_enabled_order_params
from .._resources import get_command_icon


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
            App.Console.PrintError(f"\u26a0 Could not set alias for {param_name}: {e}\n")

        row += 1

    doc.recompute()
    App.Console.PrintMessage(
        f"\u2705 Spreadsheet 'OrderVar' created/updated with {len(enabled_params)} enabled parameters.\n"
    )


class CreateGlobalsSpreadsheetCommand:
    def GetResources(self):
        return {
            "Pixmap": get_command_icon("icon_create_spreadsheet"),
            "MenuText": "Create Globals Spreadsheet",
            "ToolTip": "Create a spreadsheet with all global aliases and default values",
        }

    def IsActive(self):
        return App.ActiveDocument is not None

    def Activated(self):
        doc = App.ActiveDocument
        if not doc:
            App.Console.PrintError("No active document open.\n")
            return

        doc.openTransaction("Create Globals Spreadsheet")
        try:
            create_globals_spreadsheet(doc)
            doc.commitTransaction()
        except Exception as e:
            doc.abortTransaction()
            App.Console.PrintError(str(e) + "\n")


# Register command
Gui.addCommand("Create_Globals_Spreadsheet", CreateGlobalsSpreadsheetCommand())
