# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
import os, importlib
from AIGenFurniture.manufacturing import get_active_exports
# from .export_for_proficut import export_pal_for_proficut
# from .export_for_proficut import export_pfl_for_proficut
# from .export_for_nettfront import export_front_for_nettfront
# from .export_csv import export_csv
# from .export_stl_new import export_stl_order
# from .generate_offer_cost import export_cost_sheet, print_order_summary, generate_offer_file
# from .generate_assembly_file import generate_assembly_file, generate_drill_file
# from .generate_assembly_file_reportlab import generate_drill_pdf_reportlab


# def generate_manufacturing_files(order, output_path):
#     """
#     generate_manufacturing_files is a function that takes a cabinet object and an output_path as arguments.
#     The function creates the output directory if it doesn't exist.
#     It generates a summary file (design_summary.txt) containing information about the cabinet's dimensions, materials,
#     hardware, and additional features.
#     You can customize this function to include additional logic for generating specific manufacturing files based on
#     the type of cabinet.
#     Adjust the code according to the specific manufacturing files you need for your project and the structure of your
#     cabinet classes.
#     """
#
#     # Create the output directory if it doesn't exist
#     os.makedirs(output_path, exist_ok=True)
#
#     export_pal_for_proficut(order, output_path)
#     export_pfl_for_proficut(order, output_path)
#     export_front_for_nettfront(order, output_path)
#     export_csv(order, output_path)
#     export_stl_order(order, output_path, is_horizontal_layout=False)
#     export_cost_sheet(order, output_path)
#     print_order_summary(order)
#     generate_offer_file(order, output_path)
#     generate_assembly_file(order, output_path)
#     generate_drill_file(order, output_path)
#     generate_drill_pdf_reportlab(order, output_path)
#
#     print(f"Manufacturing files generated in: {output_path}")

def generate_manufacturing_files(order, output_path):
    """
    Run all active manufacturing exports.
    MVP-safe dispatcher.
    """

    exports = get_active_exports()

    for export_name, export_def in exports.items():
        runner_name = export_def["runner"]
        module_name = export_def["module"]

        try:

            module = importlib.import_module(
                f"AIGenFurniture.manufacturing.{module_name}"
            )
            runner = getattr(module, runner_name)

        except Exception as e:
            print(f"[ERROR] Failed to load export '{export_name}': {e}")
            continue

        try:
            runner(order, output_path)
        except Exception as e:
            print(f"[ERROR] Export '{export_name}' failed: {e}")