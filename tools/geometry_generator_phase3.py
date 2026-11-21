#!/usr/bin/env python3
"""Generate Phase 3 placeholder geometry from enriched BIM template.json files."""
from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from generators.mesh_utils import sanitize_filename, write_ascii_stl, write_geometry_json, write_obj
from generators.registry import get_generator, registry_summary

LIMITATIONS = [
    "Placeholder geometry only.",
    "Does not modify or reverse-engineer original FCStd/STEP/STL files.",
    "Not yet suitable as final production CAD geometry.",
]


@dataclass
class GenerationRow:
    asset_id: str
    element_type: str
    category: str
    template_path: str
    output_path: str
    status: str
    generator: str
    issues: List[str] = field(default_factory=list)


@dataclass
class Summary:
    rows: List[GenerationRow] = field(default_factory=list)
    formats: set[str] = field(default_factory=set)
    scanned: int = 0

    @property
    def generated(self) -> int:
        return sum(1 for row in self.rows if row.status in {"generated", "would_generate"})

    @property
    def skipped(self) -> int:
        return sum(1 for row in self.rows if row.status == "skipped")

    @property
    def failed(self) -> int:
        return sum(1 for row in self.rows if row.status == "failed")

    @property
    def unsupported(self) -> int:
        return sum(1 for row in self.rows if "unsupported" in row.issues)


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def find_templates(library_root: Path) -> Iterable[Path]:
    for path in library_root.rglob("template.json"):
        if "00_metadata" in path.relative_to(library_root).parts:
            continue
        if path.is_file():
            yield path


def selected_formats(format_name: str) -> set[str]:
    return {"json", "obj", "stl"} if format_name == "all" else {format_name}


def category_path(category: str) -> Path:
    return Path(*[sanitize_filename(part) for part in category.split(".") if part])


def asset_output_path(output_root: Path, template: Dict[str, Any]) -> Path:
    category = str(template.get("category", "uncategorized"))
    asset_id = sanitize_filename(str(template.get("id", "unknown_asset")))
    return output_root / category_path(category) / asset_id


def matches_filters(template: Dict[str, Any], limit_category: Optional[str], limit_element_type: Optional[str], asset_id: Optional[str]) -> bool:
    category = str(template.get("category", ""))
    element_type = str(template.get("elementType", ""))
    if limit_category and not (category == limit_category or category.startswith(limit_category + ".")):
        return False
    if limit_element_type and element_type != limit_element_type:
        return False
    if asset_id and template.get("id") != asset_id:
        return False
    return True


def geometry_json_payload(generated: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "assetId": generated.get("assetId"),
        "elementType": generated.get("elementType"),
        "category": generated.get("category"),
        "units": generated.get("units", "mm"),
        "parametersUsed": generated.get("parametersUsed", {}),
        "geometryType": generated.get("geometryType", "mesh"),
        "metadata": generated.get("metadata", {}),
    }


def manifest_for(template: Dict[str, Any], template_path: Path, generated: Dict[str, Any], formats: set[str]) -> Dict[str, Any]:
    outputs: Dict[str, str] = {}
    if "json" in formats:
        outputs["geometryJson"] = "geometry.json"
    if "obj" in formats:
        outputs["obj"] = "preview.obj"
    if "stl" in formats:
        outputs["stl"] = "preview.stl"
    return {
        "assetId": template.get("id"),
        "elementType": template.get("elementType"),
        "generatorName": generated.get("metadata", {}).get("generator"),
        "generatorVersion": generated.get("metadata", {}).get("generatorVersion", "phase3.v1"),
        "inputTemplate": template_path.as_posix(),
        "outputs": outputs,
        "status": "generated",
        "limitations": LIMITATIONS,
    }


def write_asset_outputs(asset_dir: Path, template: Dict[str, Any], template_path: Path, generated: Dict[str, Any], formats: set[str]) -> None:
    mesh = {"vertices": generated.get("vertices", []), "faces": generated.get("faces", [])}
    if "json" in formats:
        write_geometry_json(mesh, geometry_json_payload(generated), asset_dir / "geometry.json")
    if "obj" in formats:
        write_obj(mesh, asset_dir / "preview.obj")
    if "stl" in formats:
        write_ascii_stl(mesh, asset_dir / "preview.stl", str(template.get("id", "asset")))
    write_json(asset_dir / "generator_manifest.json", manifest_for(template, template_path, generated, formats))


def process_library(library_root: Path, output_root: Path, report_dir: Path, dry_run: bool, write: bool, limit_category: Optional[str], limit_element_type: Optional[str], asset_id: Optional[str], format_name: str) -> Summary:
    formats = selected_formats(format_name)
    summary = Summary(formats=formats)
    for template_path in sorted(find_templates(library_root)):
        template = load_json(template_path)
        if not isinstance(template, dict):
            continue
        if not matches_filters(template, limit_category, limit_element_type, asset_id):
            continue
        summary.scanned += 1
        out_dir = asset_output_path(output_root, template)
        element_type = str(template.get("elementType", "GenericBIMObject"))
        generator = get_generator(element_type)
        try:
            if not generator.can_generate(template):
                summary.rows.append(GenerationRow(str(template.get("id", "")), element_type, str(template.get("category", "")), template_path.as_posix(), out_dir.as_posix(), "skipped", generator.generator_name, ["unsupported"]))
                continue
            generated = generator.generate(template)
            issues = generator.validate_parameters(generated.get("parametersUsed", {}))
            if write:
                write_asset_outputs(out_dir, template, template_path, generated, formats)
            summary.rows.append(GenerationRow(str(template.get("id", "")), element_type, str(template.get("category", "")), template_path.as_posix(), out_dir.as_posix(), "would_generate" if dry_run else "generated", generator.generator_name, issues))
        except Exception as exc:  # report per-asset failures without stopping the full batch
            summary.rows.append(GenerationRow(str(template.get("id", "")), element_type, str(template.get("category", "")), template_path.as_posix(), out_dir.as_posix(), "failed", generator.generator_name, [str(exc)]))
    write_reports(report_dir, summary)
    return summary


