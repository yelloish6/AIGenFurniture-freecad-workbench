# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
"""Spreadsheet helpers for cabinet accessories.

Accessories remain the existing ``Accessory`` domain objects in
``cabinet.elements_list``. This module only persists and reconstructs them
through a FreeCAD spreadsheet. Legacy two-column sheets remain readable.
"""

from __future__ import annotations

import csv
import os
import re
from decimal import Decimal, InvalidOperation
from typing import Any, Callable, Iterable

from .accessory_catalog import resolve_accessory


ACCESSORY_SPREADSHEET_PROPERTY = "AccessorySpreadsheet"
ACCESSORY_SPREADSHEET_LABEL = "Accessories"
SHEET_TYPE_PROPERTY = "AIGenFurnitureSheetType"
ACCESSORY_SHEET_TYPE = "CabinetAccessories"
HEADER_NAME = "Accessory Name"
HEADER_QUANTITY = "Quantity"
HEADER_UNIT = "Unit"
LEGACY_ACCESSORY_TYPES = "AccessoryTypes"
LEGACY_ACCESSORY_COUNTS = "AccessoryCounts"

_RESOLVERS: list[Callable[[Any, str], str | None]] = []


def register_accessory_name_resolver(resolver: Callable[[Any, str], str | None]) -> None:
    if resolver not in _RESOLVERS:
        _RESOLVERS.append(resolver)


def clear_accessory_name_resolvers() -> None:
    _RESOLVERS.clear()


def resolve_accessory_name(doc, name: str) -> str:
    text = normalize_display_label(name)
    for resolver in list(_RESOLVERS):
        resolved = resolver(doc, text)
        if resolved:
            return normalize_display_label(resolved)
    return resolve_accessory(text).label


def create_accessory_spreadsheet(doc, assembly, cabinet, cabinet_label=None) -> Any:
    sheet_label = accessory_spreadsheet_label(assembly, cabinet_label)
    sheet = doc.addObject("Spreadsheet::Sheet", _document_object_name(sheet_label))
    sheet.Label = sheet_label
    _tag_accessory_spreadsheet(sheet)
    _write_accessory_sheet_header(sheet)
    populate_accessory_spreadsheet(sheet, cabinet, doc)

    if hasattr(assembly, "addObject"):
        assembly.addObject(sheet)

    if ACCESSORY_SPREADSHEET_PROPERTY not in getattr(assembly, "PropertiesList", []):
        assembly.addProperty(
            "App::PropertyLinkGlobal",
            ACCESSORY_SPREADSHEET_PROPERTY,
            "Cabinet",
            "Accessories spreadsheet",
        )
    setattr(assembly, ACCESSORY_SPREADSHEET_PROPERTY, sheet)
    return sheet


def accessory_spreadsheet_label(assembly, cabinet_label=None) -> str:
    label = normalize_display_label(cabinet_label)
    if not label:
        label = normalize_display_label(getattr(assembly, "Label", ""))
    if not label:
        label = normalize_display_label(getattr(assembly, "Name", ""))
    if not label:
        label = "Cabinet"
    return f"{label}_accessories"


def _document_object_name(label: str) -> str:
    safe_chars = []
    for char in normalize_display_label(label):
        if char.isalnum() or char == "_":
            safe_chars.append(char)
        else:
            safe_chars.append("_")
    safe_name = "".join(safe_chars).strip("_")
    return safe_name or "Cabinet_accessories"


def _tag_accessory_spreadsheet(sheet) -> None:
    if SHEET_TYPE_PROPERTY not in getattr(sheet, "PropertiesList", []):
        sheet.addProperty(
            "App::PropertyString",
            SHEET_TYPE_PROPERTY,
            "AIGenFurniture",
            "AIGenFurniture sheet type",
        )
    setattr(sheet, SHEET_TYPE_PROPERTY, ACCESSORY_SHEET_TYPE)


def _write_accessory_sheet_header(sheet) -> None:
    sheet.set("A1", HEADER_NAME)
    sheet.set("B1", HEADER_QUANTITY)
    sheet.set("C1", HEADER_UNIT)
    for cell in ("A1", "B1", "C1"):
        try:
            sheet.setStyle(cell, "bold")
        except Exception:
            pass
    try:
        sheet.setColumnWidth("A", 240)
        sheet.setColumnWidth("B", 90)
        sheet.setColumnWidth("C", 70)
    except Exception:
        pass


