from __future__ import annotations
from .base import BaseGenerator
from .mesh_utils import create_box, create_rectangular_frame, merge_meshes

class WindowGenerator(BaseGenerator):
    element_type = "Window"
    generator_name = "WindowGenerator"
    fallback_parameters = {"width":1200,"height":1200,"frameDepth":80,"frameWidth":60,"panelCount":2,"openingType":"unknown"}
    def generate(self, template: dict) -> dict:
        params = self.default_parameters(template)
        width = self.positive_number(params,"width",1200); height = self.positive_number(params,"height",1200)
        depth = self.positive_number(params,"frameDepth",80); frame = self.positive_number(params,"frameWidth",60)
        glass = create_box(width, max(6, depth/8), height, (0, depth/2, 0))
        mesh = merge_meshes([create_rectangular_frame(width, height, frame, depth), glass])
        result = self.geometry_metadata(template, params, mesh)
        result["metadata"]["panelCount"] = params.get("panelCount", 2)
        result["metadata"]["openingType"] = params.get("openingType", "unknown")
        result.update(mesh)
        return result
