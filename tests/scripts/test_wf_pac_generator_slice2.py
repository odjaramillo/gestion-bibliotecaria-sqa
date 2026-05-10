"""Tests for scripts.lib.pac_generator modules (slice 2)."""
from __future__ import annotations

import json
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from scripts.lib.pac_generator.config_reader import PacConfig
from scripts.lib.pac_generator.gemini_client import GeminiClient
from scripts.lib.pac_generator.pac_assembler import PACAssembler
from scripts.lib.pac_generator.report_writer import ReportWriter


class TestGeminiClient(unittest.TestCase):
    """Tests for gemini_client module."""

    def test_is_available_false(self):
        """When google-generativeai is not installed, returns False."""
        with patch(
            "scripts.lib.pac_generator.gemini_client.importlib.util.find_spec",
            return_value=None,
        ):
            self.assertFalse(GeminiClient.is_available())

    def test_format_section_with_mock(self):
        """Mock the API call, verify prompt contains directives and 'Do NOT invent'."""
        mock_module = MagicMock()
        fake_google = MagicMock()
        fake_google.generativeai = mock_module
        mock_model = MagicMock()
        mock_module.GenerativeModel.return_value = mock_model
        mock_model.generate_content.return_value = MagicMock(text="formatted output")

        with patch.dict(
            sys.modules, {"google": fake_google, "google.generativeai": mock_module}
        ):
            with patch(
                "scripts.lib.pac_generator.gemini_client.importlib.util.find_spec",
                return_value=MagicMock(),
            ):
                client = GeminiClient("fake-key")
                directives = {"key": "value"}
                result = client.format_section("Test Section", directives)

                self.assertEqual(result, "formatted output")
                mock_model.generate_content.assert_called_once()
                call_args = mock_model.generate_content.call_args[0][0]
                self.assertIn("Test Section", call_args)
                self.assertIn("Do NOT invent", call_args)
                self.assertIn(json.dumps(directives), call_args)

    def test_format_section_uses_cache(self):
        """Call twice with same input, verify API called only once."""
        mock_module = MagicMock()
        fake_google = MagicMock()
        fake_google.generativeai = mock_module
        mock_model = MagicMock()
        mock_module.GenerativeModel.return_value = mock_model
        mock_model.generate_content.return_value = MagicMock(text="cached")

        with patch.dict(
            sys.modules, {"google": fake_google, "google.generativeai": mock_module}
        ):
            with patch(
                "scripts.lib.pac_generator.gemini_client.importlib.util.find_spec",
                return_value=MagicMock(),
            ):
                client = GeminiClient("fake-key")
                directives = {"key": "value"}
                result1 = client.format_section("Test Section", directives)
                result2 = client.format_section("Test Section", directives)

                self.assertEqual(result1, "cached")
                self.assertEqual(result2, "cached")
                mock_model.generate_content.assert_called_once()

    def test_format_section_fallback(self):
        """When API raises exception, returns fallback message."""
        mock_module = MagicMock()
        fake_google = MagicMock()
        fake_google.generativeai = mock_module
        mock_model = MagicMock()
        mock_module.GenerativeModel.return_value = mock_model
        mock_model.generate_content.side_effect = RuntimeError("API error")

        with patch.dict(
            sys.modules, {"google": fake_google, "google.generativeai": mock_module}
        ):
            with patch(
                "scripts.lib.pac_generator.gemini_client.importlib.util.find_spec",
                return_value=MagicMock(),
            ):
                client = GeminiClient("fake-key")
                result = client.format_section("Test Section", {"key": "value"})
                self.assertEqual(
                    result, "[FORMATEO GEMINI NO DISPONIBLE: Test Section]"
                )

    def test_idempotence_same_input(self):
        """Same directives = same output."""
        mock_module = MagicMock()
        fake_google = MagicMock()
        fake_google.generativeai = mock_module
        mock_model = MagicMock()
        mock_module.GenerativeModel.return_value = mock_model
        mock_model.generate_content.return_value = MagicMock(text="stable")

        with patch.dict(
            sys.modules, {"google": fake_google, "google.generativeai": mock_module}
        ):
            with patch(
                "scripts.lib.pac_generator.gemini_client.importlib.util.find_spec",
                return_value=MagicMock(),
            ):
                client = GeminiClient("fake-key")
                directives = {"b": 2, "a": 1}
                result1 = client.format_section("Section", directives)
                # Same content but different key order
                result2 = client.format_section("Section", {"a": 1, "b": 2})

                self.assertEqual(result1, result2)
                mock_model.generate_content.assert_called_once()


