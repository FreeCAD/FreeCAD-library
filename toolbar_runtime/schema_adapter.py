"""Adapters that turn Phase 2 template.json files into toolbar-ready records."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

CONTROL_BY_TYPE = {"number":"number_input","integer":"number_input","boolean":"checkbox","text":"text_input","url":"text_input","list":"text_input"}
FALLBACK_DEFAULTS = {
 "Door":{"width":900,"height":2100,"thickness":45,"frameWidth":100,"openingAngle":90},
 "Window":{"width":1200,"height":1200,"frameDepth":80,"frameWidth":60,"panelCount":2},
 "Beam":{"length":3000,"width":200,"height":400},
 "Roof":{"length":4000,"width":3000,"thickness":150,"slope":15},
 "ConstructionBlock":{"length":390,"width":190,"height":190},
 "Pipe":{"length":1000,"diameter":100,"innerDiameter":80},
 "Duct":{"length":1000,"width":400,"height":250,"thickness":10,"ductShape":"rectangular"},
 "Furniture":{"width":600,"depth":600,"height":900},"Fixture":{"width":600,"depth":600,"height":900},
 "Foundation":{"length":1500,"width":1500,"height":500},"Vegetation":{"height":3000,"diameter":1500},
 "GenericBIMObject":{"width":1000,"depth":1000,"height":1000},
}
CONTROL_TYPES = ["number_input","select","checkbox","text_input","textarea","color_picker"]

def load_template(path: Path) -> Dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))

def scan_templates(library_root: Path) -> Iterable[Path]:
    for path in Path(library_root).rglob("template.json"):
        if "00_metadata" not in path.parts and path.is_file():
            yield path

def infer_ui_control(parameter: Dict[str, Any]) -> str:
    if parameter.get("uiControl"):
        return parameter["uiControl"]
    if parameter.get("options"):
        return "select"
    return CONTROL_BY_TYPE.get(str(parameter.get("type","text")), "text_input")

def normalize_parameter(parameter: Dict[str, Any]) -> Dict[str, Any]:
    p = dict(parameter)
    p.setdefault("name", "unnamed")
    p.setdefault("label", p["name"])
    p.setdefault("description", "")
    p.setdefault("type", "text")
    p.setdefault("unit", None)
    p.setdefault("default", None)
    p.setdefault("min", None)
    p.setdefault("max", None)
    p.setdefault("options", None)
    p["uiControl"] = infer_ui_control(p)
    p.setdefault("toolbarGroup", "general")
    p.setdefault("validation", {})
    return p

def extract_toolbar_groups(template: Dict[str, Any]) -> List[Dict[str, Any]]:
    toolbar = template.get("toolbar", {}) if isinstance(template.get("toolbar"), dict) else {}
    groups = toolbar.get("groups") if isinstance(toolbar.get("groups"), list) else []
    if groups:
        return groups
    grouped: Dict[str, List[str]] = {}
    for p in template.get("parameters", []):
        if isinstance(p, dict) and p.get("name"):
            grouped.setdefault(p.get("toolbarGroup", "general"), []).append(p["name"])
    return [{"groupId": gid, "label": gid.replace("_"," ").title(), "parameters": names} for gid, names in grouped.items()]

def template_to_toolbar_config(template: Dict[str, Any]) -> Dict[str, Any]:
    params = [normalize_parameter(p) for p in template.get("parameters", []) if isinstance(p, dict)]
    return {"mode":"floating_parameter_panel","groups":extract_toolbar_groups({**template,"parameters":params})}

def _geometry_links(asset_id: str, geometry_root: Optional[Path]) -> Dict[str, str]:
    if not geometry_root:
        return {}
    matches = list(Path(geometry_root).rglob(f"{asset_id}/geometry.json"))
    if not matches:
        return {}
    folder = matches[0].parent
    links = {}
    for key, name in [("geometryJson","geometry.json"),("obj","preview.obj"),("stl","preview.stl")]:
        p = folder / name
        if p.exists(): links[key] = p.as_posix()
    return links

def build_asset_record(template_path: Path, template: Dict[str, Any], geometry_root: Optional[Path] = None) -> Dict[str, Any]:
    params = [normalize_parameter(p) for p in template.get("parameters", []) if isinstance(p, dict)]
    return {"id":template.get("id"),"displayName":template.get("displayName", template.get("id")),"elementType":template.get("elementType","GenericBIMObject"),"category":template.get("category","uncategorized"),"templatePath":Path(template_path).as_posix(),"geometry":_geometry_links(str(template.get("id")), geometry_root),"toolbar":template_to_toolbar_config({**template,"parameters":params}),"parameters":params,"editability":template.get("editability",{})}
