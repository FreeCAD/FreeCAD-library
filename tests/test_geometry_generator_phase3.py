import json
import tempfile
import unittest
from pathlib import Path

from generators.beam_generator import BeamGenerator
from generators.door_generator import DoorGenerator
from generators.mesh_utils import create_box, write_ascii_stl, write_obj
from generators.pipe_generator import PipeGenerator
from generators.registry import GENERATOR_REGISTRY
from generators.window_generator import WindowGenerator
from tools import geometry_generator_phase3


def template(element_type="Door"):
    return {
        "id": f"{element_type.lower()}_sample",
        "elementType": element_type,
        "category": "architecture.doors" if element_type == "Door" else "generic.sample",
        "displayName": f"{element_type} Sample",
        "originalPath": "fixture",
        "parameters": [],
    }


class GeometryGeneratorPhase3Tests(unittest.TestCase):
    def test_import_registry(self):
        self.assertIn("Door", GENERATOR_REGISTRY)

    def test_create_box_returns_vertices_and_faces(self):
        mesh = create_box(1, 2, 3)
        self.assertEqual(len(mesh["vertices"]), 8)
        self.assertGreater(len(mesh["faces"]), 0)

    def test_obj_writer_writes_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "preview.obj"
            write_obj(create_box(1, 1, 1), path)
            self.assertIn("v ", path.read_text(encoding="utf-8"))

    def test_ascii_stl_writer_writes_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "preview.stl"
            write_ascii_stl(create_box(1, 1, 1), path, "box")
            self.assertIn("solid box", path.read_text(encoding="utf-8"))

    def test_door_generator_generates_mesh(self):
        result = DoorGenerator().generate(template("Door"))
        self.assertGreater(len(result["vertices"]), 0)
        self.assertEqual(result["metadata"]["generator"], "DoorGenerator")

    def test_window_generator_generates_mesh(self):
        result = WindowGenerator().generate(template("Window"))
        self.assertGreater(len(result["faces"]), 0)

    def test_beam_generator_generates_mesh(self):
        result = BeamGenerator().generate(template("Beam"))
        self.assertGreater(len(result["vertices"]), 0)

    def test_pipe_generator_generates_mesh(self):
        result = PipeGenerator().generate(template("Pipe"))
        self.assertGreater(len(result["faces"]), 0)

    def test_dry_run_does_not_create_geometry_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "library"
            asset_dir = root / "architecture" / "doors" / "sample"
            asset_dir.mkdir(parents=True)
            (asset_dir / "template.json").write_text(json.dumps(template("Door")), encoding="utf-8")
            output = Path(tmp) / "generated"
            summary = geometry_generator_phase3.process_library(root, output, Path(tmp) / "reports", True, False, None, None, None, "all")
            self.assertEqual(summary.generated, 1)
            self.assertFalse((output / "architecture" / "doors" / "door_sample" / "geometry.json").exists())

    def test_write_mode_creates_geometry_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "library"
            asset_dir = root / "architecture" / "doors" / "sample"
            asset_dir.mkdir(parents=True)
            (asset_dir / "template.json").write_text(json.dumps(template("Door")), encoding="utf-8")
            output = Path(tmp) / "generated"
            geometry_generator_phase3.process_library(root, output, output / "00_reports", False, True, None, None, None, "json")
            self.assertTrue((output / "architecture" / "doors" / "door_sample" / "geometry.json").exists())


if __name__ == "__main__":
    unittest.main()
