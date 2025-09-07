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
    gap_list = getattr(box, "tower_height", [20, 40])
    gap_heat = getattr(box, "gap_heat", 50)
    front_list = getattr(box, "front_list", [0, 0, 0, 0])
    return TowerBox(label, height, width, depth, rules, gap_list = [20, 40], gap_heat = 50, front_list = [0, 0, 0, 0])

def make_corp_cu_picioare(label, height, width, depth, rules, box=None):
    """Factory for CorpCuPicioare with extra shelves parameter."""
    plinta = getattr(box, "plinta", 100)
    return CorpCuPicioare(label, height, width, depth, rules, plinta=plinta)

def make_corp_dressing(label, height, width, depth, rules, box=None):
    """Factory for Corp Dressing with extra tower_height parameter."""
    gap_list = getattr(box, "tower_height", [20, 40])
    front_list = getattr(box, "front_list", [0, 0, 0, 0])
    return TowerBox(label, height, width, depth, rules, gap_list = [20, 40], front_list = [0, 0, 0, 0])

def make_etajera(label, height, width, depth, rules, box=None):
    """Factory for Etajera with extra shelves parameter."""
    # Read shelves count from the box if present, otherwise default = 3
    shelves = getattr(box, "shelves", 3)
    return Raft(label, height, width, depth, rules, shelves=shelves)

def make_bench(label, height, width, depth, rules, box=None):
    """Factory for Bench with extra parameters."""
    gap_front = getattr(box, "gap_front", 50)
    gap_lat = getattr(box, "gap_lat", 50)
    height_base = getattr(box, "height_base", 100)
    return Banca(label, height, width, depth, rules, gap_front = 50, gap_lat = 50, height_base = 100)

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
