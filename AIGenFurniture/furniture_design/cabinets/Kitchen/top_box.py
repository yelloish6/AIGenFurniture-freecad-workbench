from AIGenFurniture.furniture_design.cabinets.cabinet import Cabinet
from AIGenFurniture.furniture_design.cabinets.elements.accessory import Accessory
from AIGenFurniture.furniture_design.cabinets.elements.board import BoardPal, Blat

class TopBox(Cabinet):
    def __init__(self, label, height, width, depth, rules):
        super().__init__(label, height, width, depth, rules)

        self.sep_max_depth = self.depth - self.cant
        self.sep_prev = "h"
        self.append(Accessory("surub", 8))
        self.append(Accessory("pereche clema prindere perete", 1))
        self.append(Accessory("sina perete", self.width / 1000))
        self.append(Accessory("surub diblu perete", round(self.width / 201)))

        # arhitectura
        lat1 = BoardPal(self.label + ".lat1", self.height, self.depth, self.thick_pal, self.cant_lab, "",
                        self.cant_lab, self.cant_lab)
        lat1.rotate("y")
        lat1.move("x", lat1.thick)
        self.append(lat1)
        # self.palOO.append(lat1)
        jos = BoardPal(self.label + ".jos", self.width - (2 * self.thick_pal), self.depth - (self.cant),
                       self.thick_pal, self.cant_lab, "", "", "")
        jos.move("x", lat1.thick)
        jos.move("y", self.cant_lab)
        self.append(jos)
        # self.palOO.append(jos)
        lat2 = BoardPal(self.label + ".lat2", self.height, self.depth, self.thick_pal, self.cant_lab, "",
                        self.cant_lab, self.cant_lab)
        lat2.rotate("y")
        lat2.move("x", jos.length + 2 * lat2.thick)
        self.append(lat2)
        # self.palOO.append(lat2)
        sus = BoardPal(self.label + ".sus", self.width - (2 * self.thick_pal), self.depth - (self.cant),
                       self.thick_pal, self.cant_lab, "", "", "")
        sus.move("z", lat1.length - sus.thick)
        sus.move("x", lat1.thick)
        sus.move("y",self.cant_lab)
        self.append(sus)

        self.assemble_pal(lat1, jos, "wood_dowel", 6, 2)
        self.assemble_pal(lat1, sus, "wood_dowel", 6, 2)
        self.assemble_pal(lat2, jos, "wood_dowel", 6, 2)
        self.assemble_pal(lat2, sus, "wood_dowel", 6, 2)

        self.add_pfl()