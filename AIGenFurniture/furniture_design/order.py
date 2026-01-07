from .cabinets.elements.board import *

PAL_LOSS = 0.1  # used to calculate number of sheets needed
SHEET_HEIGHT = 2800
SHEET_WIDTH = 2070
IMPOZIT = 0.1
H_BOARD_HANDLING = 0.17 # 10 minutes average board handling
H_APPLIANCE = 2 # hours for installing appliance, including, sink, stove, washing machine, etc.
H_COUNTERTOP = 0.5 # 30 min per meter of countertop to install the countertop

from AIGenFurniture.furniture_design.cabinets.elements import ELEMENTS

class Order:
    def __init__(self,
                 customer_data
                 # client="Default",
                 # client_proficut="Bogdan Urs",
                 # tel_proficut="0740472185",
                 # transport="Da",
                 # address="Str. Borsa, Nr. 38, Mosnita Veche",
                 # discount=0,
                 # h_rate=120,
                 # nr_electrocasnice=0,
                 # mat_pal="Alb W962ST2",
                 # mat_pfl="Alb",
                 # mat_blat="Stejar Halifax 600",
                 # mat_front="Alb Riflat A356R3"
                 ):
        """

        :param customer_data:
        :param client:
        :param client_proficut:
        :param tel_proficut:
        :param transport:
        :param address:
        :param discount:
        :param h_rate:
        :param nr_electrocasnice:
        :param h_proiect:
        :param mat_pal:
        :param mat_pfl:
        :param mat_blat:
        :param mat_front:
        """
        # if customer_data is None:
        #     self.client = client
        #     self.client_proficut = client_proficut
        #     self.tel_proficut = tel_proficut
        #     self.transport = transport
        #     self.address = address
        #     self.discount = discount
        #     self.h_rate = h_rate
        #     self.nr_electrocasnice = nr_electrocasnice
        #     self.mat_pal = mat_pal
        #     self.mat_pfl = mat_pfl
        #     self.mat_blat = mat_blat
        #     self.mat_front = mat_front
        # else:
        self.client = customer_data.get("client")
        self.client_proficut = customer_data.get("client_proficut")
        self.tel_proficut = customer_data.get("tel_proficut")
        self.transport = customer_data.get("transport")
        self.address = customer_data.get("address")
        self.discount = customer_data.get("discount")
        self.h_rate = customer_data.get("h_rate")
        self.nr_electrocasnice = customer_data.get("nr_electrocasnice")
        self.h_proiect = customer_data.get("h_proiect")
        self.mat_pal = customer_data.get("material_pal")
        self.mat_pfl = customer_data.get("material_pfl")
        self.mat_blat = customer_data.get("material_blat")
        self.mat_front = customer_data.get("material_front")
        self.cabinets_list = []
        '''
        self.length = 0
        self.pret_manop = 0
        self.acc = []
        self.m2pal = 0
        self.mat_pal = ""
        self.m2front = 0
        self.frezare = ""
        self.m2pfl = 0
        self.mat_pfl = ""
        self.m_blat = 0
        self.mat_blat = ""
        self.m_cant = [0, 0]
        self.price_pal = 1
        self.price_pfl = 1
        self.price_front = 1
        self.price_blat = 1
        self.price_cant = [0, 0]
        self.price_list = []
        self.cost_pal = 0
        self.cost_pfl = 0
        self.cost_front = 0
        self.cost_blat = 0
        self.cost_cant = [0, 0]
        self.cost_acc = 0
        '''

    def append(self, cabinet):
        """
        Set material for all elements from the cabinet based on materials from order if material in the cabinet
        is empty, and append the cabinet to the order.
        :param cabinet:
        :return:
        """
        for element in cabinet.elements_list:
            if element.type == "pal":
                if element.material == "":
                    element.material = self.mat_pal
            elif element.type == "front":
                if element.material == "":
                    element.material = self.mat_front
            elif element.type == "pfl":
                if element.material == "":
                    element.material = self.mat_pfl
            elif element.type == "blat":
                if element.material == "":
                    element.material = self.mat_blat
            elif element.type == "accessory":
                element.material = element.label
        self.cabinets_list.append(cabinet)

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
                if element.type == "blat":
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