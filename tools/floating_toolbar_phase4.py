#!/usr/bin/env python3
"""Build and serve Phase 4 floating parameter toolbar demo data."""
from __future__ import annotations
import argparse, csv, json, shutil, sys
from dataclasses import dataclass, field
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path: sys.path.insert(0, str(REPO_ROOT))

from toolbar_runtime.export import export_assets_json, export_geometry_links, export_object_instances, export_toolbar_config
from toolbar_runtime.schema_adapter import build_asset_record, load_template, scan_templates
from toolbar_runtime.state_manager import create_object_instance
from toolbar_runtime.validation import get_validation_issues

UI_SOURCE = REPO_ROOT / "ui" / "floating_parameter_toolbar"
LIMITATIONS = ["Prototype UI only.", "Does not edit FCStd/STEP/STL/BREP/source CAD files.", "Canvas preview is simplified 2.5D placeholder drawing.", "Phase 5 is still required for real-time viewport integration."]

@dataclass
class Row:
    asset_id: str; display_name: str; element_type: str; category: str; template_path: str; toolbar_ready: bool; parameter_count: int; toolbar_group_count: int; issues: List[Dict[str,str]] = field(default_factory=list)

@dataclass
class Summary:
    rows: List[Row] = field(default_factory=list)
    scanned: int = 0
    @property
    def ready(self): return sum(1 for r in self.rows if r.toolbar_ready)
    @property
    def skipped(self): return self.scanned - len(self.rows)
    @property
    def unsupported(self): return sum(1 for r in self.rows if not r.toolbar_ready)
    @property
    def validation_issue_count(self): return sum(len(r.issues) for r in self.rows)
    @property
    def missing_toolbar_groups(self): return sum(1 for r in self.rows if r.toolbar_group_count == 0)
    @property
    def control_count(self): return sum(r.parameter_count for r in self.rows)

def matches(record: Dict[str, Any], limit_category: Optional[str], limit_element_type: Optional[str], asset_id: Optional[str]) -> bool:
    c = record.get("category", ""); e = record.get("elementType", "")
    return not ((limit_category and not (c == limit_category or c.startswith(limit_category+"."))) or (limit_element_type and e != limit_element_type) or (asset_id and record.get("id") != asset_id))

def collect_records(library_root: Path, geometry_root: Optional[Path], limit_category=None, limit_element_type=None, asset_id=None) -> tuple[List[Dict[str,Any]], Summary]:
    records=[]; summary=Summary()
    for template_path in sorted(scan_templates(library_root)):
        summary.scanned += 1
        template = load_template(template_path)
        record = build_asset_record(template_path, template, geometry_root)
        if not matches(record, limit_category, limit_element_type, asset_id):
            continue
        issues = get_validation_issues(template)
        groups = record.get("toolbar",{}).get("groups",[])
        row = Row(str(record.get("id","")), str(record.get("displayName","")), str(record.get("elementType","")), str(record.get("category","")), template_path.as_posix(), not issues, len(record.get("parameters",[])), len(groups), issues)
        summary.rows.append(row); records.append(record)
    return records, summary

def copy_ui(output_root: Path) -> None:
    target = output_root / "ui"
    if target.exists(): shutil.rmtree(target)
    shutil.copytree(UI_SOURCE, target, ignore=shutil.ignore_patterns("sample_data"))

