# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
from .banca import Banca
from .bar import Bar
from .base_box import BaseBox
from .base_corner import BaseCorner
from .base_corner_shelf import BaseCornerShelf

from .corp_cu_picioare import CorpCuPicioare
from .corp_dressing import CorpDressing
from .dulap import Dulap
from .etajera import Etajera

from .jolly_box import JollyBox
from .msv_box import MsVBox
from .raft import Raft
from .sink_box import SinkBox
from .top_box import TopBox
from .top_corner import TopCorner
from .tower_box import TowerBox
from ..cabinet import Cabinet

def _box_value(box, name, default=None):
    if isinstance(box, dict):
        return box.get(name, default)
    return getattr(box, name, default)

# Special cases: cabinets that require extra arguments
def make_base_corner_shelf(label, height, width, depth, rules, box=None):
    """Factory for BaseCornerShelf with extra shelves parameter."""
    # Read shelves count from the box if present, otherwise default = 3
    shelves = _box_value(box, "shelves", 3)
    rounded = _box_value(box, "rounded", False)
    return BaseCornerShelf(label, height, width, depth, rules, shelves=shelves, rounded=rounded)

def make_base_corner(label, height, width, depth, rules, box=None):
    """Factory for BaseCorner with extra cut_width, cut_depth, l_r, with_polita parameters."""
    cut_width = _box_value(box, "cut_width", 0)
    cut_depth = _box_value(box, "cut_depth", 0)
    l_r = _box_value(box, "l_r", 0)
    with_polita = _box_value(box, "with_polita", True)
    return BaseCorner(label, height, width, depth, rules, cut_width, cut_depth, l_r, with_polita)

def make_top_corner(label, height, width, depth, rules, box=None):
    """Factory for TopCorner with extra cut_width, cut_depth, l_r, with_polita parameters."""
    cut_width = _box_value(box, "cut_width", 0)
    cut_depth = _box_value(box, "cut_depth", 0)
    l_r = _box_value(box, "l_r", 0)
    polite = _box_value(box, "polite", 1)
    return TopCorner(label, height, width, depth, rules, cut_width, cut_depth, l_r, polite)

def make_raft(label, height, width, depth, rules, box=None):
    """Factory for BaseCornerShelf with extra shelves parameter."""
    # Read shelves count from the box if present, otherwise default = 3
    shelves = _box_value(box, "shelves", 3)
    return Raft(label, height, width, depth, rules, shelves=shelves)

def make_tower_box(label, height, width, depth, rules, box=None):
    """Factory for TowerBox with extra tower_height parameter."""
    gap_list = _box_value(box, "gap_list", [200, 400])
    gap_heat = _box_value(box, "gap_heat", 50)
    front_list = _box_value(box, "front_list", [0, 0, 0])
    return TowerBox(label, height, width, depth, rules, gap_list = gap_list, gap_heat = gap_heat, front_list = front_list)

def make_corp_cu_picioare(label, height, width, depth, rules, box=None):
    """Factory for CorpCuPicioare with extra shelves parameter."""
    h_skirt = _box_value(box, "skirt_height", 100)
    has_skirting_board = _box_value(box, "skirting_board", True)
    return CorpCuPicioare(label, height, width, depth, rules, h_skirt=h_skirt, has_skirting_board=has_skirting_board)

def make_corp_dressing(label, height, width, depth, rules, box=None):
    """Factory for Corp Dressing with extra parameter."""
    gap_list = _box_value(box, "gap_list", [200, 400])
    front_list = _box_value(box, "front_list", [0, 0, 0])
    return CorpDressing(label, height, width, depth, rules, gap_list = gap_list, front_list = front_list)

def make_etajera(label, height, width, depth, rules, box=None):
    """Factory for Etajera with extra shelves parameter."""
    # Read shelves count from the box if present, otherwise default = 3
    shelves = _box_value(box, "shelves", 3)
    return Etajera(label, height, width, depth, rules, shelves=shelves)

