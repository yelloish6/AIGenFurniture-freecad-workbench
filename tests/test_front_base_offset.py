import json
import sys
import types
import unittest
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1] / "freecad" / "AIGenFurniture"
sys.path.insert(0, str(PACKAGE_ROOT))
sys.modules.setdefault("FreeCAD", types.SimpleNamespace())

from furniture_design.cabinets.architectures import (
    Banca, BaseBox, CorpCuPicioare, CorpDressing, TowerBox,
)


class FrontBaseOffsetTest(unittest.TestCase):
    def cabinets(self):
        rules = json.loads((PACKAGE_ROOT / "furniture_design/default_rules.json").read_text())
        args = ("test", 2000, 600, 600, rules)
        return [
            (BaseBox(*args), 0),
            (TowerBox(*args, gap_list=[0], front_list=[0]), 0),
            (CorpDressing(*args, gap_list=[0], front_list=[0]), 100),
            (CorpCuPicioare(*args, h_skirt=120, has_skirting_board=True), 120),
            (CorpCuPicioare(*args, h_skirt=120, has_skirting_board=False), 120),
            (Banca(*args, height_base=150), 150),
        ]

    def test_overlay_full_split_and_custom_reveal(self):
        for split in ([[100, 100]], [[50, 100], [50, 100]], [[100, 50], [100, 50]]):
            for reveal in (None, [3, 4, 5, 6]):
                for cabinet, base in self.cabinets():
                    with self.subTest(cabinet=type(cabinet).__name__, base=base,
                                      split=split, reveal=reveal):
                        cabinet.add_front(split, "door", reveal)
                        fronts = cabinet.get_element_list_by_type("front")
                        left, top, right, bottom = reveal or [2, 2, 2, 2]
                        self.assertEqual(cabinet.front_base_offset, base)
                        self.assertEqual(len(fronts), len(split))
                        self.assertEqual(min(f.position[5] for f in fronts), base + bottom)
                        self.assertEqual(max(f.position[5] + f.length for f in fronts), 2000 - top)
                        for front, (height_percent, width_percent) in zip(fronts, split):
                            self.assertEqual(front.length, int((2000 - base - top - bottom + 2) * height_percent / 100 - 2))
                            self.assertEqual(front.width, int((600 - left - right + 2) * width_percent / 100 - 2))

    def test_inset_full_and_split(self):
        for split in ([[100, 100]], [[50, 100], [50, 100]]):
            for cabinet, base in self.cabinets():
                with self.subTest(cabinet=type(cabinet).__name__, base=base, split=split):
                    cabinet.add_inset_front(split, "door")
                    fronts = cabinet.get_element_list_by_type("front")
                    self.assertEqual(len(fronts), len(split))
                    self.assertEqual(min(f.position[5] for f in fronts), base + 20)
                    self.assertEqual(max(f.position[5] + f.length for f in fronts), 1980)
                    self.assertTrue(all(f.width == 560 for f in fronts))


if __name__ == "__main__":
    unittest.main()
