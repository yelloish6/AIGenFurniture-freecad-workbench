# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
# AIGenFurniture/manufacturing/__init__.py

# Schema version for EXPORT_DEFINITIONS structure
# Increment when the structure of EXPORT_DEFINITIONS changes (e.g., new required fields, renamed keys)
# This enables backward compatibility and migration logic in future releases
EXPORT_DEFINITIONS_SCHEMA_VERSION = "1.0"

EXPORT_DEFINITIONS = {
    "export_csv": {
        "enabled": True,
        "runner": "export_csv",
        "module": "export_csv",
        "kwargs": {
            "elements_registry": "elements_registry",
        },
    },
    "export_stl": {
        "enabled": True,
        "runner": "export_stl_order",
        "module": "export_stl_new",
        "kwargs": {
            "is_horizontal_layout": "stl.is_horizontal_layout",
        },
    }
}

def get_active_exports():
    return {
        name: data
        for name, data in EXPORT_DEFINITIONS.items()
        if data.get("enabled", False)
    }
