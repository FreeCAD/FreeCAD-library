#!/usr/bin/env python3
"""Phase 2 parameter schema enrichment for cleaned CAD/BIM templates.

The script operates on a cleaned library produced by Phase 1, or on any folder
that contains asset-level template.json files. It updates metadata only; it does
not open or edit CAD geometry files such as FCStd, STEP, STL, or BREP.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

SCHEMA_VERSION = "phase2.v1"
ALLOWED_EDITABILITY_STATUSES = {
    "static_reference",
    "parametric_source_available",
    "generator_ready",
    "fully_parametric",
    "unsupported",
}
REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA_ROOT = REPO_ROOT / "schemas" / "parameter_schema"


@dataclass
class ValidationIssue:
    asset_id: str
    template_path: str
    element_type: str
    category: str
    valid: bool
    issue_code: str
    issue_message: str
    recommended_fix: str


@dataclass
class ProcessedTemplate:
    path: Path
    original: Dict[str, Any]
    enriched: Dict[str, Any]
    issues: List[ValidationIssue]
    missing_required: List[str]
    custom_parameters: List[str]
    unsupported: bool
    changed: bool


@dataclass
class RunSummary:
    processed: List[ProcessedTemplate] = field(default_factory=list)
    categories: set[str] = field(default_factory=set)

    @property
    def scanned_count(self) -> int:
        return len(self.processed)

    @property
    def enriched_count(self) -> int:
        return sum(1 for item in self.processed if item.changed)

    @property
    def valid_count(self) -> int:
        return sum(1 for item in self.processed if not item.issues)

    @property
    def missing_required_count(self) -> int:
        return sum(1 for item in self.processed if item.missing_required)

    @property
    def unsupported_count(self) -> int:
        return sum(1 for item in self.processed if item.unsupported)

    @property
    def custom_parameter_count(self) -> int:
        return sum(len(item.custom_parameters) for item in self.processed)


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, data: Any) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")


def load_schema_config(schema_root: Path = DEFAULT_SCHEMA_ROOT) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    """Load element schemas, parameter catalog, and validation rules."""
    element_schemas = load_json(schema_root / "element_type_schemas.json")
    parameter_catalog = load_json(schema_root / "parameter_catalog.json")
    validation_rules = load_json(schema_root / "validation_rules.json")
    return element_schemas, parameter_catalog, validation_rules


def is_snake_case(value: str) -> bool:
    return bool(re.fullmatch(r"[a-z0-9]+(?:_[a-z0-9]+)*", value or ""))


def is_dot_notation(value: str) -> bool:
    return bool(re.fullmatch(r"[a-z0-9_]+(?:\.[a-z0-9_]+)*", value or ""))


def is_camel_case(value: str) -> bool:
    return bool(re.fullmatch(r"[a-z][A-Za-z0-9]*", value or ""))


def canonical_element_type(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    compact = re.sub(r"[^A-Za-z0-9]+", "", value).lower()
    aliases = {
        "door": "Door",
        "window": "Window",
        "beam": "Beam",
        "roof": "Roof",
        "constructionblock": "ConstructionBlock",
        "wall": "Wall",
        "slab": "Slab",
        "floor": "Floor",
        "column": "Column",
        "pipe": "Pipe",
        "duct": "Duct",
        "furniture": "Furniture",
        "furniturefixture": "Fixture",
        "fixture": "Fixture",
        "foundation": "Foundation",
        "vegetation": "Vegetation",
        "sitesymbol": "Vegetation",
        "topography": "GenericBIMObject",
        "electricalequipment": "Fixture",
        "genericbimobject": "GenericBIMObject",
    }
    return aliases.get(compact)


def infer_element_type(template: Dict[str, Any], template_path: Path) -> str:
    """Infer a useful BIM element type from existing metadata and path text."""
    category = str(template.get("category", ""))
    existing = canonical_element_type(str(template.get("elementType", "")))
    path_text = " ".join([category, str(template.get("originalPath", "")), template_path.as_posix()]).lower()

    if "doors" in path_text or ".door" in path_text:
        return "Door"
    if "windows" in path_text or ".window" in path_text:
        return "Window"
    if "beams" in path_text or ".beam" in path_text:
        return "Beam"
    if "roof" in path_text:
        return "Roof"
    if "construction_blocks" in path_text or "construction blocks" in path_text or "building construction" in path_text:
        return "ConstructionBlock"
    if "hvac_ducts" in path_text or " ducts" in path_text or "/duct" in path_text:
        return "Duct"
    if "pipes" in path_text or "tubes" in path_text or "hydro_equipment" in path_text:
        return "Pipe"
    if "foundation" in path_text:
        return "Foundation"
    if "bathroom" in path_text or "kitchen" in path_text:
        return "Fixture"
    if "furniture" in path_text or "living_room" in path_text or "living room" in path_text or "bedroom" in path_text:
        return "Furniture"
    if "vegetation" in path_text:
        return "Vegetation"
    return existing or "GenericBIMObject"


def normalize_editability(editability: Any, has_source_model: bool) -> Dict[str, Any]:
    if not isinstance(editability, dict):
        editability = {}
    status = editability.get("status", "static_reference")
    if status not in ALLOWED_EDITABILITY_STATUSES:
        status = "static_reference"
    normalized = dict(editability)
    if status == "static_reference" and has_source_model and editability.get("status") == "parametric_source_available":
        status = "parametric_source_available"
    normalized["status"] = status
    normalized["parametricSourceAvailable"] = bool(editability.get("parametricSourceAvailable", has_source_model))
    normalized["generatorAvailable"] = bool(editability.get("generatorAvailable", False))
    normalized["schemaReady"] = True
    return normalized


def merge_parameter(existing: Optional[Dict[str, Any]], catalog_entry: Optional[Dict[str, Any]], required: bool) -> Dict[str, Any]:
    if catalog_entry:
        merged = dict(catalog_entry)
    else:
        existing_name = existing.get("name") if existing else "customParameter"
        merged = {
            "name": existing_name,
            "label": existing_name,
            "description": "Custom parameter not yet defined in the Phase 2 catalog.",
            "type": "text",
            "unit": None,
            "default": None,
            "min": None,
            "max": None,
            "options": None,
            "uiControl": "text_input",
            "toolbarGroup": "custom",
            "validation": {"required": required},
            "custom": True,
        }
    if existing:
        for key, value in existing.items():
            if key == "validation" and isinstance(value, dict):
                validation = dict(merged.get("validation", {}))
                validation.update({k: v for k, v in value.items() if v is not None})
                merged["validation"] = validation
            elif key not in merged or value not in (None, "", []):
                merged[key] = value
    validation = dict(merged.get("validation", {}))
    validation["required"] = required
    if merged.get("type") == "number" and "positive" not in validation:
        validation["positive"] = True
    merged["validation"] = validation
    return merged


def enrich_parameters(template: Dict[str, Any], element_schema: Dict[str, Any], catalog: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], List[str], List[str]]:
    existing_parameters = template.get("parameters", [])
    if not isinstance(existing_parameters, list):
        existing_parameters = []
    existing_by_name = {param.get("name"): param for param in existing_parameters if isinstance(param, dict) and param.get("name")}
    required = list(element_schema.get("requiredParameters", []))
    optional = list(element_schema.get("optionalParameters", []))
    ordered_names: List[str] = []
    for name in required + optional + list(existing_by_name.keys()):
        if name not in ordered_names:
            ordered_names.append(name)
    enriched: List[Dict[str, Any]] = []
    custom: List[str] = []
    for name in ordered_names:
        existing = existing_by_name.get(name)
        catalog_entry = catalog.get(name)
        if not catalog_entry and (not existing or not existing.get("custom")):
            custom.append(name)
        enriched.append(merge_parameter(existing, catalog_entry, name in required))
    missing_required = [name for name in required if name not in existing_by_name]
    return enriched, missing_required, sorted(custom)


def build_toolbar(element_schema: Dict[str, Any], parameters: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    available = {param.get("name") for param in parameters}
    groups = []
    for group in element_schema.get("toolbarGroups", []):
        group_params = [name for name in group.get("parameters", []) if name in available]
        if group_params:
            copied = dict(group)
            copied["parameters"] = group_params
            groups.append(copied)
    grouped = {name for group in groups for name in group["parameters"]}
    custom_parameters = [param.get("name") for param in parameters if param.get("name") not in grouped]
    if custom_parameters:
        groups.append({"groupId": "custom", "label": "Custom", "parameters": custom_parameters})
    return {"mode": "floating_parameter_panel", "groups": groups}


def validation_issue(template: Dict[str, Any], template_path: Path, code: str, message: str, fix: str, valid: bool = False) -> ValidationIssue:
    return ValidationIssue(
        asset_id=str(template.get("id", "")),
        template_path=template_path.as_posix(),
        element_type=str(template.get("elementType", "")),
        category=str(template.get("category", "")),
        valid=valid,
        issue_code=code,
        issue_message=message,
        recommended_fix=fix,
    )


def validate_template(template: Dict[str, Any], template_path: Path, element_schemas: Dict[str, Any], catalog: Dict[str, Any], rules: Dict[str, Any]) -> List[ValidationIssue]:
    issues: List[ValidationIssue] = []
    for field_name in rules.get("requiredTemplateFields", []):
        if field_name not in template:
            issues.append(validation_issue(template, template_path, "missing_required_field", f"template.json is missing '{field_name}'.", f"Add the '{field_name}' field."))
    asset_id = template.get("id")
    if asset_id and not is_snake_case(str(asset_id)):
        issues.append(validation_issue(template, template_path, "asset_id_not_snake_case", "Asset id should use snake_case.", "Rename the asset id with lowercase words separated by underscores."))
    category = template.get("category")
    if category and not is_dot_notation(str(category)):
        issues.append(validation_issue(template, template_path, "category_not_dot_notation", "Category should use dot notation such as architecture.doors.wood.", "Normalize the category path to dot notation."))
    element_type = template.get("elementType")
    if element_type not in element_schemas:
        issues.append(validation_issue(template, template_path, "unsupported_element_type", f"Element type '{element_type}' is not in element_type_schemas.json.", "Infer or map this asset to a supported BIM element type."))
    status = template.get("editability", {}).get("status") if isinstance(template.get("editability"), dict) else None
    if status and status not in ALLOWED_EDITABILITY_STATUSES:
        issues.append(validation_issue(template, template_path, "unsupported_editability_status", f"Editability status '{status}' is not allowed.", "Use a status from validation_rules.json."))
    parameters = template.get("parameters", [])
    if not isinstance(parameters, list):
        issues.append(validation_issue(template, template_path, "parameters_not_list", "Parameters must be a list.", "Replace parameters with a list of parameter objects."))
        parameters = []
    parameter_names = set()
    for parameter in parameters:
        if not isinstance(parameter, dict):
            issues.append(validation_issue(template, template_path, "invalid_parameter", "Parameter entries must be objects.", "Replace invalid parameter entries with objects."))
            continue
        name = parameter.get("name")
        if not name:
            issues.append(validation_issue(template, template_path, "parameter_missing_name", "A parameter is missing a name.", "Add a camelCase parameter name."))
            continue
        parameter_names.add(name)
        if not is_camel_case(str(name)):
            issues.append(validation_issue(template, template_path, "parameter_name_not_camel_case", f"Parameter '{name}' should use camelCase.", "Rename the parameter using camelCase."))
        if name not in catalog and not parameter.get("custom"):
            issues.append(validation_issue(template, template_path, "parameter_not_in_catalog", f"Parameter '{name}' is not in parameter_catalog.json.", "Add it to the catalog or mark it custom."))
    schema = element_schemas.get(element_type)
    if schema:
        for required_name in schema.get("requiredParameters", []):
            if required_name not in parameter_names:
                issues.append(validation_issue(template, template_path, "missing_required_parameter", f"Required parameter '{required_name}' is missing.", "Run Phase 2 enrichment or add the required parameter."))
    return issues


def enrich_template(template: Dict[str, Any], template_path: Path, element_schemas: Dict[str, Any], catalog: Dict[str, Any], rules: Dict[str, Any]) -> ProcessedTemplate:
    original = json.loads(json.dumps(template))
    element_type = infer_element_type(template, template_path)
    schema = element_schemas.get(element_type) or element_schemas["GenericBIMObject"]
    enriched = dict(template)
    enriched["elementType"] = schema["elementType"]
    file_types = enriched.get("fileTypes", {}) if isinstance(enriched.get("fileTypes"), dict) else {}
    has_source_model = "source_model" in file_types
    enriched["editability"] = normalize_editability(enriched.get("editability", {}), has_source_model)
    parameters, missing_required, custom_parameters = enrich_parameters(enriched, schema, catalog)
    enriched["parameters"] = parameters
    enriched["toolbar"] = build_toolbar(schema, parameters)
    issues = validate_template(enriched, template_path, element_schemas, catalog, rules)
    enriched["schema"] = {
        "version": SCHEMA_VERSION,
        "schemaReady": not issues,
        "validatedAt": None,
        "issues": [issue.issue_code for issue in issues],
    }
    notes = str(enriched.get("notes", "")).strip()
    phase2_note = "Schema enriched in Phase 2."
    if phase2_note not in notes:
        notes = f"{notes} {phase2_note}".strip()
    generator_note = "Needs parametric generator before real-time editing."
    if generator_note not in notes:
        notes = f"{notes} {generator_note}".strip()
    enriched["notes"] = notes
    # Validate again after schema metadata is present so issues reflect final output.
    issues = validate_template(enriched, template_path, element_schemas, catalog, rules)
    enriched["schema"]["schemaReady"] = not issues
    enriched["schema"]["issues"] = [issue.issue_code for issue in issues]
    unsupported = enriched.get("elementType") not in element_schemas
    changed = enriched != original
    return ProcessedTemplate(template_path, original, enriched, issues, missing_required, custom_parameters, unsupported, changed)


def find_template_files(library_root: Path) -> Iterable[Path]:
    for path in library_root.rglob("template.json"):
        if "00_metadata" in path.relative_to(library_root).parts:
            continue
        if path.is_file():
            yield path


def category_matches(template: Dict[str, Any], limit_category: Optional[str]) -> bool:
    if not limit_category:
        return True
    category = str(template.get("category", ""))
    return category == limit_category or category.startswith(limit_category + ".")


def backup_template(path: Path) -> Path:
    candidate = path.with_suffix(path.suffix + ".bak")
    counter = 2
    while candidate.exists():
        candidate = path.with_suffix(path.suffix + f".bak{counter}")
        counter += 1
    shutil.copy2(path, candidate)
    return candidate


def process_library(library_root: Path, report_dir: Path, dry_run: bool, write: bool, backup: bool, limit_category: Optional[str], schema_root: Path = DEFAULT_SCHEMA_ROOT) -> RunSummary:
    element_schemas, catalog, rules = load_schema_config(schema_root)
    summary = RunSummary()
    for template_path in sorted(find_template_files(library_root)):
        template = load_json(template_path)
        if not isinstance(template, dict):
            template = {}
        if not category_matches(template, limit_category):
            continue
        processed = enrich_template(template, template_path, element_schemas, catalog, rules)
        summary.processed.append(processed)
        if processed.enriched.get("category"):
            summary.categories.add(str(processed.enriched["category"]))
        if write and processed.changed:
            if backup:
                backup_template(template_path)
            write_json(template_path, processed.enriched)
    write_reports(report_dir, summary, element_schemas)
    return summary


def write_reports(report_dir: Path, summary: RunSummary, element_schemas: Dict[str, Any]) -> None:
    report_dir.mkdir(parents=True, exist_ok=True)
    write_schema_report(report_dir / "phase2_schema_report.md", summary)
    write_validation_report(report_dir / "phase2_validation_report.csv", summary)
    write_parameter_coverage(report_dir / "phase2_parameter_coverage.csv", summary, element_schemas)
    write_toolbar_groups(report_dir / "phase2_toolbar_groups.json", summary)
    write_unsupported_assets(report_dir / "phase2_unsupported_assets.csv", summary)


def write_schema_report(path: Path, summary: RunSummary) -> None:
    lines = [
        "# Phase 2 Parameter Schema Report",
        "",
        f"- Total template.json files scanned: {summary.scanned_count}",
        f"- Total templates valid: {summary.valid_count}",
        f"- Total templates enriched: {summary.enriched_count}",
        f"- Total templates with missing required parameters: {summary.missing_required_count}",
        f"- Total templates with unsupported element type: {summary.unsupported_count}",
        f"- Total custom parameters found: {summary.custom_parameter_count}",
        "",
        "## Categories processed",
        "",
    ]
    lines.extend(f"- {category}" for category in sorted(summary.categories))
    lines.extend([
        "",
        "## Limitations",
        "",
        "- Phase 2 enriches metadata only; it does not edit FreeCAD, STEP, STL, BREP, image, or documentation assets.",
        "- Added parameters are schema placeholders and do not prove that geometry can regenerate from those values.",
        "- Static exchange and mesh files still need generator work before real-time editing is possible.",
        "",
        "## Next recommended step",
        "",
        "Phase 3 should create geometry generators that consume these validated schemas.",
    ])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_validation_report(path: Path, summary: RunSummary) -> None:
    fieldnames = ["asset id", "template path", "element type", "category", "valid true/false", "issue code", "issue message", "recommended fix"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for item in summary.processed:
            if item.issues:
                for issue in item.issues:
                    writer.writerow({
                        "asset id": issue.asset_id,
                        "template path": issue.template_path,
                        "element type": issue.element_type,
                        "category": issue.category,
                        "valid true/false": "false",
                        "issue code": issue.issue_code,
                        "issue message": issue.issue_message,
                        "recommended fix": issue.recommended_fix,
                    })
            else:
                writer.writerow({
                    "asset id": item.enriched.get("id", ""),
                    "template path": item.path.as_posix(),
                    "element type": item.enriched.get("elementType", ""),
                    "category": item.enriched.get("category", ""),
                    "valid true/false": "true",
                    "issue code": "",
                    "issue message": "",
                    "recommended fix": "",
                })


def write_parameter_coverage(path: Path, summary: RunSummary, element_schemas: Dict[str, Any]) -> None:
    totals: Dict[str, Dict[str, Any]] = defaultdict(lambda: {"assets": 0, "parameter_counts": [], "missing": 0})
    for item in summary.processed:
        element_type = str(item.enriched.get("elementType", "GenericBIMObject"))
        totals[element_type]["assets"] += 1
        totals[element_type]["parameter_counts"].append(len(item.enriched.get("parameters", [])))
        totals[element_type]["missing"] += len(item.missing_required)
    fieldnames = ["element type", "total assets", "required parameters", "optional parameters", "average parameter count", "missing required parameter count"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for element_type in sorted(totals):
            schema = element_schemas.get(element_type, {})
            counts = totals[element_type]["parameter_counts"]
            average = sum(counts) / len(counts) if counts else 0
            writer.writerow({
                "element type": element_type,
                "total assets": totals[element_type]["assets"],
                "required parameters": ";".join(schema.get("requiredParameters", [])),
                "optional parameters": ";".join(schema.get("optionalParameters", [])),
                "average parameter count": f"{average:.2f}",
                "missing required parameter count": totals[element_type]["missing"],
            })


def write_toolbar_groups(path: Path, summary: RunSummary) -> None:
    groups: Dict[str, Any] = {}
    for item in summary.processed:
        element_type = str(item.enriched.get("elementType", "GenericBIMObject"))
        groups.setdefault(element_type, item.enriched.get("toolbar", {"mode": "floating_parameter_panel", "groups": []}))
    write_json(path, groups)


def write_unsupported_assets(path: Path, summary: RunSummary) -> None:
    fieldnames = ["asset id", "template path", "element type", "category", "reason"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for item in summary.processed:
            if item.unsupported:
                writer.writerow({
                    "asset id": item.enriched.get("id", ""),
                    "template path": item.path.as_posix(),
                    "element type": item.enriched.get("elementType", ""),
                    "category": item.enriched.get("category", ""),
                    "reason": "No supported useful BIM schema could be assigned.",
                })


def print_summary(summary: RunSummary, report_dir: Path, dry_run: bool, write: bool, backup: bool) -> None:
    print("Phase 2 parameter schema processing complete")
    print(f"Dry run: {'yes' if dry_run else 'no'}")
    print(f"Write templates: {'yes' if write else 'no'}")
    print(f"Backup templates: {'yes' if backup else 'no'}")
    print(f"Templates scanned: {summary.scanned_count}")
    print(f"Templates valid after enrichment: {summary.valid_count}")
    print(f"Templates enriched: {summary.enriched_count}")
    print(f"Templates with missing required parameters before enrichment: {summary.missing_required_count}")
    print(f"Unsupported element types: {summary.unsupported_count}")
    print(f"Custom parameters found: {summary.custom_parameter_count}")
    print(f"Reports: {report_dir}")


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate and enrich Phase 1 cleaned BIM template.json files with Phase 2 parameter schemas.")
    parser.add_argument("--library-root", required=True, help="Path to the cleaned BIM library generated by Phase 1, or any folder containing template.json files.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true", help="Validate and report only; do not update template.json files.")
    mode.add_argument("--write", action="store_true", help="Update/enrich template.json files.")
    parser.add_argument("--backup", action="store_true", help="Before writing, create .bak copies of template.json files.")
    parser.add_argument("--limit-category", help="Only process a category such as architecture.doors or mep.hvac_ducts.")
    parser.add_argument("--report-dir", help="Where to write Phase 2 reports. Defaults to <library-root>/00_metadata/phase2_schema_reports.")
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    library_root = Path(args.library_root).resolve()
    if not library_root.exists() or not library_root.is_dir():
        raise SystemExit(f"Library root does not exist: {library_root}")
    if args.backup and not args.write:
        raise SystemExit("--backup can only be used with --write.")
    report_dir = Path(args.report_dir).resolve() if args.report_dir else library_root / "00_metadata" / "phase2_schema_reports"
    summary = process_library(library_root, report_dir, args.dry_run, args.write, args.backup, args.limit_category)
    print_summary(summary, report_dir, args.dry_run, args.write, args.backup)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
