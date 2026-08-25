import importlib
import sys
import types
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))


REMOVED_MANUFACTURING_PATHS = [
    "freecad/AIGenFurniture/manufacturing/export_for_proficut.py",
    "freecad/AIGenFurniture/manufacturing/export_for_nettfront.py",
    "freecad/AIGenFurniture/manufacturing/generate_offer_cost.py",
    "freecad/AIGenFurniture/manufacturing/generate_assembly_file.py",
    "freecad/AIGenFurniture/manufacturing/generate_assembly_file_reportlab.py",
    "freecad/AIGenFurniture/manufacturing/templates/Cote-Proficut-2018.xlsx",
    "freecad/AIGenFurniture/manufacturing/templates/Formular_de_comanda_nett_front.xlsx",
]


class CommunityExportBoundaryTest(unittest.TestCase):
    def setUp(self):
        self.manufacturing = importlib.import_module("freecad.AIGenFurniture.manufacturing")
        self.original_definitions = dict(self.manufacturing.EXPORT_DEFINITIONS)

    def tearDown(self):
        self.manufacturing.EXPORT_DEFINITIONS.clear()
        self.manufacturing.EXPORT_DEFINITIONS.update(self.original_definitions)

    def test_community_exports_are_exactly_csv_and_stl(self):
        self.assertEqual(
            set(self.manufacturing.EXPORT_DEFINITIONS),
            {"export_csv", "export_stl"},
        )

    def test_community_exports_are_active_with_expected_modules_and_context(self):
        self.assertEqual(
            self.manufacturing.EXPORT_DEFINITIONS["export_csv"],
            {
                "enabled": True,
                "runner": "export_csv",
                "module": "export_csv",
                "kwargs": {
                    "elements_registry": "elements_registry",
                },
            },
        )
        self.assertEqual(
            self.manufacturing.EXPORT_DEFINITIONS["export_stl"],
            {
                "enabled": True,
                "runner": "export_stl_order",
                "module": "export_stl_new",
                "kwargs": {
                    "is_horizontal_layout": "stl.is_horizontal_layout",
                },
            },
        )
        self.assertEqual(
            set(self.manufacturing.get_active_exports()),
            {"export_csv", "export_stl"},
        )

    def test_importing_community_manufacturing_does_not_require_pro(self):
        self.assertNotIn("aigenfurniture_pro", sys.modules)
        module = importlib.import_module("freecad.AIGenFurniture.manufacturing")
        self.assertIs(module, self.manufacturing)

    def test_dispatcher_loads_and_invokes_only_community_runners(self):
        generate_files = importlib.import_module(
            "freecad.AIGenFurniture.manufacturing.generate_files"
        )
        calls = []

        def make_runner(name):
            def runner(order, output_path, **kwargs):
                calls.append((name, order, output_path, kwargs))

            return runner

        modules = {
            ".export_csv": types.SimpleNamespace(export_csv=make_runner("export_csv")),
            ".export_stl_new": types.SimpleNamespace(
                export_stl_order=make_runner("export_stl")
            ),
        }

        def fake_import_module(name, package):
            self.assertEqual(package, "freecad.AIGenFurniture.manufacturing")
            return modules[name]

        context = {
            "elements_registry": {"Board": object()},
            "stl": {"is_horizontal_layout": True},
        }
        with mock.patch.object(generate_files.importlib, "import_module", fake_import_module):
            generate_files.generate_manufacturing_files(
                order="order",
                output_path="/tmp/output",
                context=context,
            )

        self.assertEqual(
            calls,
            [
                (
                    "export_csv",
                    "order",
                    "/tmp/output",
                    {"elements_registry": context["elements_registry"]},
                ),
                (
                    "export_stl",
                    "order",
                    "/tmp/output",
                    {"is_horizontal_layout": True},
                ),
            ],
        )

    def test_removed_shop_specific_paths_do_not_exist(self):
        for relative_path in REMOVED_MANUFACTURING_PATHS:
            with self.subTest(path=relative_path):
                self.assertFalse((REPO_ROOT / relative_path).exists())
        self.assertFalse(
            (REPO_ROOT / "freecad/AIGenFurniture/manufacturing/templates").exists()
        )

    def test_pro_style_export_registration_remains_possible(self):
        pro_export = {
            "export_pal_for_proficut": {
                "enabled": True,
                "runner": "export_pal_for_proficut",
                "module": "export_for_proficut",
            }
        }

        self.manufacturing.EXPORT_DEFINITIONS.update(pro_export)

        self.assertIn(
            "export_pal_for_proficut",
            self.manufacturing.EXPORT_DEFINITIONS,
        )
        self.assertIn(
            "export_pal_for_proficut",
            self.manufacturing.get_active_exports(),
        )


if __name__ == "__main__":
    unittest.main()
