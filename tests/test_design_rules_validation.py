import copy
import json
import math
import sys
import tempfile
import types
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))


class FakeConsole:
    def __init__(self):
        self.warnings = []

    def PrintWarning(self, message):
        self.warnings.append(message)


fake_console = FakeConsole()
fake_freecad = types.SimpleNamespace(
    Console=fake_console,
    getUserAppDataDir=lambda: tempfile.gettempdir(),
)

_previous_freecad_module = sys.modules.get("FreeCAD")
sys.modules["FreeCAD"] = fake_freecad
from freecad.AIGenFurniture.furniture_design import design_engine  # noqa: E402
from freecad.AIGenFurniture.furniture_design.design_engine import (  # noqa: E402
    DESIGN_RULE_LABELS,
    NON_NEGATIVE_DESIGN_RULE_KEYS,
    POSITIVE_DESIGN_RULE_KEYS,
    DesignRulesValidationError,
    load_default_rules,
    load_factory_rules,
    save_default_rules,
    validate_design_rules,
)
if _previous_freecad_module is None:
    del sys.modules["FreeCAD"]
else:
    sys.modules["FreeCAD"] = _previous_freecad_module


def valid_rules():
    return copy.deepcopy(design_engine.DEFAULT_RULES_BASELINE)


class DesignRulesValidationTest(unittest.TestCase):
    def setUp(self):
        self._old_freecad = design_engine.FreeCAD
        design_engine.FreeCAD = fake_freecad
        fake_console.warnings.clear()

    def tearDown(self):
        design_engine.FreeCAD = self._old_freecad

    def assert_invalid(self, rules):
        with self.assertRaises(DesignRulesValidationError) as cm:
            validate_design_rules(rules)
        return cm.exception.errors

    def test_factory_defaults_are_valid(self):
        self.assertEqual(load_factory_rules(), valid_rules())

    def test_positive_only_fields_reject_zero_and_negative_values(self):
        for key in POSITIVE_DESIGN_RULE_KEYS:
            for value in (0, -1):
                with self.subTest(key=key, value=value):
                    rules = valid_rules()
                    rules[key] = value

                    errors = self.assert_invalid(rules)

                    self.assertTrue(any(DESIGN_RULE_LABELS[key] in error for error in errors))
                    self.assertTrue(any(repr(value) in error for error in errors))

    def test_non_negative_fields_accept_zero_and_reject_negative_values(self):
        for key in NON_NEGATIVE_DESIGN_RULE_KEYS:
            with self.subTest(key=key, value=0):
                rules = valid_rules()
                rules[key] = 0
                self.assertEqual(validate_design_rules(rules)[key], 0)

            with self.subTest(key=key, value=-1):
                rules = valid_rules()
                rules[key] = -1

                errors = self.assert_invalid(rules)

                self.assertTrue(any(DESIGN_RULE_LABELS[key] in error for error in errors))
                self.assertTrue(any("-1" in error for error in errors))

    def test_missing_required_keys_are_reported(self):
        errors = self.assert_invalid({})

        self.assertGreaterEqual(len(errors), len(design_engine.REQUIRED_DESIGN_RULE_KEYS))
        self.assertTrue(any("Chipboard thickness is required" in error for error in errors))
        self.assertTrue(any("Default cabinet depth is required" in error for error in errors))

    def test_boolean_string_nan_and_infinity_values_are_rejected(self):
        invalid_values = (True, False, "18", float("nan"), float("inf"), float("-inf"))
        for value in invalid_values:
            with self.subTest(value=repr(value)):
                rules = valid_rules()
                rules["thick_pal"] = value

                errors = self.assert_invalid(rules)

                self.assertTrue(any("Chipboard thickness" in error for error in errors))
                self.assertTrue(any(repr(value) in error for error in errors))

    def test_multiple_invalid_fields_produce_multiple_errors(self):
        rules = valid_rules()
        rules["thick_pal"] = 0
        rules["general_width"] = "wide"
        rules["pol_depth"] = -1

        errors = self.assert_invalid(rules)

        self.assertGreaterEqual(len(errors), 3)
        self.assertTrue(any("Chipboard thickness" in error for error in errors))
        self.assertTrue(any("Default cabinet width" in error for error in errors))
        self.assertTrue(any("Shelf setback from front" in error for error in errors))

    def test_relational_constraints_are_enforced_at_boundaries(self):
        cases = (
            ("height_legs", "general_height", "Plinth height"),
            ("pol_depth", "general_depth", "Shelf setback from front"),
            ("front_clearance", "general_width", "positive front width"),
            ("front_clearance", "general_height", "positive front height"),
            ("thick_pal", "general_width", "internal cabinet width"),
            ("thick_pal", "general_height", "internal cabinet height"),
            ("cant_general", "general_depth", "General edge-band thickness"),
        )

        for changed_key, boundary_key, expected in cases:
            with self.subTest(changed_key=changed_key, boundary_key=boundary_key):
                rules = valid_rules()
                if changed_key in ("front_clearance", "thick_pal"):
                    rules[changed_key] = rules[boundary_key] / 2
                else:
                    rules[changed_key] = rules[boundary_key]

                errors = self.assert_invalid(rules)

                self.assertTrue(any(expected in error for error in errors), errors)

    def test_valid_user_configuration_loads_successfully(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            self.use_temp_freecad_dir(temp_dir)
            rules = valid_rules()
            rules["general_width"] = 700
            rules_path = Path(temp_dir) / "AIGenFurniture" / "design_rules.json"
            rules_path.parent.mkdir()
            rules_path.write_text(json.dumps(rules), encoding="utf-8")

            loaded = load_default_rules()

            self.assertEqual(loaded["general_width"], 700)

    def test_invalid_user_json_falls_back_to_factory_defaults_with_warning(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            self.use_temp_freecad_dir(temp_dir)
            fake_console.warnings.clear()
            rules_path = Path(temp_dir) / "AIGenFurniture" / "design_rules.json"
            rules_path.parent.mkdir()
            rules_path.write_text("{not json", encoding="utf-8")

            loaded = load_default_rules()

            self.assertEqual(loaded, load_factory_rules())
            self.assertTrue(fake_console.warnings)
            self.assertIn("Using factory defaults", fake_console.warnings[-1])
            self.assertEqual(rules_path.read_text(encoding="utf-8"), "{not json")

    def test_saving_invalid_rules_does_not_replace_existing_valid_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_file = Path(temp_dir) / "design_rules.json"
            existing = valid_rules()
            existing["general_width"] = 800
            output_file.write_text(json.dumps(existing, indent=4) + "\n", encoding="utf-8")

            invalid = valid_rules()
            invalid["general_width"] = math.inf
            with self.assertRaises(DesignRulesValidationError):
                save_default_rules(invalid, str(output_file))

            self.assertEqual(json.loads(output_file.read_text(encoding="utf-8")), existing)

    def test_deprecated_keys_are_migrated_before_validation(self):
        rules = valid_rules()
        rules.pop("general_depth")
        rules.pop("front_clearance")
        rules["width_blat"] = 640

        migrated = validate_design_rules(rules)

        self.assertEqual(migrated["general_depth"], 640)
        self.assertEqual(migrated["front_clearance"], rules["gap_front"])
        self.assertNotIn("width_blat", migrated)

    def test_existing_valid_design_rules_persistence_behavior_remains_intact(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_file = Path(temp_dir) / "design_rules.json"
            rules = valid_rules()
            rules["general_width"] = 650
            rules["gap_front"] = 3

            save_default_rules(rules, str(output_file))
            loaded = load_default_rules(str(output_file))

            self.assertEqual(loaded["general_width"], 650)
            self.assertEqual(loaded["gap_front"], 3)

    def use_temp_freecad_dir(self, temp_dir):
        fake_freecad.getUserAppDataDir = lambda: temp_dir
        design_engine.FreeCAD = fake_freecad


if __name__ == "__main__":
    unittest.main()
