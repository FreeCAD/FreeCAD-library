# CAD/BIM Library Next Phases

## Phase 1: Cleanup and classification

Create a safe cleaned library outside the source repository. Copy only selected BIM-relevant assets, normalize folder names, classify file types, and generate first-pass `template.json` files plus metadata reports.

## Phase 2: Parameter schema system

Enrich cleaned `template.json` metadata with reusable parameter definitions, element-type schemas, validation rules, schema readiness flags, and floating-toolbar group hints. This phase prepares data for a future UI but does not edit geometry.

## Phase 3: Geometry generator system

Create backend placeholder generators that turn enriched template parameters into neutral mesh geometry, OBJ previews, STL previews, and generator manifests. This proves the parameter-to-geometry contract before building UI or real-time editing.

## Phase 4: Floating parameter toolbar UI

Create the floating parameter toolbar after stable schemas and generator interfaces exist. The toolbar should read Phase 2 toolbar groups, edit schema-backed parameters, and call Phase 3 generator APIs rather than directly mutating static reference meshes.

## Phase 5: Real-time regeneration and viewport update

Connect toolbar edits to real-time geometry regeneration, validation, preview updates, and viewport refresh. This phase should include performance testing and fallback behavior for assets that remain static references.

## Phase 6: Save/export parametric project data

Persist schema-backed parameters, generator references, user edits, and export mappings so projects can be reopened, versioned, and exported without losing parametric intent.

## Phase 7: Advanced CAD kernel / FreeCAD / OpenCASCADE integration

Replace or augment placeholder mesh generators with robust CAD-kernel-backed generation for production solids, booleans, constraints, IFC/BIM semantics, and high-quality import/export workflows.
