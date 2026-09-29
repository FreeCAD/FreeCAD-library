"""Reusable primitive placeholder generator helpers."""
from __future__ import annotations

from .base import BaseGenerator
from .mesh_utils import create_box


class BoxPlaceholderGenerator(BaseGenerator):
    element_type = "GenericBIMObject"
    generator_name = "BoxPlaceholderGenerator"

    def generate_box(self, template: dict, width: float, depth: float, height: float, params: dict) -> dict:
        mesh = create_box(width, depth, height)
        result = self.geometry_metadata(template, params, mesh)
        result.update(mesh)
        return result
