# AI Gen Furniture

## Overview

AI Gen Furniture is a Python-based project for designing custom furniture based on customer input. The project includes modules for different types of cabinets, a design engine to process customer input, and a manufacturing module to generate manufacturing files.

The structure of a furniture is the following:

- *order*: is made up of more *cabinets*
  - *cabinet:* is made up of more *elements*
    - *element:* is either a *board* or an *accessory* containing all the characteristics of that element.

## Project Structure

The project is organized into the following directories:

- **customer_input**: Contains sample customer input files in JSON formats.
  - *{*
    - *customer parameters*
    - *array of cabinets[*
      - *label*
      - *cabinet type*
      - *height*
      - *width*
      - *depth*
      - *other cabinet_type specific parameters*
      - *additional_features: [*
        - *{feature: feature_names, feature parameters}*
      - *]*
      - *positioning{*
        - *{move: [array of axis and distance to move pairs]*
        - *{rotate: [array of axis to rotate]*
      - *}*
  - *}*
- **furniture_design**: contains the needed files to generate the furniture based on customer input. The furniture is an object containing all the necessary elements.

  - **order**: Contains the class Order that takes the customer data as input. The class also contains a list of cabinets

  - **cabinets**: Contains Python modules for different types of cabinets.
    - `cabinet.py` defines the Cabinet class
    - **elements**: contains the class files and methods for the basic elements (board and accessory)
      - `board.py`: defines classes **Board**, **BoardPal**, **Front**, **Pfl**, **Blat**
      - `accessory`: defines the class **accessory** and it's methods *print()*, *set_price()* and *add_pieces(number_of_pieces)* 
    - **Dressing**: Contains all instances of *Cabinet* for cabinet achitectures specifically used in dressings
    - **Kitchen**: Contains all instances of *Cabinet* for cabinet achitectures specifically used in dressings
      - `base_cabinet.py`: Defines the base class for all cabinets.
      - `kitchen_cabinet.py`: Implements the KitchenCabinet class.
      - `wardrobe_cabinet.py`: Implements the WardrobeCabinet class.
      - ... (other cabinet modules)

- **design_engine**: Contains the design engine module.
  - `design_engine.py`: Manages the process of designing furniture based on customer input.

- **manufacturing**: Contains the manufacturing module.
  - `generate_files.py`: Implements functions to generate manufacturing files.

- **example_output**: Contains example output folders with generated manufacturing files.

- **customer_input**: Store customer input files in this directory, each file containing the requirements for a specific customer.

- **furniture_design**:

- **cabinets**: Define different types of cabinets as separate modules.

- **elements**: Define classes for the building blocks of each furniture: boards(placa), accessories, 

- **features**: Method to add standard features to cabinets like shelves, drawers, hanger bars, etc...

    - `design_engine.py`: Implement the core logic for processing customer input and generating the design.

- **manufacturing**:

    - `generate_files.py`: Implement the logic for generating manufacturing files based on the design.

- **output**: Store the output for each customer in a separate directory, containing both the manufacturing files and a summary of the design.

- **tests**: Write unit tests for your modules and logic.

- `.gitignore`: Specify files and directories to be ignored by version control.

- `README.md`: Document your project, including instructions on how to run it, dependencies, and any other relevant information.

- `main.py`: Entry point for your application. This is where you can orchestrate the overall workflow by using the modules and logic defined in the other directories.


## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/furniture-design-project.git


Remember to replace the placeholder names like file1.txt, customer1_input.json, etc., with meaningful names based on your project requirements.

Additionally, you may want to consider using a virtual environment for your project and possibly creating a requirements.txt file to list your project dependencies. This structure is just a starting point; feel free to adapt it based on your specific needs and preferences.