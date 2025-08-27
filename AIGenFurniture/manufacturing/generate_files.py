import os
from .export_for_proficut import export_pal_for_proficut
from .export_for_proficut import export_pfl_for_proficut
from .export_for_nettfront import export_front_for_nettfront
from .export_csv import export_csv
from .export_stl_new import export_stl_order
from .generate_offer_cost import export_cost_sheet, print_order_summary, generate_offer_file
from .generate_assembly_file import generate_assembly_file, generate_drill_file


def generate_manufacturing_files(order, output_path):
    """
    generate_manufacturing_files is a function that takes a cabinet object and an output_path as arguments.
    The function creates the output directory if it doesn't exist.
    It generates a summary file (design_summary.txt) containing information about the cabinet's dimensions, materials,
    hardware, and additional features.
    You can customize this function to include additional logic for generating specific manufacturing files based on
    the type of cabinet.
    Adjust the code according to the specific manufacturing files you need for your project and the structure of your
    cabinet classes.
    """

    # Create the output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)

    export_pal_for_proficut(order, output_path)
    export_pfl_for_proficut(order, output_path)
    export_front_for_nettfront(order, output_path)
    export_csv(order, output_path)
    export_stl_order(order, output_path, is_horizontal_layout=False)
    export_cost_sheet(order, output_path)
    print_order_summary(order)
    generate_offer_file(order, output_path)
    generate_assembly_file(order, output_path)
    generate_drill_file(order, output_path)

    print(f"Manufacturing files generated in: {output_path}")

