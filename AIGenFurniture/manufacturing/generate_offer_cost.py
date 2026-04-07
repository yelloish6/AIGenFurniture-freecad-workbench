import os
import csv
import math

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm

def generate_offer_file(order, output_path):
    """
    Creates a PDF file containing the same information as print_order_summary(),
    plus a detailed breakdown table at the end.
    Items with price == 0 appear RED + BOLD in the breakdown.
    """

    client_name = order.client if order.client else "Unknown"
    pdf_filename = os.path.join(output_path, f"Oferta_{client_name}.pdf")

    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm
    )

    styles = getSampleStyleSheet()
    normal = styles["Normal"]
    title = styles["Title"]

    story = []

    # ---------------------------------------------------------------------
    # TITLE
    # ---------------------------------------------------------------------
    story.append(Paragraph("OFERTA MOBILA LA COMANDA", title))
    story.append(Spacer(1, 12))

    # Small helper
    def line(text):
        story.append(Paragraph(text, normal))
        story.append(Spacer(1, 6))

    # ---------------------------------------------------------------------
    # SUMMARY TEXT (same as print_order_summary)
    # ---------------------------------------------------------------------
    total_cost = 0

    line("*** INFORMATII GENERALE ***")
    line(f"Nume client: {order.client}")
    line(f"Numar de corpuri: {len(order.cabinets_list)}")
    line(f"Lungime totala mobila: {order.get_order_length()} m")

    total_cost += order.get_cost_pal()

    line(f"M2 PAL: {order.get_total_m2_pal():.2f}"
         f" | Nr. coli PAL: {order.get_sheets_pal():.2f}"
         f" | Nr. piese decupate: {order.get_count_cutout_pal():.2f}"
         f" | Cost decupaj piese pal: {order.get_cost_cutout_pal():.2f}"
         f" | Cost pal: {order.get_cost_pal() + order.get_cost_cutout_pal():.2f}"
         f" | Material: {order.mat_pal}")

    line(f"M Cant 0.4: {math.ceil(order.get_m_cant('0.4')):.2f}"
         f" | Pret {order.get_cost_edge('0.4'):.2f}")

    line(f"M Cant 2: {math.ceil(order.get_m_cant('2')):.2f}"
         f" | Pret {order.get_cost_edge('2'):.2f}")

    line(f"M2 PFL: {order.get_total_m2_pfl():.2f}"
         f" | Nr. coli PFL: {order.get_sheets_pfl():.2f}"
         f" | Pret PFL: {order.get_cost_pfl():.2f}")

    line(f"M2 Front: {order.get_total_m2_front():.2f}"
         f" | Pret {order.get_cost_front():.2f}"
         f" | Material: {order.mat_front}")

    line(f"M Blat: {order.get_m_blat():.2f}"
         f" | Pret {order.get_cost_countertop():.2f}")

    line(f"Cost total accesorii: {order.get_cost_accessories():.2f}")

    line(f"Cost transport: {order.get_cost_transport():.2f}")

    if order.discount == 0:
        line(f"Cost manopera: {order.get_labour_cost()[0]:.2f}")
    else:
        line(f"Cost manopera: {order.get_labour_cost()[0]:.2f}"
             f" | Discount[%]: {order.discount}"
             f" | Pret manopera cu discount: {order.get_labour_cost()[1]:.2f}")

    line(f"Cost TOTAL: {math.ceil(order.get_cost_total()):.2f} RON")

    story.append(Spacer(1, 20))

    # ---------------------------------------------------------------------
    # PRICE BREAKDOWN TABLE
    # ---------------------------------------------------------------------

    story.append(Paragraph("<b>Detaliere costuri</b>", styles["Heading2"]))
    story.append(Spacer(1, 12))

    # Table header
    data = [["Tip", "Eticheta", "Cantitate", "Unitate", "Material", "Pret (RON)"]]

    # Collect items
    for cabinet in order.cabinets_list:
        for element in cabinet.elements_list:

            if element.type in ["pal", "front", "pfl"]:
                material = element.material
                qty = element.get_m2()
                unit = "m2"
            elif element.type == "blat":
                material = element.material
                qty = element.get_length()
                unit = "m"
            elif element.type == "accessory":
                material = element.label
                qty = element.pieces
                unit = "pieces"
            else:
                continue

            price = element.get_price()

            # Format price with max 2 decimals
            price_str = f"{price:.2f}"

            # Format price cell: if 0 -> bold red
            if price == 0:
                price_cell = Paragraph('<font color="red"><b>0</b></font>', normal)
            else:
                price_cell = f"{price_str}"

            data.append([
                element.type,
                element.label,
                f"{qty}",
                unit,
                material,
                price_cell
            ])

    # Build table
    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.3, colors.grey),
        ('ALIGN', (2, 1), (2, -1), 'RIGHT'),
        ('ALIGN', (5, 1), (5, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))

    story.append(table)

    # ---------------------------------------------------------------------
    # Generate PDF
    # ---------------------------------------------------------------------
    doc.build(story)

    print(f"[OK] Offer PDF generated at: {pdf_filename}")

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
                if element.type in ["pal", "front", "pfl"]:
                    material = element.material
                    size = element.get_m2()
                    unit = "m2"
                elif element.type == "blat":
                    material = element.material
                    size = element.get_length()
                    unit = "m"
                elif element.type == "accessory":
                    material = element.label
                    size = element.pieces
                    unit = "pieces"
                else:
                    continue
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


