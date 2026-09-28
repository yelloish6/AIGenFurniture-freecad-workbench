import csv
import sys
import tempfile
import types
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
FREECAD_ROOT = REPO_ROOT / "freecad"
PACKAGE_ROOT = FREECAD_ROOT / "AIGenFurniture"
sys.path.insert(0, str(FREECAD_ROOT))
sys.path.insert(0, str(PACKAGE_ROOT))

sys.modules.setdefault(
    "FreeCAD",
    types.SimpleNamespace(
        Console=types.SimpleNamespace(
            PrintWarning=lambda _msg: None,
            PrintMessage=lambda _msg: None,
            PrintError=lambda _msg: None,
        )
    ),
)

from AIGenFurniture.furniture_design.accessory_spreadsheet import (  # noqa: E402
    ACCESSORY_SPREADSHEET_PROPERTY,
    ACCESSORY_SHEET_TYPE,
    HEADER_NAME,
    HEADER_QUANTITY,
    SHEET_TYPE_PROPERTY,
    aggregate_order_accessories,
    clear_accessory_name_resolvers,
    create_accessory_spreadsheet,
    find_accessory_spreadsheet,
    format_quantity,
    read_accessories_from_assembly,
    read_accessories_from_spreadsheet,
    register_accessory_name_resolver,
    write_accessories_csv,
)
from AIGenFurniture.furniture_design.cabinets.elements.accessory import Accessory  # noqa: E402
from AIGenFurniture.manufacturing.export_csv import export_csv  # noqa: E402


class FakeDoc:
    def __init__(self):
        self.Objects = []

    def addObject(self, type_id, name):
        obj = FakeSheet(self, name) if type_id == "Spreadsheet::Sheet" else FakeObj(self, type_id, name)
        self.Objects.append(obj)
        return obj


class FakeObj:
    def __init__(self, doc, type_id, name):
        self.Document = doc
        self.TypeId = type_id
        self.Name = name
        self.Label = name
        self.PropertiesList = []
        self.Group = []
        self._groups = {}
        self._property_types = {}

    def addProperty(self, _prop_type, name, group, _description):
        self.PropertiesList.append(name)
        self._groups[name] = group
        self._property_types[name] = _prop_type
        setattr(self, name, None)
        return self

    def addObject(self, obj):
        self.Group.append(obj)


class FakeSheet(FakeObj):
    def __init__(self, doc, name):
        super().__init__(doc, "Spreadsheet::Sheet", name)
        self.cells = {}
        self.styles = {}
        self.widths = {}

    def set(self, cell, value):
        self.cells[cell] = value

    def get(self, cell):
        return self.cells.get(cell, "")

    def getContents(self, cell):
        return self.cells.get(cell, "")

    def setStyle(self, cell, style):
        self.styles[cell] = style

    def setColumnWidth(self, column, width):
        self.widths[column] = width

    def getNonEmptyCells(self):
        return [cell for cell, value in self.cells.items() if value not in ("", None)]


class FakeCabinet:
    def __init__(self, elements=None):
        self.elements_list = list(elements or [])

    def get_element_list_by_type(self, element_type):
        return [element for element in self.elements_list if getattr(element, "type", None) == element_type]

    def append(self, element):
        self.elements_list.append(element)


class FakeOrder:
    client = "Client"

    def __init__(self, cabinets):
        self.cabinets_list = cabinets


class FakeBoard:
    type = "pal"
    material = "White"
    length = 100
    width = 50
    label = "board"


