"""Object instance state helpers for Phase 4."""
from __future__ import annotations
import copy, json
from typing import Any, Dict
from .schema_adapter import FALLBACK_DEFAULTS

_counter = 0

def apply_defaults(template: Dict[str, Any]) -> Dict[str, Any]:
    element = template.get("elementType","GenericBIMObject")
    fallbacks = FALLBACK_DEFAULTS.get(element, FALLBACK_DEFAULTS["GenericBIMObject"])
    values = {}
    for p in template.get("parameters", []):
        name = p.get("name")
        if name: values[name] = p.get("default") if p.get("default") is not None else fallbacks.get(name)
    for k,v in fallbacks.items(): values.setdefault(k,v)
    return values

def build_placement_default() -> Dict[str, float]:
    return {"x":0,"y":0,"z":0,"rotation":0}

def create_object_instance(asset_record: Dict[str, Any]) -> Dict[str, Any]:
    global _counter
    _counter += 1
    return {"instanceId":f"object_{_counter:03d}","assetId":asset_record["id"],"elementType":asset_record.get("elementType","GenericBIMObject"),"category":asset_record.get("category","uncategorized"),"parameters":apply_defaults(asset_record),"placement":build_placement_default(),"editability":copy.deepcopy(asset_record.get("editability",{}))}

def update_parameter(object_state: Dict[str, Any], parameter_name: str, value: Any) -> Dict[str, Any]:
    updated = copy.deepcopy(object_state); updated.setdefault("parameters",{})[parameter_name]=value; return updated

def serialize_object_state(object_state: Dict[str, Any]) -> str:
    return json.dumps(object_state, indent=2)
