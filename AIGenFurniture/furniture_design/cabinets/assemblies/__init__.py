import importlib
import pkgutil
import os

ASSEMBLIES = {}

# Iterate through all Python modules in this package
package_dir = os.path.dirname(__file__)
for _, module_name, is_pkg in pkgutil.iter_modules([package_dir]):
    if not is_pkg:
        module = importlib.import_module(f"{__name__}.{module_name}")

        # Only register modules that define an `assemble` function
        if hasattr(module, "assemble"):
            ASSEMBLIES[module_name] = module.assemble