from .drawers import DrawersMixin
from .shelves import ShelvesMixin
from .fronts import FrontMixin
from .backs import BackMixin

# FEATURE REGISTRY
FEATURES = {
    "add_front": {
        "label": "Front",
        "enabled": True,
        "tooltip": "Add a drawer",
        "params": {
            "split_list": ("App::PropertyString", "[[100,50],[100,50]]", "Split list of tuples"),
            "front_type": ("App::PropertyString", "door", "Front type"),
        }
    },

    "add_front_manual": {
        "label": "Manual Front",
        "enabled": False,
        "tooltip": "Add a manual front",
        "params": {
            "height": ("App::PropertyFloat", 300.0, "Height"),
            "width": ("App::PropertyFloat", 200.0, "Width"),
            "offset_x": ("App::PropertyFloat", 0.0, "Offset X"),
            "offset_z": ("App::PropertyFloat", 0.0, "Offset Z"),
        }
    },

    "remove_all_pfl": {
        "label": "Remove all HDF",
        "enabled": False,
        "tooltip": "Remove all HDF elements",
        "params": {
            "remove_all_pfl": ("App::PropertyBool", True, "Remove HDF"),
        }
    },

    "remove_element": {
        "label": "Remove element",
        "enabled": False,
        "tooltip": "Remove element by type and label",
        "params": {
            "type": ("App::PropertyString", "", "Element type"),
            "label": ("App::PropertyString", "", "Element label"),
        }
    },
    "add_pfl": {
        "label": "Add HDF",
        "enabled": False,
        "tooltip": "Add HDF on the back of the cabinet",
        "params": {}
    },

    # drawers
    "add_tandem_box": {
        "label": "Tandembox",
        "enabled": False,
        "tooltip": "Add a Tandembox drawer",
        "params": {
            "tandembox_type": ("App::PropertyString", "", "Box type"),
            "height_offset": ("App::PropertyFloat", 0.0, "Offset"),
        }
    },
    "add_drawer": {
        "label": "Drawer",
        "enabled": True,
        "tooltip": "Add a drawer",
        "params": {
            "height": ("App::PropertyFloat", 100.0, "Drawer height"),
            "offset": ("App::PropertyFloat", 24.0, "Offset"),
            "box_type": ("App::PropertyString", "a", "(a) lateral assembles on the edge of the front board, or (b) on the back"),
            "bottom": ("App::PropertyString", "pfl", "material of the bottom. Can be (pal) or (pfl) -> (default and not defined)"),
        }
    },
    "add_drawer_pal_glass": {
        "label": "Drawer Glass",
        "enabled": False,
        "tooltip": "Add a drawer with glass front",
        "params": {
            "height": ("App::PropertyFloat", 100.0, "Drawer height"),
            "offset": ("App::PropertyFloat", 0.0, "Offset"),
        }
    },

    # shelves
    "add_pol": {
        "label": "Shelves",
        "enabled": True,
        "tooltip": "Add a shelves",
        "params": {
            "nr": ("App::PropertyInteger", 1, "Number of shelves"),
            "cant": ("App::PropertyString", "2", "Edge type"),
        }
    },
    "add_pol_2": {
        "label": "Shelf - configurable",
        "enabled": False,
        "tooltip": "Add a shelf that can be configured",
        "params": {
            "orient": ("App::PropertyString", "h", "orientation [h or v]"),
            "length": ("App::PropertyFloat", 0.0, "length of the board, 0 for default width"),
            "height": ("App::PropertyFloat", 0.0, "Position offset of the shelf in the cabinet on Z"),
            "offset": ("App::PropertyFloat", 0.0, "Position offset of the shelf in the cabinet on X"),
        }
    },
    "add_separator": {
        "label": "Separator",
        "enabled": False,
        "tooltip": "Add a separator",
        "params": {
            "orient": ("App::PropertyString", "V", "Orientation"),
            "sep_cant": ("App::PropertyString", "", "Separator edge type"),
        }
    },
    "add_wine_shelf": {
        "label": "Wine rack",
        "enabled": False,
        "tooltip": "Add a wine rack inside the cabinet",
        "params": {
            "goluri": ("App::PropertyInteger", 4, "Number of slots"),
            "left_right": ("App::PropertyString", "L", "Left or Right"),
            "cant": ("App::PropertyString", "", "Edge type"),
        }
    },
    "add_sep_v": {
        "label": "Vertical Separator",
        "enabled": False,
        "tooltip": "Add a vertical separator",
        "params": {
            "height": ("App::PropertyFloat", 0.0, "Height"),
            "offset_x": ("App::PropertyFloat", 0.0, "Offset X"),
            "offset_z": ("App::PropertyFloat", 0.0, "Offset Z"),
            "cant": ("App::PropertyString", "", "Edge type"),
        }
    },
    "add_sep_h": {
        "label": "Horizontal separator",
        "enabled": False,
        "tooltip": "Add a horizontal separator",
        "params": {
            "width": ("App::PropertyFloat", 0.0, "Width"),
            "offset_x": ("App::PropertyFloat", 0.0, "Offset X"),
            "offset_z": ("App::PropertyFloat", 0.0, "Offset Z"),
            "sep_edge": ("App::PropertyString", "", "Edge type"),
            "edge_gap": ("App::PropertyFloat", 0.0, "Gap between edge of separator and edge of cabinet"),
        }
    }
}

# ─────────────────────────────────────────────
# Feature lookup API (used by commands)
# ─────────────────────────────────────────────

# def get_feature_definition(feature_name):
#     data = FEATURES.get(feature_name)
#     if not data or not data.get("active", False):
#         return None
#     return data

def get_enabled_features():
    return {
        name: data
        for name, data in FEATURES.items()
        if data.get("enabled", False)
    }

def get_feature_handler(feature_name):
    """
    Returns a callable that applies a feature to a cabinet,
    or None if the feature is disabled or unknown.
    """

    feature_def = FEATURES.get(feature_name)
    if not feature_def or not feature_def.get("enabled", False):
        return None

    def handler(cabinet, feature_data):
        method = getattr(cabinet, feature_name, None)
        if not callable(method):
            raise AttributeError(
                f"Cabinet does not support feature '{feature_name}'"
            )

        params = {
            k: v for k, v in feature_data.items()
            if k != "feature"
        }

        method(**params)

    return handler