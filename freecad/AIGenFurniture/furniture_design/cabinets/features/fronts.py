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

        default_reveal = self.front_clearance
        if reveal in (None, ""):
            reveal = [default_reveal, default_reveal, default_reveal, default_reveal]

        r_left, r_top, r_right, r_bot = parse_split_list(reveal)
        gap = float(self.front_gap)

        h_tot = self.height - r_top - r_bot + gap
        h_count = 0
        w_count = 0
        w_tot = self.width - r_right - r_left + gap
        origin_x0 = r_left
        origin = [origin_x0, r_bot]
        for i in range(len(split_list)):
            split = split_list[i]
            h = int((h_tot * split[0] / 100) - gap)
            w = int((w_tot * split[1] / 100) - gap)
            usa = Front(self.label + "_front" + str(i + 1), h, w, self.thick_front)
            usa.rotate("x")
            usa.rotate_cw("y")
            usa.move("x", origin[0])
            usa.move("z", origin[1])
            usa.move("x", usa.width)
            if w_count != 100:
                origin[0] += usa.width + int(gap)
                w_count += split[1]
                if w_count == 100:
                    origin[0] = origin_x0
                    w_count = 0
                    if h_count != 100:
                        origin[1] += usa.length + int(gap)
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

        gap = float(self.front_gap)
        clearance = float(self.front_clearance)
        h_tot  = self.height - (2 * self.thick_pal) - (2 * clearance) + gap
        w_tot  = self.width  - (2 * self.thick_pal) - (2 * clearance) + gap
        origin_x0 = self.thick_pal + clearance
        origin = [origin_x0, self.thick_pal + clearance]

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


    def add_tower_fronts(self, gap_list, front_list, base_offset_z=0, covered_height=None):
        """
        Add manual tower fronts over stacked openings.
        front_clearance controls outer cabinet clearance; front_gap controls only
        the visible gap between adjacent active fronts.
        """
        gaps = list(gap_list)
        fronts = list(front_list)
        if not fronts:
            return

        base_offset_z = float(base_offset_z)
        covered_height = float(covered_height if covered_height is not None else self.height - base_offset_z)
        gap = float(self.front_gap)
        clearance = float(self.front_clearance)
        thick = float(self.thick_pal)

        if len(gaps) < len(fronts):
            missing_gaps = len(fronts) - len(gaps)
            inferred_height = covered_height - sum(gaps) - ((len(fronts) + 1) * thick)
            inferred_gap = inferred_height / missing_gaps
            gaps.extend([inferred_gap] * missing_gaps)
        gaps = gaps[:len(fronts)]

        opening_bottoms = []
        cursor = base_offset_z + thick
        for opening_height in gaps:
            opening_bottoms.append(cursor)
            cursor += opening_height + thick

        front_width = self.width - (2 * clearance)
        offset_x = clearance - gap
        cover_top = base_offset_z + covered_height

        for i, has_front in enumerate(fronts):
            if not has_front:
                continue

            opening_bottom = opening_bottoms[i]
            opening_top = opening_bottom + gaps[i]

            below_has_front = i > 0 and fronts[i - 1] == 1
            above_has_front = i < len(fronts) - 1 and fronts[i + 1] == 1

            if below_has_front:
                bottom_edge = opening_bottom - (thick / 2) + (gap / 2)
            elif i == 0:
                bottom_edge = base_offset_z + clearance
            else:
                bottom_edge = opening_bottom - thick + clearance

            if above_has_front:
                top_edge = opening_top + (thick / 2) - (gap / 2)
            elif i == len(fronts) - 1:
                top_edge = cover_top - clearance
            else:
                top_edge = opening_top + thick - clearance

            front_height = top_edge - bottom_edge
            if front_height <= 0 or front_width <= 0:
                raise ValueError("Tower front dimensions must be positive.")

            self.add_front_manual(front_height, front_width, offset_x, bottom_edge)


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
