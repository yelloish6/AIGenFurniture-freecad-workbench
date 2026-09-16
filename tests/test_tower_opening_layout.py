import itertools
import json
import sys
import types
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = REPO_ROOT / "freecad" / "AIGenFurniture"
sys.path.insert(0, str(PACKAGE_ROOT))

sys.modules.setdefault("FreeCAD", types.SimpleNamespace())

from furniture_design.cabinets.features.fronts import (  # noqa: E402
    FrontMixin,
    validate_tower_opening_layout,
)
from furniture_design.cabinets.architectures import (  # noqa: E402
    make_tower_box,
    make_corp_dressing,
)


class TowerOpeningLayoutTest(unittest.TestCase):
    def test_no_separator_schema(self):
        for gaps in ([0], [0.0], []):
            for flag in (0, 1, False, True):
                with self.subTest(gaps=gaps, flag=flag):
                    self.assertEqual(
                        validate_tower_opening_layout(gaps, [flag], 1000, 18),
                        ([964.0], [int(flag)]),
                    )

    def test_zero_sentinel_requires_one_front_flag(self):
        with self.assertRaisesRegex(ValueError, "1 when gap_list is \\[0\\]"):
            validate_tower_opening_layout([0], [1, 0], 1000, 18)

    def test_valid_default_schema(self):
        openings, fronts = validate_tower_opening_layout([200, 400], [0, 0, 0], 1000, 18)

        self.assertEqual(openings, [200.0, 400.0, 328.0])
        self.assertEqual(fronts, [0, 0, 0])

    def test_length_mismatch(self):
        with self.assertRaisesRegex(ValueError, "front_list length.*len\\(gap_list\\) \\+ 1"):
            validate_tower_opening_layout([200, 400], [0, 0, 0, 0], 1000, 18)

    def test_empty_front_list(self):
        with self.assertRaisesRegex(ValueError, "front_list.*non-empty"):
            validate_tower_opening_layout([200, 400], [], 1000, 18)

    def test_zero_and_negative_gaps(self):
        for gap in (0, -1):
            with self.subTest(gap=gap):
                with self.assertRaisesRegex(ValueError, "gap_list\\[0\\].*strictly positive"):
                    validate_tower_opening_layout([gap, 400], [0, 0, 0], 1000, 18)

    def test_invalid_front_values(self):
        for value in (2, -1, "1", None, 0.0, 1.0):
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, "front_list\\[1\\].*0, 1, False or True"):
                    validate_tower_opening_layout([200, 400], [0, value, 0], 1000, 18)

    def test_zero_or_negative_remaining_height(self):
        for covered_height in (672, 671):
            with self.subTest(covered_height=covered_height):
                with self.assertRaisesRegex(ValueError, "covered_height.*final opening"):
                    validate_tower_opening_layout([200, 400], [0, 0, 0], covered_height, 18)

    def test_plinth_leaving_insufficient_covered_height(self):
        total_height = 750
        plinth_height = 78
        with self.assertRaisesRegex(ValueError, "covered_height.*final opening"):
            validate_tower_opening_layout(
                [200, 400],
                [0, 0, 0],
                total_height - plinth_height,
                18,
            )

    def test_calculated_final_opening(self):
        openings, fronts = validate_tower_opening_layout([200, 400], [True, False, 1], 2200, 18)

        self.assertEqual(openings[-1], 1528.0)
        self.assertEqual(fronts, [1, 0, 1])

    def test_inputs_are_not_mutated(self):
        gaps = [200, 400]
        fronts = [True, False, 1]

        validate_tower_opening_layout(gaps, fronts, 2200, 18)

        self.assertEqual(gaps, [200, 400])
        self.assertEqual(fronts, [True, False, 1])

    def test_rejects_none_strings_malformed_sequences_and_non_numeric_gaps(self):
        invalid_inputs = [
            (None, [0, 0, 0], "gap_list"),
            ("[200, 400]", [0, 0, 0], "gap_list"),
            ([200, 400], None, "front_list"),
            ([200, 400], "000", "front_list"),
            (123, [0, 0, 0], "gap_list"),
            ([200, object()], [0, 0, 0], "gap_list\\[1\\]"),
            ([True, 400], [0, 0, 0], "gap_list\\[0\\]"),
        ]

        for gaps, fronts, message in invalid_inputs:
            with self.subTest(gaps=gaps, fronts=fronts):
                with self.assertRaisesRegex(ValueError, message):
                    validate_tower_opening_layout(gaps, fronts, 2200, 18)


class TowerFrontHarness(FrontMixin):
    def __init__(self):
        self.label = "tower"
        self.height = 1000
        self.width = 600
        self.thick_pal = 18
        self.front_gap = 4
        self.front_clearance = 2
        self.fronts = []

    def add_front_manual(self, height, width, offset_x, offset_z):
        self.fronts.append((height, width, offset_x, offset_z))


class TowerFrontGenerationTest(unittest.TestCase):
    def test_full_height_front(self):
        for flag in (0, 1):
            cabinet = TowerFrontHarness()
            openings, fronts = validate_tower_opening_layout([0], [flag], 1000, 18)
            cabinet.add_tower_fronts(openings, fronts, covered_height=1000)
            self.assertEqual(cabinet.fronts, [(996.0, 596.0, -2.0, 2.0)] if flag else [])

    def test_all_three_opening_front_combinations(self):
        opening_heights, _fronts = validate_tower_opening_layout([200, 400], [0, 0, 0], 1000, 18)

        for combo in itertools.product((0, 1), repeat=3):
            with self.subTest(combo=combo):
                cabinet = TowerFrontHarness()

                cabinet.add_tower_fronts(opening_heights, list(combo), covered_height=1000)

                self.assertEqual(len(cabinet.fronts), sum(combo))
                for height, width, _offset_x, _offset_z in cabinet.fronts:
                    self.assertGreater(height, 0)
                    self.assertGreater(width, 0)

    def test_add_tower_fronts_does_not_truncate_mismatched_lists(self):
        cabinet = TowerFrontHarness()

        with self.assertRaisesRegex(ValueError, "opening_heights length must equal front_list length"):
            cabinet.add_tower_fronts([200, 400], [1, 1, 1], covered_height=1000)


class CabinetOpeningIntegrationTest(unittest.TestCase):
    def test_both_architecture_factories(self):
        rules = json.loads((PACKAGE_ROOT / "furniture_design/default_rules.json").read_text())
        for factory in (make_tower_box, make_corp_dressing):
            for gaps, flags in (([0], [0]), ([0], [1]), ([200, 400], [1, 0, 1])):
                with self.subTest(factory=factory.__name__, gaps=gaps, flags=flags):
                    cabinet = factory("test", 1000, 600, 600, rules,
                                      box={"gap_list": gaps, "front_list": flags})
                    separators = [e for e in cabinet.elements_list
                                  if ".horizontal_separator_" in e.label]
                    fronts = cabinet.get_element_list_by_type("front")
                    self.assertEqual(len(separators), 0 if gaps == [0] else len(gaps))
                    self.assertEqual(len(fronts), sum(flags))
                    if gaps == [0] and flags == [1]:
                        base = rules["height_legs"] if factory is make_corp_dressing else 0
                        self.assertEqual(fronts[0].length, 1000 - base - 2 * rules["front_clearance"])


if __name__ == "__main__":
    unittest.main()
