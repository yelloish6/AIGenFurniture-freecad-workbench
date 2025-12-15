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

# TODO: rules need to be moved to FreeCAD as a new sheet, or include it in the existing OrderVar sheet

# Special cases: cabinets that require extra arguments
def make_base_corner_shelf(label, height, width, depth, rules, box=None):
    """Factory for BaseCornerShelf with extra shelves parameter."""
    # Read shelves count from the box if present, otherwise default = 3
    shelves = getattr(box, "shelves", 3)
    rounded = getattr(box, "rounded", False)
    return BaseCornerShelf(label, height, width, depth, rules, shelves=shelves, rounded=rounded)

def make_base_corner(label, height, width, depth, rules, box=None):
    """Factory for BaseCorner with extra cut_width, cut_depth, l_r, with_polita parameters."""
    cut_width = getattr(box, "cut_width", 0)
    cut_depth = getattr(box, "cut_depth", 0)
    l_r = getattr(box, "l_r", 0)
    with_polita = getattr(box, "with_polita", True)
    return BaseCorner(label, height, width, depth, rules, cut_width, cut_depth, l_r, with_polita)

def make_top_corner(label, height, width, depth, rules, box=None):
    """Factory for TopCorner with extra cut_width, cut_depth, l_r, with_polita parameters."""
    cut_width = getattr(box, "cut_width", 0)
    cut_depth = getattr(box, "cut_depth", 0)
    l_r = getattr(box, "l_r", 0)
    polite = getattr(box, "polite", 1)
    return TopCorner(label, height, width, depth, rules, cut_width, cut_depth, l_r, polite)

def make_raft(label, height, width, depth, rules, box=None):
    """Factory for BaseCornerShelf with extra shelves parameter."""
    # Read shelves count from the box if present, otherwise default = 3
    shelves = getattr(box, "shelves", 3)
    return Raft(label, height, width, depth, rules, shelves=shelves)

def make_tower_box(label, height, width, depth, rules, box=None):
    """Factory for TowerBox with extra tower_height parameter."""
    gap_list = getattr(box, "gap_list", [20, 40])
    gap_heat = getattr(box, "gap_heat", 50)
    front_list = getattr(box, "front_list", [0, 0, 0, 0])
    return TowerBox(label, height, width, depth, rules, gap_list = gap_list, gap_heat = gap_heat, front_list = front_list)

def make_corp_cu_picioare(label, height, width, depth, rules, box=None):
    """Factory for CorpCuPicioare with extra shelves parameter."""
    h_skirt = getattr(box, "skirt_height", 100)
    has_skirting_board = getattr(box, "skirting_board", True)
    return CorpCuPicioare(label, height, width, depth, rules, h_skirt=h_skirt, has_skirting_board=has_skirting_board)

def make_corp_dressing(label, height, width, depth, rules, box=None):
    """Factory for Corp Dressing with extra parameter."""
    gap_list = getattr(box, "gap_list", [200, 400])
    front_list = getattr(box, "front_list", [0, 0, 0, 0])
    return CorpDressing(label, height, width, depth, rules, gap_list = gap_list, front_list = front_list)

def make_etajera(label, height, width, depth, rules, box=None):
    """Factory for Etajera with extra shelves parameter."""
    # Read shelves count from the box if present, otherwise default = 3
    shelves = getattr(box, "shelves", 3)
    return Etajera(label, height, width, depth, rules, shelves=shelves)

