# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
import os
import csv

from ._board_utils import (
    _get_board_type_elements,
    _get_elements_by_type,
    _group_elements_by_material,
    _safe_filename_part,
)


def _get_registry_key_by_ui_label(elements_registry, ui_label):
    for key, element_def in elements_registry.items():
        if element_def.get("UI_label", key) == ui_label:
            return key
    return None


def _get_registry_param_value(element, element_def, param_name, default_value=""):
    if hasattr(element, param_name):
        return getattr(element, param_name)

    if param_name == "Material":
        return getattr(element, "material", default_value)

    if param_name == "ManufacturingRoute":
        return getattr(element, "manufacturing_route", default_value)

    lower_name = param_name.lower()
    if hasattr(element, lower_name):
        return getattr(element, lower_name)

    cant_params = [
        name for name in element_def.get("params", {})
        if name.startswith("cant_")
    ]
    if hasattr(element, "cant_list") and param_name in cant_params:
        cant_index = cant_params.index(param_name)
        if cant_index < len(element.cant_list):
            return element.cant_list[cant_index]

    return default_value


def _get_param_default(param_spec, param_name):
    if isinstance(param_spec, tuple):
        return param_spec[1]

    if isinstance(param_spec, dict):
        return param_spec.get("default", "")

    raise TypeError(f"Unsupported property definition for '{param_name}'")


