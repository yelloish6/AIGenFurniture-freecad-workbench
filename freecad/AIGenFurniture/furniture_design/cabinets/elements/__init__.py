# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
# -------------------------
# Define the ELEMENTS dict
# -------------------------
from .board import BoardPal, Blat, Front, Pfl

ELEMENTS = {
    "BoardPal": {
        "UI_label": "Chipboard Panel",
        "class": BoardPal,
        "material_attr": "mat_pal",  # Material attribute name in Order class
        "tooltip": "Add a chipboard panel",
        "enabled": True,
        "defaults": {
            "label": "Chipboard Panel",
            "length": 600,
            "width": 500,
            "thickness": 18,
        },
        # Constructor parameters (used by design_engine)
        "constructor": [
            "label",
            "length",
            "width",
            "thick",
            "cant_L1",
            "cant_L2",
            "cant_l1",
            "cant_l2",
        ],
        "param_aliases": {
            "Edge_L1": "cant_L1",
            "Edge_L2": "cant_L2",
            "Edge_l1": "cant_l1",
            "Edge_l2": "cant_l2",
        },
        "params": {
            "Material": ("App::PropertyString", "", "Material"),
            "Edge_L1": ("App::PropertyString", "", "Long Edge 1"),
            "Edge_L2": ("App::PropertyString", "", "Long Edge 2"),
            "Edge_l1": ("App::PropertyString", "", "Short Edge 1"),
            "Edge_l2": ("App::PropertyString", "", "Short Edge 2"),
        },

    },
    "Blat": {
        "UI_label": "Countertop",
        "class": Blat,
        "material_attr": "mat_blat",  # Material attribute name in Order class
        "tooltip": "Add a countertop panel",
        "enabled": True,
        "defaults": {
            "label": "Countertop",
            "length": 1000,
            "width": 600,
            "thickness": 38,
        },
        # Constructor parameters (used by design_engine)
        "constructor": [
            "label",
            "length",
            "width",
            "thick",
        ],
        "params": {
            "Material": ("App::PropertyString", "", "Material"),
        },
    },
    "Front": {
        "UI_label": "Front",
        "class": Front,
        "material_attr": "mat_front",  # Material attribute name in Order class
        "tooltip": "Add a cabinet front",
        "enabled": True,
        "defaults": {
            "label": "Front",
            "length": 400,
            "width": 700,
            "thickness": 18,
        },
        "constructor": [
            "label",
            "length",
            "width",
            "thick",
        ],
        "params": {
            "Material": ("App::PropertyString", "", "Material"),
        },
    },
    "Pfl": {
        "UI_label": "HDF Back Panel",
        "class": Pfl,
        "material_attr": "mat_pfl",  # Material attribute name in Order class
        "tooltip": "Add an HDF back panel",
        "enabled": True,
        "defaults": {
            "label": "HDF Back Panel",
            "length": 1000,
            "width": 1000,
            "thickness": 4,
        },
        "constructor": [
            "label",
            "length",
            "width",
            "thick",
        ],
        "params": {
            "Material": ("App::PropertyString", "", "Material"),
        },
    }
}

def get_enabled_elements():
    return {
        name: data
        for name, data in ELEMENTS.items()
        if data.get("enabled", False)
    }
