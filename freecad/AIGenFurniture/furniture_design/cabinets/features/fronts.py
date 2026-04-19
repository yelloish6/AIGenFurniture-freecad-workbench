# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
from ..elements.board import Front
from ..elements.accessory import Accessory
import ast, math

class FrontMixin:
    def add_front(self, split_list, front_type):
        """

        :param split_list: [[front1_%height,front1_%width][front2_%height,front2_%width]]
        :param front_type: "door" "drawer" "cover"
        :return: none
        """
        def parse_split_list(split_list):
            if isinstance(split_list, str):
                return ast.literal_eval(split_list)
            return split_list

        split_list = parse_split_list(split_list)

        h_tot = self.height - self.front_gap
        h_count = 0
        w_count = 0
        w_tot = self.width - self.front_gap
        origin = [self.front_gap, self.front_gap]
        for i in range(len(split_list)):
            split = split_list[i]
            h = int((h_tot * split[0] / 100) - self.front_gap)
            w = int((w_tot * split[1] / 100) - self.front_gap)
            usa = Front(self.label + "_front" + str(i + 1), h, w, self.thick_front)
            usa.rotate("x")
            usa.rotate_cw("y")
            usa.move("x", origin[0])
            usa.move("z", origin[1])
            usa.move("x", usa.width)
            if w_count != 100:
                origin[0] += usa.width + int(self.front_gap / 2)
                w_count += split[1]
                if w_count == 100:
                    origin[0] = self.front_gap
                    w_count = 0
                    if h_count != 100:
                        origin[1] += usa.length + int(self.front_gap / 2)
                        h_count += split[0]

            self.append(usa)
            if front_type == "door":
                if (h * w) > 280000:
                    self.append(Accessory("balama aplicata", 3))
                    self.append(Accessory("amortizor", 2))
                    self.append(Accessory("surub 3.5x16", 12))
                else:
                    self.append(Accessory("balama aplicata", 2))
                    self.append(Accessory("amortizor", 1))
                    self.append(Accessory("surub 3.5x16", 8))
                self.append(Accessory("maner", 1))
            elif front_type == "cover":
                self.append(Accessory("surub intre corpuri", math.ceil(h * w / 40000)))
            elif front_type == "drawer":
                self.append(Accessory("maner", 1))


    def add_front_lateral(self, left_right):
        front = Front(self.label + ".fr_lat", self.height, self.depth + self.thick_front, self.thick_front)
        if left_right == "left":
            front.rotate_cw("y")
            front.move("y", -self.thick_front)
        elif left_right == "right":
            front.rotate_cw("y")
            front.move("x", self.width)
        self.append(front)


    def add_front_manual(self, height, width, offset_x, offset_z):
        fr = Front(self.label + ".front", height, width, self.thick_front)
        fr.rotate("x")
        fr.rotate_cw("y")
        fr.move("x", fr.width)
        fr.move("x", self.front_gap)
        # fr.move("z", self.front_gap)
        fr.move("x", offset_x)
        fr.move("z", offset_z)
        # fr.move("y", - self.thick_front)
        self.append(fr)
