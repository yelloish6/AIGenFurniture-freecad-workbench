import FreeCAD as App
import FreeCADGui as Gui
import os, sys, subprocess
from PySide import QtGui

# Add parent of CabinetWorkbench to sys.path if missing
workbench_dir = os.path.dirname(os.path.dirname(__file__))
if workbench_dir not in sys.path:
    sys.path.insert(0, workbench_dir)

import commands.cmd_json_export as cmd_json_export  # reuse your exporter code
from AIGenFurniture import main as AIGenFurniture_main



def export_and_generate():
    doc = App.ActiveDocument
    if not doc or not doc.FileName:
        QtGui.QMessageBox.warning(None, "Cabinet Generator", "Please save the FreeCAD file before running.")
        return

    fc_path = doc.FileName
    project_dir = os.path.dirname(fc_path)
    basename = os.path.splitext(os.path.basename(fc_path))[0]

    # Create output folder
    output_dir = os.path.join(project_dir, basename + "_output")
    os.makedirs(output_dir, exist_ok=True)

    # Export JSON directly into the output folder
    json_path = os.path.join(output_dir, "kitchen_layout.json")
    cmd_json_export.export(doc, json_path)   # you wrap your exporter in a function

    # # ensure vendor path is in PYTHONPATH
    # generator_root = os.path.join(os.path.dirname(__file__), "..", "AIGenFurniture")
    # vendor_path = os.path.join(generator_root, "vendor")
    # env = os.environ.copy()
    # env["PYTHONPATH"] = vendor_path + os.pathsep + env.get("PYTHONPATH", "")
    #
    # # Run generator via python
    # generator_main = os.path.join(generator_root, "main.py")
    # generator_main = os.path.abspath(generator_main)

    AIGenFurniture_main.run(json_path, output_dir)
    # subprocess.run([sys.executable, generator_main, "--input", json_path, "--output", output_dir], env=env)


    # Notify user
    QtGui.QMessageBox.information(None, "Cabinet Generator", f"Generation complete!\n\nFiles saved in:\n{output_dir}")

class AIGenFurnitureCommand:
    def GetResources(self):
        return {"MenuText": "AIGen Furniture generator",
                "ToolTip": "Run AIGen Furniture generator",
                "Pixmap": "icons/generate.svg"}

    def Activated(self):
        export_and_generate()

Gui.addCommand("AIGenFurniture", AIGenFurnitureCommand())
