# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
import openpyxl
import shutil, os
from .._resources import get_resource_path


def export_front_for_nettfront(order, output_folder):

    # file_path = output_folder + "/Comanda_Front_" + order.mat_front + "_" + order.client + ".xlsx"
    file_path = output_folder + "/Comanda_Front_" + order.client + ".xlsx"
    template_path = get_resource_path("manufacturing", "templates", "Formular_de_comanda_nett_front.xlsx")
    shutil.copyfile(template_path, file_path)
    file = openpyxl.load_workbook(file_path)
    sheet = file.get_sheet_by_name("Sheet1")

    sheet['C17'] = order.mat_front

    counter = 0
    for cabinet in order.cabinets_list:
        for element in cabinet.elements_list:
            if element.type == "front":
                sheet['B' + str(21 + counter)] = element.length
                sheet['C' + str(21 + counter)] = element.width
                sheet['D' + str(21 + counter)] = 1
                sheet['F' + str(21 + counter)] = element.label
                counter += 1
    file.save(file_path)
