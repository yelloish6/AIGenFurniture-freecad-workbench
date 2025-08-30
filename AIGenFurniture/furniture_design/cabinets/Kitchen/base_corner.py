from AIGenFurniture.furniture_design.cabinets.cabinet import Cabinet
from AIGenFurniture.furniture_design.cabinets.elements.accessory import Accessory
from AIGenFurniture.furniture_design.cabinets.elements.board import BoardPal, Front

class BaseCorner(Cabinet):
    def __init__(self, label, height, width, depth, rules, cut_width, cut_depth, l_r, with_polita):
        """
        o---------width----------|   o------width-----------
        |                        |   |                     |
        |     l_r="left"         |   |    l_r="right"      |
        |                        |   |                     |
        depth                    |   |                     depth
        |        ----cut_width----   --- cut_width--       |
        |        |                                 |       |
        |        cut_depth                  cut_depth      |
        |        |                                 |       |
        ----------                                 ---------

        include PFL si fronturi
        :param label:
        :param height:
        :param width:
        :param depth:
        :param rules:
        :param cut_width:
        :param cut_depth:
        :param l_r: "left" or "right"
        :param with_polita: true or false
        :return:
        """

        # depth = depth - rules["gap_spate"]
        # width = width - rules["gap_spate"]
        # cut_depth = cut_depth + rules["gap_fata"]
        # cut_width = cut_width + rules["gap_fata"]

        super().__init__(label, height, width, depth, rules)

        if l_r == "left":
            jos = BoardPal(self.label + ".jos", self.width, self.depth, self.thick_pal, "", "", "", "")
            jos.add_obs("decupaj colt stanga. Cote in sensul acelor de ceasornic, de la coltul din stanga spate: " +
                        str(self.width) + ":" + # cota1
                        str(self.depth - cut_depth) + ":" + # cota2
                        str(cut_width) + "(cant " + str(self.cant_lab) + "):" + # cota3
                        str(cut_depth) + "(cant " + str(self.cant_lab) + "):" + # cota4
                        str(self.width - cut_width) + ":" + # cota5
                        str(self.depth)) # cota6
            jos.cut_coords = [
                [0, 0],
                [self.width - cut_width, 0],
                [self.width - cut_width, cut_depth],
                [self.width, cut_depth],
                [self.width, self.depth],
                [0, self.depth]
            ]
            self.append(jos)
            # self.append(Accessory("decupare pal", 1))

            lat1 = BoardPal(self.label + ".lat1", self.height - self.thick_pal, self.depth - cut_depth, self.thick_pal,
                            self.cant_lab, "", "", "")
            lat1.rotate("x")
            lat1.rotate_cw("y")
            lat1.rotate_cw("z")
            lat1.move("z", self.thick_pal)
            lat1.move("x", jos.length)
            lat1.move("y", cut_depth)
            self.append(lat1)

            lat2 = BoardPal(self.label + ".lat2", self.height - self.thick_pal, self.width - cut_width, self.thick_pal,
                            self.cant_lab, "", "", "")
            lat2.rotate("x")
            lat2.rotate_cw("y")
            # lat2.rotate("z")
            lat2.move("x", lat2.width)
            lat2.move("z", self.thick_pal)
            lat2.move("y", self.thick_pal)
            self.append(lat2)

            spate = BoardPal(self.label + ".spate", self.depth - self.thick_pal, self.height - self.thick_pal,
                             self.thick_pal, "", "", "", "")
            # spate.rotate("x")
            # spate.move("z", self.thick_pal)
            # spate.move("y", depth)
            # spate.move("x", self.thick_pal)
            spate.rotate("x")
            spate.rotate_cw("z")
            spate.move("z", self.thick_pal)
            spate.move("y", self.thick_pal + spate.length)
            spate.move("x", self.thick_pal)
            self.append(spate)

            leg1 = BoardPal(self.label + ".leg", self.width - (2 * self.thick_pal), 100, self.thick_pal, self.cant_lab,
                            "", "", "")
            leg1.rotate("x")
            leg1.rotate("x")
            leg1.rotate("x")
            leg1.move("z", self.height)
            leg1.move("x", self.thick_pal)
            leg1.move("y", cut_depth)
            self.append(leg1)

            leg2 = BoardPal(self.label + ".leg", self.width - (2 * self.thick_pal), 100, self.thick_pal, self.cant_lab,
                            "", "", "")
            leg2.rotate("x")
            leg2.move("z", self.height - leg2.width)
            leg2.move("y", self.depth)
            leg2.move("x", self.thick_pal)
            self.append(leg2)

            leg3 = BoardPal(self.label + ".leg", cut_depth - self.thick_pal, 100, self.thick_pal, self.cant_lab, "",
                            "",
                            "")
            leg3.rotate("x")
            leg3.rotate("z")
            # leg3.rotate("z")
            # leg3.rotate("z")
            leg3.move("z", self.height - leg3.width)
            leg3.move("x", self.width - cut_width - self.thick_pal)
            leg3.move("y", self.thick_pal)
            # leg3.move("y", jos.length)
            self.append(leg3)

            if with_polita:
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
                pol.cut_coords = [
                    [0, 0],
                    [self.width - cut_width - self.thick_pal - 20, 0],
                    [self.width - cut_width - self.thick_pal - 20, cut_depth - self.thick_pal + 20],
                    [self.width - (2 * self.thick_pal), cut_depth - self.thick_pal + 20],
                    [self.width - (2 * self.thick_pal), self.depth - self.thick_pal],
                    [0, self.depth - self.thick_pal]
                ]
                pol.move("x", self.thick_pal)
                pol.move("y", self.thick_pal)
                pol.move("z", int((self.height - self.thick_pal) / 2))
                # pol.move("y", -cut_depth)
                self.append(pol)
                # self.append(Accessory("decupare pal", 1))

            front1 = Front(self.label + "_1", self.height - 2 * rules["gap_front"],
                           cut_depth - 3 - rules["thick_front"], rules["thick_front"])
            front1.rotate_cw("y")
            front1.move("x", width - cut_width + rules["thick_front"])
            front1.move("z", rules["gap_front"])
            front1.move("y", rules["gap_front"])
            self.append(front1)

            front2 = Front(self.label + "_2", self.height - 2 * rules["gap_front"],
                           cut_width - 3 - rules["thick_front"], rules["thick_front"])
            front2.rotate_cw("y")
            front2.rotate_cw("z")
            front2.move("x", width - cut_width + rules["thick_front"])
            front2.move("y", cut_depth - rules["thick_front"])
            front2.move("z", rules["gap_front"])
            self.append(front2)

            # blat2 = Blat(self.label + ".blat2", cut_depth - rules["gap_fata"], rules["width_blat"], rules["thick_blat"])
            # blat2.move("z", self.height + 10)
            # blat2.move("y", cut_depth - rules["gap_fata"])
            # blat2.move("x", - rules["gap_spate"])
            # blat2.rotate("z")
            # self.append(blat2)

        elif l_r == "right":
            jos = BoardPal(self.label + ".jos", self.width, self.depth, self.thick_pal, "", "", "", "")
            jos.add_obs(
                str("decupaj colt dreapta. Cote in sensul acelor de ceasornic, de la coltul din stanga spate: " +
                    str(self.width) + ":" + # cota1
                    str(self.depth) + ":" + # cota2
                    str(self.width - cut_width) + ":" + # cota3
                    str(cut_depth) + "(cant " + str(self.cant_lab) + "):" + # cota4
                    str(cut_width) + "(cant " + str(self.cant_lab) + "):" + # cota5
                    str(self.depth - cut_depth))) # cota6
            jos.cut_coords = [
                [0, cut_depth],
                [cut_width, cut_depth],
                [cut_width, 0],
                [self.width, 0],
                [self.width, self.depth],
                [0, self.depth]
            ]
            self.append(jos)
            # self.append(Accessory("decupare pal", 1))

            lat1 = BoardPal(self.label + ".lat1", self.height - self.thick_pal, self.depth - cut_depth, self.thick_pal,
                            self.cant_lab, "", "", "")
            lat1.rotate("x")
            lat1.rotate_cw("y")
            lat1.rotate_cw("z")
            lat1.move("z", self.thick_pal)
            lat1.move("x", self.thick_pal)
            lat1.move("y", cut_depth)
            self.append(lat1)

            lat2 = BoardPal(self.label + ".lat2", self.height - self.thick_pal, self.width - cut_width, self.thick_pal,
                            self.cant_lab, "", "", "")
            lat2.rotate("x")
            lat2.rotate_cw("y")
            lat2.move("z", self.thick_pal)
            lat2.move("x", self.width)
            lat2.move("y", self.thick_pal)
            self.append(lat2)

            spate = BoardPal(self.label + ".spate", self.depth - self.thick_pal, self.height - self.thick_pal,
                             self.thick_pal, "", "", "", "")
            spate.rotate("x")
            spate.rotate_cw("z")
            spate.move("z", self.thick_pal)
            spate.move("y", self.depth)
            # spate.move("y", -cut_depth)
            spate.move("x", self.width)
            self.append(spate)

            leg1 = BoardPal(self.label + ".leg", self.width - (2 * self.thick_pal), 100, self.thick_pal, self.cant_lab,
                            "", "", "")
            leg1.move("z", self.height - self.thick_pal)
            leg1.move("x", self.thick_pal)
            leg1.move("y", self.depth - leg1.width)
            # leg1.move("y", -cut_depth)
            self.append(leg1)

            leg2 = BoardPal(self.label + ".leg", self.width - (2 * self.thick_pal), 100, self.thick_pal, self.cant_lab,
                            "",
                            "", "")
            leg2.rotate("x")
            leg2.move("z", self.height - leg2.width)
            leg2.move("y", cut_depth)
            leg2.move("x", self.thick_pal)
            leg2.move("y", self.thick_pal)
            self.append(leg2)

            leg3 = BoardPal(self.label + ".leg", cut_depth - self.thick_pal, 100, self.thick_pal, self.cant_lab, "",
                            "", "")
            leg3.rotate("x")
            leg3.rotate_cw("z")
            leg3.move("z", self.height - leg3.width)
            leg3.move("x", cut_width)
            leg3.move("x", self.thick_pal)
            leg3.move("y", cut_depth)
            self.append(leg3)

            if with_polita:
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
                pol.cut_coords = [
                    [0, cut_depth - self.thick_pal + 20],
                    [cut_width - self.thick_pal + 20, cut_depth - self.thick_pal + 20],
                    [cut_width - self.thick_pal + 20, 0],
                    [self.width - (2 * self.thick_pal), 0],
                    [self.width - (2 * self.thick_pal), self.depth - self.thick_pal],
                    [0, self.depth - self.thick_pal]
                ]
                pol.move("x", self.thick_pal)
                pol.move("y", self.thick_pal)
                pol.move("z", int((self.height - self.thick_pal) / 2))
                # pol.move("y", -cut_depth)
                self.append(pol)
                # self.append(Accessory("decupare pal", 1))

            front1 = Front(self.label + "_1", self.height - 2 * rules["gap_front"], cut_depth - 3 -
                           rules["thick_front"], rules["thick_front"])
            front1.rotate_cw("y")
            front1.move("x", cut_width)
            front1.move("z", rules["gap_front"])
            front1.move("y", rules["gap_front"])
            self.append(front1)

            front2 = Front(self.label + "_2", self.height - 2 * rules["gap_front"], cut_width - 3 -
                           rules["thick_front"], rules["thick_front"])
            front2.rotate_cw("y")
            front2.rotate_cw("z")
            front2.move("x", rules["gap_front"])
            front2.move("y", cut_depth - rules["thick_front"])
            front2.move("z", rules["gap_front"])
            self.append(front2)

            # blat2 = Blat(self.label + ".blat2", cut_depth, rules["width_blat"], rules["thick_blat"])
            # blat2.move("z", self.height)
            # blat2.move("x", cut_width)
            # blat2.move("y", cut_depth)
            # blat2.rotate("z")
            # self.append(blat2)

        else:
            print("ERROR: Undefined orientation (only 'left' or 'right' possible!")

        self.add_pfl()
        #        self.get_item_by_type_label("pfl", self.label + ".pfl").move("y", - cut_depth)
        # self.getPFLOO()[0].getPlacaOO()

        self.append(Accessory("balama usa franta", 2))
        self.append(Accessory("balama 170 deg", 2))
        self.append(Accessory("surub 3.5x16", 4 * 4))  # pentru balamale
        self.append(Accessory("picioare", 6))
        self.append(Accessory("clema plinta", 3))
        self.append(Accessory("surub 3.5x16", 3 * 4))  # pentru picioare
        self.append(Accessory("surub blat", 4))
        self.append(Accessory("L", 2))
        self.append(Accessory("surub", 19))
        self.append(Accessory("plinta", (cut_width + cut_depth) / 1000))
        self.append(Accessory("sipca apa", (self.width + self.depth) / 1000))

        # blat1 = Blat(self.label + ".blat1", self.width + rules["gap_spate"], rules["width_blat"], rules["thick_blat"])
        # blat1.move("z", self.height)
        # blat1.move("y", cut_depth - rules["gap_fata"])
        # blat1.move("x", - rules["gap_spate"])
        # blat1.move("z", 10)
        # self.append(blat1)