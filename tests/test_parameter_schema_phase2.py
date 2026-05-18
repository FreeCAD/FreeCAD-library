import json
import tempfile
import unittest
from pathlib import Path

from tools import parameter_schema_phase2


class ParameterSchemaPhase2Tests(unittest.TestCase):
    def test_parameter_catalog_loads(self):
        _schemas, catalog, _rules = parameter_schema_phase2.load_schema_config()
        self.assertIn("width", catalog)
        self.assertEqual(catalog["width"]["uiControl"], "number_input")

    def test_element_type_schema_loads(self):
        schemas, _catalog, _rules = parameter_schema_phase2.load_schema_config()
        self.assertIn("Door", schemas)
        self.assertIn("width", schemas["Door"]["requiredParameters"])

    def test_template_validation_catches_missing_id(self):
        schemas, catalog, rules = parameter_schema_phase2.load_schema_config()
        template = {
            "elementType": "Door",
            "category": "architecture.doors.wood",
            "displayName": "Door",
            "originalPath": "Architectural Parts/Doors/Wood",
            "sourceFiles": {},
            "fileTypes": {},
            "editability": {"status": "static_reference"},
            "parameters": [],
        }
        issues = parameter_schema_phase2.validate_template(template, Path("template.json"), schemas, catalog, rules)
        self.assertTrue(any(issue.issue_code == "missing_required_field" and "id" in issue.issue_message for issue in issues))

    def test_element_type_inference_detects_doors(self):
        template = {"category": "architecture.doors.wood", "originalPath": "Architectural Parts/Doors/Wood"}
        result = parameter_schema_phase2.infer_element_type(template, Path("architecture/doors/wood/template.json"))
        self.assertEqual(result, "Door")

    def test_enriching_door_adds_required_parameters(self):
        schemas, catalog, rules = parameter_schema_phase2.load_schema_config()
        template = {
            "id": "door_sample",
            "elementType": "Door",
            "category": "architecture.doors",
            "displayName": "Door Sample",
            "originalPath": "Architectural Parts/Doors",
            "sourceFiles": {},
            "fileTypes": {},
            "editability": {"status": "static_reference"},
            "parameters": [],
        }
        processed = parameter_schema_phase2.enrich_template(template, Path("template.json"), schemas, catalog, rules)
        names = {parameter["name"] for parameter in processed.enriched["parameters"]}
        self.assertTrue({"width", "height", "thickness"}.issubset(names))

    def test_dry_run_does_not_modify_template(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            asset_dir = root / "architecture" / "doors" / "sample"
            asset_dir.mkdir(parents=True)
            template_path = asset_dir / "template.json"
            original = {
                "id": "door_sample",
                "elementType": "Door",
                "category": "architecture.doors",
                "displayName": "Door Sample",
                "originalPath": "Architectural Parts/Doors",
                "sourceFiles": {},
                "fileTypes": {},
                "editability": {"status": "static_reference"},
                "parameters": [],
            }
            template_path.write_text(json.dumps(original, indent=2) + "\n", encoding="utf-8")
            report_dir = root / "reports"
            parameter_schema_phase2.process_library(root, report_dir, dry_run=True, write=False, backup=False, limit_category=None)
            self.assertEqual(json.loads(template_path.read_text(encoding="utf-8")), original)
            self.assertTrue((report_dir / "phase2_schema_report.md").exists())

    def test_write_mode_updates_template(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            asset_dir = root / "architecture" / "doors" / "sample"
            asset_dir.mkdir(parents=True)
            template_path = asset_dir / "template.json"
            template_path.write_text(json.dumps({
                "id": "door_sample",
                "elementType": "Door",
                "category": "architecture.doors",
                "displayName": "Door Sample",
                "originalPath": "Architectural Parts/Doors",
                "sourceFiles": {},
                "fileTypes": {},
                "editability": {"status": "static_reference"},
                "parameters": [],
            }, indent=2) + "\n", encoding="utf-8")
            parameter_schema_phase2.process_library(root, root / "reports", dry_run=False, write=True, backup=True, limit_category=None)
            updated = json.loads(template_path.read_text(encoding="utf-8"))
            self.assertIn("schema", updated)
            self.assertIn("toolbar", updated)
            self.assertTrue((asset_dir / "template.json.bak").exists())


if __name__ == "__main__":
    unittest.main()
