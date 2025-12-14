from AIGenFurniture.furniture_design.cabinets.cabinet import Cabinet
from AIGenFurniture.furniture_design.cabinets.elements.accessory import Accessory

class MsVBox(Cabinet):
    def __init__(self, label, height, width, depth, rules):
        """

        :param label:
        :param height:
        :param width:
        :param depth:
        :param rules:

        """
        super().__init__(label, height, width, depth, rules)
        self.append(Accessory("sipca apa", self.width / 1000))
        self.append(Accessory("plinta", self.width / 1000))
        self.append(Accessory("surub intre corpuri", 10))
        # blatul = Blat(self.label + ".blat", self.width, self.width_blat, self.thick_blat)
        # blatul.move("z", self.height)
        # blatul.move("y", -rules["gap_fata"])
        # self.append(blatul)
        self.add_front([[100, 100]], "door")