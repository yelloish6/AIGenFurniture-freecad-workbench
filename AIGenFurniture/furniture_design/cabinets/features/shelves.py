from AIGenFurniture.furniture_design.cabinets.elements.accessory import Accessory
from AIGenFurniture.furniture_design.cabinets.elements.board import BoardPal


class ShelvesMixin:

    def add_pol(self, nr, cant):
        """
        adauga polite intr-un corp
        :param nr: numarul politelor de adaugat in corp
        :param cant: tipul de cant 0,4 sau 2 (ca si numar)
        :return: none
        """
        # TODO: adancimea trebe scazuta cu grosimea cantului si inca nu merge corect
        pol_lung = self.width - (2 * self.thick_pal)
        pol_lat = (self.depth - 20)
        for i in range(nr):
            pol = BoardPal(self.label + ".pol", pol_lung, pol_lat, self.thick_pal, cant, "", "", "")
            pol.move("x", self.thick_pal)
            pol.move("z", round(self.height / (nr + 1)) * (i + 1))
            pol.move("y", 20)
            self.append(pol)
            self.append(Accessory("bolt polita", 4))
            self.append(Accessory("surub PFL", 2))

    def add_pol_2(self, orient, length, height, offset):
        """
        adds a polita in the cabinet, but you can adjust length height and offset
        :param orient: orientation ["h" or "v"]
        :param length: length of the plank, 0 for default width
        :param height: positioning height
        :param offset: displacement from the left to the right
        :return: n/a
        """

        if orient == "h":
            if length <= 1:
                placa_length = int(length * (self.width - (2 * self.thick_pal)))
            else:
                placa_length = length
            placa = BoardPal(self.label + "_sep_h" + str(length), placa_length, self.depth - self.pol_depth,
                             self.thick_pal, self.cant_pol, "", "", "")

            if height <= 1:
                placa_height = int(self.thick_pal / 2 + (
                            self.height * height))  # TODO de verificat ce face asta si daca e necesar. Pe urma de documentat cazul
            else:
                placa_height = height
            placa.move("z", placa_height)

            if offset <= 1:
                placa_offset = int(self.thick_pal + (
                            self.width * offset))  # TODO de verificat ce face asta si daca e necesar. Pe urma de documentat cazul
            else:
                placa_offset = offset
            placa.move("x", placa_offset)

            placa.move("y", self.pol_depth)
            self.append(placa)
        elif orient == "v":
            if length <= 1:
                placa_length = int(length * (self.height - (2 * self.thick_pal)))
            else:
                placa_length = length
            placa = BoardPal(self.label + "_sep_h" + str(length), placa_length, self.depth - self.pol_depth,
                             self.thick_pal, self.cant_pol, "", "", "")
            placa.rotate("y")

            if height <= 1:
                placa_height = int(self.thick_pal + (self.height * height))
            else:
                placa_height = height
            placa.move("z", placa_height)

            if offset <= 1:
                placa_offset = int(self.thick_pal + (self.width * offset) - (self.thick_pal / 2))
            else:
                placa_offset = offset
            placa.move("x", placa_offset)

            placa.move("y", self.pol_depth)
            self.append(placa)

    def add_separator(self, orient, sep_cant):

        sep_cant_thk = round(int(sep_cant))
        if orient == "h":
            sep_l = self.sep_space_w
            sep_w = self.sep_max_depth
            sep = BoardPal(self.label + ".sep" + ".h", sep_l, sep_w, self.thick_pal, sep_cant, "", "", "")
            # self.addPalObject(sep)
            # self.addPal(self.label + ".sep" + ".h", sep_l, sep_w, self.thick_pal, sep_cant, "", "", "")

            self.sep_space_h = round((self.sep_space_h - self.thick_pal) / 2)
            if self.sep_prev == "v" or "":
                self.sep_max_depth = self.sep_max_depth - sep_cant_thk
                self.sep_prev = "h"
            self.append(Accessory("surub", 4))
            sep.move("x", self.thick_pal)
            sep.move("z", round(self.sep_space_h))
        if orient == "v":
            sep_l = self.sep_space_h
            sep_w = self.sep_max_depth
            sep = BoardPal(self.label + ".sep" + ".v", sep_l, sep_w, self.thick_pal, sep_cant, "", "", "")
            self.append(sep)

            self.sep_space_w = round((self.sep_space_w - self.thick_pal) / 2)
            # self.addPal(self.label + ".sep" + ".v", sep_l, sep_w, self.thick_pal, sep_cant, "", "", "")
            if self.sep_prev == "h" or "":
                self.sep_max_depth = self.sep_max_depth - sep_cant_thk
                self.sep_prev = "v"

            sep.rotate("y")
            sep.move("x", self.thick_pal + round(self.sep_space_w))
            sep.move("z", self.thick_pal)
            self.append(Accessory("surub", 4))

    def add_wine_shelf(self, goluri, left_right, cant):
        offset_z = round((self.height - ((goluri + 1) * self.thick_pal)) / goluri)
        if left_right == "left":
            self.add_sep_v(self.height - (2 * self.thick_pal), offset_z, 0, cant)
            for x in range(goluri - 1):
                self.add_sep_h(offset_z, 0, (offset_z * (x + 1)) + (self.thick_pal * x), cant)
        if left_right == "right":
            self.add_sep_v(self.height - (2 * self.thick_pal), self.width - offset_z - (3 * self.thick_pal), 0, cant)
            for x in range(goluri - 1):
                self.add_sep_h(offset_z, self.width - offset_z - (2 * self.thick_pal),
                               (offset_z * (x + 1)) + (self.thick_pal * x), cant)
        if offset_z < 90:
            print("ERROR: nu incap sticlele de vin in " + self.label)

    def add_sep_v(self, height, offset_x, offset_z, sep_cant, cant_gap = 0):
        """

        :param height:
        :param offset_x:
        :param offset_z:
        :param sep_cant:
        :param cant_gap: how much should the board be shorter in depth to compensate for the cant applied
        :return:
        """
        sep_l = height
        sep_w = self.depth - cant_gap
        sep = BoardPal(self.label + ".sep" + ".v", sep_l, sep_w, self.thick_pal, sep_cant, "", "", "")
        self.append(sep)
        self.sep_space_w = round((self.sep_space_w - self.thick_pal) / 2)

        sep.rotate("y")
        sep.move("x", self.thick_pal + offset_x)
        sep.move("z", self.thick_pal + offset_z)
        sep.move("y", cant_gap)
        self.append(Accessory("surub", 4))


    def add_sep_h(self, width, offset_x, offset_z, sep_cant, cant_gap = 0):
        sep_l = width
        sep_w = self.depth - cant_gap
        sep = BoardPal(self.label + ".sep" + ".h", sep_l, sep_w, self.thick_pal, sep_cant, "", "", "")
        self.append(sep)
        self.sep_space_w = round((self.sep_space_w - self.thick_pal) / 2)

        sep.move("x", self.thick_pal + offset_x)
        sep.move("z", self.thick_pal + offset_z)
        sep.move("y", cant_gap)
        self.append(Accessory("surub", 4))

