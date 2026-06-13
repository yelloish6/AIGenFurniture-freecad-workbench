from ..furniture_design.cabinets.elements.board import Board


UNKNOWN_MATERIAL = "UnknownMaterial"


def _safe_filename_part(value):
    text = str(value or "").strip()
    if not text:
        text = UNKNOWN_MATERIAL

    safe_chars = []
    for char in text:
        if char.isalnum() or char in ("-", "_", "."):
            safe_chars.append(char)
        elif char.isspace():
            safe_chars.append("_")
        else:
            safe_chars.append("_")

    safe_text = "".join(safe_chars).strip("._")
    return safe_text or UNKNOWN_MATERIAL


def _get_element_material(element):
    material = getattr(element, "material", "")
    if material in (None, ""):
        return UNKNOWN_MATERIAL
    return str(material).strip() or UNKNOWN_MATERIAL


def _get_elements_by_type(order, element_type):
    elements = []
    for cabinet in order.cabinets_list:
        for element in cabinet.elements_list:
            if getattr(element, "type", None) == element_type:
                elements.append(element)
    return elements


def _group_elements_by_material(elements):
    grouped = {}
    for element in elements:
        material = _get_element_material(element)
        grouped.setdefault(material, []).append(element)
    return grouped


def _get_board_type_elements(order, elements_registry):
    if not isinstance(elements_registry, dict):
        return {}

    key_to_class = {}
    for key, data in elements_registry.items():
        cls = data.get("class")
        if cls is not None and isinstance(cls, type) and issubclass(cls, Board):
            key_to_class[key] = cls

    grouped = {}  # now keyed by UI_label
    for cabinet in order.cabinets_list:
        for element in cabinet.elements_list:
            matched_key = None
            for key, cls in key_to_class.items():
                if type(element) is cls:
                    matched_key = key
                    break
            if matched_key is None:
                for key, cls in key_to_class.items():
                    if isinstance(element, cls):
                        matched_key = key
                        break
            if matched_key is not None:
                ui_label = elements_registry[matched_key].get("UI_label", matched_key)
                grouped.setdefault(ui_label, []).append(element)

    return grouped
