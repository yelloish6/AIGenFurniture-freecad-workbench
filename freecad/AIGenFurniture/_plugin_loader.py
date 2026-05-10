# freecad/AIGenFurniture/_plugin_loader.py
# SPDX-License-Identifier: LGPL-2.1-or-later

import importlib
import os
import sys

import FreeCAD as App


def _deep_update(target, patch):
    """Recursively merge patch into target in place."""
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(target.get(key), dict):
            _deep_update(target[key], value)
        else:
            target[key] = value


def _apply_overrides(registry, overrides, registry_name, plugin_id):
    for key, patch in overrides.items():
        if key not in registry:
            App.Console.PrintWarning(
                f"[{plugin_id}] Cannot override missing {registry_name} '{key}'.\n"
            )
            continue
        if not isinstance(patch, dict):
            App.Console.PrintWarning(
                f"[{plugin_id}] Override for {registry_name} '{key}' must be a dict.\n"
            )
            continue
        _deep_update(registry[key], patch)


def load_plugins(features_registry, elements_registry,
                 cabinets_registry, tools_registry, order_params_registry):
    mod_dir = os.path.dirname(  # .../Mod/
        os.path.dirname(        # .../Mod/AIGenFurniture/
            os.path.dirname(    # .../Mod/AIGenFurniture/freecad/
                os.path.dirname(os.path.abspath(__file__))  # .../freecad/AIGenFurniture/
            )
        )
    )

    if mod_dir not in sys.path:
        sys.path.insert(0, mod_dir)

    for name in sorted(os.listdir(mod_dir)):
        plugin_path = os.path.join(mod_dir, name)
        init_file = os.path.join(plugin_path, "plugin_init.py")
        marker = os.path.join(plugin_path, ".aigen_plugin")  # marker file

        # Only load folders that have BOTH plugin_init.py AND the marker file
        if not os.path.isfile(init_file) or not os.path.isfile(marker):
            continue

        try:
            importlib.invalidate_caches()
            mod = importlib.import_module(f"{name}.plugin_init")
            App.Console.PrintMessage(f"[AIGenFurniture] Plugin loaded: {name}\n")
        except Exception as e:
            App.Console.PrintWarning(f"[AIGenFurniture] Plugin '{name}' failed: {e}\n")
            continue

        plugin_id = getattr(mod, "PLUGIN_ID", plugin_path)

        # ── Merge additions ────────────────────────────────────────────
        for name, data in getattr(mod, "FEATURES", {}).items():
            if name in features_registry:
                App.Console.PrintWarning(
                    f"[{plugin_id}] Feature '{name}' conflicts with base. Skipping.\n"
                )
                continue
            features_registry[name] = data

        for name, data in getattr(mod, "ELEMENTS", {}).items():
            if name not in elements_registry:
                elements_registry[name] = data

        for name, data in getattr(mod, "CABINETS", {}).items():
            if name not in cabinets_registry:
                cabinets_registry[name] = data

        for name, data in getattr(mod, "ORDER_PARAMS", {}).items():
            if name not in order_params_registry:
                order_params_registry[name] = data

        for tool_def in getattr(mod, "TOOLS", []):
            tools_registry.append(tool_def)

        # ── Apply overrides to existing base entries ───────────────────
        _apply_overrides(
            features_registry,
            getattr(mod, "OVERRIDE_FEATURES", {}),
            "feature",
            plugin_id,
        )
        _apply_overrides(
            elements_registry,
            getattr(mod, "OVERRIDE_ELEMENTS", {}),
            "element",
            plugin_id,
        )
        _apply_overrides(
            cabinets_registry,
            getattr(mod, "OVERRIDE_CABINETS", {}),
            "cabinet",
            plugin_id,
        )
        _apply_overrides(
            order_params_registry,
            getattr(mod, "OVERRIDE_ORDER_PARAMS", {}),
            "order parameter",
            plugin_id,
        )

        # ── Apply disables ─────────────────────────────────────────────
        for key in getattr(mod, "DISABLE_FEATURES", []):
            if key in features_registry:
                features_registry[key]["enabled"] = False

        for key in getattr(mod, "DISABLE_ELEMENTS", []):
            if key in elements_registry:
                elements_registry[key]["enabled"] = False

        for key in getattr(mod, "DISABLE_CABINETS", []):
            if key in cabinets_registry:
                cabinets_registry[key]["enabled"] = False

        for key in getattr(mod, "DISABLE_ORDER_PARAMS", []):
            if key in order_params_registry:
                order_params_registry[key]["enabled"] = False

        for tool_id in getattr(mod, "DISABLE_TOOLS", []):
            for t in tools_registry:
                if t["id"] == tool_id:
                    t["enabled"] = False

        App.Console.PrintMessage(
            f"[AIGenFurniture] Loaded addon: {plugin_id}\n"
        )
