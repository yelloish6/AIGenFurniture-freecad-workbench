# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
from .order import Order
# from .cabinets.architectures import *
from .cabinets.cabinet import Cabinet
from .._resources import get_resource_path
# from .cabinets.elements.board import *
# from .cabinets.elements.accessory import *

import math
import numbers
import os, json, tempfile
from .cabinets.elements import ELEMENTS
from .cabinets.architectures import get_cabinet_factory
from .cabinets.features import get_feature_handler
from .cabinets.elements.accessory import Accessory
from .accessory_spreadsheet import decimal_to_number, parse_quantity

try:
    import FreeCAD
except ImportError:
    FreeCAD = None

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

# Deprecated public alias for the packaged factory rules file.
DEFAULT_RULES_PATH = get_resource_path("furniture_design", "default_rules.json")
DEFAULT_RULES_BASELINE = {
    "thick_pal": 18,
    "thick_front": 18,
    "thick_blat": 38,
    "thick_pfl": 4,
    "height_legs": 100,
    "general_height": 720,
    "general_width": 600,
    "general_depth": 500,
    "gap_front": 2,
    "front_clearance": 2,
    "pol_depth": 20,
    "cant_general": 1,
    "cant_pol": 2,
    "cant_separator": 1,
}
DESIGN_RULE_LABELS = {
    "thick_pal": "Chipboard thickness",
    "thick_front": "Front thickness",
    "thick_blat": "Countertop thickness",
    "thick_pfl": "HDF thickness",
    "height_legs": "Plinth height",
    "general_height": "Default cabinet height",
    "general_width": "Default cabinet width",
    "general_depth": "Default cabinet depth",
    "gap_front": "Gap between adjacent fronts",
    "front_clearance": "Outer front clearance",
    "cant_general": "General edge-band thickness",
    "cant_pol": "Shelf edge-band thickness",
    "cant_separator": "Separator edge-band thickness",
    "pol_depth": "Shelf setback from front",
}
REQUIRED_DESIGN_RULE_KEYS = tuple(DEFAULT_RULES_BASELINE.keys())
POSITIVE_DESIGN_RULE_KEYS = (
    "thick_pal",
    "thick_front",
    "thick_blat",
    "thick_pfl",
    "general_height",
    "general_width",
    "general_depth",
)
NON_NEGATIVE_DESIGN_RULE_KEYS = (
    "height_legs",
    "gap_front",
    "front_clearance",
    "pol_depth",
    "cant_general",
    "cant_pol",
    "cant_separator",
)
# TODO move rules to the FreeCAD as spreadsheet


class DesignRulesValidationError(ValueError):
    def __init__(self, errors):
        self.errors = list(errors)
        super().__init__("\n".join(self.errors))


def _rule_label(key):
    return DESIGN_RULE_LABELS.get(key, key.replace("_", " ").title())


def _format_rule_value(value):
    return repr(value)


def validate_design_rules(rules):
    """Validate Community Design Rules and return a migrated copy."""
    if not isinstance(rules, dict):
        raise DesignRulesValidationError(["Design rules must be a JSON object."])

    migrated = _migrate_rules(rules)
    errors = []
    normalized_values = {}

    for key in REQUIRED_DESIGN_RULE_KEYS:
        label = _rule_label(key)
        if key not in migrated:
            errors.append("{} is required.".format(label))
            continue

        value = migrated[key]
        if isinstance(value, bool) or not isinstance(value, numbers.Real):
            errors.append(
                "{} must be a finite number; got {}.".format(
                    label,
                    _format_rule_value(value),
                )
            )
            continue

        numeric_value = float(value)
        if not math.isfinite(numeric_value):
            errors.append(
                "{} must be a finite number; got {}.".format(
                    label,
                    _format_rule_value(value),
                )
            )
            continue

        normalized_values[key] = numeric_value
        if key in POSITIVE_DESIGN_RULE_KEYS and numeric_value <= 0:
            errors.append(
                "{} must be greater than 0 mm; got {}.".format(
                    label,
                    _format_rule_value(value),
                )
            )
        elif key in NON_NEGATIVE_DESIGN_RULE_KEYS and numeric_value < 0:
            errors.append(
                "{} must be 0 mm or greater; got {}.".format(
                    label,
                    _format_rule_value(value),
                )
            )

    if not errors:
        height = normalized_values["general_height"]
        width = normalized_values["general_width"]
        depth = normalized_values["general_depth"]
        thick_pal = normalized_values["thick_pal"]
        height_legs = normalized_values["height_legs"]
        front_clearance = normalized_values["front_clearance"]
        pol_depth = normalized_values["pol_depth"]
        cant_general = normalized_values["cant_general"]

        relational_checks = (
            (
                height - height_legs,
                "Plinth height must leave positive usable cabinet height; got {} with Default cabinet height {}.".format(
                    _format_rule_value(migrated["height_legs"]),
                    _format_rule_value(migrated["general_height"]),
                ),
            ),
            (
                depth - pol_depth,
                "Shelf setback from front must leave positive shelf depth; got {} with Default cabinet depth {}.".format(
                    _format_rule_value(migrated["pol_depth"]),
                    _format_rule_value(migrated["general_depth"]),
                ),
            ),
            (
                width - (2 * front_clearance),
                "Outer front clearance must leave positive front width; got {} with Default cabinet width {}.".format(
                    _format_rule_value(migrated["front_clearance"]),
                    _format_rule_value(migrated["general_width"]),
                ),
            ),
            (
                height - (2 * front_clearance),
                "Outer front clearance must leave positive front height; got {} with Default cabinet height {}.".format(
                    _format_rule_value(migrated["front_clearance"]),
                    _format_rule_value(migrated["general_height"]),
                ),
            ),
            (
                width - (2 * thick_pal),
                "Chipboard thickness must leave positive internal cabinet width; got {} with Default cabinet width {}.".format(
                    _format_rule_value(migrated["thick_pal"]),
                    _format_rule_value(migrated["general_width"]),
                ),
            ),
            (
                height - (2 * thick_pal),
                "Chipboard thickness must leave positive internal cabinet height; got {} with Default cabinet height {}.".format(
                    _format_rule_value(migrated["thick_pal"]),
                    _format_rule_value(migrated["general_height"]),
                ),
            ),
            (
                depth - cant_general,
                "General edge-band thickness must leave positive cabinet depth where edging is subtracted; got {} with Default cabinet depth {}.".format(
                    _format_rule_value(migrated["cant_general"]),
                    _format_rule_value(migrated["general_depth"]),
                ),
            ),
        )
        for remaining, message in relational_checks:
            if remaining <= 0:
                errors.append(message)

    if errors:
        raise DesignRulesValidationError(errors)

    return migrated


