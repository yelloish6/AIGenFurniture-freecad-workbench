import os
import csv


def export_csv(order, output_folder):
    """
    This method generates .csv files containing all the elements in an order, in separate files based on the element
    type
    :param order: Order object as input
    :param output_folder: output folder path
    :return:
    """

    folder_name = output_folder
    cabinets = order.cabinets_list

    # Ensure client name is not None for filename
    client_name = order.client if order.client else "Unknown"

    # output pal order
    name = os.path.join(folder_name, "BOM_pal_" + client_name + ".csv")
    with open(name, mode='w', newline="") as pal_order_file:
        order_writer = csv.writer(pal_order_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        order_writer.writerow(["Pieces", "Length", "Width", "Orientable", "Label", "L1", "L2", "l1", "l2"])
        for cabinet in cabinets:
            for element in cabinet.elements_list:
                if element.type == "pal":
                    order_writer.writerow(
                        [1, element.length, element.width, 0, element.label, element.cant_list[0],
                         element.cant_list[1], element.cant_list[2], element.cant_list[3]])
    pal_order_file.close()

    # output pfl order
    name = os.path.join(folder_name, "BOM_pfl_" + client_name + ".csv")
    with open(name, mode='w', newline="") as pfl_order_file:
        order_writer = csv.writer(pfl_order_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        order_writer.writerow(["Pieces", "Length", "Width", "Label"])
        for cabinet in cabinets:
            for element in cabinet.elements_list:
                if element.type == "pfl":
                    order_writer.writerow([1, element.length, element.width, element.label])
    pfl_order_file.close()

    # output fronts order
    name = os.path.join(folder_name, "BOM_front_" + client_name + ".csv")
    with open(name, mode='w', newline="") as front_order_file:
        order_writer = csv.writer(front_order_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        #order_writer.writerow(["Label", "Length", "Width", "Price"])
        order_writer.writerow(["Label", "Length", "Width"])
        order_writer.writerow([order.mat_front])
        for cabinet in cabinets:
            for element in cabinet.elements_list:
                if element.type == "front":
                    #order_writer.writerow([element.label, element.length, element.width, element.price])
                    order_writer.writerow([element.label, element.length, element.width])
    front_order_file.close()

    # output accessories order
    # name = os.path.join(folder_name, "order_accessories_" + client_name + ".csv")
    # with open(name, mode='w', newline="") as accessory_order_file:
    #     order_writer = csv.writer(accessory_order_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #     #order_writer.writerow(["Name", "Pieces", "Price/piece", "Total Price", "Comments"])
    #     order_writer.writerow(["Name", "Pieces", "Comments"])

    #     totals = []  # totals is a list containing total accessories and their amount and price

    #     for cabinet in cabinets:
    #         for element in cabinet.elements_list:
    #             if element.type == "accessory":
    #                 order_writer.writerow(
    #                     # [element.label, element.pieces, element.price, element.pieces * element.price, element.obs])
    #                     [element.label, element.pieces, element.obs])
    #                 found_in_totals = False
    #                 for i in range(len(totals)):
    #                     if totals[i][0] == element.label:
    #                         totals[i][1] += element.pieces
    #                         found_in_totals = True
    #                 if not found_in_totals:
    #                     #totals.append([element.label, element.pieces, element.price])
    #                     totals.append([element.label, element.pieces])

    #     # total
    #     for i in range(len(totals)):
    #         # print(totals2[i][0], totals2[i][1], totals2[i][2], totals2[i][1] * totals2[i][2])
    #         order_writer.writerow(["TOTAL " + totals[i][0], totals[i][1], totals[i][2], totals[i][1] * totals[i][2]])
    # accessory_order_file.close()

    # output for PAL optimization
    name = os.path.join(folder_name, "PanelsCuttingList_pal_" + client_name + ".csv")
    with open(name, mode='w', newline="") as pal_opt_file:
        order_writer = csv.writer(pal_opt_file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        order_writer.writerow(["Length", "Width", "Qty", "Label", "Enabled"])
        for cabinet in cabinets:
            for element in cabinet.elements_list:
                if element.type == "pal":
                    order_writer.writerow([element.length, element.width, 1, element.label, "TRUE"])
    pal_opt_file.close()

    # output for PFL optimization
    name = os.path.join(folder_name, "PanelsCuttingList_pfl_" + client_name + ".csv")
    with open(name, mode='w', newline="") as pfl_opt_file:
        order_writer = csv.writer(pfl_opt_file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        order_writer.writerow(["Length", "Width", "Qty", "Enabled"])
        for cabinet in cabinets:
            for element in cabinet.elements_list:
                if element.type == "pfl":
                    order_writer.writerow([element.length, element.width, 1, element.label, "TRUE"])
    pfl_opt_file.close()
