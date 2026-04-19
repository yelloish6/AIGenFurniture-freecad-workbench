# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
# AIGenFurniture/furniture_design/order/order.py
"""
Order class implementation.

Handles order logic and behavior, importing parameter schema from order_params.
"""

import os
import math
from ..cabinets.elements.board import *
from ..pricing.price_manager import PriceManager as pm

PAL_LOSS = 0.1  # used to calculate number of sheets needed
SHEET_HEIGHT = 2800
SHEET_WIDTH = 2070
IMPOZIT = 0.1
H_BOARD_HANDLING = 0.17 # 10 minutes average board handling
H_APPLIANCE = 2 # hours for installing appliance, including, sink, stove, washing machine, etc.
H_COUNTERTOP = 0.5 # 30 min per meter of countertop to install the countertop

from ..cabinets.elements import ELEMENTS
from .order_params import ORDER_PARAMS, get_order_attr_mapping, validate_order as validate_order_params

class Order:
    def __init__(self, customer_data):
        """
        Initialize Order from customer_data dictionary.
        
        Uses centralized ORDER_PARAMS to determine which attributes to set.
        Numeric defaults from ORDER_PARAMS (stored as strings) are converted
        to appropriate numeric types here.
        
        Handles missing (disabled) parameters gracefully by applying defaults.
        Only parameters present in OrderVar (enabled) will be in customer_data,
        but all parameters get defaults to ensure backward compatibility.
        
        :param customer_data: Dictionary of order parameters (typically from OrderVar spreadsheet)
        """
        # Get mapping from parameter names to Order class attribute names
        attr_mapping = get_order_attr_mapping()
        
        # Initialize all order parameters from customer_data using centralized definition
        # Missing (disabled) parameters get defaults and do not raise errors
        for param_name, param_def in ORDER_PARAMS.items():
            attr_name = param_def.get("order_attr", param_name)
            default_value = param_def.get("default", None)
            
            # Get value from customer_data if present (enabled params from spreadsheet),
            # otherwise use default (for disabled params or missing data)
            value = customer_data.get(param_name, default_value)
            
            # Convert string defaults to appropriate types if needed
            # Spreadsheet defaults are strings; convert numeric types here
            if value is None:
                setattr(self, attr_name, None)
            elif isinstance(default_value, str) and param_def.get("type") == "number":
                # Convert string numbers to float/int (handles both spreadsheet strings and actual strings)
                try:
                    # Try to convert to float first to handle decimals, then int if appropriate
                    float_val = float(value)
                    # Use int if the float representation is an integer
                    value = int(float_val) if float_val.is_integer() else float_val
                except (ValueError, TypeError):
                    # Keep as string if conversion fails
                    pass
                setattr(self, attr_name, value)
            else:
                setattr(self, attr_name, value)
        
        self.cabinets_list = []

    def append(self, cabinet):
        """
        Set material for all elements from the cabinet based on materials from order if material in the cabinet
        is empty, and append the cabinet to the order.
        Uses ELEMENTS dict to find material_attr by matching element class.
        :param cabinet:
        :return:
        """
        for element in cabinet.elements_list:
            # Find element definition in ELEMENTS by matching class
            material_attr = None
            for elem_def in ELEMENTS.values():
                if isinstance(element, elem_def["class"]):
                    material_attr = elem_def.get("material_attr")
                    break

            if material_attr is None:
                # Special handling for accessories - use element.label as material
                if element.type == "accessory":
                    element.material = element.label
            else:
                # For board types, assign material from order if element material is empty
                if element.material == "":
                    material_value = getattr(self, material_attr, "")
                    element.material = material_value
        self.cabinets_list.append(cabinet)

    def validate(self):
        """
        Validate that this order has all required parameters.
        
        Returns:
            tuple: (is_valid: bool, missing_params: list)
        """
        return validate_order_params(self)

    def print(self):
        print(f"[order.py] Printing order:")
        print(f"Customer, {self.client}")
        print(f"Discount, {self.discount}")
        print(f"Material Pal, {self.mat_pal}")
        print(f"Material PFL, {self.mat_pfl}")
        print(f"Material blat, {self.mat_blat}")
        print(f"Material front, {self.mat_front}")
        for corp in self.cabinets_list:
            corp.print()

    def draw(self, ox, oy, oz):
        folder_name = self.create_folder()

        name = os.path.join(folder_name, "3D " + self.client)
        if os.path.exists(name+".stl"):
            os.remove(name+".stl")
        offset = 0
        for i in range(len(self.corpuri)):
            self.corpuri[i].draw_cabinet(name, ox + offset, oy, oz)
            # the follwing line of code will draw cabinets one near the other by inserting an offset that inceases with the width of the already added cabinets
            offset = offset + self.corpuri[i].width + 1

    def get_boards_number(self):
        """
        this method returns the amount of elements that inheit the Board class in an order
        :return: nr. of elements that are subclass of Board in order
        """
        boards_counter = 0
        for cabinet in self.cabinets_list:
            for element in cabinet.elements_list:
                if isinstance(element, Board):
                    boards_counter += 1
        return boards_counter

    def get_total_m2_pal(self):
        """
        returns the surface of pal in an order
        :return:
        """
        m2pal = 0
        for cabinet in self.cabinets_list:
            m2pal = m2pal + cabinet.get_m2_pal()
        return m2pal

    def get_m3_pal(self):
        m3 = 0
        for cabinet in self.cabinets_list:
            m3 = m3 + cabinet.get_m3_pal()
        return m3

    def get_total_m2_pfl(self):
        m2pfl = 0
        for cabinet in self.cabinets_list:
            m2pfl = m2pfl + cabinet.get_m2_pfl()
        return m2pfl

    def get_total_m2_front(self):
        m2 = 0
        for cabinet in self.cabinets_list:
            m2 = m2 + cabinet.get_m2_front()
        return m2

    def get_cost_front(self):
        return float(pm.get_price_for_item("front", self.mat_front) * self.get_total_m2_front())

    def get_m_cant(self, cant_type):
        """
        :param cant_type: "0.4" sau "2"
        :return: total length of specified edge type in the complete order
        """
        m = 0
        for cabinet in self.cabinets_list:
            m = m + cabinet.get_m_cant(cant_type)
        return m

    def get_m_blat(self):
        """
        this method returns the number of blat meters as int
        :return:
        """

        m = 0
        for cabinet in self.cabinets_list:
            for element in cabinet.elements_list:
                if element.type == "countertop":
                    m = m + element.length
        return float(m / 1000)

    def get_cost_countertop(self):
        return float(pm.get_price_for_item("blat", self.mat_blat) * self.get_m_blat())

    def get_order_length(self):
        """
        sums the width of all cabinets in an order giving the total length of an order in meters
        :return:
        """
        length = 0
        for cabinet in self.cabinets_list:
            length += cabinet.width
        return length / 1000

    def get_sheets_pal(self):

        m2_pal = self.get_total_m2_pal() * (1 + PAL_LOSS)
        min_qty = float(pm.get_min_qty_for_item("pal", self.mat_pal))
        m2_min = min_qty * (SHEET_HEIGHT * SHEET_WIDTH / 1000000)
        sheets = math.ceil(m2_pal / m2_min) * min_qty
        if m2_pal < m2_min:
            return min_qty
        else:
            return sheets

    def get_sheets_pfl(self):

        m2_pfl = self.get_total_m2_pfl() * (1 + PAL_LOSS)
        min_qty = float(pm.get_min_qty_for_item("pfl", self.mat_pfl))
        m2_min = min_qty * (SHEET_HEIGHT * SHEET_WIDTH / 1000000)
        sheets = math.ceil(m2_pfl / m2_min) * min_qty
        if m2_pfl == 0:
            return 0
        elif 0 < m2_pfl < min_qty:
            return min_qty
        else:
            return sheets

    def get_cost_pfl(self):
        return float(pm.get_price_for_item("pfl", self.mat_pfl) * self.get_sheets_pfl())

    # TODO handle decupare blat as service not as accessory
    def get_cost_pal(self):
        pal_price = pm.get_price_for_item("pal", self.mat_pal) * self.get_sheets_pal()
        return pal_price

    def get_cost_edge(self, edge_type):
        '''
        param: edge_type: "2" or "0.4"
        return: cost for specified edge
        '''
        return float(pm.get_price_for_item("cant", edge_type) * self.get_m_cant(edge_type))

    def get_count_cutout_pal(self):
        cost_cutout = 0
        count_cutout = 0
        cutout_price = pm.get_price_for_item("service", "decupare pal")
        for cabinet in self.cabinets_list:
            for element in cabinet.elements_list:
                if "decupaj" in element.obs:
                    count_cutout += 1
                    cost_cutout += cutout_price
        return count_cutout

    def get_cost_cutout_pal(self):
        cost_cutout = 0
        count_cutout = 0
        cutout_price = pm.get_price_for_item("service", "decupare pal")
        for cabinet in self.cabinets_list:
            for element in cabinet.elements_list:
                if "decupaj" in element.obs:
                    count_cutout += 1
                    cost_cutout += cutout_price
        return cost_cutout

    def get_cost_accessories(self):
        cost_acc = 0
        for cabinet in self.cabinets_list:
            for element in cabinet.elements_list:
                if element.type == "accessory":
                    acc_price = float(pm.get_price_for_item(element.type, element.material))
                    cost_acc += acc_price * element.pieces
        return int(cost_acc)

    def get_labour_cost(self):
        """
        - 8h proiectare
        - 10 min/placa (pal, front,pfl) (0.17h/placa)
        - 2h montaj / electrocasnic
        - 30 min. pe metru de blat (0.5h/m)
        :param order:
        :return:
        """
        labour_cost = math.ceil(
            (self.h_proiect +
             (self.get_boards_number() * H_BOARD_HANDLING) +
             self.nr_electrocasnice * H_APPLIANCE +
             self.get_m_blat() * H_COUNTERTOP) * self.h_rate * (1 + IMPOZIT))
        labour_cost_discount = labour_cost * (100 - self.discount) / 100
        # TODO Change how the labour cost is managed in to a separate labour cost calculation module that can be adjusted based on available parameters of order
        # print("Brakdown of labour cost:")
        # print(f"Project: h: {self.h_proiect}, cost:{self.h_proiect * self.h_rate} RON")
        # print(f"Cabinet construction: h: {self.get_boards_number() * H_BOARD_HANDLING}, cost:{self.get_boards_number() * H_BOARD_HANDLING * self.h_rate} RON")
        # print(f"Appliance installation: h: {self.nr_electrocasnice * H_APPLIANCE}, cost:{self.nr_electrocasnice * H_APPLIANCE * self.h_rate} RON")
        # print(f"Countertop installation: h:{self.get_m_blat() * H_COUNTERTOP}, cost:{self.get_m_blat() * H_COUNTERTOP * self.h_rate} RON")
        return [labour_cost, labour_cost_discount]

    def get_cost_transport(self):
        if self.transport == "Da":
            return pm.get_price_for_item("service", "transport")
        else:
            print("Comanda fara transport.")
            return 0

    def get_cost_total(self):
        return (self.get_cost_pal() +
                self.get_cost_edge("0.4") +
                self.get_cost_edge("2") +
                self.get_cost_pfl() +
                self.get_cost_front() +
                self.get_cost_countertop() +
                self.get_cost_accessories() +
                self.get_labour_cost()[1]+
                self.get_cost_transport()
                )

if __name__ == "__main__":
    # TODO implement test sequence: test order and run all methods
    print("Running order.py test scenario")
    print()
