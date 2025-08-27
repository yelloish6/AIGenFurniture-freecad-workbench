from AIGenFurniture.furniture_design.cabinets.cabinet import Cabinet
from AIGenFurniture.furniture_design.cabinets.elements.accessory import Accessory
from AIGenFurniture.furniture_design.cabinets.elements.board import BoardPal, Front


class TopCorner(Cabinet):

    # TODO implemntare dubla pentru decupare placa

    def __init__(self, label, height, width, depth, rules, cut_width, cut_depth, l_r, polite):
        """
        o---------width----------||   o------width------------||
       ||                        ||   ||                      ||
       ||     l_r="left"         ||   ||   l_r="right"        ||
       ||                        ||   ||                      ||
       depth                     ||   ||                      depth
       ||        ----cut_width---||   ||-- cut_width--        ||
       ||        |                                   |        ||
       ||        cut_depth                    cut_depth       ||
       ||        |                                   |        ||
       ||=========                                   =========||
        include PFL si fronturi
        :param label:
        :param height:
        :param width:
        :param depth:
        :param rules:
        :param cut_width:
        :param cut_depth:
        :param l_r:
        :param polite:
        """
        super().__init__(label, height, width, depth, rules)
        if l_r == "left":
            # placa de jos
            jos = BoardPal(self.label + ".jos", self.width - (2 * self.thick_pal), self.depth - self.thick_pal,
                           self.thick_pal,
                           "", "", "", "")
            jos.add_obs("decupaj colt stanga. Cote in sensul acelor de ceasornic, de la coltul din stanga spate: " +
                        str(self.width - 2 * self.thick_pal) + ":" +
                        str(self.depth - cut_depth) + ":" +
                        str(cut_width - self.thick_pal) + "(cant " + str(self.cant_lab) + "):" +
                        str(cut_depth - self.thick_pal) + "(cant " + str(self.cant_lab) + "):" +
                        str(self.width - cut_width) + ":" +
                        str(self.depth - self.thick_pal))
            jos.move("y", self.thick_pal)
            jos.move("x", self.thick_pal)
            # jos.move("y", -cut_depth)
            self.append(jos)

            # placa de sus
            sus = BoardPal(self.label + ".sus", self.width - (2 * self.thick_pal), self.depth - self.thick_pal,
                           self.thick_pal,
                           "", "", "", "")
            sus.add_obs("decupaj colt stanga. Cote in sensul acelor de ceasornic, de la coltul din stanga spate: " +
                        str(self.width - 2 * self.thick_pal) + ":" +
                        str(self.depth - cut_depth) + ":" +
                        str(cut_width - self.thick_pal) + "(cant " + str(self.cant_lab) + "):" +
                        str(cut_depth - self.thick_pal) + "(cant " + str(self.cant_lab) + "):" +
                        str(self.width - cut_width) + ":" +
                        str(self.depth - self.thick_pal))
            sus.move("y", self.thick_pal)
            sus.move("x", self.thick_pal)
            sus.move("z", self.height - self.thick_pal)
            # sus.move("y", -cut_depth)
            self.append(sus)

            for polita in range(polite):
                pol = BoardPal(self.label + ".pol", self.width - (2 * self.thick_pal),
                               self.depth - (1 * self.thick_pal),
                               self.thick_pal, "", "", "", "")
                pol.add_obs("decupaj colt stanga. Cote in sensul acelor de ceasornic, de la coltul din stanga spate: " +
                            str(self.width - (2 * self.thick_pal)) + ":" +
                            str(self.depth - cut_depth - 20) + ":" +
                            str(cut_width - self.thick_pal + 20) + "(cant " + str(self.cant_lab) + "):" +
                            str(cut_depth - self.thick_pal + 20) + "(cant " + str(self.cant_lab) + "):" +
                            str(self.width - cut_width - self.thick_pal - 20) + ":" +
                            str(self.depth - self.thick_pal))
                pol.move("x", self.thick_pal)
                pol.move("y", self.thick_pal)
                pol.move("z", polita * int((self.height - self.thick_pal) / polite))
                # pol.move("y", -cut_depth)
                self.append(pol)

            spate = BoardPal(self.label + ".spate", self.height, self.depth - self.thick_pal,
                             self.thick_pal, "", "", "", "")
            spate.rotate("y")
            spate.move("y", self.thick_pal)
            spate.move("x", self.thick_pal)
            # spate.move("y", -cut_depth)
            self.append(spate)

            lat1 = BoardPal(self.label + ".lat1", self.height, self.width - cut_width, self.thick_pal, self.cant_lab,
                            "",
                            self.cant_lab, self.cant_lab)
            lat1.rotate("y")
            lat1.rotate("z")
            # lat1.move("y", -cut_depth)
            self.append(lat1)

            lat2 = BoardPal(self.label + ".lat2", self.height, self.depth - cut_depth, self.thick_pal, self.cant_lab,
                            "",
                            self.cant_lab, self.cant_lab)
            lat2.rotate("y")
            lat2.move("x", self.width)
            lat2.move("y", self.depth - lat2.width)
            # lat2.move("y", -cut_depth)
            self.append(lat2)

            front1 = Front(self.label + "_1", self.height - 2 * rules["gap_front"],
                           cut_depth - 3 - rules["thick_front"], rules["thick_front"])
            front1.rotate("y")
            front1.move("x", width - cut_width + rules["thick_front"])
            front1.move("z", rules["gap_front"])
            front1.move("y", rules["gap_front"])
            self.append(front1)

            front2 = Front(self.label + "_2", self.height - 2 * rules["gap_front"],
                           cut_width - 3 - rules["thick_front"], rules["thick_front"])
            front2.rotate("y")
            front2.rotate("z")
            front2.move("x", width - cut_width + rules["thick_front"])
            front2.move("y", cut_depth - rules["thick_front"])
            front2.move("z", rules["gap_front"])
            self.append(front2)

            # self.front = self.front + [["front", self.label + "_1", self.height - 4, cut_depth - 3 - front_thick]]
            # self.front = self.front + [["front", self.label + "_2", self.height - 4, cut_width - 3 - front_thick]]

        elif l_r == "right":
            # placa de jos
            jos = BoardPal(self.label + ".jos", self.width - (2 * self.thick_pal), self.depth - self.thick_pal,
                           self.thick_pal,
                           "", "", "", "")
            jos.add_obs("decupaj colt dreapta. Cote in sensul acelor de ceasornic, de la coltul din stanga spate: " +
                        str(self.width - (2 * self.thick_pal)) + ":" +
                        str(self.depth - self.thick_pal) + ":" +
                        str(self.width - cut_width - self.thick_pal) + ":" +
                        str(cut_depth - self.thick_pal) + "(cant " + str(self.cant_lab) + "):" +
                        str(cut_width - self.thick_pal) + "(cant " + str(self.cant_lab) + "):" +
                        str(self.depth - cut_depth) + ":")
            jos.move("y", self.thick_pal)
            # jos.move("y", -cut_depth)
            jos.move("x", self.thick_pal)
            self.append(jos)

            # placa de sus
            sus = BoardPal(self.label + ".sus", self.width - (2 * self.thick_pal), self.depth - self.thick_pal,
                           self.thick_pal,
                           "", "", "", "")
            sus.add_obs("decupaj colt dreapta. Cote in sensul acelor de ceasornic, de la coltul din stanga spate: " +
                        str(self.width - (2 * self.thick_pal)) + ":" +
                        str(self.depth - self.thick_pal) + ":" +
                        str(self.width - cut_width - self.thick_pal) + ":" +
                        str(cut_depth - self.thick_pal) + "(cant " + str(self.cant_lab) + "):" +
                        str(cut_width - self.thick_pal) + "(cant " + str(self.cant_lab) + "):" +
                        str(self.depth - cut_depth) + ":")

            sus.move("y", self.thick_pal)
            sus.move("z", self.height - self.thick_pal)
            # sus.move("y", -cut_depth)
            sus.move("x", self.thick_pal)
            self.append(sus)

            for i in range(polite):
                pol = BoardPal(self.label + ".pol", self.width - (2 * self.thick_pal),
                               self.depth - (1 * self.thick_pal),
                               self.thick_pal, "", "", "", "")
                pol.add_obs(
                    "decupaj colt dreapta. Cote in sensul acelor de ceasornic, de la coltul din stanga spate: " +
                    str(self.width - (2 * self.thick_pal)) + ":" +
                    str(self.depth - self.thick_pal) + ":" +
                    str(self.width - cut_width - self.thick_pal - 20) + ":" +
                    str(cut_depth - self.thick_pal + 20) + "(cant " + str(self.cant_lab) + "):" +
                    str(cut_width - self.thick_pal + 20) + "(cant " + str(self.cant_lab) + "):" +
                    str(self.depth - cut_depth - 20) + ":")
                pol.move("x", self.thick_pal)
                pol.move("y", self.thick_pal)
                pol.move("z", i * int((self.height - self.thick_pal) / polite))
                # pol.move("y", -cut_depth)
                self.append(pol)

            spate = BoardPal(self.label + ".spate", self.height, self.depth - self.thick_pal,
                             self.thick_pal, "", "", "", "")
            spate.rotate("y")
            spate.move("y", self.thick_pal)
            spate.move("x", self.width)
            # spate.move("z", self.thick_pal)
            # spate.move("y", -cut_depth)
            self.append(spate)

            lat1 = BoardPal(self.label + ".lat1", self.height, self.width - cut_width, self.thick_pal, self.cant_lab,
                            "",
                            self.cant_lab, self.cant_lab)
            lat1.rotate("y")
            lat1.rotate("z")
            # lat1.move("y", -cut_depth)
            lat1.move("x", cut_width)
            self.append(lat1)

            lat2 = BoardPal(self.label + ".lat2", self.height, self.depth - cut_depth, self.thick_pal, self.cant_lab,
                            "",
                            self.cant_lab, self.cant_lab)
            lat2.rotate("y")
            lat2.move("x", self.thick_pal)
            lat2.move("y", self.depth - lat2.width)
            # lat2.move("y", -cut_depth)
            self.append(lat2)

            front1 = Front(self.label + "_1", self.height - 2 * rules["gap_front"],
                           cut_depth - 3 - rules["thick_front"], rules["thick_front"])
            front1.rotate("y")
            front1.move("x", cut_width)
            front1.move("z", rules["gap_front"])
            front1.move("y", rules["gap_front"])
            self.append(front1)

            front2 = Front(self.label + "_2", self.height - 2 * rules["gap_front"],
                           cut_width - 3 - rules["thick_front"], rules["thick_front"])
            front2.rotate("y")
            front2.rotate("z")
            front2.move("x", rules["gap_front"])
            front2.move("y", cut_depth - rules["thick_front"])
            front2.move("z", rules["gap_front"])
            self.append(front2)

            # self.front = self.front + [["front", self.label + "_1", self.height - 4, cut_depth - 3 - front_thick]]
            # self.front = self.front + [["front", self.label + "_2", self.height - 4, cut_width - 3 - front_thick]]

        else:
            print("ERROR: Undefined orientation (only 'left' or 'right' possible!")

        self.add_pfl()

        self.append(Accessory("balama usa franta", 2))
        self.append(Accessory("balama 170 deg", 2))
        self.append(Accessory("surub 3.5x16", 4 * 4))  # pentru balamale
        self.append(Accessory("surub", 20))
        self.append(Accessory("pereche clema prindere perete", 1))
        self.append(Accessory("sina perete", self.width / 1000))
        self.append(Accessory("surub diblu perete", round(self.width / 201)))
