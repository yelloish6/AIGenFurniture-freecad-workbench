# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
from AIGenFurniture.furniture_design.cabinets.architectures.base_box import BaseBox
from AIGenFurniture.furniture_design.cabinets.elements.board import BoardPal
# from AIGenFurniture.furniture_design.cabinets.assemblies import ASSEMBLIES

# ASSEMBLY_TYPE = "euro_screw"

# class SinkBox(BaseBox):
#     def __init__(self, label, height, width, depth, rules):
#         super().__init__(label, height, width, depth, rules)
#         self.remove_all_pfl()
#         # for i in self.getPFLOO():
#         #    if self.getPFLOO()[i].__getattribute__("label") == self.label + ".pfl":
#         #        self.getPFLOO().pop()
#         # self.getPFLOO().pop(self.getPFLOO()[0])
#         leg_width = 100
#         legatura = BoardPal(self.label + ".leg", self.width - (2 * self.thick_pal), leg_width, self.thick_pal,
#                             self.cant_lab, "", "", "")
#         legatura.rotate("x")
#         legatura.move("x", self.thick_pal)
#         legatura.move("z", self.thick_pal)
#         legatura.move("y", self.depth - self.thick_pal)
#         legatura.move("y", legatura.thick)
#         self.append(legatura)
#
#         leg1 = self.get_item_by_type_label("pal", self.label + ".leg1")
#         leg1.rotate("x")
#         leg1.move("y", leg1.thick)
#         leg1.move("z", self.thick_pal - leg1.width)
#
#         leg2 = self.get_item_by_type_label("pal", self.label + ".leg2")
#         leg2.rotate("x")
#         leg2.move("y", leg2.thick)
#         leg2.move("z", self.thick_pal - leg2.width)
#         leg2.move("y", leg2.width - self.thick_pal)

class SinkBox(BaseBox):
    def __init__(self, label, height, width, depth, rules):
        super().__init__(label, height, width, depth, rules)
        self.remove_all_pfl()

        leg_width = 100
        legatura = BoardPal(self.label + ".link", self.width - (2 * self.thick_pal), leg_width, self.thick_pal,
                            self.cant_lab, "", "", "")
        legatura.rotate("x")
        legatura.move("x", self.thick_pal)
        legatura.move("z", self.thick_pal)
        legatura.move("y", self.depth - self.thick_pal)
        legatura.move("y", self.thick_pal)
        self.append(legatura)

        # ASSEMBLIES[ASSEMBLY_TYPE](legatura, self.get_item_by_type_label("pal", self.label + ".lat1"))
        # ASSEMBLIES[ASSEMBLY_TYPE](legatura, self.get_item_by_type_label("pal", self.label + ".lat2"))
        # ASSEMBLIES[ASSEMBLY_TYPE](legatura, self.get_item_by_type_label("pal", self.label + ".jos"))

        leg1 = self.get_item_by_type_label("pal", self.label + ".top1")

        # reset all positioning
        leg1.position_list = []
        leg1.position = [leg1.length, leg1.width, leg1.thick, 0, 0, 0]

        # position the board
        leg1.rotate("x")
        leg1.move("x", self.thick_pal)
        leg1.move("z", self.height - leg1.width)
        # # leg1.move("y", self.height)
        # leg1.move("z", self.height - leg1.width)
        leg1.move("y", leg1.thick)
        # leg1.move("z", self.thick_pal - leg1.width)

        leg2 = self.get_item_by_type_label("pal", self.label + ".top2")
        # reset all positioning
        leg2.position_list = []
        leg2.position = [leg2.length, leg2.width, leg2.thick, 0, 0, 0]

        # position the board
        leg2.rotate("x")
        leg2.move("x", self.thick_pal)
        leg2. move("z", self.height - leg2.width)
        leg2.move("y", self.depth)
        # leg2.move("z", 3 * leg2.width - self.thick_pal)
        # # leg2.move("y", leg2.thick)
        # leg2.move("z", self.thick_pal - leg2.width)
        # leg2.move("y", leg2.width - self.thick_pal)

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

    print("=== Running SinkBox test scenario ===")

    cabinet = SinkBox("test_cabinet", 720, 600, 500, RULES)

    print(cabinet.get_item_by_type_label("pal", "test_cabinet.down").__getattribute__("label"))
    print(cabinet.get_item_by_type_label("pal","test_cabinet.down").__getattribute__("position"))
    print(cabinet.get_item_by_type_label("pal","test_cabinet.down").__getattribute__("drill_list"))
    print(cabinet.get_item_by_type_label("pal", "test_cabinet.lat_l").__getattribute__("label"))
    print(cabinet.get_item_by_type_label("pal", "test_cabinet.lat_l").__getattribute__("position"))
    print(cabinet.get_item_by_type_label("pal", "test_cabinet.lat_l").__getattribute__("drill_list"))
    print(cabinet.get_item_by_type_label("pal", "test_cabinet.lat_r").__getattribute__("label"))
    print(cabinet.get_item_by_type_label("pal", "test_cabinet.lat_r").__getattribute__("position"))
    print(cabinet.get_item_by_type_label("pal", "test_cabinet.lat_r").__getattribute__("drill_list"))
    print(cabinet.get_item_by_type_label("pal", "test_cabinet.top1").__getattribute__("label"))
    print(cabinet.get_item_by_type_label("pal", "test_cabinet.top1").__getattribute__("position"))
    print(cabinet.get_item_by_type_label("pal", "test_cabinet.top1").__getattribute__("drill_list"))
    print(cabinet.get_item_by_type_label("pal", "test_cabinet.top2").__getattribute__("label"))
    print(cabinet.get_item_by_type_label("pal", "test_cabinet.top2").__getattribute__("position"))
    print(cabinet.get_item_by_type_label("pal", "test_cabinet.top2").__getattribute__("drill_list"))
    print(cabinet.get_item_by_type_label("pal", "test_cabinet.link").__getattribute__("label"))
    print(cabinet.get_item_by_type_label("pal", "test_cabinet.link").__getattribute__("position"))
    print(cabinet.get_item_by_type_label("pal", "test_cabinet.link").__getattribute__("drill_list"))