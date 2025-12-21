# -------------------------
# Define the ELEMENTS dict
# -------------------------
ELEMENTS = {
    "BoardPal": {
        "label": "Chipboard",
        "tooltip": "Add a standard chipboard [18 mm]",
        "params": {
            "cant_L1": ("App::PropertyString", "", "Edge length 1"),
            "cant_L2": ("App::PropertyString", "", "Edge length 2"),
            "cant_l1": ("App::PropertyString", "", "Edge width 1"),
            "cant_l2": ("App::PropertyString", "", "Edge width 2"),
        },

    },
    "Countertop": {
        "label": "Countertop",
        "tooltip": "Add a countertop board [38 mm]",
        "params": {},
    },
    "Front": {
        "label": "Front",
        "tooltip": "Add a front board [18 mm]",
        "params": {},
    },
    "PFL": {
        "label": "HDF",
        "tooltip": "Add a thin HDF board [4 mm]",
        "params": {},
    }
}