def write_reports(report_dir: Path, summary: Summary) -> None:
    report_dir.mkdir(parents=True, exist_ok=True)
    write_markdown_report(report_dir / "phase3_generation_report.md", summary)
    write_generation_csv(report_dir / "phase3_generation_report.csv", summary)
    write_unsupported_csv(report_dir / "phase3_unsupported_assets.csv", summary)
    write_coverage_csv(report_dir / "phase3_generator_coverage.csv", summary)
    write_json(report_dir / "phase3_generator_registry.json", registry_summary())


def write_markdown_report(path: Path, summary: Summary) -> None:
    generated_types = sorted({row.element_type for row in summary.rows if row.status in {"generated", "would_generate"}})
    lines = [
        "# Phase 3 Geometry Generation Report",
        "",
        f"- Total templates scanned: {summary.scanned}",
        f"- Total generated: {summary.generated}",
        f"- Total skipped: {summary.skipped}",
        f"- Total failed: {summary.failed}",
        f"- Element types generated: {', '.join(generated_types) if generated_types else 'none'}",
        f"- Output formats written: {', '.join(sorted(summary.formats))}",
        f"- Unsupported assets: {summary.unsupported}",
        "",
        "## Limitations",
        "",
        *[f"- {item}" for item in LIMITATIONS],
        "- Phase 3 proves template parameters can drive placeholder geometry; it is not the final CAD kernel.",
        "",
        "## Next recommended step",
        "",
        "Phase 4 should integrate these generators with a floating parameter toolbar UI.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_generation_csv(path: Path, summary: Summary) -> None:
    fieldnames = ["asset_id", "element_type", "category", "template_path", "output_path", "status", "generator", "issues"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames); writer.writeheader()
        for row in summary.rows:
            writer.writerow({"asset_id": row.asset_id, "element_type": row.element_type, "category": row.category, "template_path": row.template_path, "output_path": row.output_path, "status": row.status, "generator": row.generator, "issues": "; ".join(row.issues)})


def write_unsupported_csv(path: Path, summary: Summary) -> None:
    fieldnames = ["asset_id", "element_type", "category", "template_path", "reason"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames); writer.writeheader()
        for row in summary.rows:
            if "unsupported" in row.issues:
                writer.writerow({"asset_id": row.asset_id, "element_type": row.element_type, "category": row.category, "template_path": row.template_path, "reason": "; ".join(row.issues)})


def write_coverage_csv(path: Path, summary: Summary) -> None:
    coverage: Dict[str, Dict[str, Any]] = {}
    for row in summary.rows:
        item = coverage.setdefault(row.element_type, {"templates_found": 0, "generated_count": 0, "skipped_count": 0, "failed_count": 0, "generator_name": row.generator})
        item["templates_found"] += 1
        if row.status in {"generated", "would_generate"}: item["generated_count"] += 1
        if row.status == "skipped": item["skipped_count"] += 1
        if row.status == "failed": item["failed_count"] += 1
    fieldnames = ["element_type", "templates_found", "generated_count", "skipped_count", "failed_count", "generator_name"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames); writer.writeheader()
        for element_type, row in sorted(coverage.items()):
            writer.writerow({"element_type": element_type, **row})


def print_summary(summary: Summary, output_root: Path, report_dir: Path, dry_run: bool, write: bool) -> None:
    print("Phase 3 geometry generation complete")
    print(f"Dry run: {'yes' if dry_run else 'no'}")
    print(f"Write geometry: {'yes' if write else 'no'}")
    print(f"Templates scanned: {summary.scanned}")
    print(f"Generated: {summary.generated}")
    print(f"Skipped: {summary.skipped}")
    print(f"Failed: {summary.failed}")
    print(f"Output formats: {', '.join(sorted(summary.formats))}")
    print(f"Output root: {output_root}")
    print(f"Reports: {report_dir}")


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Phase 3 placeholder geometry from enriched CAD/BIM template.json files.")
    parser.add_argument("--library-root", required=True, help="Path to the cleaned BIM library output from Phase 1/2.")
    parser.add_argument("--output", required=True, help="Path where generated geometry should be written.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true", help="Scan templates and report what would be generated, without writing geometry files.")
    mode.add_argument("--write", action="store_true", help="Actually generate output geometry files.")
    parser.add_argument("--limit-category", help="Only process one category such as architecture.doors.")
    parser.add_argument("--limit-element-type", help="Only process one element type such as Door or Duct.")
    parser.add_argument("--asset-id", help="Generate geometry for only one asset id.")
    parser.add_argument("--format", choices=["json", "obj", "stl", "all"], default="all", help="Output format to write. Default: all.")
    parser.add_argument("--report-dir", help="Optional report directory. Default: <output>/00_reports.")
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    library_root = Path(args.library_root).resolve()
    output_root = Path(args.output).resolve()
    if not library_root.exists() or not library_root.is_dir():
        raise SystemExit(f"Library root does not exist: {library_root}")
    report_dir = Path(args.report_dir).resolve() if args.report_dir else output_root / "00_reports"
    summary = process_library(library_root, output_root, report_dir, args.dry_run, args.write, args.limit_category, args.limit_element_type, args.asset_id, args.format)
    print_summary(summary, output_root, report_dir, args.dry_run, args.write)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
