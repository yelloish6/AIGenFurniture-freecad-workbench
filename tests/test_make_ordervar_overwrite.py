import copy
import sys
import types
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))


class FakeConsole:
    def __init__(self):
        self.errors = []
        self.messages = []

    def PrintError(self, message):
        self.errors.append(message)

    def PrintMessage(self, message):
        self.messages.append(message)

    def PrintWarning(self, _message):
        pass


fake_console = FakeConsole()

sys.modules.setdefault(
    "FreeCAD",
    types.SimpleNamespace(Console=fake_console, ActiveDocument=None),
)
sys.modules.setdefault(
    "FreeCADGui",
    types.SimpleNamespace(addCommand=lambda _name, _command: None),
)
sys.modules.setdefault(
    "PySide",
    types.SimpleNamespace(
        QtGui=types.SimpleNamespace(
            QMessageBox=type(
                "QMessageBox",
                (),
                {
                    "Warning": 1,
                    "RejectRole": 0,
                    "AcceptRole": 1,
                    "__init__": lambda self: None,
                    "setIcon": lambda self, _icon: None,
                    "setWindowTitle": lambda self, _title: None,
                    "setText": lambda self, _text: None,
                    "addButton": lambda self, label, _role: label,
                    "setDefaultButton": lambda self, _button: None,
                    "setEscapeButton": lambda self, _button: None,
                    "exec_": lambda self: None,
                    "clickedButton": lambda self: None,
                },
            )
        )
    ),
)

from freecad.AIGenFurniture.commands import cmd_make_ordervar  # noqa: E402


ENABLED_PARAMS = {
    "client": {"label": "Customer Name", "default": "Customer Name"},
    "material_pal": {"label": "Chipboard Material", "default": "Alb W962ST2"},
    "material_front": {"label": "Front Material", "default": "A34R3"},
}


class FakeObject:
    def __init__(self, type_id, name):
        self.TypeId = type_id
        self.Name = name
        self.Label = name


class FakeSheet(FakeObject):
    def __init__(self, name):
        super().__init__("Spreadsheet::Sheet", name)
        self.cells = {}
        self.aliases = {}
        self.styles = {}
        self.widths = {}
        self.clear_all_calls = 0

    def snapshot(self):
        return {
            "Label": self.Label,
            "cells": copy.deepcopy(self.cells),
            "aliases": copy.deepcopy(self.aliases),
            "styles": copy.deepcopy(self.styles),
            "widths": copy.deepcopy(self.widths),
            "clear_all_calls": self.clear_all_calls,
        }

    def restore(self, state):
        self.Label = state["Label"]
        self.cells = copy.deepcopy(state["cells"])
        self.aliases = copy.deepcopy(state["aliases"])
        self.styles = copy.deepcopy(state["styles"])
        self.widths = copy.deepcopy(state["widths"])
        self.clear_all_calls = state["clear_all_calls"]

    def set(self, cell, value):
        self.cells[cell] = value

    def get(self, name):
        cell = self.aliases.get(name, name)
        return self.cells.get(cell, "")

    def setAlias(self, cell, alias):
        if alias:
            self.aliases[alias] = cell
        else:
            for existing_alias, alias_cell in list(self.aliases.items()):
                if alias_cell == cell:
                    del self.aliases[existing_alias]

    def clearAll(self):
        self.clear_all_calls += 1
        self.cells.clear()
        self.aliases.clear()
        self.styles.clear()
        self.widths.clear()


