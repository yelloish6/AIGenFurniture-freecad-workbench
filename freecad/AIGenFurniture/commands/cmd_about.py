# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
import os
import FreeCADGui as Gui
from PySide import QtGui, QtCore
from .._resources import get_command_icon

class AboutCommand:
    def GetResources(self):
        # ICON_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources", "")
        return {
            "Pixmap": get_command_icon("icon_support"),
            "MenuText": "About & Support",
            "ToolTip": "About & Support for AIGenFurniture"
        }

    def Activated(self):
        dialog = QtGui.QDialog()
        dialog.setWindowTitle("About & Support")
        dialog.setMinimumWidth(400)

        layout = QtGui.QVBoxLayout()

        # Title
        title = QtGui.QLabel("<h2>AIGenFurniture – Cabinet Generator</h2>")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        # Support section
        support_label = QtGui.QLabel(
            "<b>📧 Support & Feedback</b><br>"
            "For questions, bug reports, or feedback, email us at:<br>"
            "<a href='mailto:contact@aigenfurniture.com'>contact@aigenfurniture.com</a>"
        )
        support_label.setOpenExternalLinks(True)
        support_label.setWordWrap(True)
        layout.addWidget(support_label)

        layout.addSpacing(10)

        # Donate section
        donate_label = QtGui.QLabel(
            "<b>❤️ Support the Project</b><br>"
            "If this tool saves you time, consider buying us a coffee:<br>"
            "<a href='https://ko-fi.com/bogdan_aigenfurniture'>ko-fi.com</a><br>"
            "<a href='https://paypal.com/donate/?hosted_button_id=UV2AFNARW4RBN'>PayPal</a>"
        )
        donate_label.setOpenExternalLinks(True)
        donate_label.setWordWrap(True)
        layout.addWidget(donate_label)

        layout.addSpacing(10)

        # GitHub
        github_label = QtGui.QLabel(
            "<b>🐛 Issues & Source Code</b><br>"
            "<a href='https://github.com/yelloish6/AIGenFurniture-freecad-workbench'>"
            "github.com/yelloish6/AIGenFurniture-freecad-workbench</a>"
        )
        github_label.setOpenExternalLinks(True)
        github_label.setWordWrap(True)
        layout.addWidget(github_label)

        layout.addSpacing(16)

        # Close button
        close_btn = QtGui.QPushButton("Close")
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn, alignment=QtCore.Qt.AlignCenter)

        dialog.setLayout(layout)
        dialog.exec_()


Gui.addCommand("AIGenFurniture_About", AboutCommand())
