# Phase 1 CAD/BIM Library Cleanup

Phase 1 creates a safe, curated CAD/BIM asset library from the broader FreeCAD-library repository. The goal is cleanup and classification only: no CAD editor, floating toolbar, parametric engine, or real-time 3D editing is built in this phase.

## Why this cleanup exists

The upstream library contains many useful BIM-adjacent objects, but it also includes electronics, robotics, sports, mechanical, PCB, and general-purpose models. A CAD/BIM product needs a smaller, predictable structure organized around building elements, MEP parts, site assets, and metadata that later systems can read.

The cleanup script copies selected BIM-relevant files into a separate output folder and generates metadata beside those copied files. It intentionally does **not** modify the source library.

## Safety model

`tools/cleanup_phase1.py` is non-destructive:

- it does not delete original files;
- it does not move original files;
- it does not overwrite source files;
- it refuses to place the cleaned output inside the source repository;
- it copies only files that match Phase 1 BIM category and file-type rules.

Generated cleaned output should live outside the repository, for example `/tmp/cad_bim_library_cleaned` or `../cad_bim_library_cleaned`.

## Dry-run command

Use dry-run first to inspect what would be copied without creating output files:

```bash
python tools/cleanup_phase1.py --source . --output ../cad_bim_library_cleaned --dry-run
```

A dry-run prints totals for files scanned, BIM-relevant files that would be copied, asset folders that would be created, backup files detected, and PCB/Gerber files detected.

## Actual cleanup command

After dry-run succeeds, run the actual copy:

```bash
python tools/cleanup_phase1.py --source . --output ../cad_bim_library_cleaned
```

To create an archive placeholder for future non-BIM asset workflows, add:

```bash
python tools/cleanup_phase1.py --source . --output ../cad_bim_library_cleaned --include-archive
```

To focus on one cleaned category while testing, add a category such as:

```bash
python tools/cleanup_phase1.py --source . --output ../cad_bim_library_cleaned --limit-category architecture.doors
```

## Cleaned folder meanings

The cleaned output has these top-level areas:

- `00_metadata/` contains reports, file rules, and `library_index.json`.
- `architecture/` contains doors, windows, beams, roof assets, construction blocks, bathroom/kitchen fixtures, furniture, foundations, and architecture-related symbols.
- `mep/` contains HVAC ducts, HVAC pipes, plumbing pipes, hydro equipment, and electrical equipment relevant to building systems.
- `site/` contains topography and vegetation/site assets.
- `archive_non_bim/` is created only when `--include-archive` is passed. Phase 1 reports non-BIM candidates but does not blindly copy the entire archive.

Asset folders use normalized `snake_case` names so downstream software can depend on stable paths. For example, a source group like:

```text
Architectural Parts/Doors/Wood/Single door with trims.FCStd
Architectural Parts/Doors/Wood/Single door with trims.step
Architectural Parts/Doors/Wood/Single door with trims.stl
```

becomes:

```text
architecture/doors/wood/single_door_with_trims/
  source.FCStd
  reference.step
  preview.stl
  template.json
```

## Static reference geometry

STEP, STL, BREP, image, and documentation files are useful as geometry references, previews, or documentation, but they are not treated as live parametric generators in Phase 1. STEP files can preserve exchange geometry, and STL files can provide preview meshes, but neither guarantees editable CAD/BIM parameters such as width, height, swing direction, glazing type, or duct bend angle.

## FreeCAD source files

`.FCStd` and `.fcstd` files are treated as possible parametric sources because they may contain FreeCAD-native model data. They are still marked as `static_reference` in Phase 1 because the cleanup script does not inspect constraints, object history, sketches, or generator logic. `parametricSourceAvailable` means a native source exists, not that real-time editing is already implemented.

## Generated metadata

Each cleaned asset folder receives a `template.json` with:

- an asset ID;
- element type;
- cleaned category;
- display name;
- original source path;
- copied source file names;
- file type groups;
- editability status;
- placeholder parameters;
- notes explaining that generator work is still required.

`00_metadata/library_index.json` lists every cleaned asset for product ingestion. Reports in `00_metadata/` summarize cleanup results, missing templates, excluded non-BIM candidates, and file rules.

## Preparing for a later floating parameter toolbar

Phase 1 provides consistent asset IDs, categories, templates, and placeholder parameter names. That structure lets Phase 2 refine parameter schemas before Phase 3 creates geometry generators. Only after generator logic exists should a floating parameter toolbar attempt real-time model regeneration.
