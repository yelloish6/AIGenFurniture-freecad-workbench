# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
import os
import csv

from ._board_utils import _get_board_type_elements

def export_csv(order, output_folder, elements_registry=None):
    """
    Generates .csv files containing all elements in an order, in separate files
    based on element type.

    For every element type registered in elements_registry (including addon types)
    that inherits from Board, a file named BOM_<element_type>_<customer_name>.csv
    is produced with the fields: Label, Length, Width, Thickness, m2, m3.

    The legacy per-type files (chipboard, hdf, front, countertop) and the
    PanelsCuttingList files are preserved unchanged.

    :param order: Order object as input
    :param output_folder: output folder path
    :param elements_registry: the merged ELEMENTS registry (core + addons).
                              If None, falls back to the base-only registry.
    :return:
    """
    folder_name = output_folder
    cabinets = order.cabinets_list

    if isinstance(elements_registry, dict) and "elements_registry" in elements_registry:
        elements_registry = elements_registry["elements_registry"]

    # Ensure client name is not None for filename
    client_name = order.client if order.client else "Unknown"

    # ------------------------------------------------------------------
    # Legacy exports — kept exactly as before
    # ------------------------------------------------------------------

    # output pal order
    name = os.path.join(folder_name, "BOM_chipboard_" + client_name + ".csv")
    with open(name, mode='w', newline="") as pal_order_file:
        order_writer = csv.writer(pal_order_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        order_writer.writerow(["Pieces", "Length", "Width", "Orientable", "Label", "L1", "L2", "l1", "l2"])
        for cabinet in cabinets:
            for element in cabinet.elements_list:
                if element.type == "pal":
                    order_writer.writerow(
                        [1, element.length, element.width, 0, element.label, element.cant_list[0],
                         element.cant_list[1], element.cant_list[2], element.cant_list[3]])

    # output for solid wood
    name = os.path.join(folder_name, "BOM_solid_wood_" + client_name + ".csv")
    with open(name, mode='w', newline="") as pal_order_file:
        order_writer = csv.writer(pal_order_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        order_writer.writerow(["Label", "Length", "Width", "Thickness", "m2", "m3"])
        for cabinet in cabinets:
            for element in cabinet.elements_list:
                if element.type in ("pal", "front", "pfl", "blat"):
                    order_writer.writerow(
                        [element.label, element.length, element.width, element.thick,
                         element.get_m2(), element.get_m3()])

    # output pfl order
    name = os.path.join(folder_name, "BOM_hdf_" + client_name + ".csv")
    with open(name, mode='w', newline="") as pfl_order_file:
        order_writer = csv.writer(pfl_order_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        order_writer.writerow(["Pieces", "Length", "Width", "Label"])
        for cabinet in cabinets:
            for element in cabinet.elements_list:
                if element.type == "pfl":
                    order_writer.writerow([1, element.length, element.width, element.label])

    # output fronts order
    name = os.path.join(folder_name, "BOM_front_" + client_name + ".csv")
    with open(name, mode='w', newline="") as front_order_file:
        order_writer = csv.writer(front_order_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        order_writer.writerow(["Label", "Length", "Width"])
        order_writer.writerow([order.mat_front])
        for cabinet in cabinets:
            for element in cabinet.elements_list:
                if element.type == "front":
                    order_writer.writerow([element.label, element.length, element.width])

    # output Blat order
    name = os.path.join(folder_name, "BOM_countertop_" + client_name + ".csv")
    with open(name, mode='w', newline="") as blat_order_file:
        order_writer = csv.writer(blat_order_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        order_writer.writerow(["Label", "Length", "Width"])
        order_writer.writerow([order.mat_blat])
        for cabinet in cabinets:
            for element in cabinet.elements_list:
                if element.type == "blat":
                    order_writer.writerow([element.label, element.length, element.width])

    # output for PAL optimization
    name = os.path.join(folder_name, "PanelsCuttingList_chipboard_" + client_name + ".csv")
    with open(name, mode='w', newline="") as pal_opt_file:
        order_writer = csv.writer(pal_opt_file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        order_writer.writerow(["Length", "Width", "Qty", "Label", "Enabled"])
        for cabinet in cabinets:
            for element in cabinet.elements_list:
                if element.type == "pal":
                    order_writer.writerow([element.length, element.width, 1, element.label, "TRUE"])

    # output for PFL optimization
    name = os.path.join(folder_name, "PanelsCuttingList_hdf_" + client_name + ".csv")
    with open(name, mode='w', newline="") as pfl_opt_file:
        order_writer = csv.writer(pfl_opt_file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        order_writer.writerow(["Length", "Width", "Qty", "Enabled"])
        for cabinet in cabinets:
            for element in cabinet.elements_list:
                if element.type == "pfl":
                    order_writer.writerow([element.length, element.width, 1, element.label, "TRUE"])

    # ------------------------------------------------------------------
    # Registry-driven BOM export — one file per Board subtype
    # Covers both core types and any addon-registered Board subclasses.
    # ------------------------------------------------------------------

    if elements_registry is not None:
        grouped = _get_board_type_elements(order, elements_registry)
        for ui_label, elements in grouped.items():
            if not elements:
                continue
            safe_label = ui_label.replace(" ", "_")
            bom_name = os.path.join(folder_name, f"BOM_{safe_label}_{client_name}.csv")
            with open(bom_name, mode='w', newline="") as bom_file:
                writer = csv.writer(bom_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(["Label", "Length", "Width", "Thickness", "m2", "m3"])
                for element in elements:
                    writer.writerow([
                        element.label,
                        element.length,
                        element.width,
                        element.thick,
                        element.get_m2(),
                        element.get_m3(),
                    ])
