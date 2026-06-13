# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
import os
import shutil

import openpyxl
from openpyxl.styles.borders import Border, Side

from .._resources import get_resource_path
from ._board_utils import (
    _get_elements_by_type,
    _group_elements_by_material,
    _safe_filename_part,
)


def _prepare_proficut_workbook(template_path, file_path, clean_images=False):
    shutil.copyfile(template_path, file_path)
    file = openpyxl.load_workbook(file_path, data_only=True, keep_links=False)

    if clean_images:
        file._images = []
        for ws in file.worksheets:
            ws._images = []

    return file


def _write_proficut_order_header(sheet, order, material):
    sheet['C1'] = order.client_proficut
    sheet['D2'] = order.tel_proficut
    sheet['D3'] = order.transport
    sheet['C4'] = order.address
    sheet['G4'] = material


def _write_pal_row(sheet, row_index, element):
    sheet['A' + str(row_index)] = "1"
    sheet['B' + str(row_index)] = element.length
    sheet['C' + str(row_index)] = element.width
    sheet['D' + str(row_index)] = 0
    sheet['E' + str(row_index)] = element.label

    sheet['F' + str(row_index)] = 1 if element.cant_list[0] == 0.4 else element.cant_list[0]
    sheet['G' + str(row_index)] = 1 if element.cant_list[1] == 0.4 else element.cant_list[1]
    sheet['H' + str(row_index)] = 1 if element.cant_list[2] == 0.4 else element.cant_list[2]
    sheet['I' + str(row_index)] = 1 if element.cant_list[3] == 0.4 else element.cant_list[3]
    sheet['K' + str(row_index)] = element.obs


def _write_pfl_row(sheet, row_index, element):
    sheet['A' + str(row_index)] = "1"
    sheet['B' + str(row_index)] = element.length
    sheet['C' + str(row_index)] = element.width
    sheet['D' + str(row_index)] = 0
    sheet['E' + str(row_index)] = element.label


