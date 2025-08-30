import math

from AIGenFurniture.furniture_design.cabinets.cabinet import Cabinet
from AIGenFurniture.furniture_design.cabinets.elements.accessory import Accessory
from AIGenFurniture.furniture_design.cabinets.elements.board import BoardPal, Blat


class BaseBox(Cabinet):
    def __init__(self, label, height, width, depth, rules):
        super().__init__(label, height, width, depth, rules)
        picioare = math.ceil(self.width / 400) * 2
        self.append(Accessory("picioare", picioare))
        self.append(Accessory("clema plinta", picioare / 2))
        self.append(Accessory("surub 3.5x16", picioare * 4))  # pentru picioare
        self.append(Accessory("surub blat", 4))
        self.append(Accessory("surub", 14))
        self.append(Accessory("plinta", self.width / 1000))
        self.append(Accessory("sipca apa", self.width / 1000))

        # arhitectura
        # jos
        jos = BoardPal(self.label + ".jos", self.width, self.depth, self.thick_pal,
                       self.cant_lab,"", self.cant_lab, self.cant_lab)
        self.append(jos)

        # lat rotit pe Y si ridicat pe z cu grosimea lui jos
        lat1 = BoardPal(self.label + ".lat", self.height - self.thick_pal, self.depth, self.thick_pal,
                        self.cant_lab,"", "", "")
        lat1.rotate("y")
        lat1.rotate("y")
        lat1.rotate("y")
        lat1.move("x", lat1.thick)
        lat1.move("z", jos.thick)
        self.append(lat1)

        # lat rotit pe y, translatat pe x cu (jos - grosime), translatat pe z cu grosime jos
        lat2 = BoardPal(self.label + ".lat", self.height - self.thick_pal, self.depth, self.thick_pal, self.cant_lab,
                        "", "", "")
        lat2.rotate("y")
        lat2.rotate("y")
        lat2.rotate("y")
        lat2.move("x", lat2.thick)
        lat2.move("x", jos.length - lat2.thick)
        lat2.move("z", jos.thick)
        self.append(lat2)

        # leg translatat pe z cu (lungimea lat + offset lat - grosime leg), si pe x cu grosime lat
        leg1 = BoardPal(self.label + ".leg1", self.width - (2 * (self.thick_pal + self.cant)), 100, self.thick_pal,
                        self.cant_lab, self.cant_lab, "", "")
        leg1.move("z", lat1.length + jos.thick - leg1.thick)
        leg1.move("x", lat1.thick)
        self.append(leg1)

        # leg translatat pe z cu (lungimea lat + offset lat - grosime leg)
        #               pe y cu (latime lat - latime leg)
        #               pe x cu grosime lat
        leg2 = BoardPal(self.label + ".leg2", self.width - (2 * (self.thick_pal + self.cant)), 100, self.thick_pal,
                        self.cant_lab, self.cant_lab, "", "")
        leg2.move("z", lat1.length + jos.thick - leg1.thick)
        leg2.move("y", lat1.width - leg2.width)
        leg2.move("x", lat1.thick)
        self.append(leg2)

        blatul = Blat(self.label + ".blat", self.width, self.width_blat, self.thick_blat)
        blatul.move("z", self.height)
        blatul.move("y", -rules["gap_fata"])
        self.append(blatul)

        self.add_pfl()