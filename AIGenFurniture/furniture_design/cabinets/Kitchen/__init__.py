from .bar import Bar
from .base_box import BaseBox
from .base_corner import BaseCorner
from .base_corner_shelf import BaseCornerShelf
from .jolly_box import JollyBox
from .msv_box import MsVBox
from .raft import Raft
from .sink_box import SinkBox
from .top_box import TopBox
from .top_corner import TopCorner
from .tower_box import TowerBox

__all__ = [
    "Bar",
    "BaseBox",
    "BaseCorner",
    "BaseCornerShelf",
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
    "JollyBox": JollyBox,
    "MsVBox": MsVBox,
    "SinkBox": SinkBox,
    "TopBox": TopBox,
}

# Special cases: cabinets that require extra arguments
def make_base_corner_shelf(label, height, width, depth, rules, box=None):
    """Factory for BaseCornerShelf with extra shelves parameter."""
    # Read shelves count from the box if present, otherwise default = 3
    shelves = getattr(box, "Shelves", 3)
    return BaseCornerShelf(label, height, width, depth, rules, shelves=shelves)

def make_base_corner(label, height, width, depth, rules, box=None):
    """Factory for BaseCorner with extra cut_width, cut_depth, l_r, with_polita parameters."""
    cut_width = getattr(box, "cut_width", 0)
    cut_depth = getattr(box, "cut_depth", 0)
    l_r = getattr(box, "l_r", 0)
    with_polita = getattr(box, "with_polita", True)
    return BaseCorner(label, height, width, depth, rules, cut_width, cut_depth, l_r, with_polita)

_SPECIAL_CABINETS = {
    "BaseCorner": make_base_corner,
    "BaseCornerShelf": make_base_corner_shelf,
    "Raft": Raft,
    "TopCorner": TopCorner,
    "TowerBox": TowerBox,
}

# Unified registry
CABINETS = {}
CABINETS.update(_GENERIC_CABINETS)
CABINETS.update(_SPECIAL_CABINETS)
