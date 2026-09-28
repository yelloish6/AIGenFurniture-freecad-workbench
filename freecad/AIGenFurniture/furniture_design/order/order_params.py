# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
# AIGenFurniture/furniture_design/order/order_params.py
"""
Centralized definition of all order-level parameters (schema only).

This module defines ORDER_PARAMS and validation helpers, separated from
Order class logic to avoid circular imports and maintain clean separation.
"""

from collections import OrderedDict

# ORDER_PARAMS: Single source of truth for all order parameters
# Using OrderedDict to ensure deterministic ordering for spreadsheet generation
# All numeric defaults are stored as strings (they are spreadsheet cell values)
# Type conversion happens only when initializing Order objects
# enabled flag controls MVP inclusion (same pattern as ELEMENTS and CABINETS)

ORDER_PARAMS = OrderedDict([
    # Customer information
    ("client", {
        "default": "",
        "required": True,
        "label": "Customer Name",
        "type": "string",
        "order_attr": "client",
        "order": 1,
        "enabled": True  # MVP: used in exports and filenames
    }),
    ("client_proficut", {
        "default": "",
        "required": False,
        "label": "Company Name",
        "type": "string",
        "order_attr": "client_proficut",
        "order": 2,
        "enabled": False  # Reserved for shop-specific export plugins
    }),
    ("tel_proficut", {
        "default": "",
        "required": False,
        "label": "Company Phone",
        "type": "string",
        "order_attr": "tel_proficut",
        "order": 3,
        "enabled": False  # Reserved for shop-specific export plugins
    }),
    ("transport", {
        "default": False,
        "required": False,
        "label": "Transport",
        "type": "bool",
        "order_attr": "transport",
        "order": 4,
        "enabled": False  # MVP: used in cost calculation
    }),
    ("address", {
        "default": "",
        "required": False,
        "label": "Delivery Address",
        "type": "string",
        "order_attr": "address",
        "order": 5,
        "enabled": False  # Reserved for shop-specific export plugins
    }),
    
    # Dimension parameters
    ("h_bucatarie", {
        "default": "2400",  # String default for spreadsheet; converted in Order.__init__
        "required": False,
        "label": "Kitchen Height (mm)",
        "type": "number",
        "order_attr": "h_bucatarie",
        "order": 10,
        "enabled": False  # MVP: not used in enabled exports
    }),
    ("h_faianta_top", {
        "default": "700",  # String default for spreadsheet; converted in Order.__init__
        "required": False,
        "label": "Top Backsplash Height (mm)",
        "type": "number",
        "order_attr": "h_faianta_top",
        "order": 11,
        "enabled": False  # MVP: not used in enabled exports
    }),
    ("h_faianta_base", {
        "default": "600",  # String default for spreadsheet; converted in Order.__init__
        "required": False,
        "label": "Base Backsplash Height (mm)",
        "type": "number",
        "order_attr": "h_faianta_base",
        "order": 12,
        "enabled": False  # MVP: not used in enabled exports
    }),
    ("depth_base", {
        "default": "600",  # String default for spreadsheet; converted in Order.__init__
        "required": False,
        "label": "Base Depth (mm)",
        "type": "number",
        "order_attr": "depth_base",
        "order": 13,
        "enabled": False  # MVP: not used in enabled exports
    }),
    ("top_height", {
        "default": "720",  # String default for spreadsheet; converted in Order.__init__
        "required": False,
        "label": "Top Height (mm)",
        "type": "number",
        "order_attr": "top_height",
        "order": 14,
        "enabled": False  # MVP: not used in enabled exports
    }),
    ("top_height_2", {
        "default": "720",  # String default for spreadsheet; converted in Order.__init__
        "required": False,
        "label": "Top Height 2 (mm)",
        "type": "number",
        "order_attr": "top_height_2",
        "order": 15,
        "enabled": False  # MVP: not used in enabled exports
    }),
    ("top_depth", {
        "default": "300",  # String default for spreadsheet; converted in Order.__init__
        "required": False,
        "label": "Top Depth (mm)",
        "type": "number",
        "order_attr": "top_depth",
        "order": 16,
        "enabled": False  # MVP: not used in enabled exports
    }),
    ("top_depth_2", {
        "default": "300",  # String default for spreadsheet; converted in Order.__init__
        "required": False,
        "label": "Top Depth 2 (mm)",
        "type": "number",
        "order_attr": "top_depth_2",
        "order": 17,
        "enabled": False  # MVP: not used in enabled exports
    }),
    ("cuptor_height", {
        "default": "600",  # String default for spreadsheet; converted in Order.__init__
        "required": False,
        "label": "Oven Height (mm)",
        "type": "number",
        "order_attr": "cuptor_height",
        "order": 19,
        "enabled": False  # MVP: not used in enabled exports
    }),
    ("MsV_height_min", {
        "default": "500",  # String default for spreadsheet; converted in Order.__init__
        "required": False,
        "label": "Dishwasher Min Height (mm)",
        "type": "number",
        "order_attr": "MsV_height_min",
        "order": 20,
        "enabled": False  # MVP: not used in enabled exports
    }),
    ("MsV_height_max", {
        "default": "1200",  # String default for spreadsheet; converted in Order.__init__
        "required": False,
        "label": "Dishwasher Max Height (mm)",
        "type": "number",
        "order_attr": "MsV_height_max",
        "order": 21,
        "enabled": False  # MVP: not used in enabled exports
    }),
    
    # Material parameters
    ("material_pal", {
        "default": "White Chipboard",
        "required": False,
        "label": "Chipboard Material",
        "type": "string",
        "order_attr": "mat_pal",
        "order": 30,
        "enabled": True  # MVP: used in cost calculations
    }),
    ("material_front", {
        "default": "White Front Panel",
        "required": False,
        "label": "Front Material",
        "type": "string",
        "order_attr": "mat_front",
        "order": 31,
        "enabled": True  # MVP: used in cost calculations
    }),
    ("material_blat", {
        "default": "Oak-effect Countertop",
        "required": False,
        "label": "Countertop Material",
        "type": "string",
        "order_attr": "mat_blat",
        "order": 32,
        "enabled": True  # MVP: used in cost calculations
    }),
    ("material_pfl", {
        "default": "White HDF",
        "required": False,
        "label": "HDF Material",
        "type": "string",
        "order_attr": "mat_pfl",
        "order": 33,
        "enabled": True  # MVP: used in cost calculations
    }),
    
    # Business parameters
    ("h_rate", {
        "default": "120",  # String default for spreadsheet; converted in Order.__init__
        "required": False,
        "label": "Hourly Rate",
        "type": "number",
        "order_attr": "h_rate",
        "order": 40,
        "enabled": False  # MVP: used in labour cost calculation
    }),
    ("h_proiect", {
        "default": "8",  # String default for spreadsheet; converted in Order.__init__
        "required": False,
        "label": "Project Hours",
        "type": "number",
        "order_attr": "h_proiect",
        "order": 41,
        "enabled": False  # MVP: used in labour cost calculation
    }),
    ("discount", {
        "default": "0",  # String default for spreadsheet; converted in Order.__init__
        "required": False,
        "label": "Discount (%)",
        "type": "number",
        "order_attr": "discount",
        "order": 42,
        "enabled": False  # MVP: used in cost calculation
    }),
    ("nr_electrocasnice", {
        "default": "4",  # String default for spreadsheet; converted in Order.__init__
        "required": False,
        "label": "Number of Appliances",
        "type": "number",
        "order_attr": "nr_electrocasnice",
        "order": 43,
        "enabled": False  # MVP: used in labour cost calculation
    })
])


