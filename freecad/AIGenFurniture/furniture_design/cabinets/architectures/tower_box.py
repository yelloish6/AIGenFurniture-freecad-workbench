# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
import math

from ..cabinet import Cabinet
from ..elements.accessory import Accessory
from ..elements.board import BoardPal
from ..features.fronts import validate_tower_opening_layout

class TowerBox(Cabinet):
    def __init__(self, label, height, width, depth, rules, gap_list=None, gap_heat=50, front_list=None):
        """

        :param label:
        :param height:
        :param width:
        :param depth:
        :param rules:
        :param gap_list: intaltimea gap-urilor de jos in sus. Ultimul gap e cat ramane (ex:[gen_h_base - 2 * t1.pal_width,300, gen_h_tower - gen_h_base - 318 - gen_h_top])
        :param gap_heat: distanta in spate cat sunt mai in interior politele fata de lateriale ca sa permita evacuarea cladurii
        :param front_list: care gap-uri au front (ex. [0, 0, 0, 1])
        """
        super().__init__(label, height, width, depth, rules)
        if gap_list is None:
            gap_list = [200, 400]
        if front_list is None:
            front_list = [0, 0, 0]
        opening_heights, front_flags = validate_tower_opening_layout(
            gap_list,
            front_list,
            covered_height=self.height,
            board_thickness=self.thick_pal,
        )
        self.depth = self.depth - gap_heat
        jos = BoardPal(self.label + ".down", self.width, self.depth, self.thick_pal, self.cant_lab, "", self.cant_lab,
                       self.cant_lab)
        self.append(jos)

        lat1 = BoardPal(self.label + ".lat_l", self.height - self.thick_pal, self.depth + gap_heat, self.thick_pal,
                        self.cant_lab, "", self.cant_lab, "")
        lat1.rotate_cw("y")
        lat1.move("z", jos.thick)
        lat1.move("x", self.thick_pal)
        self.append(lat1)

        lat2 = BoardPal(self.label + ".lat_r", self.height - self.thick_pal, self.depth + gap_heat, self.thick_pal,
                        self.cant_lab, "", self.cant_lab, "")
        lat2.rotate_cw("y")
        lat2.move("z", jos.thick)
        lat2.move("x", jos.length)
        self.append(lat2)

        sus = BoardPal(self.label + ".up", self.width - (2 * self.thick_pal), self.depth - (self.cant),
                       self.thick_pal, self.cant_lab, "", "", "")
        sus.move("x", lat1.thick)
        sus.move("z", lat1.length)
        self.append(sus)

        # adding horizontal separators
        boundary_z = self.thick_pal
        for opening_height in opening_heights[:-1]:
            boundary_z += opening_height
            self.add_sep_h(self.width - 2 * self.thick_pal, 0, boundary_z - self.thick_pal, self.cant_lab)
            boundary_z += self.thick_pal
        # self.addSepH(self.width - 2 * self.thick_pal, 0, gap_list[0], self.cant_lab)
        # self.addSepH(self.width - 2 * self.thick_pal, 0, gap_list[0] + gap_list[1] + self.thick_pal, self.cant_lab)
        # self.addSepH(self.width - 2 * self.thick_pal, 0, gap_list[0] + gap_list[1] + gap_list[2] + (2 * self.thick_pal),
        #              self.cant_lab)
        self.append(Accessory("surub", 8))
        self.append(Accessory("plinta", self.width / 1000))
        picioare = math.ceil(self.width / 400) * 2
        self.append(Accessory("picioare", picioare))
        self.append(Accessory("clema plinta", picioare / 2))
        self.append(Accessory("surub 3.5x16", picioare * 4))  # pentru picioare

        self.add_pfl()
        if gap_heat > 0:
            self.get_item_by_type_label("pfl",self.label + ".hdf").__setattr__("length", self.width - (2 * self.thick_pal))
            self.get_item_by_type_label("pfl",self.label + ".hdf").move("x", self.thick_pal - 2)
        self.add_tower_fronts(opening_heights, front_flags)

        # if front_list[0] == 1:
        #     if front_list[1] == 0:
        #         self.add_front_manual(gap_list[0] + (2 * self.thick_pal) - 4, self.width - 4, 0, 0)
        #         if front_list[2] == 0:
        #
        #         elif front_list[2] == 1:
        #     elif front_list[1] == 1:
        #         self.add_front_manual(gap_list[0] + (1.5 * self.thick_pal) - 3, self.width - 4, 0, 0)

        # # Setting the front doors for the tower
        # fg = rules["gap_front"]
        # # gap_list[0]
        # if (front_list[0] == 1) and (front_list[1] == 0):
        #     # door down but not above
        #     self.add_front_manual(gap_list[0] + (self.thick_pal - fg) * 2, self.width - (2 * fg), 0, 0)
        # if (front_list[0] == 1) and (front_list[1] == 1):
        #     # door down and above
        #     self.add_front_manual(gap_list[0] + (self.thick_pal - fg) * 1.5, self.width - (2 * fg), 0, 0)
        #
        # # gap_list[1]
        # if (front_list[1] == 1) and (front_list[0] == 0) and (front_list[2] == 0):
        #     self.add_front_manual(gap_list[1] + (self.thick_pal - fg) * 2 , self.width - (2 * fg), 0,
        #                           gap_list[0] + self.thick_pal)
        # if (((front_list[1] == 1) and (front_list[0] == 1) and (front_list[2] == 0))
        #         or ((front_list[1] == 1) and (front_list[0] == 0) and (front_list[2] == 1))):
        #     self.add_front_manual(gap_list[1] + (1.5 * (self.thick_pal - fg)), self.width - (2 * fg), 0,
        #                           gap_list[0] + (self.thick_pal / 2))
        # if (front_list[1] == 1) and (front_list[0] == 1) and (front_list[2] == 1):
        #     self.add_front_manual(gap_list[1] + self.thick_pal - fg, self.width - 4, 0,
        #                           gap_list[0] + (self.thick_pal - fg) * 1.5 + fg)
        #
        # # gap_list[2]
        # if (front_list[2] == 1) and (front_list[1] == 0) and (front_list[3] == 0):
        #     self.add_front_manual(gap_list[2] + (2 * (self.thick_pal - fg)), self.width - (2 * fg), 0,
        #                           gap_list[0] + self.thick_pal + gap_list[1] + self.thick_pal)
        # if (((front_list[2] == 1) and (front_list[1] == 1) and (front_list[3] == 0))
        #         or ((front_list[2] == 1) and (front_list[1] == 0) and (front_list[3] == 1))):
        #     self.add_front_manual(gap_list[2] + (1.5 * (self.thick_pal - fg)), self.width - (2 * fg), 0,
        #                           gap_list[0] + 2 * self.thick_pal + gap_list[1])
        # if (front_list[2] == 1) and (front_list[1] == 1) and (front_list[3] == 1):
        #     self.add_front_manual(gap_list[2] + self.thick_pal - fg, self.width - 4, 0,
        #                           gap_list[0] + (self.thick_pal - fg) * 1.5 + fg +
        #                           gap_list[1] + self.thick_pal - fg + fg)
        #
        # # gap_list[3]
        # if (front_list[3] == 1) and (front_list[2] == 0):
        #     self.add_front_manual(self.height - gap_list[0] - gap_list[1] - gap_list[2] - (3 * (self.thick_pal - fg)),
        #                           self.width - (2 * fg), 0,
        #                           gap_list[0] + gap_list[1] + gap_list[2] + (3 * self.thick_pal) + fg)
        # if (front_list[3] == 1) and (front_list[2] == 1):
        #     self.add_front_manual(self.height - gap_list[0] - gap_list[1] - gap_list[2] - (3.5 * self.thick_pal) - 3,
        #                           self.width - 4, 0,
        #                           gap_list[0] + (self.thick_pal - fg) * 1.5 + fg +
        #                           gap_list[1] + self.thick_pal - fg + fg +
        #                           gap_list[2] + self.thick_pal - fg + fg)
