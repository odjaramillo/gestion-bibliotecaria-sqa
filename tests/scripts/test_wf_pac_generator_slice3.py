"""Tests for scripts.wf_pac_generator (slice 3)."""
from __future__ import annotations

import io
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from scripts.lib.pac_generator.config_reader import PacConfigError
from scripts.wf_pac_generator import main

FIXTURES_DIR = Path(__file__).parent / "fixtures"


class TestMainOrchestrator(unittest.TestCase):
    """Tests for the main orchestrator CLI."""

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.project_root = Path(self.tmpdir.name)
        (self.project_root / "sqa" / "templates").mkdir(parents=True)
        (self.project_root / "documentacion").mkdir(parents=True)
        (self.project_root / "src" / "main" / "java").mkdir(parents=True)
        (self.project_root / "biblioteca-frontend" / "src").mkdir(parents=True)
        shutil.copy(
            FIXTURES_DIR / "sample_pac_config.yaml",
            self.project_root / "sqa" / "templates" / "pac_config.yaml",
        )
        shutil.copy(
            FIXTURES_DIR / "sample_pom.xml",
            self.project_root / "pom.xml",
        )
        shutil.copy(
            FIXTURES_DIR / "sample_package.json",
            self.project_root / "biblioteca-frontend" / "package.json",
        )

        self.env_patcher = patch.dict(
            os.environ, {"PROJECT_ROOT": str(self.project_root)}, clear=False
        )
        self.env_patcher.start()

    def tearDown(self):
        self.env_patcher.stop()
        self.tmpdir.cleanup()

    def _mock_config(self) -> MagicMock:
        """Crea un mock de PacConfig con los campos mínimos necesarios."""
        config = MagicMock()
        config.proyecto = {
            "name": "Test",
            "version": "1.0",
            "descripcion": "Desc",
        }
        config.lider = {
            "nombre": "Ana",
            "email": "a@b.com",
            "rol": "Lider",
        }
        config.objetivos_calidad = {"func": 40}
        config.roles = {"dev": "Carlos"}
        config.umbrales = {"cov": 100.0}
        config.riesgos = [
            {"descripcion": "R1", "mitigacion": "M1", "aceptado": False}
        ]
        config.cronograma = [
            {
                "fase": "F1",
                "inicio": "2026-01-01",
                "fin": "2026-01-02",
                "entregables": ["E1"],
            }
        ]
        return config

    def test_main_success(self):
        """Mock all components, verify PAC written, report written."""
        mock_config = self._mock_config()
        mock_assembler_instance = MagicMock()
        mock_assembler_instance.generate.return_value = "# Test PAC\n\n## Section 1\n\nContent"

        with patch("scripts.wf_pac_generator.read_config", return_value=mock_config):
            with patch("scripts.wf_pac_generator.parse_pom", return_value={"name": "backend"}):
                with patch("scripts.wf_pac_generator.parse_package_json", return_value={"name": "frontend"}):
                    with patch("scripts.wf_pac_generator.scan_documentation", return_value=[]):
                        with patch("scripts.wf_pac_generator.scan_java_source", return_value={"total_files": 0, "total_loc": 0, "packages": []}):
                            with patch("scripts.wf_pac_generator.scan_vue_source", return_value={"total_files": 0, "total_loc": 0, "components": []}):
                                with patch("scripts.wf_pac_generator.PACAssembler", return_value=mock_assembler_instance):
                                    result = main([
                                        "--config", "sqa/templates/pac_config.yaml",
                                        "--output", "sqa/pac_generado.md",
                                        "--no-gemini",
                                    ])

        self.assertEqual(result, 0)
        pac_path = self.project_root / "sqa" / "pac_generado.md"
        self.assertTrue(pac_path.exists())
        self.assertEqual(pac_path.read_text(encoding="utf-8"), "# Test PAC\n\n## Section 1\n\nContent")

        report_dir = self.project_root / "sqa" / "reportes"
        reports = list(report_dir.glob("*_wf_pac_summary.json"))
        self.assertEqual(len(reports), 1)
        report_data = json.loads(reports[0].read_text(encoding="utf-8"))
        self.assertEqual(report_data["workflow"], "wf_pac_generator")
        self.assertEqual(report_data["estado"], "EXITOSO")

    def test_main_dry_run(self):
        """Verify --dry-run does not write files."""
        mock_config = self._mock_config()
        mock_assembler_instance = MagicMock()
        mock_assembler_instance.generate.return_value = "# Dry Run PAC"

        with patch("scripts.wf_pac_generator.read_config", return_value=mock_config):
            with patch("scripts.wf_pac_generator.PACAssembler", return_value=mock_assembler_instance):
                captured = io.StringIO()
                with patch("sys.stdout", new=captured):
                    result = main([
                        "--config", "sqa/templates/pac_config.yaml",
                        "--output", "sqa/pac_generado.md",
                        "--dry-run",
                        "--no-gemini",
                    ])

        self.assertEqual(result, 0)
        pac_path = self.project_root / "sqa" / "pac_generado.md"
        self.assertFalse(pac_path.exists())
        self.assertIn("# Dry Run PAC", captured.getvalue())

        report_dir = self.project_root / "sqa" / "reportes"
        reports = list(report_dir.glob("*_wf_pac_summary.json"))
        self.assertEqual(len(reports), 0)

    def test_main_no_gemini(self):
        """Verify --no-gemini skips Gemini client instantiation."""
        mock_config = self._mock_config()
        mock_assembler_instance = MagicMock()
        mock_assembler_instance.generate.return_value = "# PAC"

        with patch("scripts.wf_pac_generator.read_config", return_value=mock_config):
            with patch("scripts.wf_pac_generator.GeminiClient") as mock_gemini:
                with patch("scripts.wf_pac_generator.PACAssembler", return_value=mock_assembler_instance):
                    result = main([
                        "--config", "sqa/templates/pac_config.yaml",
                        "--output", "sqa/pac_generado.md",
                        "--no-gemini",
                    ])

        self.assertEqual(result, 0)
        mock_gemini.assert_not_called()

    def test_main_invalid_config(self):
        """Verify exit code 1 on bad config."""
        with patch(
            "scripts.wf_pac_generator.read_config",
            side_effect=PacConfigError("bad config"),
        ):
            captured_stderr = io.StringIO()
            with patch("sys.stderr", new=captured_stderr):
                result = main([
                    "--config", "sqa/templates/bad_config.yaml",
                    "--output", "sqa/pac_generado.md",
                    "--no-gemini",
                ])

        self.assertEqual(result, 1)
        self.assertIn("bad config", captured_stderr.getvalue())

    def test_main_missing_pom(self):
        """Verify continues with warning when pom.xml missing."""
        mock_config = self._mock_config()
        mock_assembler_instance = MagicMock()
        mock_assembler_instance.generate.return_value = "# PAC"

        (self.project_root / "pom.xml").unlink()

        with patch("scripts.wf_pac_generator.read_config", return_value=mock_config):
            with patch("scripts.wf_pac_generator.PACAssembler", return_value=mock_assembler_instance):
                captured_stderr = io.StringIO()
                with patch("sys.stderr", new=captured_stderr):
                    result = main([
                        "--config", "sqa/templates/pac_config.yaml",
                        "--output", "sqa/pac_generado.md",
                        "--no-gemini",
                    ])

        self.assertEqual(result, 0)
        self.assertIn("pom.xml", captured_stderr.getvalue())
        pac_path = self.project_root / "sqa" / "pac_generado.md"
        self.assertTrue(pac_path.exists())

    def test_idempotence(self):
        """Run twice with same inputs, verify PAC content identical."""
        args = [
            "--config", "sqa/templates/pac_config.yaml",
            "--output", "sqa/pac_generado.md",
            "--no-gemini",
        ]
        result1 = main(args)
        self.assertEqual(result1, 0)
        pac_path = self.project_root / "sqa" / "pac_generado.md"
        content1 = pac_path.read_text(encoding="utf-8")
        pac_path.unlink()

        result2 = main(args)
        self.assertEqual(result2, 0)
        content2 = pac_path.read_text(encoding="utf-8")

        self.assertEqual(content1, content2)


