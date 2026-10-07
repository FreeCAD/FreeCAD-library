"""Base generator class for Phase 3 placeholder geometry."""
from __future__ import annotations

from typing import Any, Dict, List


class BaseGenerator:
    element_type = "GenericBIMObject"
    generator_name = "BaseGenerator"
    generator_version = "phase3.v1"
    fallback_parameters: Dict[str, Any] = {"width": 1000, "depth": 1000, "height": 1000}

    def can_generate(self, template: dict) -> bool:
        return True

    def template_parameters(self, template: dict) -> Dict[str, Any]:
        values: Dict[str, Any] = {}
        for parameter in template.get("parameters", []):
            if isinstance(parameter, dict) and parameter.get("name"):
                values[parameter["name"]] = parameter.get("default")
        return values

    def default_parameters(self, template: dict) -> Dict[str, Any]:
        params = dict(self.fallback_parameters)
        for name, value in self.template_parameters(template).items():
            if value is not None:
                params[name] = value
        return params

    def positive_number(self, params: Dict[str, Any], name: str, fallback: float) -> float:
        value = params.get(name, fallback)
        try:
            value = float(value)
        except (TypeError, ValueError):
            value = float(fallback)
        return value if value > 0 else float(fallback)

    def validate_parameters(self, params: dict) -> List[str]:
        issues = []
        for key, value in params.items():
            if isinstance(value, (int, float)) and value < 0:
                issues.append(f"{key} should not be negative")
        return issues

    def geometry_metadata(self, template: dict, params: dict, mesh: dict, notes: str = "Simple parametric placeholder generated from template parameters.") -> dict:
        return {
            "assetId": template.get("id", "unknown_asset"),
            "elementType": template.get("elementType", self.element_type),
            "category": template.get("category", "uncategorized"),
            "units": "mm",
            "parametersUsed": params,
            "geometryType": "mesh",
            "metadata": {
                "generator": self.generator_name,
                "generatorVersion": self.generator_version,
                "phase": "phase3",
                "isPlaceholderGeometry": True,
                "notes": notes,
            },
        }

    def generate(self, template: dict) -> dict:
        raise NotImplementedError("Subclasses must implement generate().")