def populate_accessory_spreadsheet(sheet, cabinet, doc=None) -> None:
    rows = aggregate_accessory_elements(get_accessory_elements(cabinet), doc)
    row_index = 2
    for label, quantity, unit in rows:
        sheet.set(f"A{row_index}", label)
        sheet.set(f"B{row_index}", format_quantity(quantity))
        sheet.set(f"C{row_index}", unit)
        row_index += 1


def get_accessory_elements(cabinet) -> list[Any]:
    if hasattr(cabinet, "get_element_list_by_type"):
        return list(cabinet.get_element_list_by_type("accessory"))
    return [
        element for element in getattr(cabinet, "elements_list", [])
        if getattr(element, "type", None) == "accessory"
    ]


def aggregate_accessory_elements(elements: Iterable[Any], doc=None) -> list[tuple[str, Decimal, str]]:
    grouped: dict[str, dict[str, Any]] = {}
    for element in elements:
        raw_label = getattr(element, "legacy_label", getattr(element, "label", ""))
        definition = resolve_accessory(raw_label, getattr(element, "unit", None))
        label = resolve_accessory_name(doc, raw_label)
        if not label:
            _warn(f"Accessory with empty label was skipped")
            continue
        quantity = parse_quantity(getattr(element, "pieces", None), "accessory quantity", label)
        key = definition.code
        if key not in grouped:
            grouped[key] = {"label": label, "quantity": Decimal("0"), "unit": definition.unit}
        elif grouped[key]["unit"] != definition.unit:
            raise ValueError(
                f"Accessory '{label}' uses conflicting units: "
                f"{grouped[key]['unit']} and {definition.unit}"
            )
        grouped[key]["quantity"] += quantity

    rows = [(data["label"], data["quantity"], data["unit"]) for data in grouped.values()]
    rows.sort(key=lambda item: normalize_identity(item[0]))
    return rows


def find_accessory_spreadsheet(assembly):
    linked = getattr(assembly, ACCESSORY_SPREADSHEET_PROPERTY, None)
    if is_accessory_spreadsheet(linked):
        return linked
    for child in getattr(assembly, "Group", []) or []:
        if is_accessory_spreadsheet(child):
            return child
    doc = getattr(assembly, "Document", None)
    if doc is not None:
        for obj in getattr(doc, "Objects", []) or []:
            if is_accessory_spreadsheet(obj) and obj in (getattr(assembly, "Group", []) or []):
                return obj
    return None


def is_accessory_spreadsheet(obj) -> bool:
    if obj is None or getattr(obj, "TypeId", "") != "Spreadsheet::Sheet":
        return False
    if getattr(obj, SHEET_TYPE_PROPERTY, None) == ACCESSORY_SHEET_TYPE:
        return True
    return (
        getattr(obj, "Label", "") == ACCESSORY_SPREADSHEET_LABEL
        and _sheet_cell_value(obj, "A1") == HEADER_NAME
        and _sheet_cell_value(obj, "B1") == HEADER_QUANTITY
    )


def read_accessories_from_assembly(assembly, doc=None) -> list[Any]:
    sheet = find_accessory_spreadsheet(assembly)
    if sheet is not None:
        return read_accessories_from_spreadsheet(sheet, doc)
    return read_legacy_accessories(assembly, doc)


def read_accessories_from_spreadsheet(sheet, doc=None) -> list[Any]:
    from .cabinets.elements.accessory import Accessory

    accessories = []
    for row_index in _used_data_rows(sheet):
        name = _sheet_cell_value(sheet, f"A{row_index}")
        quantity_value = _sheet_cell_value(sheet, f"B{row_index}")
        unit_value = normalize_display_label(_sheet_cell_value(sheet, f"C{row_index}"))
        name_text = normalize_display_label(name)
        quantity_text = normalize_display_label(quantity_value)
        if not name_text and not quantity_text:
            continue
        if not name_text or not quantity_text:
            raise ValueError(f"Invalid accessory row {row_index}: name and quantity are both required")
        canonical_name = resolve_accessory_name(doc, name_text)
        quantity = parse_quantity(quantity_value, f"accessory row {row_index} quantity", canonical_name)
        accessories.append(Accessory(canonical_name, decimal_to_number(quantity), unit_value or None))
    return accessories