class FakeDoc:
    def __init__(self):
        self.Objects = []
        self.recompute_count = 0
        self.open_transactions = []
        self.committed = 0
        self.aborted = 0
        self._snapshot = None

    def addObject(self, type_id, name):
        obj = FakeSheet(name) if type_id == "Spreadsheet::Sheet" else FakeObject(type_id, name)
        self.Objects.append(obj)
        return obj

    def getObject(self, name):
        for obj in self.Objects:
            if obj.Name == name:
                return obj
        return None

    def recompute(self):
        self.recompute_count += 1

    def openTransaction(self, name):
        self.open_transactions.append(name)
        self._snapshot = {
            "objects": list(self.Objects),
            "states": {
                id(obj): obj.snapshot()
                for obj in self.Objects
                if hasattr(obj, "snapshot")
            },
            "recompute_count": self.recompute_count,
        }

    def commitTransaction(self):
        self.committed += 1
        self._snapshot = None

    def abortTransaction(self):
        self.aborted += 1
        if self._snapshot is None:
            return

        self.Objects = list(self._snapshot["objects"])
        for obj in self.Objects:
            state = self._snapshot["states"].get(id(obj))
            if state is not None:
                obj.restore(state)
        self.recompute_count = self._snapshot["recompute_count"]
        self._snapshot = None


def order_sheets(doc):
    return [
        obj
        for obj in doc.Objects
        if getattr(obj, "TypeId", "") == "Spreadsheet::Sheet"
        and (getattr(obj, "Name", "") == "OrderVar" or getattr(obj, "Label", "") == "OrderVar")
    ]


def sheet_rows(sheet):
    rows = []
    for row in range(1, 20):
        label = sheet.cells.get(f"A{row}")
        value = sheet.cells.get(f"B{row}")
        if label is not None or value is not None:
            rows.append((label, value))
    return rows


