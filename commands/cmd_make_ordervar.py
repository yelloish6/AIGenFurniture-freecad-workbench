import FreeCAD as App
import FreeCADGui as Gui

def create_globals_spreadsheet(doc):
    """Create a spreadsheet with all global_aliases prefilled and aliases set."""

    # List of global aliases (same as JSON exporter)
    global_aliases = [
        "client", "client_proficut", "tel_proficut", "transport", "address",
        "h_bucatarie", "h_faianta_top", "h_faianta_base", "depth_base",
        "top_height", "top_height_2", "top_depth", "top_depth_2",
        "blat_height", "cuptor_height", "MsV_height_min", "MsV_height_max",
        "material_pal", "material_front", "material_blat", "material_pfl",
        "h_rate", "h_proiect", "discount", "nr_electrocasnice"
    ]

    # Default values for each alias (adapt as needed)
    defaults = {
        "client": "Nume Client",
        "client_proficut": "Your Company",
        "tel_proficut": "07xxxxxxxx",
        "transport": "Da",
        "address": "Adresa Client",
        "h_bucatarie": "2400",       # mm
        "h_faianta_top": "700",      # mm
        "h_faianta_base": "600",     # mm
        "depth_base": "600",         # mm
        "top_height": "720",         # mm
        "top_height_2": "720",       # mm
        "top_depth": "300",          # mm
        "top_depth_2": "300",        # mm
        "blat_height": "40",         # mm
        "cuptor_height": "600",      # mm
        "MsV_height_min": "500",     # mm
        "MsV_height_max": "1200",    # mm
        "material_pal": "Alb W962ST2",
        "material_front": "A34R3",
        "material_blat": "Stejar Alpin Keindl",
        "material_pfl": "Alb",
        "h_rate": "120",
        "h_proiect": "8",
        "discount": "0",
        "nr_electrocasnice": "4"
    }

    # Check if spreadsheet "OrderVar" already exists
    spreadsheet = None
    for obj in doc.Objects:
        if obj.TypeId == "Spreadsheet::Sheet" and obj.Label == "OrderVar":
            spreadsheet = obj
            break

    if not spreadsheet:
        spreadsheet = doc.addObject("Spreadsheet::Sheet", "OrderVar")

    # Fill spreadsheet
    row = 1
    for alias in global_aliases:
        # Column A: alias name
        spreadsheet.set(f"A{row}", alias)

        # Column B: default value or empty string
        value = defaults.get(alias, "")
        spreadsheet.set(f"B{row}", str(value))

        # Set alias of cell in column B to alias name
        try:
            spreadsheet.setAlias(f"B{row}", alias)
        except Exception as e:
            App.Console.PrintError(f"⚠ Could not set alias for {alias}: {e}\n")

        row += 1

    doc.recompute()
    App.Console.PrintMessage("✅ Spreadsheet 'OrderVar' created/updated with global aliases and defaults.\n")


class CreateGlobalsSpreadsheetCommand:
    def GetResources(self):
        return {
            "Pixmap": "path/to/icon_create_spreadsheet.svg",  # replace with actual icon path
            "MenuText": "Create Globals Spreadsheet",
            "ToolTip": "Create a spreadsheet with all global aliases and default values"
        }

    def IsActive(self):
        return App.ActiveDocument is not None

    def Activated(self):
        doc = App.ActiveDocument
        if not doc:
            App.Console.PrintError("No active document open.\n")
            return

        try:
            create_globals_spreadsheet(doc)
        except Exception as e:
            App.Console.PrintError(str(e) + "\n")


# Register command
Gui.addCommand("Create_Globals_Spreadsheet", CreateGlobalsSpreadsheetCommand())