class AccessorySpreadsheetTest(unittest.TestCase):
    def tearDown(self):
        clear_accessory_name_resolvers()

    def test_existing_accessory_class_is_reused_and_lives_in_elements_list(self):
        cabinet = FakeCabinet()
        accessory = Accessory("maner", 2)

        cabinet.append(accessory)

        self.assertIs(cabinet.elements_list[0], accessory)
        self.assertEqual(accessory.type, "accessory")
        self.assertEqual(accessory.code, "handle")
        self.assertEqual(accessory.label, "Handle")
        self.assertEqual(accessory.unit, "pcs")
        self.assertEqual(accessory.pieces, 2)

    def test_create_sheet_grouped_global_link_tagged_and_headers_even_when_empty(self):
        doc = FakeDoc()
        assembly = doc.addObject("App::Part", "TopBox")
        cabinet = FakeCabinet()

        sheet = create_accessory_spreadsheet(doc, assembly, cabinet)

        self.assertEqual(sheet.Label, "TopBox_accessories")
        self.assertIs(find_accessory_spreadsheet(assembly), sheet)
        self.assertIn(sheet, assembly.Group)
        self.assertEqual(sheet._property_types[SHEET_TYPE_PROPERTY], "App::PropertyString")
        self.assertEqual(sheet.AIGenFurnitureSheetType, ACCESSORY_SHEET_TYPE)
        self.assertEqual(assembly._property_types[ACCESSORY_SPREADSHEET_PROPERTY], "App::PropertyLinkGlobal")
        self.assertIn(ACCESSORY_SPREADSHEET_PROPERTY, assembly.PropertiesList)
        self.assertIs(assembly.AccessorySpreadsheet, sheet)
        self.assertEqual(sheet.get("A1"), HEADER_NAME)
        self.assertEqual(sheet.get("B1"), HEADER_QUANTITY)
        self.assertEqual(sheet.get("C1"), "Unit")
        self.assertEqual(sheet.get("A2"), "")

    def test_create_sheet_can_use_source_box_label_instead_of_assembly_label(self):
        doc = FakeDoc()
        assembly = doc.addObject("App::Part", "Assy_TopBox")

        sheet = create_accessory_spreadsheet(doc, assembly, FakeCabinet(), "TopBox")

        self.assertEqual(sheet.Label, "TopBox_accessories")
        self.assertIs(find_accessory_spreadsheet(assembly), sheet)

    def test_prefill_aggregates_duplicates_and_preserves_fractional_quantities(self):
        doc = FakeDoc()
        assembly = doc.addObject("App::Part", "Assy")
        cabinet = FakeCabinet([
            Accessory(" maner ", 1),
            Accessory("maner", 2.5),
            Accessory("surub", 4),
        ])

        sheet = create_accessory_spreadsheet(doc, assembly, cabinet)

        self.assertEqual(sheet.get("A2"), "Cabinet assembly screw")
        self.assertEqual(sheet.get("B2"), "4")
        self.assertEqual(sheet.get("C2"), "pcs")
        self.assertEqual(sheet.get("A3"), "Handle")
        self.assertEqual(sheet.get("B3"), "3.5")

    def test_reconstruction_reads_spreadsheet_blank_rows_and_formula_values(self):
        doc = FakeDoc()
        assembly = doc.addObject("App::Part", "Assy")
        sheet = create_accessory_spreadsheet(doc, assembly, FakeCabinet())
        sheet.Label = "RenamedByUser"
        sheet.set("A2", "")
        sheet.set("B2", "")
        sheet.set("A4", "maner")
        sheet.set("B4", 2.5)

        accessories = read_accessories_from_assembly(assembly, doc)

        self.assertEqual(len(accessories), 1)
        self.assertIsInstance(accessories[0], Accessory)
        self.assertEqual(accessories[0].label, "Handle")
        self.assertEqual(accessories[0].pieces, 2.5)

    def test_header_only_sheet_reconstructs_no_accessories(self):
        doc = FakeDoc()
        assembly = doc.addObject("App::Part", "Assy")
        create_accessory_spreadsheet(doc, assembly, FakeCabinet())

        self.assertEqual(read_accessories_from_assembly(assembly, doc), [])

    def test_spreadsheet_takes_precedence_over_legacy_and_no_double_count(self):
        doc = FakeDoc()
        assembly = doc.addObject("App::Part", "Assy")
        assembly.addProperty("App::PropertyStringList", "AccessoryTypes", "Cabinet", "")
        assembly.addProperty("App::PropertyIntegerList", "AccessoryCounts", "Cabinet", "")
        assembly.AccessoryTypes = ["legacy"]
        assembly.AccessoryCounts = [7]
        create_accessory_spreadsheet(doc, assembly, FakeCabinet([Accessory("sheet", 2)]))

        accessories = read_accessories_from_assembly(assembly, doc)

        self.assertEqual([(item.label, item.pieces) for item in accessories], [("sheet", 2)])

    def test_legacy_only_documents_remain_readable(self):
        doc = FakeDoc()
        assembly = doc.addObject("App::Part", "Assy")
        assembly.addProperty("App::PropertyStringList", "AccessoryTypes", "Cabinet", "")
        assembly.addProperty("App::PropertyIntegerList", "AccessoryCounts", "Cabinet", "")
        assembly.AccessoryTypes = ["legacy"]
        assembly.AccessoryCounts = [1.25]

        accessories = read_accessories_from_assembly(assembly, doc)

        self.assertEqual([(item.label, item.pieces) for item in accessories], [("legacy", 1.25)])

    def test_legacy_two_column_sheet_infers_known_accessory_unit(self):
        doc = FakeDoc()
        assembly = doc.addObject("App::Part", "Assy")
        sheet = create_accessory_spreadsheet(doc, assembly, FakeCabinet())
        sheet.set("C1", "")
        sheet.set("A2", "pereche glisiera 500 mm")
        sheet.set("B2", "1")

        accessories = read_accessories_from_spreadsheet(sheet, doc)

        self.assertEqual(accessories[0].label, "Drawer slide — 500 mm")
        self.assertEqual(accessories[0].unit, "pair")

    def test_invalid_quantity_raises(self):
        doc = FakeDoc()
        assembly = doc.addObject("App::Part", "Assy")
        sheet = create_accessory_spreadsheet(doc, assembly, FakeCabinet())
        sheet.set("A2", "maner")
        sheet.set("B2", "bad")

        with self.assertRaisesRegex(ValueError, "Invalid accessory row 2 quantity"):
            read_accessories_from_spreadsheet(sheet, doc)

    def test_order_csv_aggregates_formats_and_sorts(self):
        order = FakeOrder([
            FakeCabinet([Accessory(" surub ", 1), Accessory("maner", 2.5)]),
            FakeCabinet([Accessory("SURUB", 3)]),
        ])

        rows = aggregate_order_accessories(order)

        self.assertEqual(
            [(label, format_quantity(quantity), unit) for label, quantity, unit in rows],
            [("Cabinet assembly screw", "4", "pcs"), ("Handle", "2.5", "pcs")],
        )

    def test_order_csv_reads_each_source_assembly_spreadsheet_as_authority(self):
        doc = FakeDoc()
        assembly_a = doc.addObject("App::Part", "Assy_A")
        assembly_b = doc.addObject("App::Part", "Assy_B")
        create_accessory_spreadsheet(doc, assembly_a, FakeCabinet([Accessory("old", 99)]))
        sheet_b = create_accessory_spreadsheet(doc, assembly_b, FakeCabinet([Accessory("surub", 3)]))
        assembly_a.AccessorySpreadsheet.Label = "Custom accessory sheet name"
        sheet_b.Label = "Accessories001"
        assembly_a.AccessorySpreadsheet.set("A2", "maner")
        assembly_a.AccessorySpreadsheet.set("B2", "2.5")
        sheet_b.set("A2", "surub")
        sheet_b.set("B2", "4")

        cabinet_a = FakeCabinet([Accessory("stale", 100)])
        cabinet_a.source_assembly = assembly_a
        cabinet_b = FakeCabinet()
        cabinet_b.source_assembly = assembly_b
        order = FakeOrder([cabinet_a, cabinet_b])

        rows = aggregate_order_accessories(order)

        self.assertEqual(
            [(label, format_quantity(quantity), unit) for label, quantity, unit in rows],
            [("Cabinet assembly screw", "4", "pcs"), ("Handle", "2.5", "pcs")],
        )

    def test_accessories_csv_filename_header_and_no_accessories(self):
        order = FakeOrder([FakeCabinet()])
        with tempfile.TemporaryDirectory() as tmpdir:
            path = write_accessories_csv(order, tmpdir)
            self.assertEqual(Path(path).name, "BOM_Accessories_Client.csv")
            self.assertEqual(Path(path).read_text(encoding="utf-8"), "Accessory Name,Quantity,Unit\n")

    def test_accessories_csv_quotes_special_labels(self):
        order = FakeOrder([FakeCabinet([Accessory('Handle, brushed "steel"', 1)])])
        with tempfile.TemporaryDirectory() as tmpdir:
            path = write_accessories_csv(order, tmpdir)
            with open(path, newline="", encoding="utf-8") as handle:
                rows = list(csv.reader(handle))
        self.assertEqual(rows[1], ['Handle, brushed "steel"', "1", "pcs"])

    def test_accessories_csv_rejects_blank_customer(self):
        order = FakeOrder([])
        order.client = ""
        with tempfile.TemporaryDirectory() as tmpdir:
            with self.assertRaisesRegex(ValueError, "Customer Name is required in Order Setup"):
                write_accessories_csv(order, tmpdir)

    def test_export_csv_adds_accessories_file_without_suppressing_existing_outputs(self):
        order = FakeOrder([FakeCabinet([FakeBoard(), Accessory("maner", 2)])])
        with tempfile.TemporaryDirectory() as tmpdir:
            export_csv(order, tmpdir)
            names = sorted(path.name for path in Path(tmpdir).iterdir())

        self.assertEqual(names, ["BOM_Accessories_Client.csv", "CuttingList_Chipboard_White_Client.csv"])

    def test_resolver_hook_is_optional_and_neutral(self):
        register_accessory_name_resolver(lambda _doc, name: "HANDLE_A" if name == "Handle A" else None)
        doc = FakeDoc()
        assembly = doc.addObject("App::Part", "Assy")
        sheet = create_accessory_spreadsheet(doc, assembly, FakeCabinet())
        sheet.set("A2", "Handle A")
        sheet.set("B2", "2")

        accessories = read_accessories_from_assembly(assembly, doc)

        self.assertEqual(accessories[0].label, "HANDLE_A")


if __name__ == "__main__":
    unittest.main()
