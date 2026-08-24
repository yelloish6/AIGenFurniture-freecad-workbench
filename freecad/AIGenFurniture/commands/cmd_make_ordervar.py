# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
import FreeCAD as App
import FreeCADGui as Gui

import sys
from PySide import QtGui
# Import centralized order parameters - uses deterministic ordering
from ..furniture_design.order import get_enabled_order_params
from .._resources import get_command_icon


def get_order_setup_apply_func():
    """Return the order setup hook from a loaded addon, if available."""
    for module in tuple(sys.modules.values()):
        apply_func = getattr(module, "APPLY_ORDER_SETUP_TO_PROJECT", None)
        if apply_func is not None:
            return apply_func

    return None

def apply_order_setup_addon_if_available(doc):
    """Run order setup addon extras when an addon exposes them."""
    apply_func = get_order_setup_apply_func()
    if apply_func is None:
        return

    try:
        apply_func(doc)
    except Exception as exc:
        App.Console.PrintError(
            f"[AIGenFurniture] Order Setup addon extras failed: {exc}\n"
        )


def find_order_spreadsheet(doc):
    """Return the existing OrderVar spreadsheet, if present."""
    spreadsheet = doc.getObject("OrderVar")
    if spreadsheet is not None and getattr(spreadsheet, "TypeId", "") == "Spreadsheet::Sheet":
        return spreadsheet

    for obj in doc.Objects:
        if getattr(obj, "TypeId", "") == "Spreadsheet::Sheet" and getattr(obj, "Label", "") == "OrderVar":
            return obj
    return None


def confirm_overwrite_order_spreadsheet():
    """Ask the user whether to overwrite an existing OrderVar spreadsheet."""
    message = QtGui.QMessageBox()
    message.setIcon(QtGui.QMessageBox.Warning)
    message.setWindowTitle("OrderVar already exists")
    message.setText(
        "\u26a0 An OrderVar already exists in this document.\n"
        "Creating a new order will overwrite it.\n"
        "Continue?"
    )

    cancel_button = message.addButton("Cancel", QtGui.QMessageBox.RejectRole)
    create_button = message.addButton(
        "Yes, create new order", QtGui.QMessageBox.AcceptRole
    )
    message.setDefaultButton(cancel_button)
    message.setEscapeButton(cancel_button)

    message.exec_()
    return message.clickedButton() == create_button


def get_or_create_order_spreadsheet(doc):
    """Return the existing OrderVar spreadsheet or create it."""
    spreadsheet = find_order_spreadsheet(doc)
    if spreadsheet is None:
        spreadsheet = doc.addObject("Spreadsheet::Sheet", "OrderVar")

    return spreadsheet


def clear_order_spreadsheet(spreadsheet):
    """Clear all sheet contents, formatting, sizing, and aliases."""
    spreadsheet.clearAll()


def populate_order_spreadsheet(spreadsheet, enabled_params=None):
    """Fill a spreadsheet from enabled ORDER_PARAMS only."""
    if enabled_params is None:
        enabled_params = get_enabled_order_params()

    row = 1
    for param_name, param_def in enabled_params.items():
        # Column A: English label (user-facing, no parameter keys visible)
        label = param_def.get("label", param_name)
        spreadsheet.set(f"A{row}", label)

        # Column B: default value (stored as string in ORDER_PARAMS for spreadsheet)
        default_value = param_def.get("default", "")
        spreadsheet.set(f"B{row}", str(default_value))

        # Set alias of cell in column B to parameter key (for programmatic access, not visible)
        spreadsheet.setAlias(f"B{row}", param_name)

        row += 1

    return len(enabled_params)


def create_order_spreadsheet(doc, overwrite=False):
    """Create or rebuild the OrderVar spreadsheet from enabled order parameters.

    Uses centralized ORDER_PARAMS definition for consistency.
    Only enabled parameters are included (MVP cleanliness).
    Column A: English label (user-facing)
    Column B: Value (with alias set to parameter key for programmatic access)
    """
    spreadsheet = get_or_create_order_spreadsheet(doc)
    if overwrite:
        clear_order_spreadsheet(spreadsheet)

    # Keep current label-based consumers working while preserving the object's Name.
    spreadsheet.Label = "OrderVar"

    enabled_count = populate_order_spreadsheet(spreadsheet)
    doc.recompute()
    App.Console.PrintMessage(
        f"\u2705 Spreadsheet 'OrderVar' created/updated with {enabled_count} enabled parameters.\n"
    )
    return spreadsheet


class CreateOrderSpreadsheetCommand:
    def GetResources(self):
        return {
            "Pixmap": get_command_icon("icon_order"),
            "MenuText": "Order Setup",
            "ToolTip": "Set up customer and material parameters for this order.",
        }

    def IsActive(self):
        return App.ActiveDocument is not None

    def Activated(self):
        doc = App.ActiveDocument
        if not doc:
            App.Console.PrintError("No active document open.\n")
            return

        existing_spreadsheet = find_order_spreadsheet(doc)
        if existing_spreadsheet and not confirm_overwrite_order_spreadsheet():
            App.Console.PrintMessage("OrderVar creation cancelled.\n")
            return

        doc.openTransaction("Create Globals Spreadsheet")
        try:
            spreadsheet = create_order_spreadsheet(doc, overwrite=existing_spreadsheet is not None)
            apply_order_setup_addon_if_available(doc)
            doc.commitTransaction()
            Gui.ActiveDocument.setEdit(spreadsheet.Name)
        except Exception as e:
            doc.abortTransaction()
            App.Console.PrintError(str(e) + "\n")


# Register command
Gui.addCommand("Create_Order_Spreadsheet", CreateOrderSpreadsheetCommand())
