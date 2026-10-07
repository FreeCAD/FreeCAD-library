from __future__ import annotations
import re
from .base import BaseGenerator
from .mesh_utils import create_box, create_cylinder, merge_meshes

class FoundationGenerator(BaseGenerator):
    element_type = "Foundation"
    generator_name = "FoundationGenerator"
    fallback_parameters = {"length":1500,"width":1500,"height":500}
    def generate(self, template: dict) -> dict:
        params = self.default_parameters(template)
        length = self.positive_number(params,"length",1500); width = self.positive_number(params,"width",1500); height = self.positive_number(params,"height",500)
        meshes = [create_box(length, width, height)]
        match = re.search(r"(\d+)\s*piles?", str(template.get("displayName", "")).lower())
        if match:
            count = max(1, int(match.group(1))); radius = min(length, width) / 16
            for i in range(count):
                pile = create_cylinder(radius, height * 1.5, 16)
                dx = (i + 1) * length / (count + 1)
                for vertex in pile["vertices"]:
                    vertex[0] += dx; vertex[1] += width / 2; vertex[2] -= height * 1.5
                meshes.append(pile)
            params["pileCount"] = count
        mesh = merge_meshes(meshes)
        result = self.geometry_metadata(template, params, mesh); result.update(mesh); return result