def export_csv(order, output_folder, elements_registry=None):
    """
    Generates .csv files containing all elements in an order, in separate files
    based on element type and material.

    For every element type registered in elements_registry (including addon types)
    that inherits from Board, files named
    BOM_<element_type>_<material>_<customer_name>.csv are produced with the
    fields: Label, Length, Width, Thickness, m2, m3, plus any extra element
    params declared in the registry.

    PanelsCuttingList files are generated for chipboard and HDF/PFL, split by
    element.material.

    :param order: Order object as input
    :param output_folder: output folder path
    :param elements_registry: the merged ELEMENTS registry (core + addons).
                              If None, falls back to the base-only registry.
    :return:
    """
    folder_name = output_folder

    if isinstance(elements_registry, dict) and "elements_registry" in elements_registry:
        elements_registry = elements_registry["elements_registry"]

    # Ensure client name is not None for filename
    client_name = order.client if order.client else "Unknown"

    # ------------------------------------------------------------------
    # Legacy exports — kept exactly as before
    # ------------------------------------------------------------------

    # # output pal order
    # name = os.path.join(folder_name, "BOM_chipboard_" + client_name + ".csv")
    # with open(name, mode='w', newline="") as pal_order_file:
    #     order_writer = csv.writer(pal_order_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #     order_writer.writerow(["Pieces", "Length", "Width", "Orientable", "Label", "L1", "L2", "l1", "l2"])
    #     for cabinet in cabinets:
    #         for element in cabinet.elements_list:
    #             if element.type == "pal":
    #                 order_writer.writerow(
    #                     [1, element.length, element.width, 0, element.label, element.cant_list[0],
    #                      element.cant_list[1], element.cant_list[2], element.cant_list[3]])
    #
    # # output for solid wood
    # name = os.path.join(folder_name, "BOM_solid_wood_" + client_name + ".csv")
    # with open(name, mode='w', newline="") as pal_order_file:
    #     order_writer = csv.writer(pal_order_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #     order_writer.writerow(["Label", "Length", "Width", "Thickness", "m2", "m3"])
    #     for cabinet in cabinets:
    #         for element in cabinet.elements_list:
    #             if element.type in ("pal", "front", "pfl", "blat"):
    #                 order_writer.writerow(
    #                     [element.label, element.length, element.width, element.thick,
    #                      element.get_m2(), element.get_m3()])
    #
    # # output pfl order
    # name = os.path.join(folder_name, "BOM_hdf_" + client_name + ".csv")
    # with open(name, mode='w', newline="") as pfl_order_file:
    #     order_writer = csv.writer(pfl_order_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #     order_writer.writerow(["Pieces", "Length", "Width", "Label"])
    #     for cabinet in cabinets:
    #         for element in cabinet.elements_list:
    #             if element.type == "pfl":
    #                 order_writer.writerow([1, element.length, element.width, element.label])
    #
    # # output fronts order
    # name = os.path.join(folder_name, "BOM_front_" + client_name + ".csv")
    # with open(name, mode='w', newline="") as front_order_file:
    #     order_writer = csv.writer(front_order_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #     order_writer.writerow(["Label", "Length", "Width"])
    #     order_writer.writerow([order.mat_front])
    #     for cabinet in cabinets:
    #         for element in cabinet.elements_list:
    #             if element.type == "front":
    #                 order_writer.writerow([element.label, element.length, element.width])
    #
    # # output Blat order
    # name = os.path.join(folder_name, "BOM_countertop_" + client_name + ".csv")
    # with open(name, mode='w', newline="") as blat_order_file:
    #     order_writer = csv.writer(blat_order_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #     order_writer.writerow(["Label", "Length", "Width"])
    #     order_writer.writerow([order.mat_blat])
    #     for cabinet in cabinets:
    #         for element in cabinet.elements_list:
    #             if element.type == "blat":
    #                 order_writer.writerow([element.label, element.length, element.width])

    # output for PAL optimization
    pal_by_material = _group_elements_by_material(_get_elements_by_type(order, "pal"))
    for material, elements in pal_by_material.items():
        safe_material = _safe_filename_part(material)
        name = os.path.join(
            folder_name,
            f"PanelsCuttingList_chipboard_{safe_material}_{client_name}.csv",
        )
        with open(name, mode='w', newline="") as pal_opt_file:
            order_writer = csv.writer(pal_opt_file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            order_writer.writerow(["Length", "Width", "Qty", "Label", "Enabled"])
            for element in elements:
                order_writer.writerow([element.length, element.width, 1, element.label, "TRUE"])

    # output for PFL optimization
    pfl_by_material = _group_elements_by_material(_get_elements_by_type(order, "pfl"))
    for material, elements in pfl_by_material.items():
        safe_material = _safe_filename_part(material)
        name = os.path.join(
            folder_name,
            f"PanelsCuttingList_hdf_{safe_material}_{client_name}.csv",
        )
        with open(name, mode='w', newline="") as pfl_opt_file:
            order_writer = csv.writer(pfl_opt_file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            order_writer.writerow(["Length", "Width", "Qty", "Label", "Enabled"])
            for element in elements:
                order_writer.writerow([element.length, element.width, 1, element.label, "TRUE"])

    # ------------------------------------------------------------------
    # Registry-driven BOM export — one file per Board subtype and material
    # Covers both core types and any addon-registered Board subclasses.
    # ------------------------------------------------------------------

    if elements_registry is not None:
        grouped = _get_board_type_elements(order, elements_registry)
        for ui_label, elements in grouped.items():
            if not elements:
                continue
            registry_key = _get_registry_key_by_ui_label(elements_registry, ui_label)
            element_def = elements_registry.get(registry_key, {})
            param_names = list(element_def.get("params", {}).keys())
            safe_label = _safe_filename_part(ui_label)
            for material, material_elements in _group_elements_by_material(elements).items():
                safe_material = _safe_filename_part(material)
                bom_name = os.path.join(
                    folder_name,
                    f"BOM_{safe_label}_{safe_material}_{client_name}.csv",
                )
                with open(bom_name, mode='w', newline="") as bom_file:
                    writer = csv.writer(bom_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(["Label", "Length", "Width", "Thickness", "m2", "m3"] + param_names)
                    for element in material_elements:
                        row = [
                            element.label,
                            element.length,
                            element.width,
                            element.thick,
                            element.get_m2(),
                            element.get_m3(),
                        ]
                        for param_name in param_names:
                            param_spec = element_def["params"][param_name]
                            default_value = _get_param_default(param_spec, param_name)
                            row.append(
                                _get_registry_param_value(element, element_def, param_name, default_value)
                            )
                        writer.writerow(row)
