# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
import FreeCAD as App
import FreeCADGui as Gui
from ..furniture_design.cabinets.elements import ELEMENTS, get_enabled_elements
from ..furniture_design.design_engine import load_default_rules
from ..furniture_design.order.order_params import ORDER_PARAMS


THICKNESS_RULE_BY_ELEMENT = {
    "BoardPal": "thick_pal",
    "Blat": "thick_blat",
    "Front": "thick_front",
    "Pfl": "thick_pfl",
}


def _col_letter(index):
    result = []
    while index > 0:
        index, remainder = divmod(index - 1, 26)
        result.append(chr(ord("A") + remainder))
    return "".join(reversed(result))


def _cell_text(sheet, cell_ref):
    value = None
    try:
        value = sheet.get(cell_ref)
    except Exception:
        pass

    if value in (None, ""):
        try:
            value = sheet.getContents(cell_ref)
        except Exception:
            value = None

    if value is None:
        return ""

    text = str(value).strip()
    if text.startswith("'"):
        text = text[1:].strip()
    return text


def _normalize_header(text):
    return text.strip().lower().replace(" ", "_").replace("-", "_")


def _find_order_var_sheet(doc):
    if doc is None:
        return None

    sheet = doc.getObject("OrderVar")
    if sheet is not None and getattr(sheet, "TypeId", "") == "Spreadsheet::Sheet":
        return sheet

    for obj in doc.Objects:
        if getattr(obj, "TypeId", "") == "Spreadsheet::Sheet" and getattr(obj, "Label", "") == "OrderVar":
            return obj

    return None


def _order_var_value_by_label(sheet, field_label):
    if sheet is None:
        return ""

    target_label = field_label.strip().lower()
    empty_streak = 0
    for row_index in range(1, 2001):
        label = _cell_text(sheet, f"A{row_index}")
        if not label:
            empty_streak += 1
            if empty_streak >= 25:
                break
            continue

        empty_streak = 0
        if label.strip().lower() == target_label:
            return _cell_text(sheet, f"B{row_index}")

    return ""


def _order_var_value_by_alias(sheet, alias_name):
    if sheet is None or not alias_name:
        return ""

    try:
        value = sheet.get(alias_name)
    except Exception:
        return ""

    if value in (None, ""):
        return ""

    text = str(value).strip()
    if text.startswith("'"):
        text = text[1:].strip()
    return text


def _material_order_param_name(element_name):
    material_attr = ELEMENTS.get(element_name, {}).get("material_attr")
    if not material_attr:
        return ""

    for param_name, param_def in ORDER_PARAMS.items():
        if param_def.get("order_attr") == material_attr:
            return param_name

    return ""


def _order_var_material_default(doc, element_name):
    sheet = _find_order_var_sheet(doc)
    if sheet is None:
        return ""

    material = _order_var_value_by_label(sheet, f"{element_name} Material")
    if material:
        return material

    param_name = _material_order_param_name(element_name)
    material = _order_var_value_by_alias(sheet, param_name)
    if material:
        return material

    param_label = ORDER_PARAMS.get(param_name, {}).get("label", "")
    if param_label:
        return _order_var_value_by_label(sheet, param_label)

    return ""


def _sheet_column_values(doc, sheet_name, column_name):
    if doc is None:
        return []

    sheet = doc.getObject(sheet_name)
    if sheet is None:
        App.Console.PrintWarning(
            f"[AIGenFurniture] Sheet '{sheet_name}' not found. Dropdown will be empty.\n"
        )
        return []

    target_col = None
    empty_streak = 0
    for col_index in range(1, 201):
        text = _cell_text(sheet, f"{_col_letter(col_index)}1")
        if not text:
            empty_streak += 1
            if empty_streak >= 10:
                break
            continue

        empty_streak = 0
        if _normalize_header(text) == _normalize_header(column_name):
            target_col = col_index
            break

    if target_col is None:
        App.Console.PrintWarning(
            f"[AIGenFurniture] Column '{column_name}' not found in sheet '{sheet_name}'.\n"
        )
        return []

    values = []
    seen = set()
    empty_streak = 0
    row_index = 2
    while row_index <= 2000:
        text = _cell_text(sheet, f"{_col_letter(target_col)}{row_index}")
        if not text:
            empty_streak += 1
            if empty_streak >= 25:
                break
            row_index += 1
            continue

        empty_streak = 0
        if text not in seen:
            seen.add(text)
            values.append(text)
        row_index += 1

    return values


