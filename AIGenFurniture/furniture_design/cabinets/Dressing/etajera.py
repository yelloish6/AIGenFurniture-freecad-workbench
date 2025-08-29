from AIGenFurniture.furniture_design.cabinets.elements.accessory import *
from AIGenFurniture.furniture_design.cabinets.elements.board import *
from AIGenFurniture.furniture_design.cabinets.cabinet import Cabinet

class Etajera(Cabinet):
    def __init__(self, label, height, width, depth, shelves, rules):
        super().__init__(label, height, width, depth, rules)

        lat1 = BoardPal(self.label + ".lat", self.height, self.depth, self.thick_pal, self.cant_lab, "", "", "")
        lat1.rotate("y")
        lat1.move("x", self.thick_pal)
        self.append(lat1)

        lat2 = BoardPal(self.label + ".lat", self.height, self.depth, self.thick_pal, self.cant_lab, "", "", "")
        lat2.rotate("y")
        lat2.move("x", width)
        self.append(lat2)

        sus = BoardPal(self.label + ".sus", self.width - (2 * self.thick_pal), self.depth,
                       self.thick_pal, self.cant_lab, "", "", "")
        sus.move("z", height - self.thick_pal)
        sus.move("x", self.thick_pal)
        self.append(sus)

        jos = BoardPal(self.label + ".jos", self.width - (2 * self.thick_pal), self.depth,
                       self.thick_pal, self.cant_lab, "", "", "")
        jos.move("x", self.thick_pal)
        self.append(jos)

        self.add_pfl()

        self.append(Accessory("eurosurub 7x50", 8))

        self.add_pol(shelves, 2)