# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
from .order import Order
# from .cabinets.architectures import *
from .cabinets.cabinet import Cabinet
# from .cabinets.elements.board import *
# from .cabinets.elements.accessory import *

import os, json
from AIGenFurniture.furniture_design.cabinets.elements import ELEMENTS
from AIGenFurniture.furniture_design.cabinets.architectures import get_cabinet_factory
from AIGenFurniture.furniture_design.cabinets.features import get_feature_handler

'''
The design_furniture function is the main entry point for designing furniture. It checks the cabinet_type from the 
customer input and calls specific design functions based on the type.
design_kitchen_cabinet and design_wardrobe_cabinet are design functions for specific cabinet types. They extract 
relevant information from the customer input and use it to create instances of the KitchenCabinet and WardrobeCabinet 
classes, respectively.
Make sure to adjust these functions according to the specific attributes and logic you have in your cabinet classes 
and customer input data. Additionally, you might want to add error handling and validation based on your 
project requirements.
'''

# DEFAULT_RULES_PATH = ".default_rules.json"
DEFAULT_RULES_PATH = os.path.join(os.path.dirname(__file__), "default_rules.json")
# TODO move rules to the FreeCAD as spreadsheet

def design_furniture(customer_data):
    """
    This method returns the Order object complete with all parameters cabinets and elements based on the input
    :param customer_data: file containing customer data in JSON format
    :return: Order object
    """
    order = Order(customer_data)
    cabinets_data = customer_data.get("cabinets", [])
    elements_data = customer_data.get("elements", [])

    for cabinet_data in cabinets_data:
        cabinet_label = cabinet_data.get("label")
        designed_cabinet = cabinet_handler(cabinet_data)
        if "additional_features" in cabinet_data:
            additional_features = cabinet_data.get("additional_features")
            for feature in additional_features:
                feature_handler(designed_cabinet, feature)

        # handling of "positioning" when positioning[{"move": ["x", 100]}, {"rotate": "x"}]
        if "positioning" in cabinet_data:
            positioning = cabinet_data.get("positioning")
            for movement in positioning:
                if "move" in movement:
                    move = movement.get("move")
                    designed_cabinet.move_corp(move[0], move[1])
                elif "rotate" in movement:
                    axis = movement.get("rotate")
                    designed_cabinet.rotate_corp(axis)
                else:
                    print(f"Unidentified movement")

        if "additional_elements" in cabinet_data:
            additional_elements = cabinet_data.get("additional_elements")
            for element in additional_elements:
                element_handler(designed_cabinet, element)

        order.append(designed_cabinet)
    # define dummy cabinet for additional elements
    rules = load_default_rules(DEFAULT_RULES_PATH)
    generic_cab = Cabinet("Generic", 100, 100, 100, rules)
    for element_data in elements_data:
        element_handler(generic_cab, element_data)
    order.append(generic_cab)
    return order


def load_default_rules(input_file):
    with open(input_file, 'r') as file:
        return json.load(file)


# def element_handler(cabinet, element_data):
#     """
#     Add elements like Boards and Accessories to a cabinet
#     :param cabinet:
#     :param element_data:
#     :return:
#     """
#     element_type = element_data.get("element_type")
#     if element_type == "BoardPal":
#         element = BoardPal(element_data.get("label"),
#                            element_data.get("length"),
#                            element_data.get("width"),
#                            element_data.get("thick"),
#                            element_data.get("cant_L1"),
#                            element_data.get("cant_L2"),
#                            element_data.get("cant_l1"),
#                            element_data.get("cant_l2")
#                            )
#         # element.move("z", element.thick + 2)
#         cabinet.append(element)
#     elif element_type in ("Blat", "Countertop"):
#         element = Blat(element_data.get("label"), element_data.get("length"), element_data.get("width"), element_data.get("thick"))
#         # element.move("z", element.thick + 2)
#         cabinet.append(element)
#     elif element_type == "Front":
#         element = Front(element_data.get("label"), element_data.get("length"), element_data.get("width"), element_data.get("thick"))
#         # element.move("z", element.thick + 2)
#         cabinet.append(element)
#     elif element_type == "PFL":
#         element = Pfl(element_data.get("label"), element_data.get("length"), element_data.get("width"))
#         cabinet.append(element)
#     elif element_type == "Accessory" or "accessory":
#         element = Accessory(element_data.get("label"), element_data.get("pieces"))
#         cabinet.append(element)
#     else:
#         print(f"Unsupported element {element_type}")
#         return
#
#     # Apply positioning if provided (supports same schema as cabinets)
#     if "positioning" in element_data:
#         for movement in element_data.get("positioning", []):
#             if "move" in movement:
#                 move = movement.get("move")
#                 # move is ["axis", value]
#                 element.move(move[0], move[1])
#             elif "rotate" in movement:
#                 axis = movement.get("rotate")
#                 element.rotate(axis)
#             else:
#                 print("Unidentified element movement")


