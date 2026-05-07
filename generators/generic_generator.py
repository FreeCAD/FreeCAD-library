from __future__ import annotations
from .primitive_generators import BoxPlaceholderGenerator

class GenericGenerator(BoxPlaceholderGenerator):
    element_type = "GenericBIMObject"
    generator_name = "GenericGenerator"
    fallback_parameters = {"width": 1000, "depth": 1000, "height": 1000}
    def generate(self, template: dict) -> dict:
        params = self.default_parameters(template)
        return self.generate_box(template, self.positive_number(params,"width",1000), self.positive_number(params,"depth",1000), self.positive_number(params,"height",1000), params)
