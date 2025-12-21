import math, json, os

from AIGenFurniture.furniture_design.cabinets.cabinet import Cabinet
from AIGenFurniture.furniture_design.cabinets.elements.accessory import Accessory
from AIGenFurniture.furniture_design.cabinets.elements.board import BoardPal, Blat
# from AIGenFurniture.furniture_design.cabinets.assemblies import ASSEMBLIES

# ASSEMBLY_TYPE = "euro_screw"

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
        jos = BoardPal(self.label + ".down", self.width, self.depth, self.thick_pal,
                       self.cant_lab,"", self.cant_lab, self.cant_lab)
        self.append(jos)

        # lat rotit pe Y si ridicat pe z cu grosimea lui jos
        lat1 = BoardPal(self.label + ".lat_l", self.height - self.thick_pal, self.depth, self.thick_pal,
                        self.cant_lab,"", "", "")
        lat1.rotate("y")
        lat1.rotate("y")
        lat1.rotate("y")
        lat1.move("x", lat1.thick)
        lat1.move("z", jos.thick)
        self.append(lat1)

        # ASSEMBLIES[ASSEMBLY_TYPE](jos, lat1)

        # lat rotit pe y, translatat pe x cu (jos - grosime), translatat pe z cu grosime jos
        lat2 = BoardPal(self.label + ".lat_r", self.height - self.thick_pal, self.depth, self.thick_pal, self.cant_lab,
                        "", "", "")
        lat2.rotate("y")
        lat2.rotate("y")
        lat2.rotate("y")
        lat2.move("x", lat2.thick)
        lat2.move("x", jos.length - lat2.thick)
        lat2.move("z", jos.thick)
        self.append(lat2)

        # ASSEMBLIES[ASSEMBLY_TYPE](jos, lat2)

        # leg translatat pe z cu (lungimea lat + offset lat - grosime leg), si pe x cu grosime lat
        leg1 = BoardPal(self.label + ".top1", self.width - (2 * self.thick_pal), 100, self.thick_pal,
                        self.cant_lab, self.cant_lab, "", "")
        leg1.move("z", lat1.length + jos.thick - leg1.thick)
        leg1.move("x", lat1.thick)
        self.append(leg1)

        # ASSEMBLIES[ASSEMBLY_TYPE](leg1, lat1)
        # ASSEMBLIES[ASSEMBLY_TYPE](leg1, lat2)

        leg2 = BoardPal(self.label + ".top2", self.width - (2 * self.thick_pal), 100, self.thick_pal,
                        self.cant_lab, self.cant_lab, "", "")
        leg2.move("z", lat1.length + jos.thick - leg1.thick)
        leg2.move("y", lat1.width - leg2.width)
        leg2.move("x", lat1.thick)
        self.append(leg2)

        # ASSEMBLIES[ASSEMBLY_TYPE](leg2, lat1)
        # ASSEMBLIES[ASSEMBLY_TYPE](leg2, lat2)

        # blatul = Blat(self.label + ".blat", self.width, self.width_blat, self.thick_blat)
        # blatul.move("z", self.height)
        # blatul.move("y", -rules["gap_fata"])
        # self.append(blatul)

        self.add_pfl()

if __name__ == "__main__":

    RULES = {
        "thick_pal": 18,
        "thick_front": 18,
        "thick_blat": 38,
        "height_legs": 100,
        "general_width": 600,
        "width_blat": 600,
        "gap_spate": 50,
        "gap_fata": 50,
        "gap_front": 2,
        "cant_general": 1,
        "cant_pol": 2,
        "cant_separator": 1,
        "pol_depth": 20
    }

    print("=== Running BaseBox test scenario ===")

    cabinet = BaseBox("test_cabinet", 720, 600, 500, RULES)

    print(cabinet.get_item_by_type_label("pal", "test_cabinet.jos").__getattribute__("label"))
    print(cabinet.get_item_by_type_label("pal","test_cabinet.jos").__getattribute__("position"))
    print(cabinet.get_item_by_type_label("pal","test_cabinet.jos").__getattribute__("drill_list"))
    print(cabinet.get_item_by_type_label("pal", "test_cabinet.lat1").__getattribute__("label"))
    print(cabinet.get_item_by_type_label("pal", "test_cabinet.lat1").__getattribute__("position"))
    print(cabinet.get_item_by_type_label("pal", "test_cabinet.lat1").__getattribute__("drill_list"))
    print(cabinet.get_item_by_type_label("pal", "test_cabinet.lat2").__getattribute__("label"))
    print(cabinet.get_item_by_type_label("pal", "test_cabinet.lat2").__getattribute__("position"))
    print(cabinet.get_item_by_type_label("pal", "test_cabinet.lat2").__getattribute__("drill_list"))
    print(cabinet.get_item_by_type_label("pal", "test_cabinet.leg1").__getattribute__("label"))
    print(cabinet.get_item_by_type_label("pal", "test_cabinet.leg1").__getattribute__("position"))
    print(cabinet.get_item_by_type_label("pal", "test_cabinet.leg1").__getattribute__("drill_list"))
    print(cabinet.get_item_by_type_label("pal", "test_cabinet.leg2").__getattribute__("label"))
    print(cabinet.get_item_by_type_label("pal", "test_cabinet.leg2").__getattribute__("position"))
    print(cabinet.get_item_by_type_label("pal", "test_cabinet.leg2").__getattribute__("drill_list"))