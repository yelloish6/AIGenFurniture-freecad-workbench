# from AIGenFurniture.furniture_design.cabinets.elements.accessory import Accessory
# from AIGenFurniture.furniture_design.cabinets.elements.board import BoardPal, Blat, Front
# from AIGenFurniture.furniture_design.cabinets.cabinet import Cabinet
# import math
#
#
#
# class BaseBox(Cabinet):
#     def __init__(self, label, height, width, depth, rules):
#         super().__init__(label, height, width, depth, rules)
#         picioare = math.ceil(self.width / 400) * 2
#         self.append(Accessory("picioare", picioare))
#         self.append(Accessory("clema plinta", picioare / 2))
#         self.append(Accessory("surub 3.5x16", picioare * 4))  # pentru picioare
#         self.append(Accessory("surub blat", 4))
#         self.append(Accessory("surub", 14))
#         self.append(Accessory("plinta", self.width / 1000))
#         self.append(Accessory("sipca apa", self.width / 1000))
#
#         # arhitectura
#         # jos
#         jos = BoardPal(self.label + ".jos", self.width, self.depth, self.thick_pal, self.cant_lab, "", self.cant_lab,
#                        self.cant_lab)
#         self.append(jos)
#
#         # lat rotit pe Y si ridicat pe z cu grosimea lui jos
#         lat1 = BoardPal(self.label + ".lat", self.height - self.thick_pal, self.depth, self.thick_pal, self.cant_lab,
#                         "", "", "")
#         lat1.rotate("y")
#         lat1.move("x", lat1.thick)
#         lat1.move("z", jos.thick)
#         self.append(lat1)
#
#         # lat rotit pe y, translatat pe x cu (jos - grosime), translatat pe z cu grosime jos
#         lat2 = BoardPal(self.label + ".lat", self.height - self.thick_pal, self.depth, self.thick_pal, self.cant_lab,
#                         "", "", "")
#         lat2.rotate("y")
#         lat2.move("x", lat2.thick)
#         lat2.move("x", jos.length - lat2.thick)
#         lat2.move("z", jos.thick)
#         self.append(lat2)
#
#         # leg translatat pe z cu (lungimea lat + offset lat - grosime leg), si pe x cu grosime lat
#         leg1 = BoardPal(self.label + ".leg1", self.width - (2 * self.thick_pal), 100, self.thick_pal,
#                         self.cant_lab, self.cant_lab, "", "")
#         leg1.move("z", lat1.length + jos.thick - leg1.thick)
#         leg1.move("x", lat1.thick)
#         self.append(leg1)
#
#         # leg translatat pe z cu (lungimea lat + offset lat - grosime leg)
#         #               pe y cu (latime lat - latime leg)
#         #               pe x cu grosime lat
#         leg2 = BoardPal(self.label + ".leg2", self.width - (2 * self.thick_pal), 100, self.thick_pal,
#                         self.cant_lab, self.cant_lab, "", "")
#         leg2.move("z", lat1.length + jos.thick - leg1.thick)
#         leg2.move("y", lat1.width - leg2.width)
#         leg2.move("x", lat1.thick)
#         self.append(leg2)
#
#         blatul = Blat(self.label + ".blat", self.width, self.width_blat, self.thick_blat)
#         blatul.move("z", self.height)
#         blatul.move("y", -rules["gap_fata"])
#         # self.append(blatul)
#
#         self.add_pfl()
#
#     # def drawCabinet(self, filename, ox, oy, oz):
#     #     for i in range(len(self.material_list)):
#     #         if isinstance(self.material_list[i], Placa):
#     #             if "lat1" in self.material_list[i].__getattribute__("label"):
#     #                 lat1 = self.material_list[i]
#     #                 lat1.rotate("y")
#     #                 lat1.move("x", lat1.thick)
#     #                 lat1.move("z", jos.thick)
#     #             export_stl(filename,
#     #                       self.material_list[i].label + str(i),
#     #                       self.material_list[i].position[0],
#     #                       self.material_list[i].position[1],
#     #                       self.material_list[i].position[2],
#     #                       self.material_list[i].position[3] + ox,
#     #                       self.material_list[i].position[4] + oy,
#     #                       self.material_list[i].position[5] + oz)
#
#
# class BaseCorner(Cabinet):
#     def __init__(self, label, height, width, depth, rules, cut_width, cut_depth, l_r, with_polita):
#         """
#         o---------width----------|   o------width-----------
#         |                        |   |                     |
#         |     l_r="left"         |   |    l_r="right"      |
#         |                        |   |                     |
#         depth                    |   |                     depth
#         |        ----cut_width----   --- cut_width--       |
#         |        |                                 |       |
#         |        cut_depth                  cut_depth      |
#         |        |                                 |       |
#         ----------                                 ---------
#
#         include PFL si fronturi
#         :param label:
#         :param height:
#         :param width:
#         :param depth:
#         :param rules:
#         :param cut_width:
#         :param cut_depth:
#         :param l_r: "left" or "right"
#         :param with_polita: true or false
#         :return:
#         """
#
#         # depth = depth - rules["gap_spate"]
#         # width = width - rules["gap_spate"]
#         # cut_depth = cut_depth + rules["gap_fata"]
#         # cut_width = cut_width + rules["gap_fata"]
#
#         super().__init__(label, height, width, depth, rules)
#
#         if l_r == "left":
#             jos = BoardPal(self.label + ".jos", self.width, self.depth, self.thick_pal, "", "", "", "")
#             jos.add_obs("decupaj colt stanga. Cote in sensul acelor de ceasornic, de la coltul din stanga spate: " +
#                         str(self.width) + ":" + # cota1
#                         str(self.depth - cut_depth) + ":" + # cota2
#                         str(cut_width) + "(cant " + str(self.cant_lab) + "):" + # cota3
#                         str(cut_depth) + "(cant " + str(self.cant_lab) + "):" + # cota4
#                         str(self.width - cut_width) + ":" + # cota5
#                         str(self.depth)) # cota6
#             jos.cut_coords = [
#                 [0, 0],
#                 [self.width - cut_width, 0],
#                 [self.width - cut_width, cut_depth],
#                 [self.width, cut_depth],
#                 [self.width, self.depth],
#                 [0, self.depth]
#             ]
#             self.append(jos)
#             # self.append(Accessory("decupare pal", 1))
#
#             lat1 = BoardPal(self.label + ".lat1", self.height - self.thick_pal, self.depth - cut_depth, self.thick_pal,
#                             self.cant_lab, "", "", "")
#             lat1.rotate("x")
#             lat1.rotate("y")
#             lat1.rotate("z")
#             lat1.move("z", self.thick_pal)
#             lat1.move("x", jos.length)
#             lat1.move("y", cut_depth)
#             self.append(lat1)
#
#             lat2 = BoardPal(self.label + ".lat2", self.height - self.thick_pal, self.width - cut_width, self.thick_pal,
#                             self.cant_lab, "", "", "")
#             lat2.rotate("x")
#             lat2.rotate("y")
#             # lat2.rotate("z")
#             lat2.move("x", lat2.width)
#             lat2.move("z", self.thick_pal)
#             lat2.move("y", self.thick_pal)
#             self.append(lat2)
#
#             spate = BoardPal(self.label + ".spate", self.depth - self.thick_pal, self.height - self.thick_pal,
#                              self.thick_pal, "", "", "", "")
#             # spate.rotate("x")
#             # spate.move("z", self.thick_pal)
#             # spate.move("y", depth)
#             # spate.move("x", self.thick_pal)
#             spate.rotate("x")
#             spate.rotate("z")
#             spate.move("z", self.thick_pal)
#             spate.move("y", self.thick_pal + spate.length)
#             spate.move("x", self.thick_pal)
#             self.append(spate)
#
#             leg1 = BoardPal(self.label + ".leg", self.width - (2 * self.thick_pal), 100, self.thick_pal, self.cant_lab,
#                             "", "", "")
#             leg1.rotate("x")
#             leg1.rotate("x")
#             leg1.rotate("x")
#             leg1.move("z", self.height)
#             leg1.move("x", self.thick_pal)
#             leg1.move("y", cut_depth)
#             self.append(leg1)
#
#             leg2 = BoardPal(self.label + ".leg", self.width - (2 * self.thick_pal), 100, self.thick_pal, self.cant_lab,
#                             "", "", "")
#             leg2.rotate("x")
#             leg2.move("z", self.height - leg2.width)
#             leg2.move("y", self.depth)
#             leg2.move("x", self.thick_pal)
#             self.append(leg2)
#
#             leg3 = BoardPal(self.label + ".leg", cut_depth - self.thick_pal, 100, self.thick_pal, self.cant_lab, "",
#                             "",
#                             "")
#             leg3.rotate("x")
#             leg3.rotate("z")
#             leg3.rotate("z")
#             leg3.rotate("z")
#             leg3.move("z", self.height - leg3.width)
#             leg3.move("x", self.width - cut_width - self.thick_pal)
#             leg3.move("y", self.thick_pal)
#             # leg3.move("y", jos.length)
#             self.append(leg3)
#
#             if with_polita:
#                 pol = BoardPal(self.label + ".pol", self.width - (2 * self.thick_pal),
#                                self.depth - (1 * self.thick_pal),
#                                self.thick_pal, "", "", "", "")
#
#                 pol.add_obs("decupaj colt stanga. Cote in sensul acelor de ceasornic, de la coltul din stanga spate: " +
#                             str(self.width - (2 * self.thick_pal)) + ":" +
#                             str(self.depth - cut_depth - 20) + ":" +
#                             str(cut_width - self.thick_pal + 20) + "(cant " + str(self.cant_lab) + "):" +
#                             str(cut_depth - self.thick_pal + 20) + "(cant " + str(self.cant_lab) + "):" +
#                             str(self.width - cut_width - self.thick_pal - 20) + ":" +
#                             str(self.depth - self.thick_pal))
#                 pol.cut_coords = [
#                     [0, 0],
#                     [self.width - cut_width - self.thick_pal - 20, 0],
#                     [self.width - cut_width - self.thick_pal - 20, cut_depth - self.thick_pal + 20],
#                     [self.width - (2 * self.thick_pal), cut_depth - self.thick_pal + 20],
#                     [self.width - (2 * self.thick_pal), self.depth - self.thick_pal],
#                     [0, self.depth - self.thick_pal]
#                 ]
#                 pol.move("x", self.thick_pal)
#                 pol.move("y", self.thick_pal)
#                 pol.move("z", int((self.height - self.thick_pal) / 2))
#                 # pol.move("y", -cut_depth)
#                 self.append(pol)
#                 # self.append(Accessory("decupare pal", 1))
#
#             front1 = Front(self.label + "_1", self.height - 2 * rules["gap_front"],
#                            cut_depth - 3 - rules["thick_front"], rules["thick_front"])
#             front1.rotate("y")
#             front1.move("x", width - cut_width + rules["thick_front"])
#             front1.move("z", rules["gap_front"])
#             front1.move("y", rules["gap_front"])
#             self.append(front1)
#
#             front2 = Front(self.label + "_2", self.height - 2 * rules["gap_front"],
#                            cut_width - 3 - rules["thick_front"], rules["thick_front"])
#             front2.rotate("y")
#             front2.rotate("z")
#             front2.move("x", width - cut_width + rules["thick_front"])
#             front2.move("y", cut_depth - rules["thick_front"])
#             front2.move("z", rules["gap_front"])
#             self.append(front2)
#
#             # blat2 = Blat(self.label + ".blat2", cut_depth - rules["gap_fata"], rules["width_blat"], rules["thick_blat"])
#             # blat2.move("z", self.height + 10)
#             # blat2.move("y", cut_depth - rules["gap_fata"])
#             # blat2.move("x", - rules["gap_spate"])
#             # blat2.rotate("z")
#             # self.append(blat2)
#
#         elif l_r == "right":
#             jos = BoardPal(self.label + ".jos", self.width, self.depth, self.thick_pal, "", "", "", "")
#             jos.add_obs(
#                 str("decupaj colt dreapta. Cote in sensul acelor de ceasornic, de la coltul din stanga spate: " +
#                     str(self.width) + ":" + # cota1
#                     str(self.depth) + ":" + # cota2
#                     str(self.width - cut_width) + ":" + # cota3
#                     str(cut_depth) + "(cant " + str(self.cant_lab) + "):" + # cota4
#                     str(cut_width) + "(cant " + str(self.cant_lab) + "):" + # cota5
#                     str(self.depth - cut_depth))) # cota6
#             jos.cut_coords = [
#                 [0, cut_depth],
#                 [cut_width, cut_depth],
#                 [cut_width, 0],
#                 [self.width, 0],
#                 [self.width, self.depth],
#                 [0, self.depth]
#             ]
#             self.append(jos)
#             # self.append(Accessory("decupare pal", 1))
#
#             lat1 = BoardPal(self.label + ".lat1", self.height - self.thick_pal, self.depth - cut_depth, self.thick_pal,
#                             self.cant_lab, "", "", "")
#             lat1.rotate("x")
#             lat1.rotate("y")
#             lat1.rotate("z")
#             lat1.move("z", self.thick_pal)
#             lat1.move("x", self.thick_pal)
#             lat1.move("y", cut_depth)
#             self.append(lat1)
#
#             lat2 = BoardPal(self.label + ".lat2", self.height - self.thick_pal, self.width - cut_width, self.thick_pal,
#                             self.cant_lab, "", "", "")
#             lat2.rotate("x")
#             lat2.rotate("y")
#             lat2.move("z", self.thick_pal)
#             lat2.move("x", self.width)
#             lat2.move("y", self.thick_pal)
#             self.append(lat2)
#
#             spate = BoardPal(self.label + ".spate", self.depth - self.thick_pal, self.height - self.thick_pal,
#                              self.thick_pal, "", "", "", "")
#             spate.rotate("x")
#             spate.rotate("z")
#             spate.move("z", self.thick_pal)
#             spate.move("y", self.depth)
#             # spate.move("y", -cut_depth)
#             spate.move("x", self.width)
#             self.append(spate)
#
#             leg1 = BoardPal(self.label + ".leg", self.width - (2 * self.thick_pal), 100, self.thick_pal, self.cant_lab,
#                             "", "", "")
#             leg1.move("z", self.height - self.thick_pal)
#             leg1.move("x", self.thick_pal)
#             leg1.move("y", self.depth - leg1.width)
#             # leg1.move("y", -cut_depth)
#             self.append(leg1)
#
#             leg2 = BoardPal(self.label + ".leg", self.width - (2 * self.thick_pal), 100, self.thick_pal, self.cant_lab,
#                             "",
#                             "", "")
#             leg2.rotate("x")
#             leg2.move("z", self.height - leg2.width)
#             leg2.move("y", cut_depth)
#             leg2.move("x", self.thick_pal)
#             leg2.move("y", self.thick_pal)
#             self.append(leg2)
#
#             leg3 = BoardPal(self.label + ".leg", cut_depth - self.thick_pal, 100, self.thick_pal, self.cant_lab, "",
#                             "", "")
#             leg3.rotate("x")
#             leg3.rotate("z")
#             leg3.move("z", self.height - leg3.width)
#             leg3.move("x", cut_width)
#             leg3.move("x", self.thick_pal)
#             leg3.move("y", cut_depth)
#             self.append(leg3)
#
#             if with_polita:
#                 pol = BoardPal(self.label + ".pol", self.width - (2 * self.thick_pal),
#                                self.depth - (1 * self.thick_pal),
#                                self.thick_pal, "", "", "", "")
#
#                 pol.add_obs(
#                     "decupaj colt dreapta. Cote in sensul acelor de ceasornic, de la coltul din stanga spate: " +
#                     str(self.width - (2 * self.thick_pal)) + ":" +
#                     str(self.depth - self.thick_pal) + ":" +
#                     str(self.width - cut_width - self.thick_pal - 20) + ":" +
#                     str(cut_depth - self.thick_pal + 20) + "(cant " + str(self.cant_lab) + "):" +
#                     str(cut_width - self.thick_pal + 20) + "(cant " + str(self.cant_lab) + "):" +
#                     str(self.depth - cut_depth - 20) + ":")
#                 pol.cut_coords = [
#                     [0, cut_depth - self.thick_pal + 20],
#                     [cut_width - self.thick_pal + 20, cut_depth - self.thick_pal + 20],
#                     [cut_width - self.thick_pal + 20, 0],
#                     [self.width - (2 * self.thick_pal), 0],
#                     [self.width - (2 * self.thick_pal), self.depth - self.thick_pal],
#                     [0, self.depth - self.thick_pal]
#                 ]
#                 pol.move("x", self.thick_pal)
#                 pol.move("y", self.thick_pal)
#                 pol.move("z", int((self.height - self.thick_pal) / 2))
#                 # pol.move("y", -cut_depth)
#                 self.append(pol)
#                 # self.append(Accessory("decupare pal", 1))
#
#             front1 = Front(self.label + "_1", self.height - 2 * rules["gap_front"], cut_depth - 3 -
#                            rules["thick_front"], rules["thick_front"])
#             front1.rotate("y")
#             front1.move("x", cut_width)
#             front1.move("z", rules["gap_front"])
#             front1.move("y", rules["gap_front"])
#             self.append(front1)
#
#             front2 = Front(self.label + "_2", self.height - 2 * rules["gap_front"], cut_width - 3 -
#                            rules["thick_front"], rules["thick_front"])
#             front2.rotate("y")
#             front2.rotate("z")
#             front2.move("x", rules["gap_front"])
#             front2.move("y", cut_depth - rules["thick_front"])
#             front2.move("z", rules["gap_front"])
#             self.append(front2)
#
#             # blat2 = Blat(self.label + ".blat2", cut_depth, rules["width_blat"], rules["thick_blat"])
#             # blat2.move("z", self.height)
#             # blat2.move("x", cut_width)
#             # blat2.move("y", cut_depth)
#             # blat2.rotate("z")
#             # self.append(blat2)
#
#         else:
#             print("ERROR: Undefined orientation (only 'left' or 'right' possible!")
#
#         self.add_pfl()
#         #        self.get_item_by_type_label("pfl", self.label + ".pfl").move("y", - cut_depth)
#         # self.getPFLOO()[0].getPlacaOO()
#
#         self.append(Accessory("balama usa franta", 2))
#         self.append(Accessory("balama 170 deg", 2))
#         self.append(Accessory("surub 3.5x16", 4 * 4))  # pentru balamale
#         self.append(Accessory("picioare", 6))
#         self.append(Accessory("clema plinta", 3))
#         self.append(Accessory("surub 3.5x16", 3 * 4))  # pentru picioare
#         self.append(Accessory("surub blat", 4))
#         self.append(Accessory("L", 2))
#         self.append(Accessory("surub", 19))
#         self.append(Accessory("plinta", (cut_width + cut_depth) / 1000))
#         self.append(Accessory("sipca apa", (self.width + self.depth) / 1000))
#
#         # blat1 = Blat(self.label + ".blat1", self.width + rules["gap_spate"], rules["width_blat"], rules["thick_blat"])
#         # blat1.move("z", self.height)
#         # blat1.move("y", cut_depth - rules["gap_fata"])
#         # blat1.move("x", - rules["gap_spate"])
#         # blat1.move("z", 10)
#         # self.append(blat1)
#
#
# class TopCorner(Cabinet):
#
#     # TODO implemntare dubla pentru decupare placa
#
#     def __init__(self, label, height, width, depth, rules, cut_width, cut_depth, l_r, polite):
#         """
#         o---------width----------||   o------width------------||
#        ||                        ||   ||                      ||
#        ||     l_r="left"         ||   ||   l_r="right"        ||
#        ||                        ||   ||                      ||
#        depth                     ||   ||                      depth
#        ||        ----cut_width---||   ||-- cut_width--        ||
#        ||        |                                   |        ||
#        ||        cut_depth                    cut_depth       ||
#        ||        |                                   |        ||
#        ||=========                                   =========||
#         include PFL si fronturi
#         :param label:
#         :param height:
#         :param width:
#         :param depth:
#         :param rules:
#         :param cut_width:
#         :param cut_depth:
#         :param l_r:
#         :param polite:
#         """
#         super().__init__(label, height, width, depth, rules)
#         if l_r == "left":
#             # placa de jos
#             jos = BoardPal(self.label + ".jos", self.width - (2 * self.thick_pal), self.depth - self.thick_pal,
#                            self.thick_pal,
#                            "", "", "", "")
#             jos.add_obs("decupaj colt stanga. Cote in sensul acelor de ceasornic, de la coltul din stanga spate: " +
#                         str(self.width - 2 * self.thick_pal) + ":" + #cota1
#                         str(self.depth - cut_depth) + ":" + # cota2
#                         str(cut_width - self.thick_pal) + "(cant " + str(self.cant_lab) + "):" + # cota3
#                         str(cut_depth - self.thick_pal) + "(cant " + str(self.cant_lab) + "):" + # cota4
#                         str(self.width - cut_width - self.thick_pal) + ":" + # cota5
#                         str(self.depth - self.thick_pal)) # cota6
#             jos.cut_coords = [
#                 [0, 0],
#                 [self.width - cut_width - self.thick_pal, 0],
#                 [self.width - cut_width - self.thick_pal, cut_depth - self.thick_pal],
#                 [self.width - 2 * self.thick_pal, cut_depth - self.thick_pal],
#                 [self.width - 2 * self.thick_pal, self.depth - self.thick_pal],
#                 [0, self.depth - self.thick_pal]
#             ]
#             jos.move("y", self.thick_pal)
#             jos.move("x", self.thick_pal)
#             # jos.move("y", -cut_depth)
#             self.append(jos)
#             # self.append(Accessory("decupare pal",1))
#
#             # placa de sus
#             sus = BoardPal(self.label + ".sus", self.width - (2 * self.thick_pal), self.depth - self.thick_pal,
#                            self.thick_pal,
#                            "", "", "", "")
#             sus.add_obs("decupaj colt stanga. Cote in sensul acelor de ceasornic, de la coltul din stanga spate: " +
#                         str(self.width - 2 * self.thick_pal) + ":" +
#                         str(self.depth - cut_depth) + ":" +
#                         str(cut_width - self.thick_pal) + "(cant " + str(self.cant_lab) + "):" +
#                         str(cut_depth - self.thick_pal) + "(cant " + str(self.cant_lab) + "):" +
#                         str(self.width - cut_width - self.thick_pal) + ":" +
#                         str(self.depth - self.thick_pal))
#             sus.cut_coords = [
#                 [0, 0],
#                 [self.width - cut_width - self.thick_pal, 0],
#                 [self.width - cut_width - self.thick_pal, cut_depth - self.thick_pal],
#                 [self.width - 2 * self.thick_pal, cut_depth - self.thick_pal],
#                 [self.width - 2 * self.thick_pal, self.depth - self.thick_pal],
#                 [0, self.depth - self.thick_pal]
#             ]
#             sus.move("y", self.thick_pal)
#             sus.move("x", self.thick_pal)
#             sus.move("z", self.height - self.thick_pal)
#             # sus.move("y", -cut_depth)
#             self.append(sus)
#             # # self.append(Accessory("decupare pal", 1))
#
#             for i in range(polite):
#                 pol = BoardPal(self.label + ".pol", self.width - (2 * self.thick_pal),
#                                self.depth - (1 * self.thick_pal),
#                                self.thick_pal, "", "", "", "")
#                 pol.add_obs("decupaj colt stanga. Cote in sensul acelor de ceasornic, de la coltul din stanga spate: " +
#                             str(self.width - (2 * self.thick_pal)) + ":" +
#                             str(self.depth - cut_depth - 20) + ":" +
#                             str(cut_width - self.thick_pal + 20) + "(cant " + str(self.cant_lab) + "):" +
#                             str(cut_depth - self.thick_pal + 20) + "(cant " + str(self.cant_lab) + "):" +
#                             str(self.width - cut_width - self.thick_pal - 20) + ":" +
#                             str(self.depth - self.thick_pal))
#                 pol.cut_coords = [
#                     [0, 0],
#                     [self.width - cut_width - self.thick_pal - 20, 0],
#                     [self.width - cut_width - self.thick_pal - 20, cut_depth - self.thick_pal + 20],
#                     [self.width - 2 * self.thick_pal, cut_depth - self.thick_pal + 20],
#                     [self.width - 2 * self.thick_pal, self.depth - self.thick_pal],
#                     [0, self.depth - self.thick_pal]
#                 ]
#                 pol.move("x", self.thick_pal)
#                 pol.move("y", self.thick_pal)
#                 pol.move("z", (i + 1) * int((self.height - self.thick_pal) / (polite + 1)))
#                 # pol.move("y", -cut_depth)
#                 self.append(pol)
#                 # # self.append(Accessory("decupare pal", 1))
#
#             spate = BoardPal(self.label + ".spate", self.height, self.depth - self.thick_pal,
#                              self.thick_pal, "", "", "", "")
#             spate.rotate("y")
#             spate.move("y", self.thick_pal)
#             spate.move("x", self.thick_pal)
#             # spate.move("y", -cut_depth)
#             self.append(spate)
#
#             lat1 = BoardPal(self.label + ".lat1", self.height, self.width - cut_width, self.thick_pal, self.cant_lab,
#                             "",
#                             self.cant_lab, self.cant_lab)
#             lat1.rotate("y")
#             lat1.rotate("z")
#             # lat1.move("y", -cut_depth)
#             self.append(lat1)
#
#             lat2 = BoardPal(self.label + ".lat2", self.height, self.depth - cut_depth, self.thick_pal, self.cant_lab,
#                             "",
#                             self.cant_lab, self.cant_lab)
#             lat2.rotate("y")
#             lat2.move("x", self.width)
#             lat2.move("y", self.depth - lat2.width)
#             # lat2.move("y", -cut_depth)
#             self.append(lat2)
#
#             front1 = Front(self.label + "_1", self.height - 2 * rules["gap_front"],
#                            cut_depth - 3 - rules["thick_front"], rules["thick_front"])
#             front1.rotate("y")
#             front1.move("x", width - cut_width + rules["thick_front"])
#             front1.move("z", rules["gap_front"])
#             front1.move("y", rules["gap_front"])
#             self.append(front1)
#
#             front2 = Front(self.label + "_2", self.height - 2 * rules["gap_front"],
#                            cut_width - 3 - rules["thick_front"], rules["thick_front"])
#             front2.rotate("y")
#             front2.rotate("z")
#             front2.move("x", width - cut_width + rules["thick_front"])
#             front2.move("y", cut_depth - rules["thick_front"])
#             front2.move("z", rules["gap_front"])
#             self.append(front2)
#
#             # self.front = self.front + [["front", self.label + "_1", self.height - 4, cut_depth - 3 - front_thick]]
#             # self.front = self.front + [["front", self.label + "_2", self.height - 4, cut_width - 3 - front_thick]]
#
#
#         elif l_r == "right":
#             # placa de jos
#             jos = BoardPal(self.label + ".jos", self.width - (2 * self.thick_pal), self.depth - self.thick_pal,
#                            self.thick_pal,
#                            "", "", "", "")
#             jos.add_obs("decupaj colt dreapta. Cote in sensul acelor de ceasornic, de la coltul din stanga spate: " +
#                         str(self.width - (2 * self.thick_pal)) + ":" + # cota1
#                         str(self.depth - self.thick_pal) + ":" + # cota2
#                         str(self.width - cut_width - self.thick_pal) + ":" + # cota3
#                         str(cut_depth - self.thick_pal) + "(cant " + str(self.cant_lab) + "):" + # cota4
#                         str(cut_width - self.thick_pal) + "(cant " + str(self.cant_lab) + "):" + # cota5
#                         str(self.depth - cut_depth) + ":") # cota6
#             jos.cut_coords = [[0, cut_depth - self.thick_pal],
#                               [cut_width - self.thick_pal, cut_depth - self.thick_pal],
#                               [cut_width - self.thick_pal, 0],
#                               [self.width - (2 * self.thick_pal), 0],
#                               [self.width - (2 * self.thick_pal), self.depth - self.thick_pal],
#                               [0, self.depth - self.thick_pal]
#                               ]
#             jos.move("y", self.thick_pal)
#             # jos.move("y", -cut_depth)
#             jos.move("x", self.thick_pal)
#             self.append(jos)
#             # # self.append(Accessory("decupare pal", 1))
#
#             # placa de sus
#             sus = BoardPal(self.label + ".sus", self.width - (2 * self.thick_pal), self.depth - self.thick_pal,
#                            self.thick_pal,
#                            "", "", "", "")
#             sus.add_obs("decupaj colt dreapta. Cote in sensul acelor de ceasornic, de la coltul din stanga spate: " +
#                         str(self.width - (2 * self.thick_pal)) + ":" +
#                         str(self.depth - self.thick_pal) + ":" +
#                         str(self.width - cut_width - self.thick_pal) + ":" +
#                         str(cut_depth - self.thick_pal) + "(cant " + str(self.cant_lab) + "):" +
#                         str(cut_width - self.thick_pal) + "(cant " + str(self.cant_lab) + "):" +
#                         str(self.depth - cut_depth) + ":")
#             sus.cut_coords = [[0, cut_depth - self.thick_pal],
#                               [cut_width - self.thick_pal, cut_depth - self.thick_pal],
#                               [cut_width - self.thick_pal, 0],
#                               [self.width - (2 * self.thick_pal), 0],
#                               [self.width - (2 * self.thick_pal), self.depth - self.thick_pal],
#                               [0, self.depth - self.thick_pal]
#                               ]
#             sus.move("y", self.thick_pal)
#             sus.move("z", self.height - self.thick_pal)
#             # sus.move("y", -cut_depth)
#             sus.move("x", self.thick_pal)
#             self.append(sus)
#             # self.append(Accessory("decupare pal", 1))
#
#             for i in range(polite):
#                 pol = BoardPal(self.label + ".pol", self.width - (2 * self.thick_pal),
#                                self.depth - (1 * self.thick_pal),
#                                self.thick_pal, "", "", "", "")
#                 pol.add_obs(
#                     "decupaj colt dreapta. Cote in sensul acelor de ceasornic, de la coltul din stanga spate: " +
#                     str(self.width - (2 * self.thick_pal)) + ":" +
#                     str(self.depth - self.thick_pal) + ":" +
#                     str(self.width - cut_width - self.thick_pal - 20) + ":" +
#                     str(cut_depth - self.thick_pal + 20) + "(cant " + str(self.cant_lab) + "):" +
#                     str(cut_width - self.thick_pal + 20) + "(cant " + str(self.cant_lab) + "):" +
#                     str(self.depth - cut_depth - 20) + ":")
#                 pol.cut_coords = [[0, cut_depth - self.thick_pal + 20],
#                                   [cut_width - self.thick_pal + 20, cut_depth - self.thick_pal + 20],
#                                   [cut_width - self.thick_pal + 20, 0],
#                                   [self.width - (2 * self.thick_pal), 0],
#                                   [self.width - (2 * self.thick_pal), self.depth - self.thick_pal],
#                                   [0, self.depth - self.thick_pal]
#                                   ]
#                 pol.move("x", self.thick_pal)
#                 pol.move("y", self.thick_pal)
#                 pol.move("z", (i + 1) * int((self.height - self.thick_pal) / (polite + 1)))
#                 # pol.move("y", -cut_depth)
#                 self.append(pol)
#                 # self.append(Accessory("decupare pal", 1))
#
#             spate = BoardPal(self.label + ".spate", self.height, self.depth - self.thick_pal,
#                              self.thick_pal, "", "", "", "")
#             spate.rotate("y")
#             spate.move("y", self.thick_pal)
#             spate.move("x", self.width)
#             # spate.move("z", self.thick_pal)
#             # spate.move("y", -cut_depth)
#             self.append(spate)
#
#             lat1 = BoardPal(self.label + ".lat1", self.height, self.width - cut_width, self.thick_pal, self.cant_lab,
#                             "",
#                             self.cant_lab, self.cant_lab)
#             lat1.rotate("y")
#             lat1.rotate("z")
#             # lat1.move("y", -cut_depth)
#             lat1.move("x", cut_width)
#             self.append(lat1)
#
#             lat2 = BoardPal(self.label + ".lat2", self.height, self.depth - cut_depth, self.thick_pal, self.cant_lab,
#                             "",
#                             self.cant_lab, self.cant_lab)
#             lat2.rotate("y")
#             lat2.move("x", self.thick_pal)
#             lat2.move("y", self.depth - lat2.width)
#             # lat2.move("y", -cut_depth)
#             self.append(lat2)
#
#             front1 = Front(self.label + "_1", self.height - 2 * rules["gap_front"],
#                            cut_depth - 3 - rules["thick_front"], rules["thick_front"])
#             front1.rotate("y")
#             front1.move("x", cut_width)
#             front1.move("z", rules["gap_front"])
#             front1.move("y", rules["gap_front"])
#             self.append(front1)
#
#             front2 = Front(self.label + "_2", self.height - 2 * rules["gap_front"],
#                            cut_width - 3 - rules["thick_front"], rules["thick_front"])
#             front2.rotate("y")
#             front2.rotate("z")
#             front2.move("x", rules["gap_front"])
#             front2.move("y", cut_depth - rules["thick_front"])
#             front2.move("z", rules["gap_front"])
#             self.append(front2)
#
#             # self.front = self.front + [["front", self.label + "_1", self.height - 4, cut_depth - 3 - front_thick]]
#             # self.front = self.front + [["front", self.label + "_2", self.height - 4, cut_width - 3 - front_thick]]
#
#
#         else:
#             print("ERROR: Undefined orientation (only 'left' or 'right' possible!")
#
#         self.add_pfl()
#
#         self.append(Accessory("balama usa franta", 2))
#         self.append(Accessory("balama 170 deg", 2))
#         self.append(Accessory("surub 3.5x16", 4 * 4))  # pentru balamale
#         self.append(Accessory("surub", 20))
#         self.append(Accessory("pereche clema prindere perete", 1))
#         self.append(Accessory("sina perete", self.width / 1000))
#         self.append(Accessory("surub diblu perete", round(self.width / 201)))
#
#
# class Raft(Cabinet):
#     def __init__(self, label, height, width, depth, shelves, rules):
#         super().__init__(label, height, width, depth, rules)
#         picioare = math.ceil(self.width / 400) * 2
#         self.append(Accessory("picioare", picioare))
#         self.append(Accessory("clema plinta", picioare / 2))
#         self.append(Accessory("surub 3.5x16", picioare * 4))  # pentru picioare
#         self.append(Accessory("surub blat", 4))
#         self.append(Accessory("surub", 14))
#         self.append(Accessory("plinta", self.width / 1000))
#
#         # arhitectura
#         # jos
#         jos = BoardPal(self.label + ".jos", self.width, self.depth, self.thick_pal, self.cant_lab, "", self.cant_lab,
#                        self.cant_lab)
#         self.append(jos)
#
#         # lat rotit pe Y si ridicat pe z cu grosimea lui jos
#         lat1 = BoardPal(self.label + ".lat", self.height - self.thick_pal, self.depth, self.thick_pal, self.cant_lab,
#                         "", "", "")
#         lat1.rotate("y")
#         lat1.move("z", jos.thick)
#         self.append(lat1)
#
#         # lat rotit pe y, translatat pe x cu (jos - grosime), translatat pe z cu grosime jos
#         lat2 = BoardPal(self.label + ".lat", self.height - self.thick_pal, self.depth, self.thick_pal, self.cant_lab,
#                         "", "", "")
#         lat2.rotate("y")
#         lat2.move("x", jos.length - lat2.thick)
#         lat2.move("z", jos.thick)
#         self.append(lat2)
#
#         sus = BoardPal(self.label + ".sus", self.width - (2 * self.thick_pal), self.depth - (self.cant),
#                        self.thick_pal, self.cant_lab, "", "", "")
#         sus.move("z", lat1.length)
#         sus.move("x", lat1.thick)
#         self.append(sus)
#
#         self.add_pfl()
#
#         self.add_pol(shelves, 2)
#
#
# class Bar(Cabinet):
#     def __init__(self, label, height, width, depth, rules):
#         super().__init__(label, height, width, depth, rules)
#         self.append(Accessory("surub", 14))
#
#         # arhitectura
#         lat1 = BoardPal(self.label + ".lat1", self.height - self.thick_blat, self.depth - rules["gap_fata"],
#                         self.thick_pal, self.cant_lab, self.cant_lab, self.cant_lab, "")
#         lat1.rotate("y")
#         lat1.move("x", self.thick_pal)
#         lat1.move("y", rules["gap_fata"])
#         self.append(lat1)
#
#         lat2 = BoardPal(self.label + ".lat2", self.height - self.thick_blat, self.depth - rules["gap_fata"],
#                         self.thick_pal, self.cant_lab, self.cant_lab, self.cant_lab, "")
#         lat2.rotate("y")
#         lat2.move("x", self.width)
#         lat2.move("y", rules["gap_fata"])
#         self.append(lat2)
#
#         spate = BoardPal(self.label + ".spate", self.height - self.thick_blat, self.width - 2 * self.thick_pal,
#                          self.thick_pal, self.cant_lab, "", "", "")
#         spate.rotate("x")
#         spate.rotate("y")
#         spate.rotate("y")
#         spate.rotate("y")
#         spate.move("z", self.height - self.thick_blat)
#         spate.move("y", self.depth)  # - self.thick_pal
#         spate.move("x", self.thick_pal)
#         self.append(spate)
#
#         bl = Blat(self.label + ".blat", self.width, self.depth, self.thick_blat)
#         bl.move("z", self.height - self.thick_blat)
#         self.append(bl)
#
#
# class JollyBox(BaseBox):
#     def __init__(self, label, height, width, depth, rules):
#         super().__init__(label, height, width, depth, rules)
#         self.append(Accessory("surub 3.5x16", 8))  # prentu glisiere
#         self.append(Accessory("surub 3.5x16", 8))  # pentru front
#         if width < 150:
#             raise NameError("ERROR: Cos Jolly pentru Cabinetul ", self.label, "inexistent!")
#         elif width < 200:
#             self.append(Accessory("Joly150500", 1))
#         elif width < 300:
#             self.append(Accessory("Joly240500", 1))
#         else:
#             self.append(Accessory("Joly300500", 1))
#
#         self.add_pfl()
#         self.add_front([[100, 100]], "door")
#
#
# class TopBox(Cabinet):
#     def __init__(self, label, height, width, depth, rules):
#         super().__init__(label, height, width, depth, rules)
#
#         self.sep_max_depth = self.depth - self.cant
#         self.sep_prev = "h"
#         self.append(Accessory("surub", 8))
#         self.append(Accessory("pereche clema prindere perete", 1))
#         self.append(Accessory("sina perete", self.width / 1000))
#         self.append(Accessory("surub diblu perete", round(self.width / 201)))
#
#         # arhitectura
#         lat1 = BoardPal(self.label + ".lat1", self.height, self.depth, self.thick_pal, self.cant_lab, "",
#                         self.cant_lab, self.cant_lab)
#         lat1.rotate("y")
#         lat1.move("x", lat1.thick)
#         self.append(lat1)
#         # self.palOO.append(lat1)
#         jos = BoardPal(self.label + ".jos", self.width - (2 * self.thick_pal), self.depth - (self.cant),
#                        self.thick_pal, self.cant_lab, "", "", "")
#         jos.move("x", lat1.thick)
#         jos.move("y", self.cant_lab)
#         self.append(jos)
#         # self.palOO.append(jos)
#         lat2 = BoardPal(self.label + ".lat2", self.height, self.depth, self.thick_pal, self.cant_lab, "",
#                         self.cant_lab, self.cant_lab)
#         lat2.rotate("y")
#         lat2.move("x", jos.length + 2 * lat2.thick)
#         self.append(lat2)
#         # self.palOO.append(lat2)
#         sus = BoardPal(self.label + ".sus", self.width - (2 * self.thick_pal), self.depth - (self.cant),
#                        self.thick_pal, self.cant_lab, "", "", "")
#         sus.move("z", lat1.length - sus.thick)
#         sus.move("x", lat1.thick)
#         sus.move("y",self.cant_lab)
#         self.append(sus)
#
#         self.assemble_pal(lat1, jos, "wood_dowel", 6, 2)
#         self.assemble_pal(lat1, sus, "wood_dowel", 6, 2)
#         self.assemble_pal(lat2, jos, "wood_dowel", 6, 2)
#         self.assemble_pal(lat2, sus, "wood_dowel", 6, 2)
#
#         self.add_pfl()
#
#
# class SinkBox(BaseBox):
#     def __init__(self, label, height, width, depth, rules):
#         super().__init__(label, height, width, depth, rules)
#         self.remove_all_pfl()
#
#         leg_width = 100
#         legatura = BoardPal(self.label + ".leg", self.width - (2 * self.thick_pal), leg_width, self.thick_pal,
#                             self.cant_lab, "", "", "")
#         legatura.rotate("x")
#         legatura.move("x", self.thick_pal)
#         legatura.move("z", self.thick_pal)
#         legatura.move("y", self.depth - self.thick_pal)
#         legatura.move("y", self.thick_pal)
#         self.append(legatura)
#
#         leg1 = self.get_item_by_type_label("pal", self.label + ".leg1")
#
#         # reset all positioning
#         leg1.position_list = []
#         leg1.position = [leg1.length, leg1.width, leg1.thick, 0, 0, 0]
#
#         # position the board
#         leg1.rotate("x")
#         leg1.move("x", self.thick_pal)
#         leg1.move("z", self.height - leg1.width)
#         # # leg1.move("y", self.height)
#         # leg1.move("z", self.height - leg1.width)
#         leg1.move("y", leg1.thick)
#         # leg1.move("z", self.thick_pal - leg1.width)
#
#         leg2 = self.get_item_by_type_label("pal", self.label + ".leg2")
#         # reset all positioning
#         leg2.position_list = []
#         leg2.position = [leg2.length, leg2.width, leg2.thick, 0, 0, 0]
#
#         # position the board
#         leg2.rotate("x")
#         leg2.move("x", self.thick_pal)
#         leg2. move("z", self.height - leg2.width)
#         leg2.move("y", self.depth)
#         # leg2.move("z", 3 * leg2.width - self.thick_pal)
#         # # leg2.move("y", leg2.thick)
#         # leg2.move("z", self.thick_pal - leg2.width)
#         # leg2.move("y", leg2.width - self.thick_pal)
#
#
# class TowerBox(Cabinet):
#     def __init__(self, label, height, width, depth, rules, gap_list = [20, 40], gap_heat = 50, front_list = [0, 0, 0, 0]):
#         """
#
#         :param label:
#         :param height:
#         :param width:
#         :param depth:
#         :param rules:
#         :param gap_list: intaltimea gap-urilor de jos in sus. Ultimul gap e cat ramane (ex:[gen_h_base - 2 * t1.pal_width,300, gen_h_tower - gen_h_base - 318 - gen_h_top])
#         :param gap_heat: distanta in spate cat sunt mai in interior politele fata de lateriale ca sa permita evacuarea cladurii
#         :param front_list: care gap-uri au front (ex. [0, 0, 0, 1])
#         """
#         super().__init__(label, height, width, depth, rules)
#         self.depth = self.depth - gap_heat
#         jos = BoardPal(self.label + ".jos", self.width, self.depth, self.thick_pal, self.cant_lab, "", self.cant_lab,
#                        self.cant_lab)
#         self.append(jos)
#
#         lat1 = BoardPal(self.label + ".lat", self.height - self.thick_pal, self.depth + gap_heat, self.thick_pal,
#                         self.cant_lab, "", self.cant_lab, "")
#         lat1.rotate("y")
#         lat1.move("z", jos.thick)
#         lat1.move("x", self.thick_pal)
#         self.append(lat1)
#
#         lat2 = BoardPal(self.label + ".lat", self.height - self.thick_pal, self.depth + gap_heat, self.thick_pal,
#                         self.cant_lab, "", self.cant_lab, "")
#         lat2.rotate("y")
#         lat2.move("z", jos.thick)
#         lat2.move("x", jos.length)
#         self.append(lat2)
#
#         sus = BoardPal(self.label + ".sus", self.width - (2 * self.thick_pal), self.depth - (self.cant),
#                        self.thick_pal, self.cant_lab, "", "", "")
#         sus.move("x", lat1.thick)
#         sus.move("z", lat1.length)
#         self.append(sus)
#
#         # adding horizontal separators
#         offset = 0
#         for gap in range(len(gap_list)):
#             offset += gap_list[gap]  # + self.thick_pal
#             self.add_sep_h(self.width - 2 * self.thick_pal, 0, offset, self.cant_lab)
#             offset += self.thick_pal
#         # self.addSepH(self.width - 2 * self.thick_pal, 0, gap_list[0], self.cant_lab)
#         # self.addSepH(self.width - 2 * self.thick_pal, 0, gap_list[0] + gap_list[1] + self.thick_pal, self.cant_lab)
#         # self.addSepH(self.width - 2 * self.thick_pal, 0, gap_list[0] + gap_list[1] + gap_list[2] + (2 * self.thick_pal),
#         #              self.cant_lab)
#
#         self.append(Accessory("surub", 8))
#         self.append(Accessory("plinta", self.width / 1000))
#         picioare = math.ceil(self.width / 400) * 2
#         self.append(Accessory("picioare", picioare))
#         self.append(Accessory("clema plinta", picioare / 2))
#         self.append(Accessory("surub 3.5x16", picioare * 4))  # pentru picioare
#
#         self.add_pfl()
#
#         # if front_list[0] == 1:
#         #     if front_list[1] == 0:
#         #         self.add_front_manual(gap_list[0] + (2 * self.thick_pal) - 4, self.width - 4, 0, 0)
#         #         if front_list[2] == 0:
#         #
#         #         elif front_list[2] == 1:
#         #     elif front_list[1] == 1:
#         #         self.add_front_manual(gap_list[0] + (1.5 * self.thick_pal) - 3, self.width - 4, 0, 0)
#
#         # Setting the front doors for the tower
#         fg = rules["gap_front"]
#         # gap_list[0]
#         if (front_list[0] == 1) and (front_list[1] == 0):
#             # door down but not above
#             self.add_front_manual(gap_list[0] + (self.thick_pal - fg) * 2, self.width - (2 * fg), 0, 0)
#         if (front_list[0] == 1) and (front_list[1] == 1):
#             # door down and above
#             self.add_front_manual(gap_list[0] + (self.thick_pal - fg) * 1.5, self.width - (2 * fg), 0, 0)
#
#         # gap_list[1]
#         if (front_list[1] == 1) and (front_list[0] == 0) and (front_list[2] == 0):
#             self.add_front_manual(gap_list[1] + (self.thick_pal - fg) * 2 , self.width - (2 * fg), 0,
#                                   gap_list[0] + self.thick_pal)
#         if (((front_list[1] == 1) and (front_list[0] == 1) and (front_list[2] == 0))
#                 or ((front_list[1] == 1) and (front_list[0] == 0) and (front_list[2] == 1))):
#             self.add_front_manual(gap_list[1] + (1.5 * (self.thick_pal - fg)), self.width - (2 * fg), 0,
#                                   gap_list[0] + (self.thick_pal / 2))
#         if (front_list[1] == 1) and (front_list[0] == 1) and (front_list[2] == 1):
#             self.add_front_manual(gap_list[1] + self.thick_pal - fg, self.width - 4, 0,
#                                   gap_list[0] + (self.thick_pal - fg) * 1.5 + fg)
#
#         # gap_list[2]
#         if (front_list[2] == 1) and (front_list[1] == 0) and (front_list[3] == 0):
#             self.add_front_manual(gap_list[2] + (2 * (self.thick_pal - fg)), self.width - (2 * fg), 0,
#                                   gap_list[0] + self.thick_pal + gap_list[1] + self.thick_pal)
#         if (((front_list[2] == 1) and (front_list[1] == 1) and (front_list[3] == 0))
#                 or ((front_list[2] == 1) and (front_list[1] == 0) and (front_list[3] == 1))):
#             self.add_front_manual(gap_list[2] + (1.5 * (self.thick_pal - fg)), self.width - (2 * fg), 0,
#                                   gap_list[0] + 2 * self.thick_pal + gap_list[1])
#         if (front_list[2] == 1) and (front_list[1] == 1) and (front_list[3] == 1):
#             self.add_front_manual(gap_list[2] + self.thick_pal - fg, self.width - 4, 0,
#                                   gap_list[0] + (self.thick_pal - fg) * 1.5 + fg +
#                                   gap_list[1] + self.thick_pal - fg + fg)
#
#         # gap_list[3]
#         if (front_list[3] == 1) and (front_list[2] == 0):
#             self.add_front_manual(self.height - gap_list[0] - gap_list[1] - gap_list[2] - (3 * (self.thick_pal - fg)),
#                                   self.width - (2 * fg), 0,
#                                   gap_list[0] + gap_list[1] + gap_list[2] + (3 * self.thick_pal) + fg)
#         if (front_list[3] == 1) and (front_list[2] == 1):
#             self.add_front_manual(self.height - gap_list[0] - gap_list[1] - gap_list[2] - (3.5 * self.thick_pal) - 3,
#                                   self.width - 4, 0,
#                                   gap_list[0] + (self.thick_pal - fg) * 1.5 + fg +
#                                   gap_list[1] + self.thick_pal - fg + fg +
#                                   gap_list[2] + self.thick_pal - fg + fg)
#
#
# class MsVBox(Cabinet):
#     def __init__(self, label, height, width, depth, rules):
#         """
#
#         :param label:
#         :param height:
#         :param width:
#         :param depth:
#         :param rules:
#
#         """
#         super().__init__(label, height, width, depth, rules)
#         self.append(Accessory("sipca apa", self.width / 1000))
#         self.append(Accessory("plinta", self.width / 1000))
#         self.append(Accessory("surub intre corpuri", 10))
#         # blatul = Blat(self.label + ".blat", self.width, self.width_blat, self.thick_blat)
#         # blatul.move("z", self.height)
#         # blatul.move("y", -rules["gap_fata"])
#         # self.append(blatul)
#         self.add_front([[100, 100]], "door")
#
#
# class BaseCornerShelf(Cabinet):
#     def __init__(self, label, height, width, depth, shelves, rules, rounded=False):
#         super().__init__(label, height, width, depth, rules)
#
#         back1 = BoardPal(self.label + ".back1", self.height, self.width - self.thick_pal, self.thick_pal, 1, 1, 1, 0)
#         back1.rotate("y")
#         back1.rotate("z")
#         back1.move("x", self.thick_pal)
#         back1.move("y", self.depth - self.thick_pal)
#         self.append(back1)
#
#         back2 = BoardPal(self.label + ".back2", self.height, self.depth, self.thick_pal, 1, 0, 1, 0)
#         back2.rotate("y")
#         self.append(back2)
#         back2.move("x", self.thick_pal)
#         self.append(Accessory("surub", 2))
#
#         base = BoardPal(self.label + ".base", self.width - self.thick_pal, self.depth - self.thick_pal, self.thick_pal, 0, 0, 0, 0)
#         # base.add_obs("decupaj rotund cu raza de " + str(min(self.width, self.depth) - self.thick_pal))
#         # round coordinates:
#         # x = radius * Math.sin(Math.PI * 2 * angle / 360);
#         #
#         # y = radius * Math.cos(Math.PI * 2 * angle / 360);
#         #
#         if rounded:
#             radius = min(self.width, self.depth) - self.thick_pal
#             base.add_obs("decupaj rotund cu raza de " + str(radius))
#             base.cut_coords = [
#                 [0, 0],
#                 [radius * math.sin(math.radians(15)), radius - (radius * math.cos(math.radians(15)))],
#                 [radius * math.sin(math.radians(2 * 15)), radius - (radius * math.cos(math.radians(2 * 15)))],
#                 [radius * math.sin(math.radians(3 * 15)), radius - (radius * math.cos(math.radians(3 * 15)))],
#                 [radius * math.sin(math.radians(4 * 15)), radius - (radius * math.cos(math.radians(4 * 15)))],
#                 [radius * math.sin(math.radians(5 * 15)), radius - (radius * math.cos(math.radians(5 * 15)))],
#                 [base.length, radius],
#                 [base.length, base.width],
#                 [0, base.width]
#             ]
#         base.move("x", self.thick_pal)
#         self.append(base)
#         self.append(Accessory("surub", 4))
#
#         for i in range(shelves):
#             shelf = BoardPal(self.label + ".shelf", self.width  - self.thick_pal, self.depth  - self.thick_pal, self.thick_pal, 0, 0, 0, 0)
#             if rounded:
#                 radius = min(self.width, self.depth) - self.thick_pal
#                 shelf.add_obs("decupaj rotund cu raza de " + str(radius))
#                 shelf.cut_coords = [
#                     [0, 0],
#                     [radius * math.sin(math.radians(15)), radius - (radius * math.cos(math.radians(15)))],
#                     [radius * math.sin(math.radians(2 * 15)), radius - (radius * math.cos(math.radians(2 * 15)))],
#                     [radius * math.sin(math.radians(3 * 15)), radius - (radius * math.cos(math.radians(3 * 15)))],
#                     [radius * math.sin(math.radians(4 * 15)), radius - (radius * math.cos(math.radians(4 * 15)))],
#                     [radius * math.sin(math.radians(5 * 15)), radius - (radius * math.cos(math.radians(5 * 15)))],
#                     [shelf.length, radius],
#                     [shelf.length, shelf.width],
#                     [0, shelf.width]
#                 ]
#             # shelf.add_obs("decupaj rotund cu raza de " + str(min(self.width, self.depth) - self.thick_pal))
#             shelf.move("z", ((self.height - ((shelves + 1) * self.thick_pal))/(shelves+1))*(i+1) + self.thick_pal)
#             shelf.move("x", self.thick_pal)
#             self.append(shelf)
#             self.append(Accessory("surub", 4))
