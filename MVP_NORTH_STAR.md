## 1. Purpose (WHY this MVP exists)

> This MVP exists to prove that furniture professionals will pay for a tool that turns a rough kitchen idea into production-ready cabinet geometry in under 10 minutes.

If a feature does not help prove this → it does not belong.

## 2. Target User (WHO it is for)

> Primary user:
Small furniture workshops and independent kitchen designers who already use CAD and want to reduce layout-to-production time.

> Explicitly not for:
End customers, hobbyists, large factories, interior designers without CAD skills.

This prevents “just one more feature”.

## 3. One-Sentence North Star (THE anchor)

> “From idea to production-ready cabinet geometry in under 10 minutes, inside FreeCAD.”

Nothing else gets equal weight.

## 4. Canonical User Story (HOW it is used)

> As a furniture professional, I sketch a kitchen layout using simple cabinet boxes in FreeCAD, define cabinet dimensions and basic features globally or per cabinet, and run a single command to generate structured, production-ready cabinet geometry.

If a change breaks this flow → it’s wrong.

## 5. MVP Scope (WHAT is included)

### Elements

- Chipboard (BoardPal)
- Front (Front)
- Countertop (Blat)
- HDF (PFL)

### Cabinets
- Base Cabinet (BaseBox)
- Wall Cabinet (TopBox)
- Tower Cabinet (TowerBox)

### Features

- Add Front (add_front)
- Add Shelves (add_pol)
- Add Drawer (add_drawer)

### Workflow

- FreeCAD only
- Placeholder box → generated cabinet
- One command (Explode cabinet)

### Output

- Editable FreeCAD geometry (.FCStd)

## 6. Explicit Non-Goals (WHAT is forbidden)

This is the most powerful section.


The MVP explicitly does NOT aim to:

- Generate CNC toolpaths
- Export DXF / STEP / STL
- Produce BOMs or pricing
- Handle hardware selection
- Cover all cabinet types
- Support non-FreeCAD workflows
- Be production-perfect

If a feature sounds “nice” but fits here → it’s out.

## 7. Definition of “Done” (WHEN MVP is finished)


The MVP is done when:
- A new user installs the addon
- Creates cabinet boxes
- Runs one command
- Gets correct cabinet geometry
- In under 10 minutes
- Without assistance

Not “when all planned features are implemented”.