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
META_KEYS = {"label", "active", "tooltip"} # all keys in the UI_CABINETS that are not parameters of the cabinets

UI_CABINETS = {
    # BaseCabinet
    "BaseBox": {
        "label": "Base Cabinet",
        "active": True,
        "tooltip": "Add a base cabinet",
    },
    "BaseCorner": {
        "label": "Base Corner",
        "active": True,
        "tooltip": "Add a base corner cabinet",
        "cut_width": ("App::PropertyInteger", 300, "Cut Width"),
        "cut_depth": ("App::PropertyInteger", 200, "Cut Depth"),
        "l_r": ("App::PropertyString", "right", "left or right Corner"),
        "with_polita": ("App::PropertyBool", True, "Has a shelf")
    },
    #BaseShelf
    "Raft": {
        "label": "Base Shelf",
        "active": True,
        "tooltip": "Add a shelf unit (Raft)",
        "shelves": ("App::PropertyInteger", 1, "Number of shelves included")
    },
    # Base Shelf with Skirt
    "CorpCuPicioare": {
        "label": "Base Shelf with Skirt",
        "active": True,
        "tooltip": "Add a cabinet with legs (CorpCuPicioare)",
        "skirt_height": ("App::PropertyInteger", 100, "Height of skirting area"),
        "skirting_board": ("App::PropertyBool", True, "Has a skirting board"),
    },
    #BaseJolly
    "JollyBox": {
        "label": "Base Jolly",
        "active": True,
        "tooltip": "Add a JollyBox cabinet",
    },
    # BaseSink
    "SinkBox": {
        "label": "Base Sink",
        "active": True,
        "tooltip": "Add a sink cabinet",
    },
    "BaseCornerShelf": {
        "label": "Base Corner Shelf",
        "active": True,
        "tooltip": "Add a base corner shelf cabinet",
        "shelves": ("App::PropertyInteger", 1, "Number of shelves included"),
        "rounded": ("App::PropertyBool", False, "Rounded shelves"),
    },
    # Dishwasher
    "MsVBox": {
        "label": "Dishwasher",
        "active": True,
        "tooltip": "Add a MsVBox cabinet",
    },
    #TopCabinet
    "TopBox": {
        "label": "Top Cabinet",
        "active": True,
        "tooltip": "Add a top box cabinet",
    },
    "TopCorner": {
        "label": "Top Corner",
        "active": True,
        "tooltip": "Add a top corner cabinet",
        "cut_width": ("App::PropertyInteger", 300, "Cut Width"),
        "cut_depth": ("App::PropertyInteger", 200, "Cut Depth"),
        "l_r": ("App::PropertyString", "right", "Left or Right Corner"),
        "polite": ("App::PropertyInteger", 1, "Number of shelves included")
    },
    #Tower
    "TowerBox": {
        "label": "Tower",
        "active": True,
        "tooltip": "Add a tower cabinet",
        "gap_list": ("App::PropertyIntegerList", [200, 400], "Gap List"),
        "gap_heat": ("App::PropertyInteger", 50, "Gap for heat dissipation on the back of the cabinet"),
        "front_list": ("App::PropertyIntegerList", [0, 0, 0, 0], "List which gaps should be closed by doors")
    },
    "Etajera": {
        "label": "Etajera (n.a)",
        "active": False,
        "tooltip": "Add an Etajera (shelf unit)",
        "shelves": ("App::PropertyInteger", 1, "Number of shelves included"),
    },
    #Tower with Skirt
    "CorpDressing": {
        "label": "Tower with skirt",
        "active": True,
        "tooltip": "Add a wardrobe cabinet",
        "gap_list": ("App::PropertyIntegerList", [200, 400], "Gap List"),
        "front_list": ("App::PropertyIntegerList", [0, 0, 0, 0], "List which gaps should be closed by doors"),
    },
    "Dulap": {
        "label": "Base Cabinet",
        "active": False,
        "tooltip": "Add a simple closet (Dulap)",
    },

    "Bar": {
        "label": "Bar",
        "active": True,
        "tooltip": "Add a bar cabinet",
    },
    # Bench
    "Banca": {
        "label": "Bench",
        "active": True,
        "tooltip": "Add a bench cabinet",
        "gap_front": ("App::PropertyInteger", 50, "Gap for front"),
        "gap_lat": ("App::PropertyInteger", 50, "Gap for lateral"),
        "height_base": ("App::PropertyInteger", 100, "Height of base"),
    }
}

__all__ = [
    "Banca",
    "Bar",
    "BaseBox",
    "BaseCorner",
    "BaseCornerShelf",
    "CorpCuPicioare",
    "CorpDressing",
    "Dulap",
    "Etajera",
    "JollyBox",
    "MsVBox",
    "Raft",
    "SinkBox",
    "TopBox",
    "TopCorner",
    "TowerBox",
]

# Generic registry: all cabinets that follow the standard constructor
_GENERIC_CABINETS = {
    "Bar": Bar,
    "BaseBox": BaseBox,
    "Dulap": Dulap,
    "JollyBox": JollyBox,
    "MsVBox": MsVBox,
    "SinkBox": SinkBox,
    "TopBox": TopBox,
}

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

_SPECIAL_CABINETS = {
    "Banca": make_bench,
    "BaseCorner": make_base_corner,
    "BaseCornerShelf": make_base_corner_shelf,
    "CorpCuPicioare": make_corp_cu_picioare,
    "CorpDressing": make_corp_dressing,
    "Etajera": make_etajera,
    "Raft": make_raft,
    "TopCorner": make_top_corner,
    "TowerBox": make_tower_box,
}

# Unified registry
CABINETS = {}
CABINETS.update(_GENERIC_CABINETS)
CABINETS.update(_SPECIAL_CABINETS)
