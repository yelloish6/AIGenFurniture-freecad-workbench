# ... existing code ...
from .corp_cu_picioare import CorpCuPicioare
from .banca import Banca
from .corp_dressing import CorpDressing
from .dulap import Dulap
from .etajera import Etajera
# from .tower_box import TowerBox

__all__ = [
    # ... existing exported classes ...,
    "CorpCuPicioare", "Banca", "CorpDressing", "Dulap", "Etajera"
]

CABINETS = {name: globals()[name] for name in __all__}

# # Optional registry (handy for factories)
# try:
#     CABINETS  # if already defined, extend it
# except NameError:
#     CABINETS = {}
# CABINETS["CorpCuPicioare"] = CorpCuPicioare
# # ... existing code ...