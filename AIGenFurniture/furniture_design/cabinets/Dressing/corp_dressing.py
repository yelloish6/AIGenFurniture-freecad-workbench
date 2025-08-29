from AIGenFurniture.furniture_design.cabinets.elements.accessory import *
from AIGenFurniture.furniture_design.cabinets.elements.board import *
from AIGenFurniture.furniture_design.cabinets.cabinet import Cabinet

import math

class CorpDressing(Cabinet):
    def __init__(self, label, height, width, depth, rules, gap_list, front_list):
        """

        :param label:
        :param height:
        :param width:
        :param depth:
        :param rules:
        :param gap_list: intaltimea gap-urilor de jos in sus. Ultimul gap e cat ramane (ex:[gen_h_base - 2 * t1.pal_width,300, gen_h_tower - gen_h_base - 318 - gen_h_top])
        :param front_list: care gap-uri au front (ex. [0, 0, 0, 1])
        """
        super().__init__(label, height, width, depth, rules)

        jos = BoardPal(self.label + ".jos", self.width - (2 * self.thick_pal), self.depth, self.thick_pal, self.cant_lab, "",
                       self.cant_lab, self.cant_lab)
        jos.move("x", self.thick_pal)
        jos.move("z", rules["height_legs"])
        self.append(jos)

        lat1 = BoardPal(self.label + ".lat", self.height, self.depth, self.thick_pal,
                        self.cant_lab, "", self.cant_lab, "")
        lat1.rotate("y")
        lat1.move("x", self.thick_pal)
        self.append(lat1)

        lat2 = BoardPal(self.label + ".lat", self.height, self.depth, self.thick_pal,
                        self.cant_lab, "", self.cant_lab, "")
        lat2.rotate("y")
        lat2.move("x", self.width)
        self.append(lat2)

        sus = BoardPal(self.label + ".sus", self.width - (2 * self.thick_pal), self.depth - self.cant,
                       self.thick_pal, self.cant_lab, "", "", "")
        sus.move("x", lat1.thick)
        sus.move("z", lat1.length - self.thick_pal)
        self.append(sus)

        plinta = BoardPal(self.label + ".plinta", self.width - (2 * self.thick_pal), rules["height_legs"],
                          self.thick_pal, self.cant_lab, "", "", "")
        plinta.rotate("x")
        plinta.move("x", self.thick_pal)
        plinta.move("y", self.thick_pal)
        self.append(plinta)

        # adding horizontal separators
        offset = 0
        for gap in range(len(gap_list)):
            offset += gap_list[gap] + self.thick_pal
            self.add_sep_h(self.width - 2 * self.thick_pal, 0, offset, self.cant_lab)
        # self.addSepH(self.width - 2 * self.thick_pal, 0, gap_list[0], self.cant_lab)
        # self.addSepH(self.width - 2 * self.thick_pal, 0, gap_list[0] + gap_list[1] + self.thick_pal, self.cant_lab)
        # self.addSepH(self.width - 2 * self.thick_pal, 0, gap_list[0] + gap_list[1] + gap_list[2] + (2 * self.thick_pal),
        #              self.cant_lab)

        self.append(Accessory("surub", 8))
        self.append(Accessory("plinta", self.width / 1000))
        picioare = math.ceil(self.width / 400) * 2
        self.append(Accessory("picioare", picioare))
        self.append(Accessory("clema plinta", picioare / 2))
        self.append(Accessory("surub 3.5x16", picioare * 4))  # pentru picioare

        self.add_pfl()

        # Se seteaza fronturile pentru turn
        # gap_list[0]
        if (front_list[0] == 1) and (front_list[1] == 0):
            self.add_front_manual(gap_list[0] + (2 * self.thick_pal) - 4, self.width - 4)
        if (front_list[0] == 1) and (front_list[1] == 1):
            self.add_front_manual(gap_list[0] + (1.5 * self.thick_pal) - 3, self.width - 4)
        # gap_list[1]
        if (front_list[1] == 1) and (front_list[0] == 0) and (front_list[2] == 0):
            self.add_front_manual(gap_list[1] + (2 * self.thick_pal) - 4, self.width - 4)
        if (((front_list[1] == 1) and (front_list[0] == 1) and (front_list[2] == 0))
                or ((front_list[1] == 1) and (front_list[0] == 0) and (front_list[2] == 1))):
            self.add_front_manual(gap_list[1] + (1.5 * self.thick_pal) - 3, self.width - 4)
        if (front_list[1] == 1) and (front_list[0] == 1) and (front_list[2] == 1):
            self.add_front_manual(gap_list[1] + self.thick_pal - 4, self.width - 4)

        # gap_list[2]
        if (front_list[2] == 1) and (front_list[1] == 0) and (front_list[3] == 0):
            self.add_front_manual(gap_list[2] + (2 * self.thick_pal) - 4, self.width - 4)
        if (((front_list[2] == 1) and (front_list[1] == 1) and (front_list[3] == 0))
                or ((front_list[2] == 1) and (front_list[1] == 0) and (front_list[3] == 1))):
            self.add_front_manual(gap_list[2] + (1.5 * self.thick_pal) - 3, self.width - 4)
        if (front_list[2] == 1) and (front_list[1] == 1) and (front_list[3] == 1):
            self.add_front_manual(gap_list[2] + self.thick_pal - 4, self.width - 4)

        # gap4
        if (front_list[3] == 1) and (front_list[2] == 0):
            self.add_front_manual(self.height - gap_list[0] - gap_list[1] - gap_list[2] - (3 * self.thick_pal) - 4,
                                  self.width - 4)
        if (front_list[3] == 1) and (front_list[2] == 1):
            self.add_front_manual(
                self.height - gap_list[0] - gap_list[1] - gap_list[2] - (3.5 * self.thick_pal) - 3,
                self.width - 4)