def _draw_cutout_sketch_template(sheet_2):
    # L-Shape - left
    sheet_2['B2'] = 'label'

    sheet_2['B4'].border = Border(top=Side(style='thick'), left=Side(style='thick'))
    sheet_2['C4'].border = Border(top=Side(style='thick'))
    sheet_2['D4'].border = Border(top=Side(style='thick'))
    sheet_2['E4'].border = Border(top=Side(style='thick'))
    sheet_2['F4'].border = Border(top=Side(style='thick'), right=Side(style='thick'))

    sheet_2['B5'].border = Border(left=Side(style='thick'))
    sheet_2['B6'].border = Border(left=Side(style='thick'))
    sheet_2['B7'].border = Border(left=Side(style='thick'))
    sheet_2['B8'].border = Border(left=Side(style='thick'))
    sheet_2['B9'].border = Border(left=Side(style='thick'), bottom=Side(style='thick'))

    sheet_2['C9'].border = Border(bottom=Side(style='thick'), right=Side(style='thick'))
    sheet_2['C8'].border = Border(right=Side(style='thick'))
    sheet_2['C7'].border = Border(right=Side(style='thick'))

    sheet_2['D6'].border = Border(bottom=Side(style='thick'))
    sheet_2['E6'].border = Border(bottom=Side(style='thick'))
    sheet_2['F6'].border = Border(bottom=Side(style='thick'), right=Side(style='thick'))

    sheet_2['F5'].border = Border(right=Side(style='thick'))

    sheet_2['D3'] = "cota 1"
    sheet_2['G5'] = "cota 2"
    sheet_2['E7'] = "cota 3"
    sheet_2['D8'] = "cota 4"
    sheet_2['B10'] = "cota 5"
    sheet_2['A7'] = "cota 6"

    # L-Shape - right
    sheet_2['B12'] = 'label'

    sheet_2['B14'].border = Border(top=Side(style='thick'), left=Side(style='thick'))
    sheet_2['C14'].border = Border(top=Side(style='thick'))
    sheet_2['D14'].border = Border(top=Side(style='thick'))
    sheet_2['E14'].border = Border(top=Side(style='thick'))
    sheet_2['F14'].border = Border(top=Side(style='thick'), right=Side(style='thick'))

    sheet_2['B15'].border = Border(left=Side(style='thick'))
    sheet_2['B16'].border = Border(left=Side(style='thick'), bottom=Side(style='thick'))
    sheet_2['C16'].border = Border(bottom=Side(style='thick'))
    sheet_2['D16'].border = Border(bottom=Side(style='thick'))

    sheet_2['E17'].border = Border(left=Side(style='thick'))
    sheet_2['E18'].border = Border(left=Side(style='thick'))

    sheet_2['E19'].border = Border(bottom=Side(style='thick'), left=Side(style='thick'))
    sheet_2['F19'].border = Border(bottom=Side(style='thick'), right=Side(style='thick'))

    sheet_2['F15'].border = Border(right=Side(style='thick'))
    sheet_2['F16'].border = Border(right=Side(style='thick'))
    sheet_2['F17'].border = Border(right=Side(style='thick'))
    sheet_2['F18'].border = Border(right=Side(style='thick'))

    sheet_2['D13'] = "cota 1"
    sheet_2['G16'] = "cota 2"
    sheet_2['E20'] = "cota 3"
    sheet_2['D18'] = "cota 4"
    sheet_2['C17'] = "cota 5"
    sheet_2['A15'] = "cota 6"

    # U-Shape
    sheet_2['B22'] = 'label'

    sheet_2['B24'].border = Border(top=Side(style='thick'), left=Side(style='thick'), right=Side(style='thick'))
    sheet_2['B25'].border = Border(left=Side(style='thick'), right=Side(style='thick'))
    sheet_2['B26'].border = Border(left=Side(style='thick'), right=Side(style='thick'))
    sheet_2['B27'].border = Border(left=Side(style='thick'), right=Side(style='thick'))
    sheet_2['B28'].border = Border(left=Side(style='thick'))
    sheet_2['B29'].border = Border(left=Side(style='thick'), bottom=Side(style='thick'))

    sheet_2['F24'].border = Border(top=Side(style='thick'), left=Side(style='thick'), right=Side(style='thick'))
    sheet_2['F25'].border = Border(left=Side(style='thick'), right=Side(style='thick'))
    sheet_2['F26'].border = Border(left=Side(style='thick'), right=Side(style='thick'))
    sheet_2['F27'].border = Border(left=Side(style='thick'), right=Side(style='thick'))
    sheet_2['F28'].border = Border(right=Side(style='thick'))
    sheet_2['F29'].border = Border(right=Side(style='thick'), bottom=Side(style='thick'))

    sheet_2['C27'].border = Border(bottom=Side(style='thick'))
    sheet_2['D27'].border = Border(bottom=Side(style='thick'))
    sheet_2['E27'].border = Border(bottom=Side(style='thick'))

    sheet_2['C29'].border = Border(bottom=Side(style='thick'))
    sheet_2['D29'].border = Border(bottom=Side(style='thick'))
    sheet_2['E29'].border = Border(bottom=Side(style='thick'))

    sheet_2['B23'] = "cota 1"
    sheet_2['C25'] = "cota 2"
    sheet_2['D27'] = "cota 3"
    sheet_2['E25'] = "cota 4"
    sheet_2['F23'] = "cota 5"
    sheet_2['G26'] = "cota 6"
    sheet_2['D30'] = "cota 7"
    sheet_2['A26'] = "cota 8"


def export_pal_for_proficut(order, output_folder):
    template_path = get_resource_path("manufacturing", "templates", "Cote-Proficut-2018.xlsx")
    client_name = order.client if order.client else "Unknown"
    pal_by_material = _group_elements_by_material(_get_elements_by_type(order, "pal"))

    for material, elements in pal_by_material.items():
        safe_material = _safe_filename_part(material)
        file_path = os.path.join(output_folder, f"Comanda_PAL_{safe_material}_{client_name}.xlsx")
        file = _prepare_proficut_workbook(template_path, file_path, clean_images=True)
        sheet = file.get_sheet_by_name("Sheet1")

        _write_proficut_order_header(sheet, order, material)

        for counter, element in enumerate(elements):
            _write_pal_row(sheet, 10 + counter, element)

        sheet_2 = file.get_sheet_by_name("Sheet2")
        _draw_cutout_sketch_template(sheet_2)
        file.save(file_path)


def export_pfl_for_proficut(order, output_folder):
    template_path = get_resource_path("manufacturing", "templates", "Cote-Proficut-2018.xlsx")
    client_name = order.client if order.client else "Unknown"
    pfl_by_material = _group_elements_by_material(_get_elements_by_type(order, "pfl"))

    for material, elements in pfl_by_material.items():
        safe_material = _safe_filename_part(material)
        file_path = os.path.join(output_folder, f"Comanda_PFL_{safe_material}_{client_name}.xlsx")
        file = _prepare_proficut_workbook(template_path, file_path)
        sheet = file.get_sheet_by_name("Sheet1")

        _write_proficut_order_header(sheet, order, material)

        for counter, element in enumerate(elements):
            _write_pfl_row(sheet, 10 + counter, element)
        file.save(file_path)
