import os, sys
import json
import argparse

# 🔹 Add vendor folder to sys.path
_vendor_path = os.path.join(os.path.dirname(__file__), "vendor")
if _vendor_path not in sys.path:
    sys.path.insert(0, _vendor_path)

from .furniture_design.design_engine import design_furniture
from .manufacturing.generate_files import generate_manufacturing_files
''' 
Loads customer input data from JSON files in the customer_input directory.
Uses the design_furniture function from the design_engine module to create an order based on customer input.
Displays a summary of the order.
Generates manufacturing files using the generate_manufacturing_files function from the manufacturing module.
Saves the manufacturing files in the customer's output directory within the output folder.
'''


def load_customer_input(input_file):
    with open(input_file, 'r') as file:
        return json.load(file)

def run(input_path, output_path):
    customer_data = load_customer_input(input_path)
    order = design_furniture(customer_data)
    os.makedirs(output_path, exist_ok=True)
    generate_manufacturing_files(order, output_path)

def main():
    parser = argparse.ArgumentParser(description="AIGen Furniture Generator")
    parser.add_argument("--input", required=True, help="Path to input JSON file")
    parser.add_argument("--output", required=True, help="Path to output directory")
    args = parser.parse_args()

    run(args.input, args.output)

    print(f"✅ Furniture generation complete.\nInput:  {input_path}\nOutput: {output_dir}")

if __name__ == "__main__":
    main()
