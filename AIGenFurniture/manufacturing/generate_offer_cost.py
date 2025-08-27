import os
import csv
import math
# import fitz

PAL_LOSS = 0.1
SHEET_HEIGHT = 2800
SHEET_WIDTH = 2070
IMPOZIT = 0.1


def generate_offer_file(order, output_path):
    # doc = fitz.open()
    # page = doc.new_page()
    # shape = page.new_shape()
    # shape.draw_rect([1, 1, 594, 841]) # the size of one page
    # shape.draw_line(fitz.Point(4, 4),  fitz.Point(40, 40))
    # shape.finish(color=(0, 0, 0), width=1)
    # shape.commit()
    # doc.save(output_path + '/offer.pdf')
    # TODO implement offer file generation in .pdf
    print(f"Generating offer file in {output_path} to be implemented")


def export_cost_sheet(order, output_folder):
    """
    This method generates .csv files containing the prices for all elements from an order
    It calls the get_price method for each element
    :param order:  object as input
    :param output_folder: output folder path
    :return:
    """

    folder_name = output_folder
    cabinets = order.cabinets_list

    # output pal order
    name = os.path.join(folder_name, "Cost_Sheet" + order.client + ".csv")
    with open(name, mode='w', newline="") as cost_sheet_file:
        cost_writer = csv.writer(cost_sheet_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        cost_writer.writerow(["Element type", "Element Label", "Size", "Unit", "Material", "Price"])
        for cabinet in cabinets:
            for element in cabinet.elements_list:
                if element.type == "pal":  # TODO this IF statement can be shorter. All cases do mostly the same thing.
                    material = element.material
                    size = element.get_m2()
                    unit = element.get_unit_for_item(element.type, element.material)
                elif element.type == "front":
                    material = element.material
                    size = element.get_m2()
                    unit = element.get_unit_for_item(element.type, element.material)
                elif element.type == "pfl":
                    material = element.material
                    size = element.get_m2()
                    unit = element.get_unit_for_item(element.type, element.material)
                elif element.type == "blat":
                    material = element.material
                    size = element.get_length()
                    unit = element.get_unit_for_item(element.type, element.material)
                elif element.type == "accessory":
                    material = element.label
                    size = element.pieces
                    unit = "pieces"
                # cant1_size = element.get_m_cant("0.4")
                # cant2_size = element.get_m_cant("2")
                price = element.get_price()
                # cant1_price = get_price_for_item("cant", "0.4")
                # cant2_price = get_price_for_item("cant", "2")

                cost_writer.writerow([element.type, element.label, size, unit, material, price])
                # cost_writer.writerow(["cant", element.label, cant1_size, "m", "cant 0.4",
                #                      cant1_price, float(cant1_size) * float(cant1_price)])
                # cost_writer.writerow(["cant", element.label, cant1_size, "m", "cant 2",
                #                       cant2_price, float(cant2_size) * float(cant2_price)])
    cost_sheet_file.close()


def print_order_summary(order):
    """
    Prints a summary of the size and costs of an order, mainly for debugging purposes. Actual offer for the customer
    is generated using the generate_offer_file() method
    :param order:
    :return:
    """

    total_cost = 0

    print("*** INFORMATII GENERALE ***")
    print("Nume client: ", order.client)
    print("Numar de corpuri: ", len(order.cabinets_list))
    print("Lungime totala mobila: ", get_order_length(order))

    total_cost += get_cost_pal(order)
    print("M2 PAL: ", "{:.2f}".format(get_m2_pal(order)),
          " | Nr. coli PAL: ", get_sheets_pal(order),
          " | Nr. piese decupate:", get_count_cost_cutout_pal(order)[0],
          " | Cost decupaj piese pal: ", get_count_cost_cutout_pal(order)[1],
          " | Cost pal:", get_cost_pal(order) + get_count_cost_cutout_pal(order)[1],
          " | Material:", order.mat_pal)

    cant_price_04 = get_price_for_item("cant", "0.4") * get_m_cant(order, "0.4")
    cant_price_2 = get_price_for_item("cant", "2") * get_m_cant(order, "2")
    total_cost += cant_price_04 + cant_price_2
    print("M Cant 0.4", math.ceil(get_m_cant(order, "0.4")),
          " | Pret ", "{:.2f}".format(cant_price_04))
    print("M Cant 2", math.ceil(get_m_cant(order, "2")),
          " | Pret ", "{:.2f}".format(cant_price_2))

    pfl_price = float(get_price_for_item("pfl", order.mat_pfl) * get_sheets_pfl(order))
    total_cost += pfl_price
    print("M2 PFL: ", "{:.2f}".format(get_m2_pfl(order)),
          " | Nr. coli PFL: ", get_sheets_pfl(order),
          " | Pret PFL: ", pfl_price)

    front_price = float(get_price_for_item("front", order.mat_front) * get_m2_front(order))
    total_cost += front_price
    print("M2 Front: ", "{:.2f}".format(get_m2_front(order)),
          " | Pret ", "{:.2f}".format(front_price),
          " | Material: ", "NETT FRONT", order.mat_front)

    blat_price = float(get_price_for_item("blat", order.mat_blat) * get_m_blat(order))
    total_cost += blat_price
    print("M Blat: ", "{:.2f}".format(get_m_blat(order)),
          " | Pret", blat_price)

    cost_acc = get_cost_accessories(order)
    total_cost += cost_acc
    print("Cost total accesorii: ", cost_acc)

    cost_transport = get_cost_transport(order)
    total_cost += cost_transport
    print("Cost transport:", cost_transport)

    cost_manopera = get_cost_manopera(order)[0]
    cost_man_disc = get_cost_manopera(order)[1]
    total_cost += cost_man_disc
    if order.discount == 0:
        print("Cost manopera:", cost_manopera)
    else:
        print("Cost manopera:", cost_manopera,
              "| Discount[%]:", order.discount,
              "| Pret manopera cu discount:", cost_man_disc)

    print("Cost TOTAL:", math.ceil(total_cost))


def get_price_for_item(element_type, material):
    """
    this method returns the price of a specific element from the price_list.csv file, based on item type and material
    :param element_type:
    :param material:
    :return:
    """
    # TODO store price_list.csv in one place only, now it's in 2 places, and rewrite all paths to it. Or even write a method that reads prices that every file can access
    price_list_path = os.path.join(os.path.dirname(__file__), "templates", "price_list.csv")
    with open(price_list_path) as price_list_file:
        price_reader = csv.DictReader(price_list_file, delimiter=',')
        found = False
        for row in price_reader:
            if row["Item"] == element_type and row["Material"] == material:
                found = True
                return float(row["Price"])
        if not found:
            print("ERROR: Price for " + element_type + ":" + material + " not found. Setting to 0 RON.")
            return 0


def get_min_qty_for_item(element_type, material):
    price_list_path = os.path.join(os.path.dirname(__file__), "templates", "price_list.csv")
    with open(price_list_path) as price_list_file:
        price_reader = csv.DictReader(price_list_file, delimiter=',')
        found = False
        for row in price_reader:
            if row["Item"] == element_type and row["Material"] == material:
                found = True
                return row["Minimum"]
        if not found:
            print("ERROR: Minimum quantity for " + element_type + " : " + material + " not found. Considering 1 unit")
            return 1


def get_m2_pal(order):
    """
    returns the surface of pal in an order
    :param order:
    :return:
    """
    m2pal = 0
    for cabinet in order.cabinets_list:
        m2pal = m2pal + cabinet.get_m2_pal()
    return m2pal


def get_m2_pfl(order):
    m2pfl = 0
    for cabinet in order.cabinets_list:
        m2pfl = m2pfl + cabinet.get_m2_pfl()
    return m2pfl


def get_m2_front(order):
    m2 = 0
    for cabinet in order.cabinets_list:
        m2 = m2 + cabinet.get_m2_front()
    return m2


def get_m_cant(order, cant_type):
    """

    :param order:
    :param cant_type: "0.4" sau "2"
    :return: lungimea cantului selectat din toata comanda
    """

    m = 0
    for element in order.cabinets_list:
        m = m + element.get_m_cant(cant_type)
    return m


def get_m_blat(order):
    """
    this method returns the number of blat meters as int
    :param order:
    :return:
    """

    m = 0
    for cabinet in order.cabinets_list:
        for element in cabinet.elements_list:
            if element.type == "blat":
                m = m + element.length
    return float(m / 1000)


def get_order_length(order):
    """
    sums the width of all cabinets in an order giving the total length of an order in meters
    :param order:
    :return:
    """
    length = 0
    for cabinet in order.cabinets_list:
        length += cabinet.width
    return length / 1000


def get_sheets_pal(order):

    m2_pal = get_m2_pal(order) * (1 + PAL_LOSS)
    min_qty = float(get_min_qty_for_item("pal", order.mat_pal))
    m2_min = float(get_min_qty_for_item("pal", order.mat_pal)) * (SHEET_HEIGHT * SHEET_WIDTH / 1000000)
    sheets = math.ceil(m2_pal / m2_min) * min_qty
    if m2_pal < m2_min:
        return min_qty
    else:
        return sheets


def get_sheets_pfl(order):

    m2_pfl = get_m2_pfl(order) * (1 + PAL_LOSS)
    min_qty = float(get_min_qty_for_item("pfl", order.mat_pfl))
    m2_min = float(get_min_qty_for_item("pfl", order.mat_pfl)) * (SHEET_HEIGHT * SHEET_WIDTH / 1000000)
    sheets = math.ceil(m2_pfl / m2_min) * min_qty
    if m2_pfl == 0:
        return 0
    elif 0 < m2_pfl < min_qty:
        return min_qty
    else:
        return sheets


#TODO handle decupare blat as service not as accessory
def get_cost_pal(order):
    pal_price = get_price_for_item("pal", order.mat_pal) * get_sheets_pal(order)
    return pal_price


def get_count_cost_cutout_pal(order):
    cost_cutout = 0
    count_cutout = 0
    cutout_price = get_price_for_item("service", "decupare pal")
    for cabinet in order.cabinets_list:
        for element in cabinet.elements_list:
            if "decupaj" in element.obs:
                count_cutout += 1
                cost_cutout += cutout_price
    return [count_cutout, cost_cutout]


def get_cost_accessories(order):
    cost_acc = 0
    for cabinet in order.cabinets_list:
        for element in cabinet.elements_list:
            if element.type == "accessory":
                acc_price = float(get_price_for_item(element.type, element.material))
                cost_acc += acc_price * element.pieces
    return int(cost_acc)


# def get_cost_manopera_old(order):
#     """
#     - 8h proictare
#     - 2h per corp asamblare, pozitionare si montaj fronturi
#     - 2h montaj / electrocasnic
#     - 0.5h pe metru de blat, montaj blat
#     :return: [pret manopera, pret manopera cu discount]
#     """
#
#     discount = order.discount
#     h_rate = order.h_rate
#     electrocasnice = order.nr_electrocasnice
#     pret_manop = math.ceil((8 + (len(order.cabinets_list) * 2) + electrocasnice * 2 + get_m_blat(order) * 0.5)) * h_rate
#     pret_manop_discount = pret_manop * (100 - discount) / 100
#     return [pret_manop, pret_manop_discount]


def get_cost_manopera(order):
    """
    - 8h proiectare
    - 10 min/placa (pal, front,pfl) (0.17h/placa)
    - 2h montaj / electrocasnic
    - 30 min. pe metru de blat (0.5h/m)
    :param order:
    :return:
    """
    discount = order.discount
    h_rate = order.h_rate
    electrocasnice = order.nr_electrocasnice
    boards = order.get_boards_number()
    h_proiect = order.h_proiect
    print()
    pret_manop = math.ceil((h_proiect + (boards * 0.17) + electrocasnice * 2 + get_m_blat(order) * 0.5) * h_rate*(1 + IMPOZIT))
    pret_manop_discount = pret_manop * (100 - discount) / 100
    return [pret_manop, pret_manop_discount]


def get_cost_transport(order):
    if order.transport == "Da":
        return get_price_for_item("service", "transport")
    else:
        print("Comanda fara transport.")
        return 0

# def print_m_cant(order):
#     """
#     for debugging cant length
#     :return:
#     """
#     m1 = 0
#     m2 = 0
#     for i in range(len(order.corpuri)):
#         for j in range(len(order.corpuri[i].elements_list)):
#             placa = order.corpuri[i].elements_list[j]
#             if placa.type == "pal":
#                 m1 = m1 + placa.get_m_cant("0.4")
#                 m2 = m2 + placa.get_m_cant("2")
#     print(m1)
#     print(m2)

