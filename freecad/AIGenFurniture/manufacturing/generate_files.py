# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
import importlib
from . import get_active_exports

def generate_manufacturing_files(order, output_path, context=None):
    """
    Run all active manufacturing exports.
    MVP-safe dispatcher.
    """
    exports = get_active_exports()
    context = context or {}

    for export_name, export_def in exports.items():
        runner_name = export_def["runner"]
        module_name = export_def["module"]

        try:

            module = importlib.import_module(
                f".{module_name}",
                package=__package__,
            )
            runner = getattr(module, runner_name)

        except Exception as e:
            print(f"[ERROR] Failed to load export '{export_name}': {e}")
            continue

        try:
            kwargs = _resolve_export_kwargs(export_def, context)
            runner(order, output_path, **kwargs)
        except Exception as e:
            print(f"[ERROR] Export '{export_name}' failed: {e}")


def _resolve_context_path(context, path):
    value = context
    for part in path.split("."):
        if not isinstance(value, dict) or part not in value:
            return None
        value = value[part]
    return value


def _resolve_export_kwargs(export_def, context):
    kwargs = {}
    for arg_name, context_path in export_def.get("kwargs", {}).items():
        value = _resolve_context_path(context, context_path)
        if value is not None:
            kwargs[arg_name] = value
    return kwargs
