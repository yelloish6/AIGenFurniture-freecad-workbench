import math

from AIGenFurniture.furniture_design.cabinets.elements.accessory import Accessory
from AIGenFurniture.furniture_design.cabinets.elements.board import BoardPal
from AIGenFurniture.furniture_design.cabinets.cabinet import Cabinet


class Raft(Cabinet):
    def __init__(self, label, height, width, depth, shelves, rules):
        super().__init__(label, height, width, depth, rules)
        legs = math.ceil(self.width / 400) * 2
        self.append(Accessory("picioare", legs))
        self.append(Accessory("clema plinta", legs / 2))
        self.append(Accessory("surub 3.5x16", legs * 4))  # for the legs
        self.append(Accessory("surub blat", 4))
        self.append(Accessory("surub", 14))
        self.append(Accessory("plinta", self.width / 1000))

        # arhitectura
        # jos
        jos = BoardPal(self.label + ".jos", self.width, self.depth, self.thick_pal, self.cant_lab, "", self.cant_lab,
                       self.cant_lab)
        self.append(jos)

        # lat rotit pe Y si ridicat pe z cu grosimea lui jos
        lat1 = BoardPal(self.label + ".lat", self.height - self.thick_pal, self.depth, self.thick_pal, self.cant_lab,
                        "", "", "")
        lat1.rotate("y")
        lat1.move("x", 2 * self.thick_pal)
        lat1.move("z", jos.thick)
        self.append(lat1)

        # lat rotit pe y, translatat pe x cu (jos - grosime), translatat pe z cu grosime jos
        lat2 = BoardPal(self.label + ".lat", self.height - self.thick_pal, self.depth, self.thick_pal, self.cant_lab,
                        "", "", "")
        lat2.rotate("y")
        lat2.move("x", jos.length + self.thick_pal)
        lat2.move("z", jos.thick)
        self.append(lat2)

        sus = BoardPal(self.label + ".sus", self.width - (2 * self.thick_pal), self.depth - (self.cant),
                       self.thick_pal, self.cant_lab, "", "", "")
        sus.move("z", lat1.length)
        sus.move("x", lat1.thick)
        self.append(sus)

        self.add_pfl()

        self.add_pol(shelves, 2)
