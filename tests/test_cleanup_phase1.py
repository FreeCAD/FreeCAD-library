import tempfile
import unittest
from pathlib import Path

from tools import cleanup_phase1


class CleanupPhase1Tests(unittest.TestCase):
    def test_classify_common_extensions(self):
        self.assertEqual(cleanup_phase1.classify_file_type("door.FCStd"), "source_model")
        self.assertEqual(cleanup_phase1.classify_file_type("door.step"), "exchange_geometry")
        self.assertEqual(cleanup_phase1.classify_file_type("door.STL"), "preview_mesh")
        self.assertEqual(cleanup_phase1.classify_file_type("board.GTL"), "pcb_manufacturing_file")
        self.assertIsNone(cleanup_phase1.classify_file_type("unknown.xyz"))

    def test_normalize_name(self):
        self.assertEqual(cleanup_phase1.normalize_name("Single door with trims"), "single_door_with_trims")
        self.assertEqual(cleanup_phase1.normalize_name("  HVAC/Pipe-90° Bend  "), "hvac_pipe_90_bend")

    def test_dry_run_main_completes_on_minimal_fixture(self):
        with tempfile.TemporaryDirectory() as source, tempfile.TemporaryDirectory() as parent:
            source_root = Path(source)
            asset_dir = source_root / "Architectural Parts" / "Doors" / "Wood"
            asset_dir.mkdir(parents=True)
            (asset_dir / "Single door with trims.FCStd").write_text("fixture", encoding="utf-8")
            output_root = Path(parent) / "cleaned"
            result = cleanup_phase1.main(["--source", str(source_root), "--output", str(output_root), "--dry-run"])
            self.assertEqual(result, 0)
            self.assertFalse(output_root.exists())


if __name__ == "__main__":
    unittest.main()
