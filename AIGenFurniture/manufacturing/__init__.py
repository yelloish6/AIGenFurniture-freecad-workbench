EXPORT_DEFINITIONS = {
    "export_pal_for_proficut":{
        "enabled": True,
        "runner": "export_pal_for_proficut",
        "module": "export_for_proficut",
    },
    "export_pfl_for_proficut": {
        "enabled": True,
        "runner": "export_pfl_for_proficut",
        "module": "export_for_proficut",
    },
    "export_front_for_nettfront": {
        "enabled": True,
        "runner": "export_front_for_nettfront",
        "module": "export_for_nettfront",
    },
    "export_csv": {
        "enabled": True,
        "runner": "export_csv",
        "module": "export_csv",
    },
    "export_stl": {
        "enabled": True,
        "runner": "export_stl_order",
        "module": "export_stl_new",
    },
    "export_cost_sheet":{
        "enabled": True,
        "runner": "export_cost_sheet",
        "module": "generate_offer_cost",
    },
    "print_order_summary":{
        "enabled": True,
        "runner": "print_order_summary",
        "module": "generate_offer_cost",
    },
    "generate_offer_file":{
        "enabled": True,
        "runner": "generate_offer_file",
        "module": "generate_offer_cost",
    },
    "generate_assembly_file":{
        "enabled": True,
        "runner": "generate_assembly_file",
        "module": "generate_assembly_file",
    },
    "generate_drill_file":{
        "enabled": True,
        "runner": "generate_drill_file",
        "module": "generate_assembly_file",
    },
    "generate_drill_pdf_reportlab":{
        "enabled": True,
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

# export_pal_for_proficut(order, output_path)
# export_pfl_for_proficut(order, output_path)
# export_front_for_nettfront(order, output_path)
# export_csv(order, output_path)
# export_stl_order(order, output_path, is_horizontal_layout=False)
# export_cost_sheet(order, output_path)
# print_order_summary(order)
# generate_offer_file(order, output_path)
# generate_assembly_file(order, output_path)
# generate_drill_file(order, output_path)
# generate_drill_pdf_reportlab(order, output_path)