def get_order_param_names():
    """Return list of all order parameter names in deterministic order."""
    return list(ORDER_PARAMS.keys())


def get_enabled_order_params():
    """Return dict of enabled order parameters (same pattern as ELEMENTS and CABINETS)."""
    return {
        name: param
        for name, param in ORDER_PARAMS.items()
        if param.get("enabled", False)
    }


def get_enabled_param_names():
    """Return list of enabled order parameter names in deterministic order."""
    return [
        name for name, param in ORDER_PARAMS.items()
        if param.get("enabled", False)
    ]


def get_required_params():
    """Return list of required parameter names (only enabled ones)."""
    return [
        name for name, param in ORDER_PARAMS.items()
        if param.get("required", False) and param.get("enabled", False)
    ]


def get_order_attr_mapping():
    """Return mapping from param name to Order class attribute name."""
    return {
        name: param.get("order_attr", name)
        for name, param in ORDER_PARAMS.items()
    }


def validate_order(order_obj):
    """
    Validate that an Order object has all required parameters set.
    
    Checks all required parameters and collects all missing ones before returning.
    
    Args:
        order_obj: Order instance to validate
        
    Returns:
        tuple: (is_valid: bool, missing_params: list)
    """
    missing = []
    required = get_required_params()
    attr_mapping = get_order_attr_mapping()
    
    # Check all required parameters and collect all missing ones
    for param_name in required:
        attr_name = attr_mapping.get(param_name, param_name)
        value = getattr(order_obj, attr_name, None)
        
        # Check if value is None, empty string, or empty after stripping
        if value is None or (isinstance(value, str) and not value.strip()):
            missing.append(param_name)
    
    # Return after checking all parameters
    is_valid = len(missing) == 0
    return is_valid, missing


__all__ = [
    "ORDER_PARAMS",
    "get_order_param_names",
    "get_enabled_order_params",
    "get_enabled_param_names",
    "get_required_params",
    "get_order_attr_mapping",
    "validate_order"
]
