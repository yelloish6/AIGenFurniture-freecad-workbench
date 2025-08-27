from AIGenFurniture.furniture_design.cabinets.elements.accessory import Accessory
from AIGenFurniture.furniture_design.cabinets.elements.board import BoardPal, Pfl


class DrawersMixin:

    def add_tandem_box(self, tip, height_offset):
        """
        method to add a BLUM TandemBox drawer in a Cabinet
        :param tip:
        :return:
        """
        fund_label = self.label + ".ser.jos"
        spate_label = self.label + ".ser.sp"
        fund_lung = int(self.width - (2 * self.thick_pal) - (37.5 * 2))
        spate_lung = self.width - 2 * 18 - 87
        fund_lat = self.depth - 20
        spate_lat = 0
        if tip == "M":
            spate_lat = 68
        elif tip == "D":
            spate_lat = 183
        fund = BoardPal(fund_label, fund_lung, fund_lat, 16, "", "", "", "")
        fund.add_obs("PAL 16")
        fund.move("x", self.thick_pal + 37.5)
        fund.move("z", 3 + height_offset)
        self.append(fund)

        spate = BoardPal(spate_label, spate_lung, spate_lat, 16, self.cant_lab, "", "", "")
        spate.add_obs("PAL 16")
        spate.rotate("x")
        spate.move("x", self.thick_pal + 43.5)
        spate.move("y", fund.width + spate.thick)
        spate.move("z", height_offset + fund.thick)
        self.append(spate)
        self.append(Accessory("tandembox " + tip, 1))
        self.append(Accessory("surub 3.5x16", 18))

    def add_drawer_a_pfl(self, sert_h, height_offset):
        """
        adds an "A" box drawer with PFL bottom
        :param sert_h: height of the drawer (cuttlery drawer 100, regular drawers 200)
        :param height_offset: positioning of the drawer in the cabinet
        :return:
        """
        gap_glisiera = 13
        sert_height = sert_h
        sert_width = self.width - (2 * self.thick_pal) - (2 * gap_glisiera)
        sert_depth = self.depth - gap_glisiera

        self.create_drawer_box_a(sert_height, sert_width, sert_depth, self.thick_pal + gap_glisiera, 0, height_offset)

        pfl = Pfl(self.label + ".ser", sert_width - 4, sert_depth - 4)
        pfl.move("x", self.thick_pal + gap_glisiera + 2)
        pfl.move("y", 2)
        pfl.move("z", height_offset - pfl.thick)
        self.append(pfl)

        self.append(Accessory("pereche glisiera " + str(self.get_standard_slide_length(sert_depth)) + " mm", 1))
        self.append(Accessory("surub 3.5x16", 12))
        self.append(Accessory("surub", 8))
        self.append(Accessory("surub PFL", 2 * round(sert_width / 100) + 2 * round(sert_depth / 100)))
        
    def add_drawer_a_pal(self, sert_h, height_offset):
        """
        adds an "A" box drawer with PAL bottom
        :param sert_h: height of the drawer (cuttlery drawer 100, regular drawers 200)
        :param height_offset: positioning of the drawer in the cabinet
        :return:
        """

        gap_glisiera = 13
        sert_height = sert_h
        sert_width = self.width - (2 * self.thick_pal) - (2 * gap_glisiera)
        sert_depth = self.depth - gap_glisiera

        self.create_drawer_box_a(sert_height, sert_width, sert_depth, self.thick_pal + gap_glisiera, 0, height_offset)

        fund = BoardPal(self.label + ".ser.f", sert_width - (2 * self.thick_pal), sert_depth - (2 * self.thick_pal),
                        self.thick_pal, "", "", "", "")
        fund.move("x", (2 * self.thick_pal) + gap_glisiera)
        fund.move("y", self.thick_pal)
        fund.move("z", height_offset)
        self.append(fund)

        self.append(Accessory("pereche glisiera " + str(self.get_standard_slide_length(sert_depth)) + " mm", 1))
        self.append(Accessory("surub 3.5x16", 12))
        self.append(Accessory("surub", 8))
        self.append(Accessory("surub PFL", 2 * round(sert_width / 100) + 2 * round(sert_depth / 100)))

    def add_drawer_b_pal(self, sert_h, height_offset):
        """
        adds an "B" box drawer with PAL bottom
        :param sert_h: height of the drawer (cuttlery drawer 100, regular drawers 200)
        :param height_offset: positioning of the drawer in the cabinet
        :return:
        """
        # sertar de tacamuri de 100, sertare adanci de 200

        gap_glisiera = 13
        sert_height = sert_h
        sert_width = self.width - (2 * self.thick_pal) - (2 * gap_glisiera)
        sert_depth = self.depth - gap_glisiera

        self.create_drawer_box_b(sert_height, sert_width, sert_depth, self.thick_pal + gap_glisiera, 0, height_offset)

        fund = BoardPal(self.label + ".ser.f", sert_width - (2 * self.thick_pal), sert_depth - (2 * self.thick_pal),
                        self.thick_pal, "", "", "", "")
        fund.move("x", (2 * self.thick_pal) + gap_glisiera)
        fund.move("y", self.thick_pal)
        fund.move("z", height_offset)
        self.append(fund)

        self.append(Accessory("pereche glisiera " + str(self.get_standard_slide_length(sert_depth)) + " mm", 1))
        self.append(Accessory("surub 3.5x16", 12))
        self.append(Accessory("surub", 8))
        self.append(Accessory("surub PFL", 2 * round(sert_width / 100) + 2 * round(sert_depth / 100)))

    def add_drawer_pal_glass(self, sert_h, height_offset):
        """
        Adds a "B" box drawer
        _____________
        |           |
        |           |
        _____________

        with glass on the front board
        |---|             |---|
        |   |             |   |
        |   |_____________|   |
        |_____________________|

        :param sert_h:
        :param height_offset:
        :return:
        """

        margine = 50
        overlap_sticla = 20
        gap_glisiera = 13
        sert_height = sert_h
        sert_width = self.width - (2 * self.thick_pal) - (2 * gap_glisiera)
        sert_depth = self.depth - gap_glisiera

        self.create_drawer_box_b(sert_height, sert_width, sert_depth, self.thick_pal + gap_glisiera, 0, height_offset)

        fund = BoardPal(self.label + ".ser.f", sert_width - (2 * self.thick_pal), sert_depth - (2 * self.thick_pal),
                        self.thick_pal, "", "", "", "")
        fund.move("x", (2 * self.thick_pal) + gap_glisiera)
        fund.move("y", self.thick_pal)
        fund.move("z", height_offset)
        self.append(fund)

        # sert_height = sert_h
        # sert_width = self.width - (2 * self.thick_pal) - (2 * gap_glisiera)
        # sert_depth = self.depth - gap_glisiera
        #
        # self.create_drawer_box_b(sert_height, sert_width, sert_depth, self.thick_pal + gap_glisiera, 0, height_offset)
        #
        # fund = BoardPal(self.label + ".ser.f", sert_width - (2 * self.thick_pal), sert_depth - (2 * self.thick_pal),
        #                 self.thick_pal, "", "", "", "")
        # fund.move("x", (2 * self.thick_pal) + gap_glisiera)
        # fund.move("y", self.thick_pal)
        # fund.move("z", height_offset)
        # self.append(fund)

        fata = BoardPal(self.label + ".ser.fata", sert_width, sert_h, self.thick_pal,
                        self.cant_lab, self.cant_lab, self.cant_lab, self.cant_lab)
        fata.add_obs("decupaj U. Cote in sensul acelor de ceasornic, de la coltul din stanga spate: " +
                      str(margine) + ":" +
                      str(fata.width - margine) + ":" +
                      str(fata.length - 2 * margine) + ":" +
                      str(fata.width - margine) + ":" +
                      str(margine) + ":" +
                      str(fata.width) + ":" +
                      str(fata.length) + ":" +
                      str(fata.width)
                      )
        fata.rotate("x")
        fata.move("x", self.thick_pal + gap_glisiera)
        fata.move("z", height_offset)
        fata.move("y", self.thick_pal)

        #lat1.move("y", -1000) #pentru debug, sa iasa sertarul din corp
        self.append(fata)
        sticla = Accessory("sticla",1)
        sticla.add_obs("sticla: " +  str(fata.length - 2 * margine + 2 * overlap_sticla) + " x " +
                              str(fata.width - margine + overlap_sticla))

        self.append(sticla)


        self.append(Accessory("pereche glisiera " + str(self.get_standard_slide_length(sert_depth)) + " mm", 1))
        self.append(Accessory("surub 3.5x16", 12))
        self.append(Accessory("surub", 8))
        self.append(Accessory("surub PFL", 2 * round(sert_width / 100) + 2 * round(sert_depth / 100)))

    # TODO drawer box methods should create a Cabinet object for the box itself, not alter the main cabinet.
    def create_drawer_box_a(self, sert_height, sert_width, sert_depth, offset_x, offset_y, offset_z):
        """
        Sertar incadrat intre laturi
        |___________|
        |           |
        |           |
        |___________|
        :param sert_height: drawer height
        :param sert_width: drawer width
        :param sert_depth: drawer depth
        :param offset_x:
        :param offset_y:
        :param offset_z:
        """

        left = BoardPal(self.label + ".ser.left", sert_depth, sert_height, self.thick_pal, self.cant_lab, "", self.cant_lab, self.cant_lab)
        left.rotate("y")
        left.rotate("x")
        left.rotate("z")
        left.rotate("z")
        left.move("x", offset_x)
        left.move("z", offset_z)
        self.append(left)

        front = BoardPal(self.label + ".ser.front", sert_width - (2 * self.thick_pal), sert_height, self.thick_pal,
                        self.cant_lab, "", "", "")
        front.rotate("x")
        front.move("x", offset_x + self.thick_pal)
        front.move("z", offset_z)
        front.move("y", self.thick_pal)
        self.append(front)

        back = BoardPal(self.label + ".ser.back", sert_width - (2 * self.thick_pal), sert_height, self.thick_pal,
                        self.cant_lab, "", "", "")
        back.rotate("x")
        back.move("x", offset_x+ self.thick_pal)
        back.move("y", left.length)
        back.move("z", offset_z)
        self.append(back)

        right = BoardPal(self.label + ".ser.right", sert_depth, sert_height, self.thick_pal, self.cant_lab, "", self.cant_lab, self.cant_lab)
        right.rotate("x")
        right.rotate("z")
        right.rotate("z")
        right.rotate("z")
        right.move("x", offset_x + back.length + right.thick)
        right.move("z", offset_z)
        self.append(right)

    def create_drawer_box_b(self, sert_height, sert_width, sert_depth, offset_x, offset_y, offset_z):
        """
        Drawer with full front and back boards
        _____________
        |           |
        |           |
        _____________
        :param sert_height: drawer height
        :param sert_width: drawer width
        :param sert_depth: drawer depth
        :param offset_x:
        :param offset_y:
        :param offset_z:
        :return:
        """
        front = BoardPal(self.label + ".ser.front", sert_width, sert_height, self.thick_pal,
                        self.cant_lab, self.cant_lab, self.cant_lab, self.cant_lab)
        front.rotate("x")
        front.move("x", offset_x)
        front.move("z", offset_z)
        front.move("y", front.thick)
        self.append(front)

        left = BoardPal(self.label + ".ser.long", sert_depth - (2 * self.thick_pal), sert_height, self.thick_pal, self.cant_lab, self.cant_lab, "", "")
        left.rotate("y")
        left.rotate("x")
        left.rotate("z")
        left.rotate("z")
        left.move("x", offset_x)
        left.move("z", offset_z)
        left.move("y", front.thick)
        self.append(left)

        right = BoardPal(self.label + ".ser.right", sert_depth - (2 * self.thick_pal), sert_height, self.thick_pal, self.cant_lab, self.cant_lab, "", "")
        right.rotate("x")
        right.rotate("z")
        right.rotate("z")
        right.rotate("z")
        right.move("x", offset_x + front.length - right.thick)
        right.move("z", offset_z)
        right.move("y", front.thick)
        self.append(right)

        back = BoardPal(self.label + ".ser.back", sert_width, sert_height, self.thick_pal,
                        self.cant_lab, self.cant_lab, self.cant_lab, self.cant_lab)
        back.rotate("x")
        back.move("x", offset_x)
        back.move("y", left.length + back.thick + front.thick)
        back.move("z", offset_z)
        self.append(back)

    def get_standard_slide_length(self, drawer_depth):
        """
        returns the standard drawer slider length based on given drawer depth
        :param drawer_depth:
        :return:
        """
        standard_slide_length = [300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 900, 1000, 1100]
        if drawer_depth < standard_slide_length[0] or drawer_depth > standard_slide_length[len(standard_slide_length)-1] + 100:
            print(f"ERROR: {self.label} drawer slide length our of limits!")
        for i in range(len(standard_slide_length)-1):
            if standard_slide_length[i] < drawer_depth < standard_slide_length[i + 1]:
                # print(f"DEBUG: Std length for {drawer_depth} is {standard_slide_length[i]}")
                return standard_slide_length[i]