def make_bench(label, height, width, depth, rules, box=None):
    """Factory for Bench with extra parameters."""
    gap_front = getattr(box, "gap_front")
    gap_lat = getattr(box, "gap_lat")
    height_base = getattr(box, "height_base")
    return Banca(label, height, width, depth, rules, gap_front = gap_front, gap_lat = gap_lat, height_base = height_base)

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
            "label": "Base Corner",
            "enabled": True,
            "tooltip": "Add a base corner cabinet",
        },
        "params": {
            "cut_width": ("App::PropertyInteger", 300, "Cut Width"),
            "cut_depth": ("App::PropertyInteger", 200, "Cut Depth"),
            "l_r": ("App::PropertyString", "right", "left or right Corner"),
            "with_polita": ("App::PropertyBool", True, "Has a shelf")
        }
    },
    "Raft": {
        "class": Raft,
        "factory": make_raft,
        "ui": {
            "label": "Base Shelf",
            "enabled": True,
            "tooltip": "Add a shelf unit (Raft)",
        },
        "params":{
            "shelves": ("App::PropertyInteger", 1, "Number of shelves included")
        }
    },
    "CorpCuPicioare": {
        "class": CorpCuPicioare,
        "factory": make_corp_cu_picioare,
        "ui": {
            "label": "Base Shelf with Skirt",
            "enabled": True,
            "tooltip": "Add a cabinet with legs (CorpCuPicioare)",
        },
        "params": {
            "skirt_height": ("App::PropertyInteger", 100, "Height of skirting area"),
            "skirting_board": ("App::PropertyBool", True, "Has a skirting board"),
        }
    },
    "JollyBox": {
        "class": JollyBox,
        "factory": None,
        "ui": {
            "label": "Base Jolly",
            "enabled": True,
            "tooltip": "Add a JollyBox cabinet",
        },
        "params": {}
    },
    "SinkBox": {
        "class": SinkBox,
        "factory": None,
        "ui": {
            "label": "Base Sink",
            "enabled": True,
            "tooltip": "Add a sink cabinet",
        },
        "params": {}
    },
    "BaseCornerShelf": {
        "class": BaseCornerShelf,
        "factory": make_base_corner_shelf,
        "ui": {
            "label": "Base Corner Shelf",
            "enabled": True,
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
            "label": "Dishwasher",
            "enabled": True,
            "tooltip": "Add a MsVBox cabinet",
        },
        "params": {}
    },
    "TopBox": {
        "class": TopBox,
        "factory": None,
        "ui": {
            "label": "Top Cabinet",
            "enabled": True,
            "tooltip": "Add a top box cabinet",
        },
        "params": {}
    },
    "TopCorner": {
        "class": TopCorner,
        "factory": make_top_corner,
        "ui": {
            "label": "Top Corner",
            "enabled": True,
            "tooltip": "Add a top corner cabinet",
        },
        "params": {
            "cut_width": ("App::PropertyInteger", 300, "Cut Width"),
            "cut_depth": ("App::PropertyInteger", 200, "Cut Depth"),
            "l_r": ("App::PropertyString", "right", "Left or Right Corner"),
            "polite": ("App::PropertyInteger", 1, "Number of shelves included")
        }

    },
    "TowerBox": {
        "class": TowerBox,
        "factory": make_tower_box,
        "ui": {
            "label": "Tower",
            "enabled": True,
            "tooltip": "Add a tower cabinet",
        },
        "params": {
            "gap_list": ("App::PropertyIntegerList", [200, 400], "Gap List"),
            "gap_heat": ("App::PropertyInteger", 50, "Gap for heat dissipation on the back of the cabinet"),
            "front_list": ("App::PropertyIntegerList", [0, 0, 0, 0], "List which gaps should be closed by doors")
        },
    },
    "Etajera": {
        "class": Etajera,
        "factory": make_etajera,
        "ui": {
            "label": "Etajera (n.a)",
            "enabled": True,
            "tooltip": "Add an Etajera (shelf unit)",
        },
        "params": {
            "shelves": ("App::PropertyInteger", 1, "Number of shelves included"),
        }


    },
    "CorpDressing": {
        "class": CorpDressing,
        "factory": make_corp_dressing,
        "ui": {
            "label": "Tower with skirt",
            "enabled": True,
            "tooltip": "Add a wardrobe cabinet",
        },
        "params": {
            "gap_list": ("App::PropertyIntegerList", [200, 400], "Gap List"),
            "front_list": ("App::PropertyIntegerList", [0, 0, 0, 0], "List which gaps should be closed by doors"),
        }
    },
    "Dulap": {
        "class": Dulap,
        "factory": None,
        "ui": {
            "label": "Base Cabinet (n.a)",
            "enabled": True,
            "tooltip": "Add a simple closet (Dulap)",
        },
        "params": {}
    },

    "Bar": {
        "class": Bar,
        "factory": None,
        "ui": {
            "label": "Bar",
            "enabled": True,
            "tooltip": "Add a bar cabinet",
        },
        "params": {}

    },
    "Banca": {
        "class": Banca,
        "factory": make_bench,
        "ui": {
            "label": "Bench",
            "enabled": True,
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
