from __future__ import annotations
import math
from .base import BaseGenerator

class RoofGenerator(BaseGenerator):
    element_type = "Roof"
    generator_name = "RoofGenerator"
    fallback_parameters = {"length":4000,"width":3000,"thickness":150,"slope":15}
    def generate(self, template: dict) -> dict:
        params = self.default_parameters(template)
        length = self.positive_number(params,"length",4000); width = self.positive_number(params,"width",3000); t = self.positive_number(params,"thickness",150)
        rise = math.tan(math.radians(float(params.get("slope",15) or 15))) * width
        vertices = [[0,0,0],[length,0,0],[length,width,rise],[0,width,rise],[0,0,t],[length,0,t],[length,width,rise+t],[0,width,rise+t]]
        faces = [[0,1,2],[0,2,3],[4,6,5],[4,7,6],[0,4,5],[0,5,1],[1,5,6],[1,6,2],[2,6,7],[2,7,3],[3,7,4],[3,4,0]]
        mesh = {"vertices": vertices, "faces": faces}
        result = self.geometry_metadata(template, params, mesh); result.update(mesh); return result