class TestIdempotence(unittest.TestCase):
    """End-to-end idempotence tests."""

    def test_full_pipeline_idempotence(self):
        """End-to-end with temp dirs and fixtures, verify byte-for-byte identical output on second run."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            (project_root / "sqa" / "templates").mkdir(parents=True)
            (project_root / "documentacion").mkdir(parents=True)
            (project_root / "src" / "main" / "java").mkdir(parents=True)
            (project_root / "biblioteca-frontend" / "src").mkdir(parents=True)
            shutil.copy(
                FIXTURES_DIR / "sample_pac_config.yaml",
                project_root / "sqa" / "templates" / "pac_config.yaml",
            )
            shutil.copy(
                FIXTURES_DIR / "sample_pom.xml",
                project_root / "pom.xml",
            )
            shutil.copy(
                FIXTURES_DIR / "sample_package.json",
                project_root / "biblioteca-frontend" / "package.json",
            )

            old_project_root = os.environ.get("PROJECT_ROOT")
            os.environ["PROJECT_ROOT"] = str(project_root)
            try:
                args = [
                    "--config", "sqa/templates/pac_config.yaml",
                    "--output", "sqa/pac_generado.md",
                    "--no-gemini",
                ]
                result1 = main(args)
                self.assertEqual(result1, 0)
                pac_path = project_root / "sqa" / "pac_generado.md"
                content1 = pac_path.read_bytes()
                pac_path.unlink()

                # Limpiar reportes para no acumular archivos entre corridas
                report_dir = project_root / "sqa" / "reportes"
                if report_dir.exists():
                    for f in report_dir.glob("*_wf_pac_summary.json"):
                        f.unlink()

                result2 = main(args)
                self.assertEqual(result2, 0)
                content2 = pac_path.read_bytes()

                self.assertEqual(content1, content2)
            finally:
                if old_project_root is None:
                    os.environ.pop("PROJECT_ROOT", None)
                else:
                    os.environ["PROJECT_ROOT"] = old_project_root


if __name__ == "__main__":
    unittest.main()
