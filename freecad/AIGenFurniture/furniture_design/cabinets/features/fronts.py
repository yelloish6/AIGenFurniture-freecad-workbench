# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
from ..elements.board import Front
from ..elements.accessory import Accessory
import ast, math

class FrontMixin:
    def add_front(self, split_list, front_type, reveal = None):
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

        default_reveal = self.front_gap
        if reveal is None:
            reveal = [default_reveal, default_reveal, default_reveal, default_reveal]

        r_left, r_top, r_right, r_bot = parse_split_list(reveal)

        h_tot = self.height - r_top - r_bot + self.front_gap
        h_count = 0
        w_count = 0
        w_tot = self.width - r_right - r_left + self.front_gap
        origin = [r_left, r_bot]
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
                origin[0] += usa.width + int(self.front_gap)
                w_count += split[1]
                if w_count == 100:
                    origin[0] = self.front_gap
                    w_count = 0
                    if h_count != 100:
                        origin[1] += usa.length + int(self.front_gap)
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

    def add_inset_front(self, split_list, front_type):
        """
        Inset front. Front sits inside the cabinet opening, reduced by
        front_gap + thick_front on every side, and recessed inward by
        thick_front along the Y axis.

        :param split_list: [[front1_%height, front1_%width], ...]
        :param front_type: "door" | "drawer" | "cover"
        :return: none
        """
        def parse_split_list(split_list):
            if isinstance(split_list, str):
                return ast.literal_eval(split_list)
            return split_list

        split_list = parse_split_list(split_list)

        gap = self.front_gap
        margin = gap + self.thick_front
        h_tot  = self.height - 2 * margin + gap
        w_tot  = self.width  - 2 * margin + gap
        origin = [margin, margin]
        origin_x0 = margin

        h_count = 0
        w_count = 0

        for i, split in enumerate(split_list):
            h = int((h_tot * split[0] / 100) - gap)
            w = int((w_tot * split[1] / 100) - gap)

            usa = Front(self.label + "_front" + str(i + 1), h, w, self.thick_front)
            usa.rotate("x")
            usa.rotate_cw("y")
            usa.move("x", origin[0])
            usa.move("z", origin[1])
            usa.move("x", usa.width)
            usa.move("y", self.thick_front)  # recess behind face plane

            if w_count != 100:
                origin[0] += usa.width + int(gap)
                w_count   += split[1]
                if w_count == 100:
                    origin[0] = origin_x0
                    w_count   = 0
                    if h_count != 100:
                        origin[1] += usa.length + int(gap)
                        h_count   += split[0]

            self.append(usa)
            if front_type == "door":
                if (h * w) > 280000:
                    self.append(Accessory("balama ingropata", 3))
                    self.append(Accessory("amortizor", 2))
                    self.append(Accessory("surub 3.5x16", 12))
                else:
                    self.append(Accessory("balama ingropata", 2))
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