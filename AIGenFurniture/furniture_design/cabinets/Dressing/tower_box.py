import math

from AIGenFurniture.furniture_design.cabinets import accesoriu, PlacaPal


class TowerBox(corp):
    def __init__(self, label, height, width, depth, rules, gap_list, gap_heat, front_list):
        """

        :param label:
        :param height:
        :param width:
        :param depth:
        :param rules:
        :param gap_list: intaltimea gap-urilor de jos in sus. Ultimul gap e cat ramane (ex:[gen_h_base - 2 * t1.pal_width,300, gen_h_tower - gen_h_base - 318 - gen_h_top])
        :param gap_heat: distanta in spate cat sunt mai in interior politele fata de lateriale ca sa permita evacuarea cladurii
        :param front_list: care gap-uri au front (ex. [0, 0, 0, 1])
        """
        super().__init__(label, height, width, depth, rules)
        self.depth = self.depth - gap_heat
        jos = PlacaPal(self.label + ".jos", self.width, self.depth, self.thick_pal, self.cant_lab, "", self.cant_lab,
                       self.cant_lab)
        self.append(jos)

        lat1 = PlacaPal(self.label + ".lat", self.height - self.thick_pal, self.depth + gap_heat, self.thick_pal,
                        self.cant_lab, "", self.cant_lab, "")
        lat1.rotate("y")
        lat1.move("z", jos.thick)
        lat1.move("x", self.thick_pal)
        self.append(lat1)

        lat2 = PlacaPal(self.label + ".lat", self.height - self.thick_pal, self.depth + gap_heat, self.thick_pal,
                        self.cant_lab, "", self.cant_lab, "")
        lat2.rotate("y")
        lat2.move("z", jos.thick)
        lat2.move("x", jos.length)
        self.append(lat2)

        sus = PlacaPal(self.label + ".sus", self.width - (2 * self.thick_pal), self.depth - (self.cant),
                       self.thick_pal, self.cant_lab, "", "", "")
        sus.move("x", lat1.thick)
        sus.move("z", lat1.length)
        self.append(sus)

        #adding horizontal separators
        offset = 0
        for gap in range(len(gap_list)):
            offset += gap_list[gap] # + self.thick_pal
            self.add_sep_h(self.width - 2 * self.thick_pal, 0, offset, self.cant_lab)
        # self.addSepH(self.width - 2 * self.thick_pal, 0, gap_list[0], self.cant_lab)
        # self.addSepH(self.width - 2 * self.thick_pal, 0, gap_list[0] + gap_list[1] + self.thick_pal, self.cant_lab)
        # self.addSepH(self.width - 2 * self.thick_pal, 0, gap_list[0] + gap_list[1] + gap_list[2] + (2 * self.thick_pal),
        #              self.cant_lab)

        self.append(accesoriu("surub", 8))
        self.append(accesoriu("plinta", self.width / 1000))
        picioare = math.ceil(self.width / 400) * 2
        self.append(accesoriu("picioare", picioare))
        self.append(accesoriu("clema plinta", picioare / 2))
        self.append(accesoriu("surub 3.5x16", picioare * 4))  # pentru picioare

        self.add_pfl()

        # if front_list[0] == 1:
        #     if front_list[1] == 0:
        #         self.add_front_manual(gap_list[0] + (2 * self.thick_pal) - 4, self.width - 4, 0, 0)
        #         if front_list[2] == 0:
        #
        #         elif front_list[2] == 1:
        #     elif front_list[1] == 1:
        #         self.add_front_manual(gap_list[0] + (1.5 * self.thick_pal) - 3, self.width - 4, 0, 0)

        # Se seteaza fronturile pentru turn
        # gap_list[0]
        if (front_list[0] == 1) and (front_list[1] == 0):
            # front jos fara ala de sus
            self.add_front_manual(gap_list[0] + (2 * self.thick_pal) - 4, self.width - 4, 0, 0)
        if (front_list[0] == 1) and (front_list[1] == 1):
            # front jos si ala de sus
            self.add_front_manual(gap_list[0] + (1.5 * self.thick_pal) - 3, self.width - 4, 0, 0)
        # gap_list[1]
        if (front_list[1] == 1) and (front_list[0] == 0) and (front_list[2] == 0):
            self.add_front_manual(gap_list[1] + (2 * self.thick_pal) - 4, self.width - 4, 0, gap_list[0])
        if (((front_list[1] == 1) and (front_list[0] == 1) and (front_list[2] == 0))
                or ((front_list[1] == 1) and (front_list[0] == 0) and (front_list[2] == 1))):
            self.add_front_manual(gap_list[1] + (1.5 * self.thick_pal) - 3, self.width - 4, 0, gap_list[0] + (self.thick_pal / 2))
        if (front_list[1] == 1) and (front_list[0] == 1) and (front_list[2] == 1):
            self.add_front_manual(gap_list[1] + self.thick_pal - 4, self.width - 4, 0, gap_list[0] + (self.thick_pal / 2))

        # gap_list[2]
        if (front_list[2] == 1) and (front_list[1] == 0) and (front_list[3] == 0):
            self.add_front_manual(gap_list[2] + (2 * self.thick_pal) - 4, self.width - 4, 0, gap_list[0] + gap_list[1] + 2)
        if (((front_list[2] == 1) and (front_list[1] == 1) and (front_list[3] == 0))
                or ((front_list[2] == 1) and (front_list[1] == 0) and (front_list[3] == 1))):
            self.add_front_manual(gap_list[2] + (1.5 * self.thick_pal) - 3, self.width - 4, 0, gap_list[0] + gap_list[1] + 2)
        if (front_list[2] == 1) and (front_list[1] == 1) and (front_list[3] == 1):
            self.add_front_manual(gap_list[2] + self.thick_pal - 4, self.width - 4, 0, gap_list[0] + gap_list[1] + 2)

        # gap4
        if (front_list[3] == 1) and (front_list[2] == 0):
            self.add_front_manual(self.height - gap_list[0] - gap_list[1] - gap_list[2] - (3 * self.thick_pal) - 4,
                                  self.width - 4, 0, gap_list[0] + gap_list[1] + gap_list[2] + 4)
        if (front_list[3] == 1) and (front_list[2] == 1):
            self.add_front_manual(self.height - gap_list[0] - gap_list[1] - gap_list[2] - (3.5 * self.thick_pal) - 3,
                                  self.width - 4, 0, gap_list[0] + gap_list[1] + gap_list[2] + 4)