from __future__ import annotations
from .primitive_generators import BoxPlaceholderGenerator

class ConstructionBlockGenerator(BoxPlaceholderGenerator):
    element_type = "ConstructionBlock"
    generator_name = "ConstructionBlockGenerator"
    fallback_parameters = {"length":390,"width":190,"height":190}
    def generate(self, template: dict) -> dict:
        params = self.default_parameters(template)
        result = self.generate_box(template, self.positive_number(params,"length",390), self.positive_number(params,"width",190), self.positive_number(params,"height",190), params)
        text = f"{template.get('displayName','')} {template.get('originalPath','')}".lower()
        if "hollow" in text or "canal" in text:
            result["metadata"]["hollowDetail"] = "Metadata only in Phase 3; hollow geometry not modeled yet."
        return result
