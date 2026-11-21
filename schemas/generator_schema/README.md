# Phase 3 Generator Schema

This folder documents the metadata shape written by `tools/geometry_generator_phase3.py`.

- `geometry_output_schema.json` describes the neutral mesh payload in `geometry.json`.
- `generator_manifest_schema.json` describes `generator_manifest.json`, including the generator used, requested outputs, status, and limitations.

The schemas are intentionally lightweight JSON documentation files. They do not require external validation libraries and they do not describe final production CAD geometry.
