"""Generator registry for Phase 3 placeholder geometry."""
from __future__ import annotations

from .beam_generator import BeamGenerator
from .block_generator import ConstructionBlockGenerator
from .door_generator import DoorGenerator
from .duct_generator import DuctGenerator
from .foundation_generator import FoundationGenerator
from .furniture_generator import FurnitureGenerator
from .generic_generator import GenericGenerator
from .pipe_generator import PipeGenerator
from .roof_generator import RoofGenerator
from .vegetation_generator import VegetationGenerator
from .window_generator import WindowGenerator

GENERATOR_REGISTRY = {
    "Door": DoorGenerator,
    "Window": WindowGenerator,
    "Beam": BeamGenerator,
    "Roof": RoofGenerator,
    "ConstructionBlock": ConstructionBlockGenerator,
    "Pipe": PipeGenerator,
    "Duct": DuctGenerator,
    "Furniture": FurnitureGenerator,
    "Fixture": FurnitureGenerator,
    "Foundation": FoundationGenerator,
    "Vegetation": VegetationGenerator,
    "GenericBIMObject": GenericGenerator,
}


def get_generator(element_type: str):
    return GENERATOR_REGISTRY.get(element_type, GenericGenerator)()


def registry_summary() -> list[dict[str, str]]:
    rows = []
    for element_type, generator_class in sorted(GENERATOR_REGISTRY.items()):
        generator = generator_class()
        rows.append({"elementType": element_type, "generatorName": generator.generator_name, "generatorVersion": generator.generator_version})
    return rows
