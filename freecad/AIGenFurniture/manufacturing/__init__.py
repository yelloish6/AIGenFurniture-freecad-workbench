# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
# AIGenFurniture/manufacturing/__init__.py

# Schema version for EXPORT_DEFINITIONS structure
# Increment when the structure of EXPORT_DEFINITIONS changes (e.g., new required fields, renamed keys)
# This enables backward compatibility and migration logic in future releases
EXPORT_DEFINITIONS_SCHEMA_VERSION = "1.0"

EXPORT_DEFINITIONS = {
    # this export is shop-specific for my shop. Should not be part of any release
    "export_pal_for_proficut":{
        "enabled": True, #False for MVP
        "runner": "export_pal_for_proficut",
        "module": "export_for_proficut",
    },
    # this export is shop-specific for my shop. Should not be part of any release
    "export_pfl_for_proficut": {
        "enabled": True, #False for MVP
        "runner": "export_pfl_for_proficut",
        "module": "export_for_proficut",
    },
    # this export is shop-specific for my shop. Should not be part of any release
    "export_front_for_nettfront": {
        "enabled": True, #False for MVP
        "runner": "export_front_for_nettfront",
        "module": "export_for_nettfront",
    },
    # this export is generic. It outputs all elements that inherit Board class,
    "export_csv": {
        "enabled": True, #True for MVP
        "runner": "export_csv",
        "module": "export_csv",
    },
    # this export is generic for all projects
    "export_stl": {
        "enabled": True, #False for MVP
        "runner": "export_stl_order",
        "module": "export_stl_new",
    },
    # this export is generic for all elements
    "export_cost_sheet":{
        "enabled": False, #False for MVP
        "runner": "export_cost_sheet",
        "module": "generate_offer_cost",
    },
    # this is shop specific - each shop will want a different type of print
    "print_order_summary":{
        "enabled": False, #False for MVP
        "runner": "print_order_summary",
        "module": "generate_offer_cost",
    },
    # this is shop specific - each shop will want a different offer file format
    "generate_offer_file":{
        "enabled": False, #False for MVP
        "runner": "generate_offer_file",
        "module": "generate_offer_cost",
    },
    # this is shop specific - each shop will want a different offer file format
    "generate_assembly_file":{
        "enabled": False, #False for MVP
        "runner": "generate_assembly_file",
        "module": "generate_assembly_file",
    },
    # this is shop specific - each shop will want a different offer file format
    "generate_drill_file":{
        "enabled": False, #False for MVP
        "runner": "generate_drill_file",
        "module": "generate_assembly_file",
    },
    # this is shop specific - each shop will want a different offer file format
    "generate_drill_pdf_reportlab":{
        "enabled": False, #False for MVP
        "runner": "generate_drill_pdf_reportlab",
        "module": "generate_assembly_file_reportlab",
    }
}

def get_active_exports():
    return {
        name: data
        for name, data in EXPORT_DEFINITIONS.items()
        if data.get("enabled", False)
    }
