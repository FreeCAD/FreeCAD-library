# Phase 3 Geometry Generator System

Phase 3 creates a backend generator framework that turns enriched `template.json` metadata into simple parametric placeholder geometry. It proves this workflow:

```text
template.json parameters -> generator -> geometry output
```

This phase is not the final CAD kernel, not a floating toolbar UI, and not real-time viewport editing.

## How Phase 3 depends on Phase 1 and Phase 2

Phase 1 creates a cleaned BIM-oriented library outside the original FreeCAD-library repository. Phase 2 enriches each cleaned asset's `template.json` with consistent parameters and toolbar-ready metadata. Phase 3 reads those enriched templates and generates simple geometry from their parameters.

The original FreeCAD source assets are not modified. Phase 3 does not edit `.FCStd`, `.step`, `.stl`, `.brep`, images, or documentation files.

## Why generated geometry is placeholder geometry

The goal is not to perfectly recreate the original FreeCAD assets. Instead, each element type gets a simple standard-library mesh:

- doors become a panel and frame;
- windows become a frame and glass panel;
- beams become a box or simple I-beam approximation;
- roofs become a sloped slab;
- construction blocks become rectangular blocks;
- pipes and ducts become cylinder-like or rectangular placeholder meshes;
- furniture, fixtures, foundations, vegetation, and generic BIM objects become simple representative forms.

This creates a safe backend contract for future UI work while keeping expectations clear: these meshes are not production CAD geometry.

## Dry-run command

Use dry-run to scan templates and write reports without writing geometry files:

```bash
python tools/geometry_generator_phase3.py --library-root /tmp/cad_bim_library_cleaned --output /tmp/cad_bim_generated_geometry --dry-run
```

## Generate geometry

Generate all supported output formats with:

```bash
python tools/geometry_generator_phase3.py --library-root /tmp/cad_bim_library_cleaned --output /tmp/cad_bim_generated_geometry --write
```

Generate only one element type:

```bash
python tools/geometry_generator_phase3.py --library-root /tmp/cad_bim_library_cleaned --output /tmp/cad_bim_generated_geometry --write --limit-element-type Door
```

Generate only one asset:

```bash
python tools/geometry_generator_phase3.py --library-root /tmp/cad_bim_library_cleaned --output /tmp/cad_bim_generated_geometry --write --asset-id door_wood_single_door_with_trims
```

Use `--format json`, `--format obj`, `--format stl`, or `--format all` to choose outputs.

## Output files

Each generated asset folder can contain:

- `geometry.json`: neutral mesh representation with asset id, element type, category, units, parameters used, vertices, faces, and generator metadata.
- `preview.obj`: Wavefront OBJ preview mesh.
- `preview.stl`: ASCII STL preview mesh.
- `generator_manifest.json`: manifest explaining which generator ran, which template was used, which outputs were written, and the known limitations.

Reports are written to `<output>/00_reports/` by default:

- `phase3_generation_report.md`
- `phase3_generation_report.csv`
- `phase3_unsupported_assets.csv`
- `phase3_generator_coverage.csv`
- `phase3_generator_registry.json`

## How a future floating toolbar will use this system

A Phase 4 toolbar can edit schema-backed parameters from the enriched templates and then call these generator classes to regenerate placeholder geometry. Phase 5 can connect that regeneration loop to a viewport. Later phases can replace placeholder mesh generation with production-grade CAD-kernel operations.

## Limitations

- Placeholder geometry only.
- No original FreeCAD, STEP, STL, BREP, or image assets are modified.
- No dimensions are reverse-engineered from source CAD files.
- OBJ and STL outputs are preview meshes, not authoritative BIM/CAD models.
- Advanced constraints, boolean operations, openings, connectors, and parametric histories remain future work.

## What Phase 4 should do next

Phase 4 should build the floating parameter toolbar UI that reads Phase 2 schema metadata and calls Phase 3 generators through a stable backend interface. The UI should still communicate clearly when an asset is placeholder-only versus backed by a production generator.
