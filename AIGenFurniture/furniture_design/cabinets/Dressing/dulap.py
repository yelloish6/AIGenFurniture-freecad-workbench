from AIGenFurniture.furniture_design.cabinets.elements.accessory import *
from AIGenFurniture.furniture_design.cabinets.elements.board import *
from AIGenFurniture.furniture_design.cabinets.cabinet import Cabinet

class Dulap(Cabinet):
    def __init__(self, label, height, width, depth, rules):
        """
        Cabinet simplu:
        |-------|
        |       |
        |       |
        |_______|
        :param label:
        :param haight:
        :param width:
        :param depth:
        :param rules:
        """
        super().__init__(label, height, width, depth, rules)

        lat1 = BoardPal(self.label + "_lat", self.height, self.depth, self.thick_pal, self.cant_lab, "", self.cant_lab, self.cant_lab)
        lat1.rotate("y")
        lat1.move("x", self.thick_pal)
        self.append(lat1)

        lat2 = BoardPal(self.label + "_lat", self.height, self.depth, self.thick_pal, self.cant_lab, "", self.cant_lab,
                        self.cant_lab)
        lat2.rotate("y")
        lat2.move("x", self.width)
        self.append(lat2)

        jos = BoardPal(self.label + "_jos", self.width - 2 * self.thick_pal, self.depth, self.thick_pal, self.cant_lab,
                       "", "", "")
        jos.move("x", self.thick_pal)
        self.append(jos)

        sus = BoardPal(self.label + "_sus", self.width - 2 * self.thick_pal, self.depth, self.thick_pal, self.cant_lab,
                       "", "", "")
        sus.move("x", self.thick_pal)
        sus.move("z", self.height - self.thick_pal)
        self.append(sus)

        self.append(Accessory("surub", 8))