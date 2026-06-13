# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
import os
import shutil

import openpyxl

from .._resources import get_resource_path
from ._board_utils import (
    _get_elements_by_type,
    _group_elements_by_material,
    _safe_filename_part,
)


def export_front_for_nettfront(order, output_folder):

    template_path = get_resource_path("manufacturing", "templates", "Formular_de_comanda_nett_front.xlsx")
    client_name = order.client if order.client else "Unknown"
    fronts_by_material = _group_elements_by_material(_get_elements_by_type(order, "front"))

    for material, elements in fronts_by_material.items():
        safe_material = _safe_filename_part(material)
        file_path = os.path.join(
            output_folder,
            f"Comanda_Front_{safe_material}_{client_name}.xlsx",
        )
        shutil.copyfile(template_path, file_path)
        file = openpyxl.load_workbook(file_path)
        sheet = file.get_sheet_by_name("Sheet1")

        sheet['C17'] = material

        for counter, element in enumerate(elements):
            sheet['B' + str(21 + counter)] = element.length
            sheet['C' + str(21 + counter)] = element.width
            sheet['D' + str(21 + counter)] = 1
            sheet['F' + str(21 + counter)] = element.label
        file.save(file_path)
