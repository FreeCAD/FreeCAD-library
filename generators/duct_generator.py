from __future__ import annotations
from .base import BaseGenerator
from .mesh_utils import create_pipe, create_rectangular_duct

class DuctGenerator(BaseGenerator):
    element_type = "Duct"
    generator_name = "DuctGenerator"
    fallback_parameters = {"length":1000,"width":400,"height":250,"thickness":10,"ductShape":"rectangular","diameter":300}
    def generate(self, template: dict) -> dict:
        params = self.default_parameters(template)
        length = self.positive_number(params,"length",1000); shape = str(params.get("ductShape","rectangular")).lower()
        if shape in {"circular","round"}:
            diameter = self.positive_number(params,"diameter",300); thickness = self.positive_number(params,"thickness",10)
            mesh = create_pipe(diameter, max(diameter - 2*thickness, 1), length)
        else:
            mesh = create_rectangular_duct(self.positive_number(params,"width",400), self.positive_number(params,"height",250), length, self.positive_number(params,"thickness",10))
        result = self.geometry_metadata(template, params, mesh); result.update(mesh); return result
