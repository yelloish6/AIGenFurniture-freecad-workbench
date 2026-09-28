# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
"""Canonical accessory identities, display labels, units, and legacy aliases."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class AccessoryDefinition:
    code: str
    label: str
    unit: str = "pcs"
    aliases: tuple[str, ...] = ()


ACCESSORIES = (
    AccessoryDefinition("cabinet_assembly_screw", "Cabinet assembly screw", aliases=("surub",)),
    AccessoryDefinition("chipboard_screw_3_5x16", "Chipboard screw 3.5 × 16 mm", aliases=("surub 3.5x16",)),
    AccessoryDefinition("chipboard_screw_3_5x30", "Chipboard screw 3.5 × 30 mm", aliases=("surub 3.5x30",)),
    AccessoryDefinition("hdf_back_screw", "HDF back screw", aliases=("surub PFL",)),
    AccessoryDefinition("countertop_fixing_screw", "Countertop fixing screw", aliases=("surub blat",)),
    AccessoryDefinition("cabinet_connector_screw", "Cabinet connector screw", aliases=("surub intre corpuri",)),
    AccessoryDefinition("wall_plug_screw", "Wall-plug screw", aliases=("surub diblu perete",)),
    AccessoryDefinition("euro_screw_7x50", "Euro screw 7 × 50 mm", aliases=("eurosurub 7x50",)),
    AccessoryDefinition("adjustable_cabinet_leg", "Adjustable cabinet leg", aliases=("picioare",)),
    AccessoryDefinition("plinth_clip", "Plinth clip", aliases=("clema plinta",)),
    AccessoryDefinition("plinth", "Plinth", unit="m", aliases=("plinta",)),
    AccessoryDefinition("countertop_wall_trim", "Countertop wall trim", unit="m", aliases=("sipca apa",)),
    AccessoryDefinition("wall_cabinet_hanger", "Wall cabinet hanger", unit="pair", aliases=("pereche clema prindere perete",)),
    AccessoryDefinition("wall_mounting_rail", "Wall mounting rail", unit="m", aliases=("sina perete",)),
    AccessoryDefinition("overlay_hinge", "Overlay hinge", aliases=("balama aplicata",)),
    AccessoryDefinition("inset_hinge", "Inset hinge", aliases=("balama ingropata",)),
    AccessoryDefinition("bi_fold_corner_hinge", "Bi-fold corner hinge", aliases=("balama usa franta",)),
    AccessoryDefinition("hinge_170_degree", "170° hinge", aliases=("balama 170 deg",)),
    AccessoryDefinition("soft_close_damper", "Soft-close damper", aliases=("amortizor",)),
    AccessoryDefinition("handle", "Handle", aliases=("maner",)),
    AccessoryDefinition("shelf_support", "Shelf support", aliases=("bolt polita",)),
    AccessoryDefinition("glass_panel", "Glass panel", aliases=("sticla",)),
    AccessoryDefinition("cam_connector_fitting", "Cam connector fitting", aliases=("demontabil cama",)),
    AccessoryDefinition("l_bracket", "L-bracket", aliases=("L",)),
    AccessoryDefinition("jolly_pull_out_150x500", "Jolly pull-out — 150 × 500 mm", unit="set", aliases=("Joly150500",)),
    AccessoryDefinition("jolly_pull_out_240x500", "Jolly pull-out — 240 × 500 mm", unit="set", aliases=("Joly240500",)),
    AccessoryDefinition("jolly_pull_out_300x500", "Jolly pull-out — 300 × 500 mm", unit="set", aliases=("Joly300500",)),
)


def _identity(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip()).casefold()


_BY_NAME = {
    _identity(name): definition
    for definition in ACCESSORIES
    for name in (definition.code, definition.label, *definition.aliases)
}
_DRAWER_SLIDE = re.compile(r"^(?:pereche\s+glisiera|drawer\s+slide\s+[—-])\s*(\d+)\s*mm$", re.IGNORECASE)
_TANDEMBOX = re.compile(r"^tandembox(?:\s+(.+))?$", re.IGNORECASE)


def resolve_accessory(value: object, unit: str | None = None) -> AccessoryDefinition:
    """Return canonical metadata, preserving unknown extension-defined names."""
    text = str(value or "").strip()
    definition = _BY_NAME.get(_identity(text))
    if definition:
        return definition if not unit else AccessoryDefinition(definition.code, definition.label, unit, definition.aliases)

    slide_match = _DRAWER_SLIDE.match(text)
    if slide_match:
        length = slide_match.group(1)
        return AccessoryDefinition(
            f"drawer_slide_{length}_mm", f"Drawer slide — {length} mm", unit or "pair", (text,)
        )

    tandembox_match = _TANDEMBOX.match(text)
    if tandembox_match:
        variant = (tandembox_match.group(1) or "").strip()
        code_suffix = re.sub(r"[^a-z0-9]+", "_", variant.casefold()).strip("_")
        return AccessoryDefinition(
            "tandembox" + (f"_{code_suffix}" if code_suffix else ""),
            "TANDEMBOX" + (f" {variant}" if variant else ""),
            unit or "set",
            (text,),
        )

    code = re.sub(r"[^a-z0-9]+", "_", text.casefold()).strip("_") or "unknown_accessory"
    return AccessoryDefinition(code, text, unit or "pcs", (text,))
