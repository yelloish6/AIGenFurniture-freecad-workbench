# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
import FreeCAD as App
import FreeCADGui as Gui
from ..furniture_design.cabinets.elements import ELEMENTS, get_enabled_elements


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
                box.Height = defaults.get("thickness", f"{element_name}")

                # Add an ElementType property
                box.addProperty(
                    "App::PropertyString", "ElementType", "Element", "Type of element"
                ).ElementType = element_name

                # Add parameters as properties
                params = data.get("params", element_name)
                for pname, value in params.items():
                    ptype, default, desc, options = _resolve_property_spec(doc, pname, value)
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
