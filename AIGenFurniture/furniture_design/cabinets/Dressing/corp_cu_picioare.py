from AIGenFurniture.furniture_design.cabinets.elements.accessory import *
from AIGenFurniture.furniture_design.cabinets.elements.board import *
from AIGenFurniture.furniture_design.cabinets.cabinet import Cabinet

class CorpCuPicioare(Cabinet):
    def __init__(self, label, height, width, depth, plinta, rules):
        drill_depth_offset = 120 # distance from the other edge of the cabinet to where the screw is assembled
        """
        Cabinet simplu:
        |-------|
        |       |
        |       |
        |_______|
        |       |
        :param label:
        :param height:
        :param width:
        :param depth:
        :param rules:
        :param plinta: cat de inalta sa fie plinta
        """
        super().__init__(label, height, width, depth, rules)
        lat1 = BoardPal(self.label + ".lat1", self.height, self.depth, self.thick_pal, self.cant_lab, "", self.cant_lab,
            self.cant_lab)
        lat1.rotate("y")
        lat1.move("x", self.thick_pal)

        lat2 = BoardPal(self.label + ".lat2", self.height, self.depth, self.thick_pal, self.cant_lab, "", self.cant_lab,
                        self.cant_lab)
        lat2.rotate("y")
        lat2.move("x", self.width)

        jos = BoardPal(self.label + ".jos", self.width - 2 * self.thick_pal, self.depth, self.thick_pal, self.cant_lab,
                       "", "", "")
        jos.move("x", self.thick_pal)
        jos.move("z", plinta)
        # assembly jos
        jos.drill("up", drill_depth_offset, jos.thick/2)
        jos.drill("up", depth - drill_depth_offset, jos.thick / 2)
        jos.drill("down", drill_depth_offset, jos.thick / 2)
        jos.drill("down", depth - drill_depth_offset, jos.thick / 2)
        lat1.drill("front", drill_depth_offset, plinta + jos.thick / 2)
        lat2.drill("front", drill_depth_offset, plinta + jos.thick / 2)
        lat1.drill("front", depth - drill_depth_offset, plinta + jos.thick / 2)
        lat2.drill("front", depth - drill_depth_offset, plinta + jos.thick / 2)

        sus = BoardPal(self.label + ".sus", self.width - 2 * self.thick_pal, self.depth, self.thick_pal, self.cant_lab,
                       "", "", "")
        sus.move("x", self.thick_pal)
        sus.move("z", self.height - self.thick_pal)

        sus.drill("up", drill_depth_offset, jos.thick/2)
        sus.drill("up", depth - drill_depth_offset, jos.thick / 2)
        sus.drill("down", drill_depth_offset, jos.thick / 2)
        sus.drill("down", depth - drill_depth_offset, jos.thick / 2)
        lat1.drill("front", drill_depth_offset, height - jos.thick / 2)
        lat2.drill("front", drill_depth_offset, height - jos.thick / 2)
        lat1.drill("front", depth - drill_depth_offset, height - jos.thick / 2)
        lat2.drill("front", depth - drill_depth_offset, height - jos.thick / 2)

        self.append(Accessory("surub", 8))
        self.append(lat1)
        self.append(lat2)
        self.append(jos)
        self.append(sus)

    def add_pol_2(self, orient, length, height, offset):
        """
        adds a polita in the cabinet, but you can adjust length height and offset
        :param orient: orientation ["h" or "v"]
        :param length: length of the plank, 0 for default width
        :param height: positioning height
        :param offset: displacement from the left to the right
        :return: n/a
        """
    # TODO rewrite add_pol method
        #  to integrate the different versions of implementation of sep and pol by using optional arguments with default values
        #  every new cabinet type can have a separate method depending on how it's using it and have one general definition under the Cabinet class
        #  it must include also the drills
        drill_depth_offset = 120 # distance from the other edge of the cabinet to where the screw is assembled

        if orient == "h":
            if length <= 1:
                placa_length = int(length * (self.width - (2 * self.thick_pal)))
            else:
                placa_length = length
            placa = BoardPal(self.label + "_sep_h" + str(int(height)), placa_length, self.depth - self.pol_depth,
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
            placa.drill("up", drill_depth_offset, 9)
            placa.drill("up", placa.width - drill_depth_offset, 9)
            placa.drill("down", drill_depth_offset, 9)
            placa.drill("down", placa.width - drill_depth_offset, 9)
            lat1 = self.get_item_by_type_label("pal", self.label + ".lat1")
            lat1.drill("front", self.depth - placa.width + drill_depth_offset, placa_height + self.thick_pal/2)
            lat1.drill("front", self.depth - drill_depth_offset, int(placa_height + self.thick_pal / 2))
            lat2 = self.get_item_by_type_label("pal", self.label + ".lat2")
            lat2.drill("front", self.depth - placa.width + drill_depth_offset, int(placa_height + self.thick_pal/2))
            lat2.drill("front", self.depth - drill_depth_offset, int(placa_height + self.thick_pal / 2))

            self.append(placa)
        elif orient == "v":
            if length <= 1:
                placa_length = int(length * (self.height - (2 * self.thick_pal)))
            else:
                placa_length = length
            placa = BoardPal(self.label + "_sep_h" + str(int(height)), placa_length, self.depth - self.pol_depth,
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

    def add_sep_h(self, width, offset_x, offset_z, sep_cant):
        drill_depth_offset = 120
        sep_l = width
        sep_w = self.depth
        placa = BoardPal(self.label + ".sep" + ".h", sep_l, sep_w, self.thick_pal, sep_cant, "", "", "")
        # placa.move("y", self.pol_depth)
        placa.drill("up", drill_depth_offset, 9)
        placa.drill("up", placa.width - drill_depth_offset, 9)
        placa.drill("down", drill_depth_offset, 9)
        placa.drill("down", placa.width - drill_depth_offset, 9)
        lat1 = self.get_item_by_type_label("pal", self.label + ".lat1")
        lat1.drill("front", self.depth - placa.width + drill_depth_offset, offset_z + self.thick_pal / 2)
        lat1.drill("front", self.depth - drill_depth_offset, int(offset_z + self.thick_pal / 2))
        lat2 = self.get_item_by_type_label("pal", self.label + ".lat2")
        lat2.drill("front", self.depth - placa.width + drill_depth_offset, int(offset_z + self.thick_pal / 2))
        lat2.drill("front", self.depth - drill_depth_offset, int(offset_z + self.thick_pal / 2))
        self.append(placa)
        self.sep_space_w = round((self.sep_space_w - self.thick_pal) / 2)

        placa.move("x", self.thick_pal + offset_x)
        placa.move("z", self.thick_pal + offset_z)
        self.append(Accessory("surub", 4))

    def add_drawer_b_pal(self, sert_h, height_offset):
        super(Cabinet, self).add_drawer_b_pal(sert_h, height_offset)
        lat1 = self.get_item_by_type_label("pal", self.label + ".lat1")
        lat1.drill("front", self.depth - 200, height_offset + sert_h/2)
        lat1.drill("front", 200, height_offset + sert_h / 2)
        lat2 = self.get_item_by_type_label("pal", self.label + ".lat2")
        lat2.drill("front", self.depth - 200, height_offset + sert_h / 2)
        lat2.drill("front", 200, height_offset + sert_h / 2)


# class CorpCuPicioare(Cabinet):
#     def __init__(self, label, height, width, depth, rules, plinta = 100):
#         """
#         corp simplu:
#         |-------|
#         |       |
#         |       |
#         |_______|
#         |       |
#         :param label:
#         :param height:
#         :param width:
#         :param depth:
#         :param rules:
#         :param plinta: cat de inalta sa fie plinta
#         """
#         super().__init__(label, height, width, depth, rules)
#         lat1 = BoardPal(self.label + ".lat1", self.height, self.depth, self.thick_pal, self.cant_lab, "",
#                         self.cant_lab, self.cant_lab)
#         lat1.rotate("y")
#         lat1.move("x", self.thick_pal)
#         self.append(lat1)
#
#         lat2 = BoardPal(self.label + ".lat2", self.height, self.depth, self.thick_pal, self.cant_lab, "", self.cant_lab,
#                         self.cant_lab)
#         lat2.rotate("y")
#         lat2.move("x", self.width)
#         self.append(lat2)
#
#         jos = BoardPal(self.label + ".jos", self.width - 2 * self.thick_pal, self.depth, self.thick_pal, self.cant_lab,
#                        "", "", "")
#         jos.move("x", self.thick_pal)
#         jos.move("z", plinta)
#         self.append(jos)
#
#         sus = BoardPal(self.label + ".sus", self.width - 2 * self.thick_pal, self.depth, self.thick_pal, self.cant_lab,
#                        "", "", "")
#         sus.move("x", self.thick_pal)
#         sus.move("z", self.height - self.thick_pal)
#         self.append(sus)
#
#         self.append(Accessory("surub", 8))
