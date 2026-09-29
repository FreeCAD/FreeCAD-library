from __future__ import annotations
from .primitive_generators import BoxPlaceholderGenerator

class FurnitureGenerator(BoxPlaceholderGenerator):
    element_type = "Furniture"
    generator_name = "FurnitureGenerator"
    fallback_parameters = {"width":600,"depth":600,"height":900}
    def generate(self, template: dict) -> dict:
        params = self.default_parameters(template)
        return self.generate_box(template, self.positive_number(params,"width",600), self.positive_number(params,"depth",600), self.positive_number(params,"height",900), params)
