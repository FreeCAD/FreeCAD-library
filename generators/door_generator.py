from __future__ import annotations
from .base import BaseGenerator
from .mesh_utils import create_box, create_rectangular_frame, merge_meshes

class DoorGenerator(BaseGenerator):
    element_type = "Door"
    generator_name = "DoorGenerator"
    fallback_parameters = {"width":900,"height":2100,"thickness":45,"frameWidth":100,"openingAngle":90,"swingDirection":"unknown"}
    def generate(self, template: dict) -> dict:
        params = self.default_parameters(template)
        width = self.positive_number(params,"width",900); height = self.positive_number(params,"height",2100)
        thickness = self.positive_number(params,"thickness",45); frame = self.positive_number(params,"frameWidth",100)
        panel = create_box(width, thickness, height)
        frame_mesh = create_rectangular_frame(width, height, frame, max(thickness, frame/2))
        mesh = merge_meshes([panel, frame_mesh])
        result = self.geometry_metadata(template, params, mesh)
        result["metadata"]["swingDirection"] = params.get("swingDirection", "unknown")
        result["metadata"]["openingAngle"] = params.get("openingAngle", 90)
        result.update(mesh)
        return result