def write_reports(report_dir: Path, summary: Summary) -> None:
    report_dir.mkdir(parents=True, exist_ok=True)
    types = sorted({r.element_type for r in summary.rows})
    lines=["# Phase 4 Floating Toolbar Report","",f"- Total templates scanned: {summary.scanned}",f"- Total toolbar-ready assets: {summary.ready}",f"- Total skipped assets: {summary.skipped}",f"- Total unsupported assets: {summary.unsupported}",f"- Element types covered: {', '.join(types) if types else 'none'}",f"- Parameter controls generated: {summary.control_count}",f"- Assets with missing toolbar groups: {summary.missing_toolbar_groups}",f"- Validation issues found: {summary.validation_issue_count}","","## Limitations","",*[f"- {x}" for x in LIMITATIONS],"","## Next recommended step","","Phase 5 should connect toolbar edits to real-time regeneration and viewport integration."]
    (report_dir/"phase4_toolbar_report.md").write_text("\n".join(lines)+"\n", encoding="utf-8")
    with (report_dir/"phase4_toolbar_report.csv").open("w",encoding="utf-8",newline="") as h:
        w=csv.DictWriter(h, fieldnames=["asset_id","display_name","element_type","category","template_path","toolbar_ready","parameter_count","toolbar_group_count","issues"]); w.writeheader()
        for r in summary.rows: w.writerow({"asset_id":r.asset_id,"display_name":r.display_name,"element_type":r.element_type,"category":r.category,"template_path":r.template_path,"toolbar_ready":str(r.toolbar_ready).lower(),"parameter_count":r.parameter_count,"toolbar_group_count":r.toolbar_group_count,"issues":"; ".join(i['code'] for i in r.issues)})
    with (report_dir/"phase4_toolbar_unsupported_assets.csv").open("w",encoding="utf-8",newline="") as h:
        w=csv.DictWriter(h, fieldnames=["asset_id","element_type","category","template_path","reason"]); w.writeheader()
        for r in summary.rows:
            if not r.toolbar_ready: w.writerow({"asset_id":r.asset_id,"element_type":r.element_type,"category":r.category,"template_path":r.template_path,"reason":"; ".join(i['message'] for i in r.issues)})
    with (report_dir/"phase4_toolbar_validation_report.csv").open("w",encoding="utf-8",newline="") as h:
        w=csv.DictWriter(h, fieldnames=["asset_id","template_path","issue_code","issue_message","severity","recommended_fix"]); w.writeheader()
        for r in summary.rows:
            for i in r.issues: w.writerow({"asset_id":r.asset_id,"template_path":r.template_path,"issue_code":i.get("code"),"issue_message":i.get("message"),"severity":i.get("severity"),"recommended_fix":i.get("recommendedFix")})

def write_demo(output_root: Path, records: List[Dict[str,Any]], summary: Summary, report_dir: Path) -> None:
    output_root.mkdir(parents=True, exist_ok=True)
    export_assets_json(records, output_root/"assets.json")
    export_toolbar_config(records, output_root/"toolbar_config.json")
    export_object_instances([create_object_instance(r) for r in records[:5]], output_root/"object_instances.json")
    export_geometry_links(records, output_root/"geometry_links.json")
    copy_ui(output_root); write_reports(report_dir, summary)

def serve(output: Path, port: int) -> None:
    import os
    os.chdir(output)
    print(f"Serving Phase 4 toolbar demo at http://localhost:{port}/ui/index.html")
    ThreadingHTTPServer(("", port), SimpleHTTPRequestHandler).serve_forever()

def process(library_root: Optional[Path], output: Path, geometry_root: Optional[Path], dry_run: bool, write: bool, report_dir: Path, **filters) -> Summary:
    if not library_root:
        raise SystemExit("--library-root is required for --dry-run or --write.")
    records, summary = collect_records(library_root, geometry_root, **filters)
    if write: write_demo(output, records, summary, report_dir)
    else: write_reports(report_dir, summary)
    return summary

def parse_args(argv: Optional[Sequence[str]]=None):
    p=argparse.ArgumentParser(description="Build or serve Phase 4 floating parameter toolbar demo data.")
    p.add_argument("--library-root"); p.add_argument("--generated-geometry-root"); p.add_argument("--output", required=True)
    mode=p.add_mutually_exclusive_group(required=True); mode.add_argument("--dry-run", action="store_true"); mode.add_argument("--write", action="store_true"); mode.add_argument("--serve", action="store_true")
    p.add_argument("--port", type=int, default=8765); p.add_argument("--limit-category"); p.add_argument("--limit-element-type"); p.add_argument("--asset-id"); p.add_argument("--report-dir")
    return p.parse_args(argv)

def main(argv: Optional[Sequence[str]]=None) -> int:
    a=parse_args(argv); out=Path(a.output).resolve(); report=Path(a.report_dir).resolve() if a.report_dir else out/"00_reports"
    if a.serve: serve(out, a.port); return 0
    lib=Path(a.library_root).resolve() if a.library_root else None; geo=Path(a.generated_geometry_root).resolve() if a.generated_geometry_root else None
    s=process(lib,out,geo,a.dry_run,a.write,report,limit_category=a.limit_category,limit_element_type=a.limit_element_type,asset_id=a.asset_id)
    print("Phase 4 toolbar data processing complete"); print(f"Dry run: {'yes' if a.dry_run else 'no'}"); print(f"Write demo: {'yes' if a.write else 'no'}"); print(f"Templates scanned: {s.scanned}"); print(f"Toolbar-ready assets: {s.ready}"); print(f"Validation issues: {s.validation_issue_count}"); print(f"Output: {out}"); print(f"Reports: {report}")
    return 0
if __name__ == "__main__": raise SystemExit(main())
