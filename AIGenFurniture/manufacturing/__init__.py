EXPORT_DEFINITIONS = {
    "export_pal_for_proficut":{
        "enabled": False,
        "runner": "export_pal_for_proficut",
        "module": "export_for_proficut",
    },
    "export_pfl_for_proficut": {
        "enabled": False,
        "runner": "export_pfl_for_proficut",
        "module": "export_for_proficut",
    },
    "export_front_for_nettfront": {
        "enabled": False,
        "runner": "export_front_for_nettfront",
        "module": "export_for_nettfront",
    },
    "export_csv": {
        "enabled": True,
        "runner": "export_csv",
        "module": "export_csv",
    },
    "export_stl": {
        "enabled": False,
        "runner": "export_stl_order",
        "module": "export_stl_new",
    },
    "export_cost_sheet":{
        "enabled": False,
        "runner": "export_cost_sheet",
        "module": "generate_offer_cost",
    },
    "print_order_summary":{
        "enabled": False,
        "runner": "print_order_summary",
        "module": "generate_offer_cost",
    },
    "generate_offer_file":{
        "enabled": False,
        "runner": "generate_offer_file",
        "module": "generate_offer_cost",
    },
    "generate_assembly_file":{
        "enabled": False,
        "runner": "generate_assembly_file",
        "module": "generate_assembly_file",
    },
    "generate_drill_file":{
        "enabled": False,
        "runner": "generate_drill_file",
        "module": "generate_assembly_file",
    },
    "generate_drill_pdf_reportlab":{
        "enabled": False,
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
