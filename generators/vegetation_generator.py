from __future__ import annotations
from .base import BaseGenerator
from .mesh_utils import create_box, create_cylinder, merge_meshes

class VegetationGenerator(BaseGenerator):
    element_type = "Vegetation"
    generator_name = "VegetationGenerator"
    fallback_parameters = {"height":3000,"diameter":1500}
    def generate(self, template: dict) -> dict:
        params = self.default_parameters(template)
        height = self.positive_number(params,"height",3000); diameter = self.positive_number(params,"diameter",1500)
        trunk = create_cylinder(max(diameter*0.06, 40), height*0.45, 12)
        canopy = create_box(diameter, diameter, height*0.55, (-diameter/2, -diameter/2, height*0.4))
        mesh = merge_meshes([trunk, canopy])
        result = self.geometry_metadata(template, params, mesh, "Simple trunk and canopy placeholder generated from template parameters."); result.update(mesh); return result
