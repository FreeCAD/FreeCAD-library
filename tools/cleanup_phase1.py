#!/usr/bin/env python3
"""Phase 1 CAD/BIM library cleanup for FreeCAD-library.

This script is intentionally conservative:
- it never deletes or moves source files;
- it copies only recognized BIM-relevant asset files;
- it writes all generated files to a separate output directory;
- dry-run mode scans and reports without creating output files.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

FILE_TYPE_RULES = {
    ".FCStd": "source_model",
    ".fcstd": "source_model",
    ".step": "exchange_geometry",
    ".stp": "exchange_geometry",
    ".STEP": "exchange_geometry",
    ".STP": "exchange_geometry",
    ".brep": "kernel_geometry",
    ".stl": "preview_mesh",
    ".STL": "preview_mesh",
    ".png": "preview_or_documentation_image",
    ".jpg": "preview_or_documentation_image",
    ".jpeg": "preview_or_documentation_image",
    ".svg": "preview_or_documentation_image",
    ".avif": "preview_or_documentation_image",
    ".md": "documentation",
    ".txt": "documentation",
    ".pdf": "documentation",
    ".FCMacro": "macro_or_parametric_tool",
    ".FCBak": "backup_file",
    ".GKO": "pcb_manufacturing_file",
    ".GBO": "pcb_manufacturing_file",
    ".GBL": "pcb_manufacturing_file",
    ".GBS": "pcb_manufacturing_file",
    ".GTL": "pcb_manufacturing_file",
    ".GTP": "pcb_manufacturing_file",
    ".GTO": "pcb_manufacturing_file",
    ".GTS": "pcb_manufacturing_file",
    ".DRL": "pcb_manufacturing_file",
}

PCB_EXTENSIONS = {ext for ext, kind in FILE_TYPE_RULES.items() if kind == "pcb_manufacturing_file"}
COPYABLE_FILE_TYPES = {
    "source_model",
    "exchange_geometry",
    "kernel_geometry",
    "preview_mesh",
    "preview_or_documentation_image",
    "documentation",
    "macro_or_parametric_tool",
}

# Source prefix, cleaned category, element type, id prefix.
BIM_CATEGORY_RULES: Sequence[Tuple[str, str, str, str]] = (
    ("Architectural Parts/Doors", "architecture.doors", "Door", "door"),
    ("Architectural Parts/Windows", "architecture.windows", "Window", "window"),
    ("Architectural Parts/Beams", "architecture.beams", "Beam", "beam"),
    ("Architectural Parts/Roof", "architecture.roof", "Roof", "roof"),
    ("Architectural Parts/Construction blocks", "architecture.construction_blocks", "Construction block", "construction_block"),
    ("Architectural Parts/Building Construction", "architecture.construction_blocks", "Construction block", "construction_block"),
    ("Architectural Parts/Bathroom", "architecture.bathroom", "Furniture/fixture", "fixture"),
    ("Architectural Parts/Kitchen", "architecture.kitchen", "Furniture/fixture", "fixture"),
    ("Architectural Parts/Bedroom", "architecture.furniture", "Furniture/fixture", "furniture"),
    ("Architectural Parts/Living room", "architecture.furniture", "Furniture/fixture", "furniture"),
    ("Architectural Parts/Hydro equipment", "mep.hydro_equipment", "Pipe", "pipe"),
    ("Architectural Parts/Electric equipment", "mep.electrical_equipment", "Electrical equipment", "electrical_equipment"),
    ("Generic objects/Foundation", "architecture.foundations", "Foundation", "foundation"),
    ("HVAC/Ducts", "mep.hvac_ducts", "Duct", "duct"),
    ("HVAC/Pipes", "mep.hvac_pipes", "Pipe", "pipe"),
    ("Pipes and tubes", "mep.plumbing_pipes", "Pipe", "pipe"),
    ("Topography", "site.topography", "Topography", "topography"),
    ("Architectural Parts/Symbols/Vegetation symbols", "site.vegetation", "Site symbol", "site_symbol"),
)

NON_BIM_ROOTS = {
    "Computing": "Computing hardware is outside Phase 1 BIM scope.",
    "Electrical Parts": "Electrical/electronic components are archive candidates, except BIM electrical equipment under Architectural Parts.",
    "Electronics Parts": "Electronics/PCB components are outside Phase 1 BIM scope.",
    "Mechanical Parts": "Mechanical components are outside Phase 1 BIM scope.",
    "Robots": "Robotics assets are outside Phase 1 BIM scope.",
    "Sports": "Sports assets are outside Phase 1 BIM scope.",
    "DummiesAndSculptures": "Character/sculpture assets are outside Phase 1 BIM scope.",
}

BASE_OUTPUT_FOLDERS = [
    "00_metadata",
    "architecture/doors",
    "architecture/windows",
    "architecture/beams",
    "architecture/roof",
    "architecture/construction_blocks",
    "architecture/bathroom",
    "architecture/kitchen",
    "architecture/furniture",
    "architecture/foundations",
    "architecture/site_symbols",
    "mep/hvac_ducts",
    "mep/hvac_pipes",
    "mep/plumbing_pipes",
    "mep/hydro_equipment",
    "mep/electrical_equipment",
    "site/topography",
    "site/vegetation",
]


@dataclass(frozen=True)
class CategoryRule:
    source_prefix: PurePosixPath
    category: str
    element_type: str
    id_prefix: str


@dataclass
class SourceFile:
    path: Path
    relative_path: PurePosixPath
    file_type: str
    cleaned_name: str = ""


@dataclass
class AssetGroup:
    id: str
    display_name: str
    category: str
    element_type: str
    id_prefix: str
    original_folder: PurePosixPath
    cleaned_folder: PurePosixPath
    files: List[SourceFile] = field(default_factory=list)


def normalize_name(value: str) -> str:
    """Return a safe snake_case name for folders, IDs, and predictable paths."""
    normalized = value.strip().lower()
    normalized = re.sub(r"[^a-z0-9]+", "_", normalized)
    normalized = re.sub(r"_+", "_", normalized).strip("_")
    return normalized or "unnamed"


def display_name_from_stem(stem: str) -> str:
    words = re.split(r"[^A-Za-z0-9]+", stem.strip())
    return " ".join(word.capitalize() for word in words if word) or "Unnamed"


def classify_file_type(path: Path | str) -> Optional[str]:
    return FILE_TYPE_RULES.get(Path(path).suffix)


def as_posix_relative(path: Path, source_root: Path) -> PurePosixPath:
    return PurePosixPath(path.relative_to(source_root).as_posix())


def build_category_rules() -> List[CategoryRule]:
    rules = [CategoryRule(PurePosixPath(src), category, element, prefix) for src, category, element, prefix in BIM_CATEGORY_RULES]
    return sorted(rules, key=lambda rule: len(rule.source_prefix.parts), reverse=True)


def path_starts_with(path: PurePosixPath, prefix: PurePosixPath) -> bool:
    return path.parts[: len(prefix.parts)] == prefix.parts


def find_bim_rule(relative_path: PurePosixPath, rules: Sequence[CategoryRule]) -> Optional[CategoryRule]:
    for rule in rules:
        if path_starts_with(relative_path, rule.source_prefix):
            return rule
    return None


def non_bim_reason(relative_path: PurePosixPath, file_type: Optional[str]) -> Optional[str]:
    if file_type == "pcb_manufacturing_file":
        return "PCB/Gerber/drill manufacturing file is outside BIM scope."
    if not relative_path.parts:
        return None
    root = relative_path.parts[0]
    if root in NON_BIM_ROOTS:
        return NON_BIM_ROOTS[root]
    if root == "Generic objects" and not path_starts_with(relative_path, PurePosixPath("Generic objects/Foundation")):
        return "Generic objects are archive candidates in Phase 1 except Foundation assets."
    return None


def cleaned_file_name(source_file: Path, file_type: str, used_names: set[str]) -> str:
    extension = source_file.suffix
    base_by_type = {
        "source_model": "source",
        "exchange_geometry": "reference",
        "kernel_geometry": "kernel",
        "preview_mesh": "preview",
        "preview_or_documentation_image": "image",
        "documentation": "documentation",
        "macro_or_parametric_tool": "macro",
        "backup_file": "backup",
        "pcb_manufacturing_file": "pcb",
    }
    base = base_by_type.get(file_type, normalize_name(source_file.stem))
    candidate = f"{base}{extension}"
    counter = 2
    while candidate in used_names:
        candidate = f"{base}_{counter}{extension}"
        counter += 1
    used_names.add(candidate)
    return candidate


def parameter(name: str, label: str, kind: str = "number", unit: Optional[str] = "mm") -> Dict[str, object]:
    data: Dict[str, object] = {"name": name, "label": label, "type": kind, "unit": unit, "default": None}
    if kind == "number":
        data["min"] = None
        data["max"] = None
    return data


def default_parameters(element_type: str) -> List[Dict[str, object]]:
    element = element_type.lower()
    if element == "door":
        return [
            parameter("width", "Width"), parameter("height", "Height"), parameter("thickness", "Thickness"),
            parameter("frameWidth", "Frame Width"), parameter("swingDirection", "Swing Direction", "text", None),
            parameter("openingAngle", "Opening Angle", "number", "deg"), parameter("material", "Material", "text", None),
        ]
    if element == "window":
        return [
            parameter("width", "Width"), parameter("height", "Height"), parameter("frameDepth", "Frame Depth"),
            parameter("glazingType", "Glazing Type", "text", None), parameter("openingType", "Opening Type", "text", None),
            parameter("panelCount", "Panel Count", "integer", None), parameter("material", "Material", "text", None),
        ]
    if element == "beam":
        return [parameter("length", "Length"), parameter("width", "Width"), parameter("height", "Height"), parameter("profileType", "Profile Type", "text", None), parameter("material", "Material", "text", None)]
    if element == "roof":
        return [parameter("length", "Length"), parameter("width", "Width"), parameter("thickness", "Thickness"), parameter("slope", "Slope", "number", "deg"), parameter("material", "Material", "text", None)]
    if element == "construction block":
        return [parameter("length", "Length"), parameter("width", "Width"), parameter("height", "Height"), parameter("material", "Material", "text", None)]
    if element in {"duct", "pipe"}:
        return [parameter("diameter", "Diameter"), parameter("width", "Width"), parameter("height", "Height"), parameter("length", "Length"), parameter("thickness", "Thickness"), parameter("bendAngle", "Bend Angle", "number", "deg"), parameter("material", "Material", "text", None)]
    return [parameter("width", "Width"), parameter("depth", "Depth"), parameter("height", "Height"), parameter("material", "Material", "text", None)]


def source_files_map(files: Sequence[SourceFile]) -> Dict[str, str]:
    result: Dict[str, str] = {}
    key_by_type = {
        "source_model": "freecad",
        "exchange_geometry": "step",
        "kernel_geometry": "brep",
        "preview_mesh": "stl",
        "preview_or_documentation_image": "image",
        "documentation": "documentation",
        "macro_or_parametric_tool": "macro",
    }
    for source in files:
        key = key_by_type.get(source.file_type)
        if key and key not in result:
            result[key] = source.cleaned_name
    return result


def file_types_map(files: Sequence[SourceFile]) -> Dict[str, List[str]]:
    result: Dict[str, List[str]] = {}
    for source in files:
        result.setdefault(source.file_type, []).append(source.cleaned_name)
    return result


def build_template(asset: AssetGroup) -> Dict[str, object]:
    parametric = any(source.file_type == "source_model" for source in asset.files)
    return {
        "id": asset.id,
        "elementType": asset.element_type,
        "category": asset.category,
        "displayName": asset.display_name,
        "originalPath": asset.original_folder.as_posix(),
        "sourceFiles": source_files_map(asset.files),
        "fileTypes": file_types_map(asset.files),
        "editability": {
            "status": "static_reference",
            "parametricSourceAvailable": parametric,
            "generatorAvailable": False,
        },
        "parameters": default_parameters(asset.element_type),
        "notes": "Imported from FreeCAD-library. Needs parametric generator before real-time editing.",
    }


def iter_source_files(source_root: Path) -> Iterable[Path]:
    ignored_dirs = {".git", "__pycache__"}
    for path in source_root.rglob("*"):
        if any(part in ignored_dirs for part in path.relative_to(source_root).parts):
            continue
        if path.is_file():
            yield path


def scan_assets(source_root: Path, limit_category: Optional[str] = None) -> Tuple[Dict[Tuple[str, str], AssetGroup], Dict[str, object]]:
    rules = build_category_rules()
    assets: Dict[Tuple[str, str], AssetGroup] = {}
    non_bim_rows: List[Dict[str, str]] = []
    total_files = 0
    backup_files = 0
    pcb_files = 0

    for path in iter_source_files(source_root):
        total_files += 1
        relative = as_posix_relative(path, source_root)
        file_type = classify_file_type(path)
        if file_type == "backup_file":
            backup_files += 1
        if file_type == "pcb_manufacturing_file":
            pcb_files += 1

        rule = find_bim_rule(relative, rules)
        reason = non_bim_reason(relative, file_type)
        if reason:
            non_bim_rows.append({"path": relative.as_posix(), "type": "file", "reason": reason})

        if not rule or file_type not in COPYABLE_FILE_TYPES:
            continue
        if limit_category and rule.category != limit_category:
            continue

        after_prefix = PurePosixPath(*relative.parts[len(rule.source_prefix.parts) :])
        source_subfolder = PurePosixPath(*after_prefix.parent.parts)
        normalized_parts = [normalize_name(part) for part in source_subfolder.parts]
        asset_slug = normalize_name(path.stem)
        cleaned_folder = PurePosixPath(*rule.category.split("."), *normalized_parts, asset_slug)
        category_suffix = ".".join(normalized_parts)
        category = rule.category if not category_suffix else f"{rule.category}.{category_suffix}"
        id_middle = "_".join(normalized_parts + [asset_slug])
        asset_id = f"{rule.id_prefix}_{id_middle}" if id_middle else f"{rule.id_prefix}_{asset_slug}"
        original_folder = relative.parent
        key = (category, cleaned_folder.as_posix())
        if key not in assets:
            assets[key] = AssetGroup(
                id=asset_id,
                display_name=display_name_from_stem(path.stem),
                category=category,
                element_type=rule.element_type,
                id_prefix=rule.id_prefix,
                original_folder=original_folder,
                cleaned_folder=cleaned_folder,
            )
        assets[key].files.append(SourceFile(path=path, relative_path=relative, file_type=file_type))

    for asset in assets.values():
        used_names: set[str] = set()
        for source in sorted(asset.files, key=lambda item: item.relative_path.as_posix()):
            source.cleaned_name = cleaned_file_name(source.path, source.file_type, used_names)
        asset.files.sort(key=lambda item: item.cleaned_name)

    stats = {
        "total_files": total_files,
        "backup_files": backup_files,
        "pcb_files": pcb_files,
        "non_bim_rows": non_bim_rows,
    }
    return assets, stats


def ensure_output_structure(output_root: Path, include_archive: bool) -> None:
    for folder in BASE_OUTPUT_FOLDERS:
        (output_root / folder).mkdir(parents=True, exist_ok=True)
    if include_archive:
        (output_root / "archive_non_bim").mkdir(parents=True, exist_ok=True)


def copy_asset_files(output_root: Path, assets: Iterable[AssetGroup]) -> int:
    copied = 0
    for asset in assets:
        target_folder = output_root / asset.cleaned_folder
        target_folder.mkdir(parents=True, exist_ok=True)
        for source in asset.files:
            shutil.copy2(source.path, target_folder / source.cleaned_name)
            copied += 1
        with (target_folder / "template.json").open("w", encoding="utf-8") as handle:
            json.dump(build_template(asset), handle, indent=2)
            handle.write("\n")
    return copied


def write_json(path: Path, data: object) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")


def write_metadata(output_root: Path, assets: Sequence[AssetGroup], stats: Dict[str, object], copied_count: int, include_archive: bool, missing_templates: Sequence[Dict[str, str]]) -> None:
    metadata_root = output_root / "00_metadata"
    index = []
    for asset in assets:
        template = build_template(asset)
        index.append({
            "id": asset.id,
            "displayName": asset.display_name,
            "elementType": asset.element_type,
            "category": asset.category,
            "cleanedPath": asset.cleaned_folder.as_posix(),
            "originalPath": asset.original_folder.as_posix(),
            "availableFormats": sorted(template["fileTypes"].keys()),
            "editability.status": template["editability"]["status"],
            "parametricSourceAvailable": template["editability"]["parametricSourceAvailable"],
        })
    write_json(metadata_root / "library_index.json", index)
    write_json(metadata_root / "file_rules.json", FILE_TYPE_RULES)

    non_bim_rows = stats["non_bim_rows"]
    categories = sorted({asset.category for asset in assets})
    report = [
        "# Phase 1 CAD/BIM Library Cleanup Report",
        "",
        f"- Total files scanned: {stats['total_files']}",
        f"- Total BIM-relevant files copied: {copied_count}",
        f"- Total assets created: {len(assets)}",
        f"- Categories created: {len(categories)}",
        f"- Non-BIM folders/files detected: {len(non_bim_rows)}",
        f"- Backup files detected: {stats['backup_files']}",
        f"- PCB/Gerber files detected: {stats['pcb_files']}",
        f"- Archive folder included: {'yes' if include_archive else 'no'}",
        "",
        "## Categories created",
        "",
        *[f"- {category}" for category in categories],
        "",
        "## Limitations",
        "",
        "- Phase 1 does not reverse-engineer dimensions or constraints from CAD files.",
        "- STEP, STL, BREP, and image files are treated as static reference assets.",
        "- FCStd files are marked as possible parametric sources, but not guaranteed editable.",
        "- The script copies selected BIM-relevant files only and leaves the original repository untouched.",
        "",
        "## Next recommended step",
        "",
        "Phase 2 should refine parameter schemas and identify which assets need real generator logic before toolbar-driven editing.",
    ]
    (metadata_root / "cleanup_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")

    with (metadata_root / "missing_template_report.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["asset_id", "cleaned_path", "reason"])
        writer.writeheader()
        writer.writerows(missing_templates)

    with (metadata_root / "non_bim_assets_report.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["path", "type", "reason"])
        writer.writeheader()
        writer.writerows(non_bim_rows)


def validate_templates(assets: Sequence[AssetGroup]) -> List[Dict[str, str]]:
    missing = []
    required = {"id", "elementType", "category", "displayName", "originalPath", "sourceFiles", "fileTypes", "editability", "parameters", "notes"}
    for asset in assets:
        template = build_template(asset)
        missing_keys = sorted(required - set(template.keys()))
        if missing_keys or not asset.files:
            reason = "missing keys: " + ", ".join(missing_keys) if missing_keys else "no source files grouped"
            missing.append({"asset_id": asset.id, "cleaned_path": asset.cleaned_folder.as_posix(), "reason": reason})
    return missing


def print_summary(assets: Sequence[AssetGroup], stats: Dict[str, object], copied_count: int, dry_run: bool, output_root: Path) -> None:
    action = "would copy" if dry_run else "copied"
    print("Phase 1 cleanup scan complete")
    print(f"Output: {output_root}")
    print(f"Dry run: {'yes' if dry_run else 'no'}")
    print(f"Total files scanned: {stats['total_files']}")
    print(f"BIM-relevant files {action}: {copied_count}")
    print(f"Assets created: {len(assets)}")
    print(f"Backup files detected: {stats['backup_files']}")
    print(f"PCB/Gerber files detected: {stats['pcb_files']}")


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Safely copy selected FreeCAD-library assets into a cleaned CAD/BIM structure.")
    parser.add_argument("--source", required=True, help="Path to the FreeCAD-library source repository.")
    parser.add_argument("--output", required=True, help="Path for the cleaned output folder.")
    parser.add_argument("--dry-run", action="store_true", help="Scan and report without creating or copying files.")
    parser.add_argument("--include-archive", action="store_true", help="Create archive_non_bim for future non-BIM archive workflows.")
    parser.add_argument("--limit-category", help="Optional cleaned category filter such as architecture.doors or mep.hvac_pipes.")
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    source_root = Path(args.source).resolve()
    output_root = Path(args.output).resolve()
    if not source_root.exists() or not source_root.is_dir():
        raise SystemExit(f"Source folder does not exist: {source_root}")
    if output_root == source_root or source_root in output_root.parents:
        raise SystemExit("Output must be outside the source repository to keep cleanup non-destructive.")

    assets_by_key, stats = scan_assets(source_root, args.limit_category)
    assets = sorted(assets_by_key.values(), key=lambda asset: asset.cleaned_folder.as_posix())
    copied_count = sum(len(asset.files) for asset in assets)
    missing_templates = validate_templates(assets)

    if not args.dry_run:
        ensure_output_structure(output_root, args.include_archive)
        copied_count = copy_asset_files(output_root, assets)
        write_metadata(output_root, assets, stats, copied_count, args.include_archive, missing_templates)

    print_summary(assets, stats, copied_count, args.dry_run, output_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