def print_order_summary(order, output_folder):
    """
    Prints a summary of the size and costs of an order, mainly for debugging purposes. Actual offer for the customer
    is generated using the generate_offer_file() method
    :param order:
    :param output_folder: not used
    :return:
    """

    total_cost = 0

    print("*** INFORMATII GENERALE ***")
    print("Nume client: ", order.client)
    print("Numar de corpuri: ", len(order.cabinets_list))
    print("Lungime totala mobila: ", order.get_order_length())
    print("M2 PAL: ", "{:.2f}".format(order.get_total_m2_pal()),
          " | Nr. coli PAL: ", order.get_sheets_pal(),
          " | Nr. piese decupate:", order.get_count_cutout_pal(),
          " | Cost decupaj piese pal: ", order.get_cost_cutout_pal(),
          " | Cost pal:", order.get_cost_pal() + order.get_cost_cutout_pal(),
          " | Material:", order.mat_pal)
    print("M3 lemn: ", "{:.2f}".format(order.get_m3_pal()))
    print("M Cant 0.4", math.ceil(order.get_m_cant('0.4')),
          " | Pret ", "{:.2f}".format(order.get_cost_edge('0.4')))
    print("M Cant 2", math.ceil(order.get_m_cant('2')),
          " | Pret ", "{:.2f}".format(order.get_cost_edge('2')))
    print("M2 PFL: ", "{:.2f}".format(order.get_total_m2_pfl()),
          " | Nr. coli PFL: ", order.get_sheets_pfl(),
          " | Pret PFL: ", order.get_cost_pfl())
    print("M2 Front: ", "{:.2f}".format(order.get_total_m2_front()),
          " | Pret ", "{:.2f}".format(order.get_cost_front()),
          " | Material: ", order.mat_front)
    print("M Blat: ", "{:.2f}".format(order.get_m_blat()),
          " | Pret", order.get_cost_countertop())
    print("Cost total accesorii: ", order.get_cost_accessories())
    print("Cost transport:", order.get_cost_transport())
    if order.discount == 0:
        print("Cost manopera:", order.get_labour_cost()[0])
    else:
        print("Cost manopera:", order.get_labour_cost()[0],
              "| Discount[%]:", order.discount,
              "| Pret manopera cu discount:", order.get_labour_cost()[1])

    print("Cost TOTAL:", math.ceil(order.get_cost_total()))