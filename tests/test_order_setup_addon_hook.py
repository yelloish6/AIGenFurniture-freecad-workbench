import sys
import types
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))


class FakeConsole:
    def __init__(self):
        self.warnings = []
        self.errors = []
        self.messages = []

    def PrintWarning(self, message):
        self.warnings.append(message)

    def PrintError(self, message):
        self.errors.append(message)

    def PrintMessage(self, message):
        self.messages.append(message)


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


class OrderSetupAddonHookTest(unittest.TestCase):
    def setUp(self):
        fake_console.warnings.clear()
        fake_console.errors.clear()
        fake_console.messages.clear()

    def test_missing_addon_hook_is_silent(self):
        self.assertIsNone(cmd_make_ordervar.get_order_setup_apply_func())

        cmd_make_ordervar.apply_order_setup_addon_if_available(object())

        self.assertEqual(fake_console.warnings, [])
        self.assertEqual(fake_console.errors, [])

    def test_command_source_does_not_reference_paid_edition(self):
        source = Path(cmd_make_ordervar.__file__).read_text()

        self.assertNotIn("aigenfurniture_pro", source)
        self.assertNotIn("AIGenFurniture Pro", source)


if __name__ == "__main__":
    unittest.main()
