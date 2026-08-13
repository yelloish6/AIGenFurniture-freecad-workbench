# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
from ..elements.accessory import *
from ..elements.board import *
from ..cabinet import Cabinet
from ..features.fronts import validate_tower_opening_layout

import math

class CorpDressing(Cabinet):
    def __init__(self, label, height, width, depth, rules, gap_list=None, front_list=None):
        """

        :param label:
        :param height:
        :param width:
        :param depth:
        :param rules:
        :param gap_list: intaltimea gap-urilor de jos in sus. Ultimul gap e cat ramane (ex:[gen_h_base - 2 * t1.pal_width,300, gen_h_tower - gen_h_base - 318 - gen_h_top])
        :param front_list: care gap-uri au front (ex. [0, 0, 0, 1])
        """
        super().__init__(label, height, width, depth, rules)
        if gap_list is None:
            gap_list = [200, 400]
        if front_list is None:
            front_list = [0, 0, 0]
        plinth_height = rules["height_legs"]
        covered_height = self.height - plinth_height
        opening_heights, front_flags = validate_tower_opening_layout(
            gap_list,
            front_list,
            covered_height=covered_height,
            board_thickness=self.thick_pal,
        )

        jos = BoardPal(self.label + ".jos", self.width - (2 * self.thick_pal), self.depth, self.thick_pal, self.cant_lab, "",
                       self.cant_lab, self.cant_lab)
        jos.move("x", self.thick_pal)
        jos.move("z", rules["height_legs"])
        self.append(jos)

        lat1 = BoardPal(self.label + ".lat", self.height, self.depth, self.thick_pal,
                        self.cant_lab, "", self.cant_lab, "")
        lat1.rotate_cw("y")
        lat1.move("x", self.thick_pal)
        self.append(lat1)

        lat2 = BoardPal(self.label + ".lat", self.height, self.depth, self.thick_pal,
                        self.cant_lab, "", self.cant_lab, "")
        lat2.rotate_cw("y")
        lat2.move("x", self.width)
        self.append(lat2)

        sus = BoardPal(self.label + ".sus", self.width - (2 * self.thick_pal), self.depth - self.cant,
                       self.thick_pal, self.cant_lab, "", "", "")
        sus.move("x", lat1.thick)
        sus.move("z", lat1.length - self.thick_pal)
        self.append(sus)

        plinta = BoardPal(self.label + ".plinta", self.width - (2 * self.thick_pal), rules["height_legs"],
                          self.thick_pal, self.cant_lab, "", "", "")
        plinta.rotate("x")
        plinta.move("x", self.thick_pal)
        plinta.move("y", self.thick_pal)
        self.append(plinta)

        # adding horizontal separators
        boundary_z = plinth_height + self.thick_pal
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

        self.add_tower_fronts(
            opening_heights,
            front_flags,
            base_offset_z=plinth_height,
            covered_height=covered_height,
        )
