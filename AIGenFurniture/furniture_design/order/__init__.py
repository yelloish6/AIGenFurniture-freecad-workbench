# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
# AIGenFurniture/furniture_design/order/__init__.py
"""
Order module - re-exports for backward compatibility.

Maintains existing import paths:
    from AIGenFurniture.furniture_design.order import Order
    from AIGenFurniture.furniture_design.order import ORDER_PARAMS
"""

from .order import Order
from .order_params import (
    ORDER_PARAMS,
    get_order_param_names,
    get_enabled_order_params,
    get_enabled_param_names,
    get_required_params,
    get_order_attr_mapping,
    validate_order
)

__all__ = [
    "Order",
    "ORDER_PARAMS",
    "get_order_param_names",
    "get_enabled_order_params",
    "get_enabled_param_names",
    "get_required_params",
    "get_order_attr_mapping",
    "validate_order"
]
