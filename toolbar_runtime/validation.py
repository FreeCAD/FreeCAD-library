"""Validation helpers for Phase 4 toolbar state and parameter edits."""
from __future__ import annotations
from typing import Any, Dict, List

REQUIRED_TEMPLATE_FIELDS = ["id","elementType","category","displayName","parameters"]

def validate_template_for_toolbar(template: Dict[str, Any]) -> List[Dict[str, str]]:
    issues=[]
    for f in REQUIRED_TEMPLATE_FIELDS:
        if f not in template: issues.append({"code":"missing_field","message":f"Missing {f}","severity":"error","recommendedFix":f"Add {f} to template.json."})
    if not isinstance(template.get("parameters", []), list): issues.append({"code":"parameters_not_list","message":"parameters must be a list","severity":"error","recommendedFix":"Use a list of parameter objects."})
    return issues

def validate_parameter_value(parameter_definition: Dict[str, Any], value: Any) -> List[str]:
    issues=[]; typ=parameter_definition.get("type")
    if typ in {"number","integer"} or parameter_definition.get("uiControl") == "number_input":
        try: number=float(value)
        except (TypeError,ValueError): return ["Value must be numeric."]
        if parameter_definition.get("validation",{}).get("positive") and number <= 0: issues.append("Value must be positive.")
        if parameter_definition.get("min") is not None and number < float(parameter_definition["min"]): issues.append(f"Value must be >= {parameter_definition['min']}.")
        if parameter_definition.get("max") is not None and number > float(parameter_definition["max"]): issues.append(f"Value must be <= {parameter_definition['max']}.")
    if parameter_definition.get("options") and value not in parameter_definition["options"]: issues.append("Value must be one of the allowed options.")
    return issues

def validate_object_state(object_state: Dict[str, Any]) -> List[str]:
    return [f"Missing {f}" for f in ["instanceId","assetId","elementType","parameters","placement","editability"] if f not in object_state]

def get_validation_issues(template: Dict[str, Any]) -> List[Dict[str, str]]:
    return validate_template_for_toolbar(template)
