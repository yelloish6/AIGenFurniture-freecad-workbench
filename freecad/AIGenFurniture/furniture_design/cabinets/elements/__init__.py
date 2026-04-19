# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
# -------------------------
# Define the ELEMENTS dict
# -------------------------
from .board import BoardPal, Blat, Front, Pfl

ELEMENTS = {
    "BoardPal": {
        "UI_label": "Chipboard",
        "class": BoardPal,
        "material_attr": "mat_pal",  # Material attribute name in Order class
        "tooltip": "Add a standard chipboard [18 mm]",
        "enabled": True,
        "defaults": {
            "label": "BoardPal",
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
        "params": {
            "cant_L1": ("App::PropertyString", "", "Edge length 1"),
            "cant_L2": ("App::PropertyString", "", "Edge length 2"),
            "cant_l1": ("App::PropertyString", "", "Edge width 1"),
            "cant_l2": ("App::PropertyString", "", "Edge width 2"),
        },

    },
    "Blat": {
        "UI_label": "Countertop",
        "class": Blat,
        "material_attr": "mat_blat",  # Material attribute name in Order class
        "tooltip": "Add a countertop board [38 mm]",
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
        "params": {},
    },
    "Front": {
        "UI_label": "Front",
        "class": Front,
        "material_attr": "mat_front",  # Material attribute name in Order class
        "tooltip": "Add a front board [18 mm]",
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
        "params": {},
    },
    "Pfl": {
        "UI_label": "HDF",
        "class": Pfl,
        "material_attr": "mat_pfl",  # Material attribute name in Order class
        "tooltip": "Add a thin HDF board [4 mm]",
        "enabled": True,
        "defaults": {
            "label": "hdf",
            "length": 1000,
            "width": 1000,
            "thickness": 4,
        },
        "constructor": [
            "label",
            "length",
            "width",
        ],
        "params": {},
    }
}