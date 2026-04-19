# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
from ..cabinet import Cabinet
from ..elements.accessory import Accessory
from ..elements.board import BoardPal, Blat
# from ..assemblies import ASSEMBLIES

# ASSEMBLY_TYPE = "euro_screw"

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
        lat1 = BoardPal(self.label + ".lat_l", self.height, self.depth, self.thick_pal, self.cant_lab, "",
                        self.cant_lab, self.cant_lab)
        lat1.rotate_cw("y")
        lat1.move("x", lat1.thick)
        self.append(lat1)
        # self.palOO.append(lat1)
        jos = BoardPal(self.label + ".down", self.width - (2 * self.thick_pal), self.depth - (self.cant),
                       self.thick_pal, self.cant_lab, "", "", "")
        jos.move("x", lat1.thick)
        jos.move("y", self.cant_lab)
        self.append(jos)
        # self.palOO.append(jos)
        lat2 = BoardPal(self.label + ".lat_r", self.height, self.depth, self.thick_pal, self.cant_lab, "",
                        self.cant_lab, self.cant_lab)
        lat2.rotate_cw("y")
        lat2.move("x", jos.length + 2 * lat2.thick)
        self.append(lat2)
        # self.palOO.append(lat2)
        sus = BoardPal(self.label + ".up", self.width - (2 * self.thick_pal), self.depth - (self.cant),
                       self.thick_pal, self.cant_lab, "", "", "")
        sus.move("z", lat1.length - sus.thick)
        sus.move("x", lat1.thick)
        sus.move("y",self.cant_lab)
        self.append(sus)

        # ASSEMBLIES[ASSEMBLY_TYPE](lat1, sus)
        # ASSEMBLIES[ASSEMBLY_TYPE](lat1, jos)
        # ASSEMBLIES[ASSEMBLY_TYPE](lat2, sus)
        # ASSEMBLIES[ASSEMBLY_TYPE](lat2, jos)

        # self.assemble_pal(lat1, jos, "wood_dowel", 6, 2)
        # self.assemble_pal(lat1, sus, "wood_dowel", 6, 2)
        # self.assemble_pal(lat2, jos, "wood_dowel", 6, 2)
        # self.assemble_pal(lat2, sus, "wood_dowel", 6, 2)

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

    cabinet = TopBox("test_cabinet", 720, 600, 500, RULES)

    print(cabinet.get_item_by_type_label("pal", "test_cabinet.jos").__getattribute__("label"))
    print(cabinet.get_item_by_type_label("pal","test_cabinet.jos").__getattribute__("position"))
    print(cabinet.get_item_by_type_label("pal","test_cabinet.jos").__getattribute__("drill_list"))
    print(cabinet.get_item_by_type_label("pal", "test_cabinet.lat1").__getattribute__("label"))
    print(cabinet.get_item_by_type_label("pal", "test_cabinet.lat1").__getattribute__("position"))
    print(cabinet.get_item_by_type_label("pal", "test_cabinet.lat1").__getattribute__("drill_list"))
    print(cabinet.get_item_by_type_label("pal", "test_cabinet.lat2").__getattribute__("label"))
    print(cabinet.get_item_by_type_label("pal", "test_cabinet.lat2").__getattribute__("position"))
    print(cabinet.get_item_by_type_label("pal", "test_cabinet.lat2").__getattribute__("drill_list"))
    print(cabinet.get_item_by_type_label("pal", "test_cabinet.sus").__getattribute__("label"))
    print(cabinet.get_item_by_type_label("pal", "test_cabinet.sus").__getattribute__("position"))
    print(cabinet.get_item_by_type_label("pal", "test_cabinet.sus").__getattribute__("drill_list"))