def read_legacy_accessories(assembly, doc=None) -> list[Any]:
    from .cabinets.elements.accessory import Accessory

    names = list(getattr(assembly, LEGACY_ACCESSORY_TYPES, []) or [])
    counts = list(getattr(assembly, LEGACY_ACCESSORY_COUNTS, []) or [])
    if len(names) != len(counts):
        _warn(
            f"Legacy accessory list length mismatch on {getattr(assembly, 'Label', assembly)}: "
            f"{len(names)} names and {len(counts)} quantities"
        )

    accessories = []
    for index, raw_name in enumerate(names):
        name = normalize_display_label(raw_name)
        if not name:
            _warn(f"Legacy accessory row {index + 1} has an empty name")
            continue
        quantity_value = counts[index] if index < len(counts) else None
        quantity = parse_quantity(quantity_value, f"legacy accessory '{name}' quantity", name)
        accessories.append(Accessory(resolve_accessory_name(doc, name), decimal_to_number(quantity)))
    return accessories


def _used_data_rows(sheet) -> list[int]:
    rows: set[int] = set()
    try:
        cells = sheet.getNonEmptyCells()
    except Exception:
        cells = []
    for cell in cells or []:
        match = re.match(r"^[A-Z]+([0-9]+)$", str(cell))
        if match:
            row = int(match.group(1))
            if row >= 2:
                rows.add(row)
    if rows:
        return sorted(rows)

    max_row = 1
    for row_index in range(2, 1002):
        if normalize_display_label(_sheet_cell_value(sheet, f"A{row_index}")) or normalize_display_label(_sheet_cell_value(sheet, f"B{row_index}")):
            max_row = row_index
    return list(range(2, max_row + 1))


def _sheet_cell_value(sheet, cell_ref: str):
    try:
        value = sheet.get(cell_ref)
    except Exception:
        value = None
    if value in (None, ""):
        try:
            value = sheet.getContents(cell_ref)
        except Exception:
            value = ""
    if hasattr(value, "Value"):
        value = value.Value
    return value


def parse_quantity(value, context: str, accessory_label: str = "") -> Decimal:
    if hasattr(value, "Value"):
        value = value.Value
    text = str(value).strip()
    if text.startswith("'"):
        text = text[1:].strip()
    text = text.replace(" ", "").replace(",", ".")
    try:
        quantity = Decimal(text)
    except (InvalidOperation, ValueError):
        raise ValueError(f"Invalid {context} for accessory '{accessory_label}': {value!r}")
    if not quantity.is_finite() or quantity <= 0:
        raise ValueError(f"Invalid {context} for accessory '{accessory_label}': {value!r}")
    return quantity


def decimal_to_number(value: Decimal):
    return float(value)


def format_quantity(value) -> str:
    quantity = value if isinstance(value, Decimal) else parse_quantity(value, "quantity")
    if quantity == quantity.to_integral_value():
        return format(quantity.quantize(Decimal("1")), "f")
    return format(quantity.normalize(), "f")


def normalize_display_label(value) -> str:
    return str(value or "").strip()


def normalize_identity(value) -> str:
    return re.sub(r"\s+", " ", normalize_display_label(value)).casefold()


def aggregate_order_accessories(order) -> list[tuple[str, Decimal, str]]:
    return aggregate_accessory_elements(_iter_order_accessories(order), None)


def _iter_order_accessories(order):
    for cabinet in getattr(order, "cabinets_list", []) or []:
        source_assembly = getattr(cabinet, "source_assembly", None)
        if source_assembly is None:
            source_assembly = getattr(cabinet, "SourceAssembly", None)
        if source_assembly is not None and find_accessory_spreadsheet(source_assembly) is not None:
            source_doc = getattr(cabinet, "source_document", None)
            if source_doc is None:
                source_doc = getattr(source_assembly, "Document", None)
            yield from read_accessories_from_assembly(source_assembly, source_doc)
            continue
        yield from get_accessory_elements(cabinet)


def write_accessories_csv(order, output_folder: str, delimiter: str = ",") -> str:
    client_name = normalize_display_label(getattr(order, "client", None))
    if not client_name or client_name == "Customer Name":
        raise ValueError("Customer Name is required in Order Setup before exporting.")
    path = os.path.join(output_folder, f"BOM_Accessories_{client_name}.csv")
    rows = aggregate_order_accessories(order)
    with open(path, mode="w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter=delimiter, quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([HEADER_NAME, HEADER_QUANTITY, HEADER_UNIT])
        for label, quantity, unit in rows:
            writer.writerow([label, format_quantity(quantity), unit])
    return path


def _warn(message: str) -> None:
    try:
        import FreeCAD as App

        App.Console.PrintWarning(f"[AIGenFurniture] {message}\n")
    except Exception:
        print(f"[AIGenFurniture] {message}")