def element_handler(cabinet, element_data):
    element_type = element_data.get("element_type")

    element_def = ELEMENTS.get(element_type)
    if not element_def or not element_def.get("enabled", False):
        print(f"[INFO] Element skipped (disabled or unknown): {element_type}")
        return

    element_cls = element_def.get("class")
    if not callable(element_cls):
        raise TypeError(
            f"Invalid element class for '{element_type}'"
        )

    ctor_keys = element_def["constructor"]
    ctor_args = {
        k: element_data[k]
        for k in ctor_keys
        if k in element_data
    }
    # allowed_params = element_def.get("params")
    # print(allowed_params)
    #
    # # Remove meta keys before constructor
    # params = {
    #     k: v for k, v in element_data.items()
    #     if k not in allowed_params
    # }
    # print(params)

    element = element_cls(**ctor_args)
    cabinet.append(element)

    # Optional positioning
    for movement in element_data.get("positioning", []):
        if "move" in movement:
            axis, value = movement["move"]
            element.move(axis, value)
        elif "rotate" in movement:
            element.rotate(movement["rotate"])

# def feature_handler(cabinet, feature_data):
#     """
#     This method maps the feature type to the matching feature method:
#         front -> add_front
#         add_pol_2 -> add_pol_2
#
#     :param cabinet: Cabinet object to which the features are added
#     :param feature_data: data of the feature to be added
#     :return:
#     """
#     feature_type = feature_data.get("feature")
#     # direct cabinet features
#     if feature_type == "front":
#         cabinet.add_front(feature_data.get("split_list"), feature_data.get("front_type"))
#     elif feature_type == "remove_all_pfl":
#         cabinet.remove_all_pfl()
#     elif feature_type == "remove_element":
#         cabinet.remove_element(feature_data.get("type"), feature_data.get("label"))
#     elif feature_type == "add_pfl":
#         cabinet.add_pfl()
#     # drawers features
#     elif feature_type == "add_tandem_box":
#         cabinet.add_tandem_box(feature_data.get("type"), feature_data.get("offset"))
#     elif feature_type == "add_drawer":
#         cabinet.add_drawer(feature_data.get("height"), feature_data.get("offset"), feature_data.get("box_type"), feature_data.get("bottom"))
#     elif feature_type == "add_drawer_a_pfl":
#         cabinet.add_drawer_a_pfl(feature_data.get("height"), feature_data.get("offset"))
#     elif feature_type == "add_drawer_a_pal":
#         cabinet.add_drawer_a_pal(feature_data.get("height"), feature_data.get("offset"))
#     elif feature_type == "add_drawer_b_pal":
#         cabinet.add_drawer_b_pal(feature_data.get("height"), feature_data.get("offset"))
#     elif feature_type == "add_drawer_pal_glass":
#         cabinet.add_drawer_pal_glass(feature_data.get("height"), feature_data.get("offset"))
#     # shelves features
#     elif feature_type == "add_pol":
#         cabinet.add_pol(feature_data.get("nr"), feature_data.get("cant"))
#     elif feature_type == "add_pol_2":
#         cabinet.add_pol_2(feature_data.get("orient"), feature_data.get("length"), feature_data.get("height"), feature_data.get("offset"))
#     elif feature_type == "add_separator":
#         cabinet.add_separator(feature_data.get("orient"), feature_data.get("sep_cant"))
#     elif feature_type == "add_wine_shelf":
#         cabinet.add_wine_shelf(feature_data.get("goluri"), feature_data.get("left_right"), feature_data.get("cant"))
#     elif feature_type == "add_sep_v":
#         cabinet.add_sep_v(feature_data.get("height"), feature_data.get("offset_x"), feature_data.get("offset_z"), feature_data.get("cant"))
#     elif feature_type == "add_sep_h":
#         cabinet.add_sep_h(feature_data.get("width"), feature_data.get("offset_x"), feature_data.get("offset_z"), feature_data.get("cant"))
#     else:
#         print(f"Unsupported feature {feature_type}")

def feature_handler(cabinet, feature_data):
    feature_type = feature_data.get("feature")

    handler = get_feature_handler(feature_type)

    if not handler:
        print(f"[WARNING] Feature disabled or unknown: {feature_type}")
        return

    handler(cabinet, feature_data)

