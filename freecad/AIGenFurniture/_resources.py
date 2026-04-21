# freecad/AIGenFurniture/_resources.py
from importlib.resources import files

# Package root
_PKG = files("freecad.AIGenFurniture")

def get_resource_path(*parts) -> str:
    """Return an absolute path string to a resource inside the package."""
    ref = _PKG
    for part in parts:
        ref = ref.joinpath(part)
    return str(ref)

def get_command_icon(icon_filename: str) -> str:
    """Resolve a command toolbar icon by filename only."""
    return get_resource_path("commands", "resources", icon_filename + ".svg")