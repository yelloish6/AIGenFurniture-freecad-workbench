from ..furniture_design.cabinets.elements.board import Board

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
