from __future__ import annotations
from .base import BaseGenerator
from .mesh_utils import create_box, merge_meshes

class BeamGenerator(BaseGenerator):
    element_type = "Beam"
    generator_name = "BeamGenerator"
    fallback_parameters = {"length":3000,"width":200,"height":400,"profileType":"rectangular"}
    def generate(self, template: dict) -> dict:
        params = self.default_parameters(template)
        length = self.positive_number(params,"length",3000); width = self.positive_number(params,"width",200); height = self.positive_number(params,"height",400)
        profile = str(params.get("profileType", "rectangular")).lower()
        if any(token in profile for token in ["hea", "heb", "i-beam", "ibeam"]) or profile == "i":
            flange = max(height * 0.18, 20); web = max(width * 0.35, 20)
            mesh = merge_meshes([create_box(length, width, flange, (0,0,0)), create_box(length, web, height, (0,(width-web)/2,0)), create_box(length, width, flange, (0,0,height-flange))])
        else:
            mesh = create_box(length, width, height)
        result = self.geometry_metadata(template, params, mesh); result.update(mesh); return result
