# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
import FreeCADGui as Gui
from PySide import QtGui, QtCore

from .._resources import get_command_icon
from ..furniture_design.design_engine import (
    DESIGN_RULE_LABELS,
    NON_NEGATIVE_DESIGN_RULE_KEYS,
    POSITIVE_DESIGN_RULE_KEYS,
    DesignRulesValidationError,
    load_factory_rules,
    load_default_rules,
    save_default_rules,
)


RULE_GROUPS = (
    (
        "Board Thicknesses",
        ("thick_pal", "thick_front", "thick_blat", "thick_pfl"),
    ),
    (
        "Cabinet Defaults",
        ("height_legs", "general_height", "general_width", "general_depth"),
    ),
    (
        "Gaps and Clearances",
        ("gap_front", "front_clearance", "pol_depth"),
    ),
    (
        "Edging Rules",
        ("cant_general", "cant_pol", "cant_separator"),
    ),
)


class DesignRulesDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(DesignRulesDialog, self).__init__(parent)
        self.setWindowTitle("Design Rules")
        self.setModal(True)
        self.setMinimumWidth(420)

        self._rules = load_default_rules()
        self._widgets = {}

        layout = QtGui.QVBoxLayout(self)

        title = QtGui.QLabel("<h2>Design Rules</h2>")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        hint = QtGui.QLabel("Defaults used for cabinet generation. Values are stored in millimeters.")
        hint.setWordWrap(True)
        layout.addWidget(hint)

        self._build_rule_sections(layout)

        buttons = QtGui.QHBoxLayout()
        restore_btn = QtGui.QPushButton("Restore Defaults")
        cancel_btn = QtGui.QPushButton("Cancel")
        save_btn = QtGui.QPushButton("Save")

        restore_btn.clicked.connect(self.restore_defaults)
        cancel_btn.clicked.connect(self.reject)
        save_btn.clicked.connect(self.save_rules)

        buttons.addWidget(restore_btn)
        buttons.addStretch()
        buttons.addWidget(cancel_btn)
        buttons.addWidget(save_btn)
        layout.addLayout(buttons)

    def _build_rule_sections(self, layout):
        grouped_keys = set()
        for section_title, keys in RULE_GROUPS:
            present_keys = [key for key in keys if key in self._rules]
            if not present_keys:
                continue

            group = QtGui.QGroupBox(section_title)
            form = QtGui.QFormLayout(group)
            for key in present_keys:
                form.addRow(self._label_for_key(key), self._create_spinbox(key, self._rules[key]))
                grouped_keys.add(key)
            layout.addWidget(group)

        extra_keys = [key for key in self._rules.keys() if key not in grouped_keys]
        if extra_keys:
            group = QtGui.QGroupBox("Other Rules")
            form = QtGui.QFormLayout(group)
            for key in extra_keys:
                form.addRow(self._label_for_key(key), self._create_spinbox(key, self._rules[key]))
            layout.addWidget(group)

    def _label_for_key(self, key):
        label = DESIGN_RULE_LABELS.get(key, key.replace("_", " ").title())
        # return "{} ({})".format(label, key)
        return "{}".format(label)

    def _create_spinbox(self, key, value):
        if isinstance(value, int) and not isinstance(value, bool):
            widget = QtGui.QSpinBox()
            widget.setRange(-1000000, 1000000)
            widget.setValue(value)
        else:
            widget = QtGui.QDoubleSpinBox()
            widget.setRange(-1000000.0, 1000000.0)
            widget.setDecimals(3)
            widget.setValue(float(value))
        if key in POSITIVE_DESIGN_RULE_KEYS:
            widget.setMinimum(1)
        elif key in NON_NEGATIVE_DESIGN_RULE_KEYS:
            widget.setMinimum(0)
        widget.setSuffix(" mm")
        self._widgets[key] = widget
        return widget

    def restore_defaults(self):
        factory_rules = load_factory_rules()
        for key, widget in self._widgets.items():
            if key in factory_rules:
                widget.setValue(factory_rules[key])

    def _collect_rules(self):
        rules = {}
        for key, original_value in self._rules.items():
            widget = self._widgets[key]
            if isinstance(original_value, int) and not isinstance(original_value, bool):
                rules[key] = int(widget.value())
            else:
                rules[key] = float(widget.value())
        return rules

    def save_rules(self):
        try:
            save_default_rules(self._collect_rules())
        except DesignRulesValidationError as exc:
            QtGui.QMessageBox.critical(
                self,
                "Design Rules",
                "Design rules were not saved:\n{}".format("\n".join(exc.errors)),
            )
            return
        except Exception as exc:
            QtGui.QMessageBox.critical(self, "Design Rules", "Could not save design rules:\n{}".format(exc))
            return
        self.accept()


class DesignRulesCommand:
    def GetResources(self):
        return {
            "Pixmap": get_command_icon("icon_design_rules"),
            "MenuText": "Design Rules",
            "ToolTip": "Edit AIGenFurniture design rules",
        }

    def Activated(self):
        dialog = DesignRulesDialog()
        dialog.exec_()


Gui.addCommand("AIGenFurniture_Design_Rules", DesignRulesCommand())
