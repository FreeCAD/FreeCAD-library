# Phase 2 Parameter Schema Configuration

This folder contains the reusable schema configuration used by `tools/parameter_schema_phase2.py`.

## Files

- `parameter_catalog.json` is the master dictionary of reusable parameter definitions. Each entry includes labels, descriptions, units, UI-control hints, toolbar grouping, and validation metadata.
- `element_type_schemas.json` maps BIM element types such as `Door`, `Window`, `Pipe`, and `Duct` to required parameters, optional parameters, allowed file types, and floating-toolbar groups.
- `validation_rules.json` records the general template validation rules used by Phase 2.

## Scope

These files describe metadata only. They do not modify FreeCAD source assets and do not make STEP, STL, or BREP files parametric. Phase 3 still needs geometry generators before real-time editing can work.
