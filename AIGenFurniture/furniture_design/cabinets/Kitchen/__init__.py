from .bar import Bar
from .base_box import BaseBox
from .base_corner import BaseCorner
from .base_corner_shelf import BaseCornerShelf
from .jolly_box import JollyBox
from .top_corner import TopCorner
from .msv_box import MsVBox
from .raft import Raft
from .sink_box import SinkBox
from .top_box import TopBox
from .top_corner import TopCorner
from .tower_box import TowerBox

__all__ = [
    # ... existing exported classes ...,
    "Bar", "BaseBox", "BaseCorner", "BaseCornerShelf", "JollyBox", "TopCorner", "MsVBox", "Raft", "SinkBox", "TopBox", "TopCorner", "TowerBox"
]

CABINETS = {name: globals()[name] for name in __all__}