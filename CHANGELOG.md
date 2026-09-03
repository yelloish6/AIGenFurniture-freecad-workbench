<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
<!-- SPDX-FileNotice: Part of the AIGenFurniture addon. -->

# Changelog

<br/>

## [0.2.0] - 2026-09-02

### Added

- Added an editable Design Rules dialog for configuring board thicknesses,
  default cabinet dimensions, plinth height, front clearances, shelf setback,
  and edge-banding rules.
- Added persistent Design Rules stored in the FreeCAD user-data directory,
  including validation, factory-default restoration, and safe fallback when
  stored rules are invalid.
- Added the Tower with Plinth cabinet type to the Community edition.
- Added a dedicated accessories spreadsheet to every generated cabinet
  assembly, prefilled with the accessories required by its architecture.
- Added an aggregated accessories CSV containing accessory quantities for the
  complete order.
- Added accessory support to the JSON import and export workflows.
- Added an Order Setup extension hook that allows Pro and shop-specific addons
  to add their own setup spreadsheets and configuration.

### Changed

- Renamed Create Globals Spreadsheet to Order Setup and added a dedicated icon
  and clearer user-facing description.
- Order Setup now opens the OrderVar spreadsheet for editing after creation.
- Rebuilding an existing OrderVar spreadsheet now requires confirmation,
  preserves the spreadsheet object, removes obsolete content and aliases, and
  rolls back safely if rebuilding fails.
- Manual and generated elements now inherit their material from the matching
  OrderVar material parameter.
- Cabinet placeholders now use the dimensions configured in Design Rules.
- Generated boards, HDF panels, drawer bottoms, shelves, fronts, and edge
  banding now consistently use the configured Design Rules.
- Manufacturing export dispatch now passes exporter-specific configuration
  explicitly, improving compatibility with Pro and custom addons.
- Restricted the Community manufacturing registry to the general-purpose CSV
  and STL exporters.

### Fixed

- Added validation for Tower and Tower with Plinth opening and front lists.
- Corrected calculation of the automatically generated final tower opening.
- Corrected tower-front dimensions and positioning for all front combinations,
  including plinth-aware layouts.
- Corrected overlay and inset front clearances and visible gaps.
- Corrected HDF thickness usage for cabinet backs and drawer bottoms.
- Corrected manual element thicknesses that previously used hardcoded values.
- Corrected shelf setback, shelf edge-banding, and board edge-property handling.
- Corrected manufacturing export context dispatch.

### Removed

- Removed supplier-specific exporters from the Community package.
- Removed Community implementations and templates for pricing, offers,
  assembly instructions, and drilling documents. These outputs can be
  supplied by Pro or custom shop addons.


## [0.1.6] - 2026-05-03

### Changed


- Drawer slide gap can be adjusted via the slider_gap parameter of the drawer feature

## Added
- Implemented different types of overlay for fronts. Full overlay and partial 
overlay supported via the reveal parameter of the Front feature. Separate inset
front type added.
- Introduced the Material attribute as free text for all elements. BOM lists the content
of the Material attribute for every element in an order.


## [0.1.5] - 2026-05-03

### Changed

- Manufacturing BOM export (export_csv) is now registry-driven:
all Board subclasses registered by core or addons are automatically included
in BOM outputs without requiring changes to the workbench.

## [0.1.4] - 2026-04-23

### Fixed

- Corrected behavior of all commands at undo (Ctrl + Z)

### Changed

- Refactored for compatibility with FreeCAD Addon Manager
- Replaced tool icons updated ones in .svg format

### Added

-   License file 
-   Change log
-   About page accessible from new <b>Support</b> button in the workbench
-   overview.md file as base for Addon Manager description

## [0.1.3] - 2026-04-10

### Fixed

- Installer update for compatibility with FreeCAD 1.1 
- Minor cabinet architecture corrections.

### Changed

-   Added New AIGenFurniture Logo for cabinet workbench


## [0.1.2] - 2026-02-02

### Added

-   First launch of the MVP.

<br/>


[0.1.0]: #
