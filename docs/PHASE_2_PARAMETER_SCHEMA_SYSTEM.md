# Phase 2 Parameter Schema System

Phase 2 makes the cleaned CAD/BIM library metadata more structured and ready for future parameter-driven editing. It works on the cleaned output from Phase 1, not on the original FreeCAD-library source assets.

This phase still does **not** build a CAD editor, floating toolbar UI, real-time modelling engine, or geometry generator.

## How Phase 2 connects to Phase 1

Phase 1 copies selected BIM-relevant assets into a separate cleaned folder and creates one `template.json` for each cleaned asset. Those first templates contain useful starting metadata, but their parameters are intentionally broad placeholders.

Phase 2 reads those `template.json` files and enriches them with consistent parameter definitions, validation metadata, toolbar group hints, schema status, and reports. The original `.FCStd`, `.step`, `.stl`, `.brep`, image, and documentation files are not edited.

## What the Phase 2 script does

`tools/parameter_schema_phase2.py` scans a cleaned library folder for asset-level `template.json` files. For each template it:

- loads the existing template metadata;
- infers a standard BIM element type when needed;
- compares parameters against `element_type_schemas.json`;
- adds missing required parameters;
- enriches parameters from `parameter_catalog.json`;
- adds validation metadata;
- adds floating-toolbar grouping metadata for a future UI;
- normalizes `editability.status` to an allowed value;
- preserves existing data wherever possible;
- writes an updated template only when `--write` is passed.

## Dry-run command

Run dry-run first to validate and preview enrichment without updating templates:

```bash
python tools/parameter_schema_phase2.py --library-root /tmp/cad_bim_library_cleaned --dry-run
```

Dry-run writes Phase 2 reports by default to:

```text
/tmp/cad_bim_library_cleaned/00_metadata/phase2_schema_reports/
```

## Apply schema enrichment

After reviewing dry-run output, apply enrichment with:

```bash
python tools/parameter_schema_phase2.py --library-root /tmp/cad_bim_library_cleaned --write --backup
```

`--backup` creates `.bak` copies of `template.json` files before writing updated metadata. This backup affects only cleaned metadata files in the Phase 1 output folder, not the original FreeCAD source assets.

To process one category while testing, use:

```bash
python tools/parameter_schema_phase2.py --library-root /tmp/cad_bim_library_cleaned --dry-run --limit-category architecture.doors
```

## Schema configuration files

The schema configuration lives in `schemas/parameter_schema/`.

### `parameter_catalog.json`

`parameter_catalog.json` is the master dictionary of reusable parameters. Each parameter includes its name, label, description, type, unit, default value, min/max rules, options, UI-control hint, toolbar group, and validation metadata.

Examples include `width`, `height`, `thickness`, `swingDirection`, `openingType`, `material`, `fireRating`, `flowDirection`, `ductShape`, `manufacturer`, and `sourceUrl`.

### `element_type_schemas.json`

`element_type_schemas.json` maps BIM element types to required parameters, optional parameters, allowed file types, and toolbar groups. For example, `Door` requires `width`, `height`, and `thickness`, while `Pipe` requires `diameter` and `length`.

### `validation_rules.json`

`validation_rules.json` documents the general rules for valid templates: required top-level fields, known parameter names, required parameters by element type, naming conventions, category dot notation, and allowed editability statuses.

## Phase 2 reports

Reports are written under `00_metadata/phase2_schema_reports/` unless `--report-dir` is supplied:

- `phase2_schema_report.md` summarizes scanned templates, valid templates, enriched templates, missing required parameters, unsupported assets, custom parameters, processed categories, limitations, and the next recommended step.
- `phase2_validation_report.csv` lists validation issues or success rows per asset.
- `phase2_parameter_coverage.csv` summarizes parameter coverage by element type.
- `phase2_toolbar_groups.json` aggregates toolbar group definitions by element type.
- `phase2_unsupported_assets.csv` lists assets that could not be mapped to a useful schema.

## How a future floating toolbar will use this schema

The enriched templates include a `toolbar` block with `floating_parameter_panel` mode and grouped parameter names. A later UI can read these groups to decide which controls to show for dimensions, operation, materials, MEP settings, classification, or metadata.

However, Phase 2 only prepares metadata for that UI. It does not create the UI itself.

## Why STEP/STL files are still not truly editable

STEP and STL files can describe reference geometry or preview meshes, but they do not automatically expose product parameters such as door swing direction, pipe schedule, duct shape, or window glazing type. Phase 2 can add clean parameter metadata beside those files, but it cannot make a static mesh or exchange file regenerate from parameter changes.

## Why Phase 3 geometry generators are still required

A future editor needs generator logic that consumes parameters and creates or updates real geometry. Phase 3 should define and implement those generators. Only after generator APIs exist should Phase 4 build the floating toolbar UI and Phase 5 connect toolbar edits to real-time viewport regeneration.
