"""JSON export helpers for Phase 4 toolbar demo data."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict, List
from .schema_adapter import CONTROL_TYPES, FALLBACK_DEFAULTS

def _write(path: Path, data: Any) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True); Path(path).write_text(json.dumps(data, indent=2)+"\n", encoding="utf-8")

def export_assets_json(records: List[Dict[str, Any]], path: Path) -> None: _write(path, {"assets": records})

def export_toolbar_config(records: List[Dict[str, Any]], path: Path) -> None:
    types=sorted({r.get("elementType") for r in records if r.get("elementType")})
    groups={}
    for r in records: groups.setdefault(r.get("elementType","GenericBIMObject"), r.get("toolbar",{}).get("groups",[]))
    _write(path,{"availableElementTypes":types,"controlTypes":CONTROL_TYPES,"toolbarGroupsByElementType":groups,"validationRules":{"positiveNumbers":True,"respectMinMax":True},"fallbackDefaults":FALLBACK_DEFAULTS})

def export_object_instances(instances: List[Dict[str, Any]], path: Path) -> None: _write(path, {"instances": instances})

def export_geometry_links(records: List[Dict[str, Any]], path: Path) -> None: _write(path, {r["id"]: r.get("geometry",{}) for r in records})