def make_bench(label, height, width, depth, rules, box=None):
    """Factory for Bench with extra parameters."""
    gap_front = _box_value(box, "gap_front")
    gap_lat = _box_value(box, "gap_lat")
    height_base = _box_value(box, "height_base")
    return Banca(label, height, width, depth, rules, gap_front = gap_front, gap_lat = gap_lat, height_base = height_base)

def make_bar(label, height, width, depth, rules, box=None):
    """Factory for Bar with cabinet-specific clearances."""
    front_clearance = _box_value(box, "front_clearance", 50)
    back_clearance = _box_value(box, "back_clearance", 0)
    return Bar(label, height, width, depth, rules, front_clearance=front_clearance, back_clearance=back_clearance)

CABINET_DEFINITIONS = {
    "BaseBox": {
        "class": BaseBox,
        "factory": None,
        "ui": {
            "label": "Base Cabinet",
            "enabled": True,
            "tooltip": "Add a base cabinet",
        },
        "params": {}

    },
    "BaseCorner": {
        "class": BaseCorner,
        "factory": make_base_corner,
        "ui": {
            "label": "Base Corner Cabinet",
            "enabled": False,
            "tooltip": "Add a base corner cabinet",
        },
        "params": {
            "cut_width": ("App::PropertyInteger", 300, "Cut Width"),
            "cut_depth": ("App::PropertyInteger", 200, "Cut Depth"),
            "l_r": ("App::PropertyString", "right", "Corner side (left or right)"),
            "with_polita": ("App::PropertyBool", True, "Has a shelf")
        }
    },
    "Raft": {
        "class": Raft,
        "factory": make_raft,
        "ui": {
            "label": "Open Base Shelving Unit",
            "enabled": False,
            "tooltip": "Add an open base shelving unit",
        },
        "params":{
            "shelves": ("App::PropertyInteger", 1, "Number of shelves included")
        }
    },
    "CorpCuPicioare": {
        "class": CorpCuPicioare,
        "factory": make_corp_cu_picioare,
        "ui": {
            "label": "Open Base Shelving Unit with Plinth",
            "enabled": False,
            "tooltip": "Add an open base shelving unit with a plinth",
        },
        "params": {
            "skirt_height": ("App::PropertyInteger", 100, "Plinth height"),
            "skirting_board": ("App::PropertyBool", True, "Include plinth"),
        }
    },
    "JollyBox": {
        "class": JollyBox,
        "factory": None,
        "ui": {
            "label": "Pull-out Base Cabinet",
            "enabled": False,
            "tooltip": "Add a pull-out base cabinet",
        },
        "params": {}
    },
    "SinkBox": {
        "class": SinkBox,
        "factory": None,
        "ui": {
            "label": "Base Sink",
            "enabled": False,
            "tooltip": "Add a sink cabinet",
        },
        "params": {}
    },
    "BaseCornerShelf": {
        "class": BaseCornerShelf,
        "factory": make_base_corner_shelf,
        "ui": {
            "label": "Base Corner Shelf",
            "enabled": False,
            "tooltip": "Add a base corner shelf cabinet",
        },
        "params": {
            "shelves": ("App::PropertyInteger", 1, "Number of shelves included"),
            "rounded": ("App::PropertyBool", False, "Rounded shelves"),
        }
    },
    "MsVBox": {
        "class": MsVBox,
        "factory": None,
        "ui": {
            "label": "Dishwasher Housing",
            "enabled": False,
            "tooltip": "Add a dishwasher housing",
        },
        "params": {}
    },
    "TopBox": {
        "class": TopBox,
        "factory": None,
        "ui": {
            "label": "Wall Cabinet",
            "enabled": True,
            "tooltip": "Add a wall cabinet",
        },
        "params": {}
    },
    "TopCorner": {
        "class": TopCorner,
        "factory": make_top_corner,
        "ui": {
            "label": "Wall Corner Cabinet",
            "enabled": False,
            "tooltip": "Add a wall corner cabinet",
        },
        "params": {
            "cut_width": ("App::PropertyInteger", 300, "Cut Width"),
            "cut_depth": ("App::PropertyInteger", 200, "Cut Depth"),
            "l_r": ("App::PropertyString", "right", "Corner side (left or right)"),
            "polite": ("App::PropertyInteger", 1, "Number of shelves included")
        }

    },
    "TowerBox": {
        "class": TowerBox,
        "factory": make_tower_box,
        "ui": {
            "label": "Tall Cabinet",
            "enabled": True,
            "tooltip": "Add a tall cabinet",
        },
        "params": {
            "gap_list": ("App::PropertyIntegerList", [200, 400], "Opening Heights (bottom to top)"),
            "gap_heat": ("App::PropertyInteger", 50, "Rear ventilation clearance"),
            "front_list": ("App::PropertyIntegerList", [0, 0, 0], "Fronts per opening (0 = open, 1 = front), bottom to top")
        },
    },
    "Etajera": {
        "class": Etajera,
        "factory": make_etajera,
        "ui": {
            "label": "Shelving Unit (Unavailable)",
            "enabled": False,
            "tooltip": "Add a shelving unit",
        },
        "params": {
            "shelves": ("App::PropertyInteger", 1, "Number of shelves included"),
        }


    },
    "Tower": {
        "class": CorpDressing,
        "factory": make_corp_dressing,
        "ui": {
            "label": "Tall Cabinet with Plinth",
            "enabled": True,
            "tooltip": "Add a tall cabinet with an integrated plinth",
        },
        "params": {
            "gap_list": ("App::PropertyIntegerList", [200, 400], "Opening Heights (bottom to top)"),
            "front_list": ("App::PropertyIntegerList", [0, 0, 0], "Fronts per opening (0 = open, 1 = front), bottom to top"),
        }
    },
    "Dulap": {
        "class": Dulap,
        "factory": None,
        "ui": {
            "label": "Wardrobe (Unavailable)",
            "enabled": False,
            "tooltip": "Add a wardrobe",
        },
        "params": {}
    },

    "Bar": {
        "class": Bar,
        "factory": make_bar,
        "ui": {
            "label": "Bar",
            "enabled": False,
            "tooltip": "Add a bar cabinet",
        },
        "params": {
            "front_clearance": ("App::PropertyInteger", 50, "Front clearance"),
            "back_clearance": ("App::PropertyInteger", 0, "Back clearance"),
        }

    },
    "Banca": {
        "class": Banca,
        "factory": make_bench,
        "ui": {
            "label": "Bench",
            "enabled": False,
            "tooltip": "Add a bench cabinet",
        },
        "params": {
            "gap_front": ("App::PropertyInteger", 50, "Gap for front"),
            "gap_lat": ("App::PropertyInteger", 50, "Gap for lateral"),
            "height_base": ("App::PropertyInteger", 100, "Height of base"),
        }
    }
}

__all__ = list(CABINET_DEFINITIONS.keys())
CABINETS = list(CABINET_DEFINITIONS.keys(), )

def get_enabled_ui_cabinets():
    return {
        name: data
        for name, data in CABINET_DEFINITIONS.items()
        if data["ui"].get("enabled", False)
    }

def get_cabinet_factory(cab_type):
    """
    Return a callable that creates a cabinet instance.
    The callable ALWAYS accepts (label, height, width, depth, rules, box=None)
    """
    data = CABINET_DEFINITIONS.get(cab_type)
    if not data:
        return None

    if not data["ui"].get("enabled", False):
        return None

    factory = data.get("factory")
    if factory:
        return factory

    # Default: wrap class constructor
    cls = data["class"]

    def _default_factory(label, height, width, depth, rules, box=None):
        return cls(label, height, width, depth, rules)

    return _default_factory


def get_cabinet_params(name):
    return CABINET_DEFINITIONS[name].get("params", {})
