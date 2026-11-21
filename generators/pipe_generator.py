from __future__ import annotations
from .base import BaseGenerator
from .mesh_utils import create_cylinder, create_pipe

class PipeGenerator(BaseGenerator):
    element_type = "Pipe"
    generator_name = "PipeGenerator"
    fallback_parameters = {"length":1000,"diameter":100,"innerDiameter":80}
    def generate(self, template: dict) -> dict:
        params = self.default_parameters(template)
        length = self.positive_number(params,"length",1000); diameter = self.positive_number(params,"diameter",100)
        inner = params.get("innerDiameter")
        mesh = create_pipe(diameter, self.positive_number(params,"innerDiameter",80), length) if inner is not None else create_cylinder(diameter/2, length)
        result = self.geometry_metadata(template, params, mesh); result.update(mesh); return result