class TestPACAssembler(unittest.TestCase):
    """Tests for pac_assembler module."""

    def setUp(self):
        self.config = PacConfig(
            proyecto={
                "name": "Test",
                "version": "1.0",
                "descripcion": "Desc",
            },
            lider={"nombre": "Ana", "email": "a@b.com", "rol": "Lider"},
            objetivos_calidad={"func": 40},
            roles={"dev": "Carlos"},
            umbrales={"cov": 100.0},
            riesgos=[
                {"descripcion": "R1", "mitigacion": "M1", "aceptado": False}
            ],
            cronograma=[
                {
                    "fase": "F1",
                    "inicio": "2026-01-01",
                    "fin": "2026-01-02",
                    "entregables": ["E1"],
                }
            ],
        )
        self.stack = {
            "backend": {
                "name": "backend",
                "version": "1.0",
                "build_tool": "Maven",
                "java_version": "21",
                "spring_boot_version": "3.4.5",
                "dependencies": [
                    {"groupId": "g", "artifactId": "a", "version": "1"}
                ],
            },
            "frontend": {
                "name": "frontend",
                "version": "1.0",
                "build_tool": "npm",
                "vue_version": "3",
                "dependencies": [{"name": "vue", "version": "3"}],
                "dev_dependencies": [],
            },
        }
        self.artifacts = {
            "documentation": [
                {"filename": "doc.pdf", "path": "documentacion/doc.pdf"}
            ],
            "java_source": {"total_files": 5, "total_loc": 100, "packages": []},
            "vue_source": {"total_files": 2, "total_loc": 50, "components": []},
        }
        self.gemini = MagicMock()
        self.gemini.format_section.return_value = "[FORMATEADO]"

    def test_generate_auto_sections(self):
        """With mocked Gemini, verify auto sections contain expected data."""
        assembler = PACAssembler(self.config, self.stack, self.artifacts, self.gemini)
        result = assembler.generate()
        self.assertIn("Test", result)
        self.assertIn("Desc", result)
        self.assertIn("Maven", result)
        self.assertIn("doc.pdf", result)

    def test_generate_calls_gemini_for_manual(self):
        """Verify Gemini called for manual sections."""
        assembler = PACAssembler(self.config, self.stack, self.artifacts, self.gemini)
        assembler.generate()
        manual_sections = [
            "4. Objetivos de Calidad",
            "5. Gestión y Organización",
            "8. Métricas",
            "9. Análisis de Riesgos",
            "10. Cronograma",
        ]
        self.assertEqual(self.gemini.format_section.call_count, 5)
        called_names = [
            call[0][0] for call in self.gemini.format_section.call_args_list
        ]
        for name in manual_sections:
            self.assertIn(name, called_names)

    def test_generate_structure(self):
        """Verify all 13 sections present in output."""
        assembler = PACAssembler(self.config, self.stack, self.artifacts, self.gemini)
        result = assembler.generate()
        expected_sections = [
            "Plan de Aseguramiento de Calidad",
            "1. Alcance y Propósito",
            "2. Stack Tecnológico",
            "3. Inventario de Artefactos",
            "4. Objetivos de Calidad",
            "5. Gestión y Organización",
            "6. Estándares Aplicables",
            "7. Herramientas Tecnológicas",
            "8. Métricas",
            "9. Análisis de Riesgos",
            "10. Cronograma",
            "11. Gestión de Defectos",
            "12. CI/CD",
        ]
        for sec in expected_sections:
            self.assertIn(sec, result)

    def test_generate_idempotence(self):
        """Run twice with same data, outputs identical."""
        assembler = PACAssembler(self.config, self.stack, self.artifacts, self.gemini)
        result1 = assembler.generate()
        result2 = assembler.generate()
        self.assertEqual(result1, result2)


class TestReportWriter(unittest.TestCase):
    """Tests for report_writer module."""

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.writer = ReportWriter(self.tmpdir.name)

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_write_summary_success(self):
        """Verify JSON written correctly."""
        path = self.writer.write_summary(
            pac_path=Path("sqa/reportes/pac.md"),
            status="EXITOSO",
            sections_total=13,
            sections_auto=8,
            sections_manual=5,
            sections_completed=10,
            issues=[],
        )
        self.assertTrue(path.exists())
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(data["workflow"], "wf_pac_generator")
        self.assertEqual(data["estado"], "EXITOSO")
        self.assertEqual(data["archivo_pac"], "sqa/reportes/pac.md")
        self.assertEqual(data["resumen"]["total_secciones"], 13)
        self.assertEqual(data["resumen"]["secciones_auto"], 8)
        self.assertEqual(data["resumen"]["secciones_manual"], 5)
        self.assertEqual(data["resumen"]["secciones_completadas"], 10)
        self.assertEqual(data["resumen"]["secciones_pendientes"], 3)
        self.assertEqual(data["metricas"]["cobertura_secciones"], "76.9%")
        self.assertEqual(data["issues"], [])

    def test_write_summary_creates_dir(self):
        """If report_dir doesn't exist, creates it."""
        nested = Path(self.tmpdir.name) / "a" / "b"
        writer = ReportWriter(nested)
        path = writer.write_summary(
            pac_path=Path("pac.md"),
            status="PARCIAL",
            sections_total=13,
            sections_auto=8,
            sections_manual=5,
            sections_completed=5,
            issues=["issue1"],
        )
        self.assertTrue(path.exists())
        self.assertTrue(nested.exists())

    def test_write_summary_filename_format(self):
        """Verify filename pattern."""
        path = self.writer.write_summary(
            pac_path=Path("pac.md"),
            status="FALLIDO",
            sections_total=13,
            sections_auto=8,
            sections_manual=5,
            sections_completed=0,
            issues=["fail"],
        )
        self.assertRegex(
            path.name, r"^\d{8}_\d{6}_wf_pac_summary\.json$"
        )


if __name__ == "__main__":
    unittest.main()