def _resolve_property_spec(doc, pname, spec):
    if isinstance(spec, tuple):
        ptype, default, desc = spec
        return ptype, default, desc, None

    if isinstance(spec, dict):
        ptype = spec["type"]
        default = spec.get("default", "")
        desc = spec.get("description", pname)
        options = None
        options_spec = spec.get("options")
        if ptype == "App::PropertyEnumeration" and options_spec:
            options = _sheet_column_values(
                doc,
                options_spec["sheet"],
                options_spec["column"],
            )
            if default and default not in options:
                options.insert(0, default)
            if not options:
                options = [default] if default else [""]
            if not default:
                default = options[0]
        return ptype, default, desc, options

    raise TypeError(f"Unsupported property definition for '{pname}'")


def _element_thickness_default(element_name, defaults):
    fallback = defaults.get("thickness", f"{element_name}")
    rule_key = THICKNESS_RULE_BY_ELEMENT.get(element_name)
    if not rule_key:
        return fallback

    try:
        rules = load_default_rules()
    except Exception as exc:
        App.Console.PrintWarning(
            f"[AIGenFurniture] Could not load design rules for {element_name} thickness: {exc}\n"
        )
        return fallback

    return rules.get(rule_key, fallback)


# -------------------------
# Command class generator
# -------------------------
def make_element_command(element_name, data):
    class ElementCommand:
        def GetResources(self):
            return {
                "Pixmap": "",  # put path to icon if you have one
                "MenuText": data.get("UI_label", f"{element_name}"),
                "ToolTip": data.get("tooltip", f"{element_name}"),
            }

        def Activated(self):
            doc = App.ActiveDocument or App.newDocument("Cabinets")

            doc.openTransaction(f"Add Element {element_name}")
            try:
                # Create a box placeholder
                box = doc.addObject("Part::Box", f"{element_name}")
                defaults = data.get("defaults", {})
                box.Label = defaults.get("label", f"{element_name}")
                box.Length = defaults.get("length", f"{element_name}")
                box.Width = defaults.get("width", f"{element_name}")
                box.Height = _element_thickness_default(element_name, defaults)

                # Add an ElementType property
                box.addProperty(
                    "App::PropertyString", "ElementType", "Element", "Type of element"
                ).ElementType = element_name

                # Add parameters as properties
                params = data.get("params", element_name)
                for pname, value in params.items():
                    ptype, default, desc, options = _resolve_property_spec(doc, pname, value)
                    if pname == "Material":
                        default = _order_var_material_default(doc, element_name) or default
                    if not hasattr(box, pname):
                        box.addProperty(ptype, pname, "Element", desc)
                    if ptype == "App::PropertyEnumeration":
                        setattr(box, pname, options or [])
                        if default in (options or []):
                            setattr(box, pname, default)
                    else:
                        setattr(box, pname, default)

                doc.recompute()
                doc.commitTransaction()
                App.Console.PrintMessage(f"{element_name} created.\n")
            except Exception as e:
                doc.abortTransaction()
                App.Console.PrintError(str(e) + "\n")

    return ElementCommand()


# -------------------------
# Register commands in FreeCAD
# -------------------------
REGISTERED_ELEMENTS = get_enabled_elements()

def get_elements_registry():
    return REGISTERED_ELEMENTS

def register_element_commands(elements_registry):
    registered = []
    for ele_name, ele_data in elements_registry.items():
        if not ele_data.get("enabled", False):
            continue
        Gui.addCommand(f"Cmd_Add_{ele_name}", make_element_command(ele_name, ele_data))
        registered.append(ele_name)
    return registered

# for ele_name, ele_data in ELEMENTS.items():
#     Gui.addCommand(f"Cmd_Add_{ele_name}", make_element_command(ele_name, ele_data))