class MakeOrderVarOverwriteTest(unittest.TestCase):
    def setUp(self):
        fake_console.errors.clear()
        fake_console.messages.clear()
        console = cmd_make_ordervar.App.Console
        for attr in ("errors", "messages"):
            if hasattr(console, attr):
                getattr(console, attr).clear()
        cmd_make_ordervar.App.ActiveDocument = None
        self.enabled_patch = mock.patch.object(
            cmd_make_ordervar,
            "get_enabled_order_params",
            return_value=ENABLED_PARAMS,
        )
        self.enabled_patch.start()

    def tearDown(self):
        self.enabled_patch.stop()
        cmd_make_ordervar.App.ActiveDocument = None

    def run_command(self, doc, confirm=None):
        cmd_make_ordervar.App.ActiveDocument = doc
        if confirm is not None:
            with mock.patch.object(
                cmd_make_ordervar,
                "confirm_overwrite_order_spreadsheet",
                return_value=confirm,
            ):
                cmd_make_ordervar.CreateOrderSpreadsheetCommand().Activated()
        else:
            with mock.patch.object(
                cmd_make_ordervar,
                "confirm_overwrite_order_spreadsheet",
                side_effect=AssertionError("confirmation should not be requested"),
            ):
                cmd_make_ordervar.CreateOrderSpreadsheetCommand().Activated()

    def sheet_content(self, sheet):
        return {
            "Label": sheet.Label,
            "cells": copy.deepcopy(sheet.cells),
            "aliases": copy.deepcopy(sheet.aliases),
            "styles": copy.deepcopy(sheet.styles),
            "widths": copy.deepcopy(sheet.widths),
        }

    def test_no_existing_ordervar_creates_one_sheet(self):
        doc = FakeDoc()

        self.run_command(doc)

        self.assertEqual(len(order_sheets(doc)), 1)
        self.assertEqual(doc.Objects[0].Name, "OrderVar")
        self.assertEqual(doc.Objects[0].Label, "OrderVar")
        self.assertEqual(doc.committed, 1)
        self.assertEqual(doc.aborted, 0)

    def test_cancel_leaves_existing_spreadsheet_unchanged(self):
        doc = FakeDoc()
        sheet = doc.addObject("Spreadsheet::Sheet", "OrderVar")
        sheet.Label = "Custom Label"
        sheet.set("A1", "Old")
        sheet.set("B7", "stale")
        sheet.setAlias("B7", "stale_alias")
        sheet.styles["B7"] = "bold"
        before = sheet.snapshot()

        self.run_command(doc, confirm=False)

        self.assertEqual(sheet.snapshot(), before)
        self.assertEqual(doc.open_transactions, [])
        self.assertEqual(doc.committed, 0)
        self.assertEqual(doc.aborted, 0)

    def test_confirmation_clears_stale_rows_and_stale_aliases(self):
        doc = FakeDoc()
        sheet = doc.addObject("Spreadsheet::Sheet", "OrderVar")
        sheet.set("A9", "Obsolete")
        sheet.set("B9", "unused")
        sheet.setAlias("B9", "obsolete_param")
        sheet.styles["A9"] = "bold"
        sheet.widths["A"] = 42

        self.run_command(doc, confirm=True)

        self.assertEqual(sheet.clear_all_calls, 1)
        self.assertNotIn("A9", sheet.cells)
        self.assertNotIn("B9", sheet.cells)
        self.assertNotIn("obsolete_param", sheet.aliases)
        self.assertEqual(sheet.styles, {})
        self.assertEqual(sheet.widths, {})

    def test_existing_spreadsheet_object_identity_is_preserved(self):
        doc = FakeDoc()
        sheet = doc.addObject("Spreadsheet::Sheet", "OrderVar")

        self.run_command(doc, confirm=True)

        self.assertIs(doc.getObject("OrderVar"), sheet)
        self.assertEqual(len(order_sheets(doc)), 1)

    def test_renamed_label_is_found_through_internal_name(self):
        doc = FakeDoc()
        sheet = doc.addObject("Spreadsheet::Sheet", "OrderVar")
        sheet.Label = "User Renamed"

        self.assertIs(cmd_make_ordervar.find_order_spreadsheet(doc), sheet)
        self.run_command(doc, confirm=True)

        self.assertIs(doc.getObject("OrderVar"), sheet)
        self.assertEqual(sheet.Label, "OrderVar")
        self.assertEqual(len(order_sheets(doc)), 1)

    def test_rebuilt_sheet_contains_exactly_enabled_parameters(self):
        doc = FakeDoc()
        sheet = doc.addObject("Spreadsheet::Sheet", "OrderVar")
        sheet.set("A4", "Old Disabled")
        sheet.set("B4", "legacy")
        sheet.setAlias("B4", "disabled_param")

        self.run_command(doc, confirm=True)

        expected_rows = [
            ("Customer Name", "Customer Name"),
            ("Chipboard Material", "Alb W962ST2"),
            ("Front Material", "A34R3"),
        ]
        self.assertEqual(sheet_rows(sheet), expected_rows)
        self.assertEqual(
            sheet.aliases,
            {"client": "B1", "material_pal": "B2", "material_front": "B3"},
        )
        self.assertEqual(set(sheet.cells), {"A1", "B1", "A2", "B2", "A3", "B3"})

    def test_failure_during_rebuild_aborts_transaction_without_partial_sheet(self):
        doc = FakeDoc()
        sheet = doc.addObject("Spreadsheet::Sheet", "OrderVar")
        sheet.set("A1", "Existing")
        sheet.set("B1", "Value")
        sheet.setAlias("B1", "existing_alias")
        before = sheet.snapshot()

        def fail_after_first_cell(spreadsheet, enabled_params=None):
            spreadsheet.set("A1", "Partial")
            raise RuntimeError("rebuild failed")

        with mock.patch.object(
            cmd_make_ordervar,
            "confirm_overwrite_order_spreadsheet",
            return_value=True,
        ), mock.patch.object(
            cmd_make_ordervar,
            "populate_order_spreadsheet",
            side_effect=fail_after_first_cell,
        ):
            cmd_make_ordervar.App.ActiveDocument = doc
            cmd_make_ordervar.CreateOrderSpreadsheetCommand().Activated()

        self.assertEqual(doc.committed, 0)
        self.assertEqual(doc.aborted, 1)
        self.assertEqual(sheet.snapshot(), before)

    def test_confirmed_overwrite_twice_produces_same_final_content(self):
        doc = FakeDoc()
        sheet = doc.addObject("Spreadsheet::Sheet", "OrderVar")

        self.run_command(doc, confirm=True)
        first_state = self.sheet_content(sheet)
        self.run_command(doc, confirm=True)

        self.assertEqual(self.sheet_content(sheet), first_state)
        self.assertEqual(len(order_sheets(doc)), 1)


if __name__ == "__main__":
    unittest.main()
