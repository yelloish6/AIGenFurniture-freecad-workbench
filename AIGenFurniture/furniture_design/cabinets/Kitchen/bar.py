from AIGenFurniture.furniture_design.cabinets.elements.accessory import Accessory
from AIGenFurniture.furniture_design.cabinets.elements.board import BoardPal, Blat
from AIGenFurniture.furniture_design.cabinets.cabinet import Cabinet

class Bar(Cabinet):
    def __init__(self, label, height, width, depth, rules):
        super().__init__(label, height, width, depth, rules)
        self.append(Accessory("surub", 14))

        # arhitectura
        lat1 = BoardPal(self.label + ".lat1", self.height - self.thick_blat, self.depth - rules["gap_fata"],
                        self.thick_pal, self.cant_lab, self.cant_lab, self.cant_lab, "")
        lat1.rotate("y")
        lat1.move("x", self.thick_pal)
        lat1.move("y", rules["gap_fata"])
        self.append(lat1)

        lat2 = BoardPal(self.label + ".lat2", self.height - self.thick_blat, self.depth - rules["gap_fata"],
                        self.thick_pal, self.cant_lab, self.cant_lab, self.cant_lab, "")
        lat2.rotate("y")
        lat2.move("x", self.width)
        lat2.move("y", rules["gap_fata"])
        self.append(lat2)

        spate = BoardPal(self.label + ".spate", self.height - self.thick_blat, self.width - 2 * self.thick_pal,
                         self.thick_pal, self.cant_lab, "", "", "")
        spate.rotate("x")
        spate.rotate("y")
        spate.rotate("y")
        spate.rotate("y")
        spate.move("z", self.height - self.thick_blat)
        spate.move("y", self.depth)  # - self.thick_pal
        spate.move("x", self.thick_pal)
        self.append(spate)

        bl = Blat(self.label + ".blat", self.width, self.depth, self.thick_blat)
        bl.move("z", self.height - self.thick_blat)
        self.append(bl)