# def cabinet_handler(cabinet_data):
#
#     cabinet_type = cabinet_data.get("cabinet_type")
#     label = cabinet_data.get("label", {})
#     height = cabinet_data.get("height")
#     width = cabinet_data.get("width")
#     depth = cabinet_data.get("depth")
#     rules = load_default_rules(DEFAULT_RULES_PATH)
#
#     if cabinet_type == "Cabinet":
#         return Cabinet(label, height, width, depth, rules)
#     elif cabinet_type == "BaseBox":
#         return BaseBox(label, height, width, depth, rules)
#     elif cabinet_type == "BaseCorner":
#         cut_depth = cabinet_data.get("cut_depth")
#         cut_width = cabinet_data.get("cut_width")
#         l_r = cabinet_data.get("l_r")
#         with_polita = cabinet_data.get("with_polita")
#         return BaseCorner(label, height, width, depth, rules, cut_width, cut_depth, l_r, with_polita)
#     elif cabinet_type == "TopCorner":
#         cut_width = cabinet_data.get("cut_width")
#         cut_depth = cabinet_data.get("cut_depth")
#         l_r = cabinet_data.get("l_r")
#         polite = cabinet_data.get("polite")
#         return TopCorner(label, height, width, depth, rules, cut_width, cut_depth, l_r, polite)
#     elif cabinet_type == "Raft":
#         shelves = cabinet_data.get("shelves")
#         return Raft(label, height, width, depth, rules, shelves)
#     elif cabinet_type == "Bar":
#         return Bar(label, height, width, depth, rules)
#     elif cabinet_type == "JollyBox":
#         return JollyBox(label, height, width, depth, rules)
#     elif cabinet_type == "TopBox":
#         return TopBox(label, height, width, depth, rules)
#     elif cabinet_type == "SinkBox":
#         return SinkBox(label, height, width, depth, rules)
#     elif cabinet_type == "TowerBox":
#         kwargs = {}
#         if "gap_list" in cabinet_data:
#             kwargs["gap_list"] = cabinet_data["gap_list"]
#         if "gap_heat" in cabinet_data:
#             kwargs["gap_heat"] = cabinet_data["gap_heat"]
#         if "front_list" in cabinet_data:
#             kwargs["front_list"] = cabinet_data["front_list"]
#         # gap_list = cabinet_data.get("gap_list")
#         # gap_heat = cabinet_data.get("gap_heat")
#         # front_list = cabinet_data.get("front_list")
#         return TowerBox(label, height, width, depth, rules, **kwargs)
#     elif cabinet_type == "MsVBox":
#         return MsVBox(label, height, width, depth, rules)
#     elif cabinet_type == "BaseCornerShelf":
#         shelves = cabinet_data.get("shelves")
#         return BaseCornerShelf(label, height, width, depth, rules, shelves)
#     elif cabinet_type == "Banca":
#         gap_front = cabinet_data.get("gap_front")
#         gap_lat = cabinet_data.get("gap_lat")
#         height_base = cabinet_data.get("height_base")
#         return Banca(label, height, width, depth, rules, gap_front, gap_lat, height_base)
#     elif cabinet_type == "Etajera":
#         shelves = cabinet_data.get("shelves")
#         return Etajera(label, height, width, depth, rules, shelves)
#     elif cabinet_type == "CorpDressing":
#         gap_list = cabinet_data.get("gap_list")
#         front_list = cabinet_data.get("front_list")
#         return CorpDressing(label, height, width, depth, rules, gap_list, front_list)
#     elif cabinet_type == "Dulap":
#         return Dulap(label, height, width, depth, rules)
#     elif cabinet_type == "CorpCuPicioare":
#         plinta = cabinet_data.get("skirt_height")
#         return CorpCuPicioare(label, height, width, depth, rules, plinta)
#
#     else:
#         raise ValueError(f"Unsupported cabinet type: {cabinet_type}")

def cabinet_handler(cabinet_data):
    cabinet_type = cabinet_data.get("cabinet_type")
    label = cabinet_data.get("label", "")
    height = cabinet_data.get("height")
    width = cabinet_data.get("width")
    depth = cabinet_data.get("depth")

    rules = load_default_rules(DEFAULT_RULES_PATH)

    factory = get_cabinet_factory(cabinet_type)
    if not factory:
        raise ValueError(f"Unsupported or disabled cabinet type: {cabinet_type}")

    # Factory handles simple vs special constructors internally
    return factory(
        label,
        height,
        width,
        depth,
        rules,
        box=cabinet_data  # pass full data, factory picks what it needs
    )