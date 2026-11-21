# Phase 4 Floating Parameter Toolbar Prototype

Phase 4 creates a zero-build browser prototype and Python integration layer for editing schema-backed BIM parameters. It proves that a cleaned/enriched `template.json` can become a floating editable toolbar, validated object state, preview drawing, and exported JSON.

## How it depends on earlier phases

- Phase 1 creates the cleaned BIM library and first `template.json` files.
- Phase 2 enriches templates with parameters, validation metadata, and toolbar groups.
- Phase 3 can optionally provide generated placeholder geometry links for preview/export context.

Phase 4 still does not edit `.FCStd`, `.step`, `.stl`, `.brep`, image, or source CAD files.

## Why this is still a prototype

The UI uses plain HTML, CSS, JavaScript, and a simple canvas preview. It is meant to validate workflow and state management before investing in a production CAD viewport or OpenCASCADE/FreeCAD kernel integration.

## Dry-run

```bash
python tools/floating_toolbar_phase4.py --library-root /tmp/cad_bim_library_cleaned --output /tmp/cad_bim_toolbar_demo --dry-run
```

Dry-run scans templates and writes reports only.

## Generate toolbar demo data

```bash
python tools/floating_toolbar_phase4.py --library-root /tmp/cad_bim_library_cleaned --generated-geometry-root /tmp/cad_bim_generated_geometry --output /tmp/cad_bim_toolbar_demo --write
```

This writes `assets.json`, `toolbar_config.json`, `object_instances.json`, `geometry_links.json`, reports, and a copy of the static UI under `/tmp/cad_bim_toolbar_demo/ui/`.

## Open the UI

Open this file in a browser:

```text
/tmp/cad_bim_toolbar_demo/ui/index.html
```

Or run a local server:

```bash
python tools/floating_toolbar_phase4.py --output /tmp/cad_bim_toolbar_demo --serve --port 8765
```

Then open `http://localhost:8765/ui/index.html`.

## How the floating toolbar works

When an asset is selected, the UI creates an object instance with parameters initialized from template defaults or Phase 3 fallback defaults. It builds toolbar groups from `template.toolbar.groups`, falling back to each parameter's `toolbarGroup`. Number, select, checkbox, text, textarea, and color controls are generated dynamically.

## Validation and preview updates

Number inputs validate min/max and positive rules inline. Valid changes update the object-state JSON and redraw a simplified 2.5D canvas preview immediately after a short debounce.

## What Phase 5 should do next

Phase 5 should connect this state and toolbar workflow to real-time geometry regeneration and viewport integration. Later phases can replace placeholder preview drawing with CAD-kernel-backed model updates.
