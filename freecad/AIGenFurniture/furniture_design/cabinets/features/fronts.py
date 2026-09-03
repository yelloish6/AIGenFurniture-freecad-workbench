# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
from ..elements.board import Front
from ..elements.accessory import Accessory
import ast, math


def validate_tower_opening_layout(gap_list, front_list, covered_height, board_thickness):
    """
    Validate and normalize the tower opening/front schema.

    gap_list contains explicitly dimensioned openings ordered bottom to top.
    The final top opening is calculated from the remaining covered height.
    """
    if gap_list is None:
        raise ValueError("gap_list must be a sequence of positive numeric explicit opening heights.")
    if front_list is None:
        raise ValueError(
            "front_list must be a non-empty sequence of 0/1 values with len(front_list) == len(gap_list) + 1."
        )
    if isinstance(gap_list, (str, bytes)):
        raise ValueError("gap_list must be a sequence of positive numeric explicit opening heights, not a string.")
    if isinstance(front_list, (str, bytes)):
        raise ValueError(
            "front_list must be a non-empty sequence of 0/1 values, not a string; expected len(front_list) == len(gap_list) + 1."
        )

    try:
        gaps_in = list(gap_list)
    except TypeError as exc:
        raise ValueError("gap_list must be a sequence of positive numeric explicit opening heights.") from exc

    try:
        fronts_in = list(front_list)
    except TypeError as exc:
        raise ValueError(
            "front_list must be a non-empty sequence of 0/1 values with len(front_list) == len(gap_list) + 1."
        ) from exc

    if not fronts_in:
        raise ValueError("front_list must be non-empty; expected len(front_list) == len(gap_list) + 1.")

    try:
        covered_height = float(covered_height)
    except (TypeError, ValueError) as exc:
        raise ValueError("covered_height must be numeric and large enough to leave a positive final opening.") from exc
    try:
        board_thickness = float(board_thickness)
    except (TypeError, ValueError) as exc:
        raise ValueError("board_thickness must be numeric and positive.") from exc
    if board_thickness <= 0:
        raise ValueError("board_thickness must be positive.")

    normalized_gaps = []
    for index, gap in enumerate(gaps_in):
        if isinstance(gap, (str, bytes, bool)) or gap is None:
            raise ValueError(f"gap_list[{index}] must be a positive numeric explicit opening height.")
        try:
            normalized_gap = float(gap)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"gap_list[{index}] must be a positive numeric explicit opening height.") from exc
        if normalized_gap <= 0:
            raise ValueError(f"gap_list[{index}] must be strictly positive.")
        normalized_gaps.append(normalized_gap)

    normalized_fronts = []
    for index, front in enumerate(fronts_in):
        if not (front is False or front is True or (type(front) is int and front in (0, 1))):
            raise ValueError(
                f"front_list[{index}] must be one of 0, 1, False or True; expected len(front_list) == len(gap_list) + 1."
            )
        normalized_fronts.append(1 if bool(front) else 0)

    expected_front_count = len(normalized_gaps) + 1
    if len(normalized_fronts) != expected_front_count:
        raise ValueError(
            "front_list length must equal len(gap_list) + 1; "
            f"got len(front_list)={len(normalized_fronts)} and len(gap_list)={len(normalized_gaps)}."
        )

    final_opening_height = (
        covered_height
        - sum(normalized_gaps)
        - ((len(normalized_fronts) + 1) * board_thickness)
    )
    if final_opening_height <= 0:
        raise ValueError(
            "covered_height must leave a strictly positive calculated final opening; "
            "expected covered_height - sum(gap_list) - ((len(front_list) + 1) * board_thickness) > 0."
        )

    return normalized_gaps + [final_opening_height], normalized_fronts


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
            usa = Front(self.label + ".front_" + str(i + 1), h, w, self.thick_front)
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

            usa = Front(self.label + ".front_" + str(i + 1), h, w, self.thick_front)
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
        front = Front(self.label + (".left_side_front" if left_right == "left" else ".right_side_front"), self.height, self.depth + self.thick_front, self.thick_front)
        if left_right == "left":
            front.rotate_cw("y")
            front.move("y", -self.thick_front)
        elif left_right == "right":
            front.rotate_cw("y")
            front.move("x", self.width)
        self.append(front)


    def add_tower_fronts(self, opening_heights, front_list, base_offset_z=0, covered_height=None):
        """
        Add manual tower fronts over stacked openings.
        opening_heights must already include the calculated final/top opening.
        front_clearance controls outer cabinet clearance; front_gap controls only
        the visible gap between adjacent active fronts.
        """
        base_offset_z = float(base_offset_z)
        covered_height = float(covered_height if covered_height is not None else self.height - base_offset_z)
        gap = float(self.front_gap)
        clearance = float(self.front_clearance)
        thick = float(self.thick_pal)
        openings = list(opening_heights)
        fronts = list(front_list)

        if len(openings) != len(fronts):
            raise ValueError(
                "opening_heights length must equal front_list length; use validate_tower_opening_layout first."
            )

        opening_bottoms = []
        cursor = base_offset_z + thick
        for opening_height in openings:
            opening_bottoms.append(cursor)
            cursor += opening_height + thick

        front_width = self.width - (2 * clearance)
        offset_x = clearance - gap
        cover_top = base_offset_z + covered_height

        for i, has_front in enumerate(fronts):
            if not has_front:
                continue

            opening_bottom = opening_bottoms[i]
            opening_top = opening_bottom + openings[i]

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
                raise ValueError("Tall Cabinet front dimensions must be positive.")

            self.add_front_manual(front_height, front_width, offset_x, bottom_edge)


    def add_front_manual(self, height, width, offset_x, offset_z):
        front_number = 1 + sum(
            1 for element in self.elements_list
            if getattr(element, "type", None) == "front" and getattr(element, "label", "").startswith(self.label + ".front_")
        )
        fr = Front(self.label + ".front_" + str(front_number), height, width, self.thick_front)
        fr.rotate("x")
        fr.rotate_cw("y")
        fr.move("x", fr.width)
        fr.move("x", self.front_gap)
        # fr.move("z", self.front_gap)
        fr.move("x", offset_x)
        fr.move("z", offset_z)
        # fr.move("y", - self.thick_front)
        self.append(fr)