def get_user_rules_path():
    if FreeCAD is None:
        raise RuntimeError("FreeCAD is required to resolve the user design rules path")

    return os.path.join(
        FreeCAD.getUserAppDataDir(),
        "AIGenFurniture",
        "design_rules.json",
    )


def _print_rules_warning(message):
    text = "[AIGenFurniture] {}\n".format(message)
    if FreeCAD is not None and hasattr(FreeCAD, "Console"):
        FreeCAD.Console.PrintWarning(text)
    else:
        print(text, end="")


def _load_rules_file(input_file):
    with open(input_file, "r") as file:
        rules = json.load(file)

    if not isinstance(rules, dict):
        raise ValueError("design rules JSON must contain an object")

    return rules


def _migrate_rules(rules):
    migrated = dict(rules)

    if "general_depth" not in migrated and "width_blat" in migrated:
        migrated["general_depth"] = migrated["width_blat"]
    if "front_clearance" not in migrated and "gap_front" in migrated:
        migrated["front_clearance"] = migrated["gap_front"]

    for deprecated_key in ("width_blat", "gap_spate", "gap_fata"):
        migrated.pop(deprecated_key, None)

    return migrated


def _overlay_rules(base_rules, loaded_rules):
    rules = dict(base_rules)
    rules.update(_migrate_rules(loaded_rules))
    return rules


def load_factory_rules():
    rules = dict(DEFAULT_RULES_BASELINE)
    rules = _overlay_rules(rules, _load_rules_file(DEFAULT_RULES_PATH))
    try:
        return validate_design_rules(rules)
    except DesignRulesValidationError as exc:
        raise RuntimeError("Packaged factory design rules are invalid: {}".format(exc)) from exc


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

        if "accessories" in cabinet_data:
            designed_cabinet.elements_list = [
                element for element in designed_cabinet.elements_list
                if getattr(element, "type", None) != "accessory"
            ]

        for accessory_data in cabinet_data.get("accessories", []) or []:
            if not isinstance(accessory_data, dict):
                continue
            label = accessory_data.get("Accessory Name", accessory_data.get("label", ""))
            quantity = accessory_data.get("Quantity", accessory_data.get("pieces", ""))
            unit = accessory_data.get("Unit", accessory_data.get("unit"))
            designed_cabinet.append(
                Accessory(label, decimal_to_number(parse_quantity(quantity, "JSON accessory quantity", label)), unit)
            )

        order.append(designed_cabinet)
    # define dummy cabinet for additional elements
    rules = load_default_rules()
    generic_cab = Cabinet("Generic", 100, 100, 100, rules)
    for element_data in elements_data:
        element_handler(generic_cab, element_data)
    order.append(generic_cab)
    return order


def load_default_rules(input_file=None):
    if input_file is not None:
        return validate_design_rules(_overlay_rules(DEFAULT_RULES_BASELINE, _load_rules_file(input_file)))

    rules = load_factory_rules()
    user_rules_path = get_user_rules_path()
    if not os.path.exists(user_rules_path):
        return rules

    try:
        return validate_design_rules(_overlay_rules(rules, _load_rules_file(user_rules_path)))
    except (OSError, ValueError, TypeError, DesignRulesValidationError) as exc:
        _print_rules_warning(
            "Could not read user design rules from '{}': {}. Using factory defaults.".format(
                user_rules_path,
                exc,
            )
        )
        return rules


def save_default_rules(rules: dict, output_file=None):
    rules = validate_design_rules(rules)
    rules_path = output_file or get_user_rules_path()
    rules_dir = os.path.dirname(rules_path)
    if rules_dir:
        os.makedirs(rules_dir, exist_ok=True)

    temp_file = tempfile.NamedTemporaryFile(
        "w",
        delete=False,
        dir=rules_dir or ".",
        prefix=".design_rules.",
        suffix=".tmp",
    )
    temp_path = temp_file.name
    try:
        with temp_file as file:
            json.dump(rules, file, indent=4)
            file.write("\n")
            file.flush()
            os.fsync(file.fileno())
        os.replace(temp_path, rules_path)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


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
    param_aliases = element_def.get("param_aliases", {})
    canonical_aliases = {target: alias for alias, target in param_aliases.items()}
    ctor_args = {}
    for key in ctor_keys:
        if key in element_data:
            ctor_args[key] = element_data[key]
            continue

        alias = canonical_aliases.get(key)
        if alias in element_data:
            ctor_args[key] = element_data[alias]
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

    rules = load_default_rules()

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
