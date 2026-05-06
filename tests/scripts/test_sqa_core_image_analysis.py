"""Tests for scripts.sqa_core.image_analysis."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Mock missing third-party modules before importing SQA code
for _mod in ("jira", "requests"):
    if _mod not in sys.modules:
        sys.modules[_mod] = MagicMock()

if "google" not in sys.modules:
    sys.modules["google"] = MagicMock()
if "google.generativeai" not in sys.modules:
    sys.modules["google.generativeai"] = MagicMock()

from scripts.sqa_core.image_analysis import (
    DiagramType,
    ImageAnalyzer,
    VisualFinding,
)


class TestVisualFinding(unittest.TestCase):
    """Tests for VisualFinding dataclass."""

    def test_finding_creation(self):
        finding = VisualFinding(
            id="VIS-DAS-01",
            diagram_type=DiagramType.C4_CONTEXT,
            description="Falta el usuario administrador en el diagrama de contexto",
            severity="Alta",
            page_reference="DAS page 7",
            evidence="El actor 'Administrador' no aparece en el diagrama C4 de contexto",
        )
        self.assertEqual(finding.id, "VIS-DAS-01")
        self.assertEqual(finding.severity, "Alta")


class TestImageAnalyzer(unittest.TestCase):
    """Tests for ImageAnalyzer."""

    def _make_analyzer(self, response_text: str | None = None) -> ImageAnalyzer:
        mock_client = MagicMock()
        analyzer = ImageAnalyzer(gemini_client=mock_client)
        # Patch _generate_multimodal to avoid real Gemini calls
        default_response = response_text or json.dumps(
            {
                "findings": [
                    {
                        "id": "VIS-DAS-01",
                        "diagram_type": "c4_context",
                        "description": "Falta actor Administrador",
                        "severity": "Alta",
                        "page_reference": "page 7",
                        "evidence": "Actor no presente",
                    }
                ]
            }
        )
        analyzer._generate_multimodal = lambda _p, _b, _m: default_response
        return analyzer

    @patch("pathlib.Path.exists", return_value=True)
    @patch("pathlib.Path.read_bytes", return_value=b"fake_image_data")
    def test_analyze_image_returns_findings(self, mock_read, mock_exists):
        analyzer = self._make_analyzer()
        findings = analyzer.analyze_image(
            image_path=Path("/tmp/test.png"),
            diagram_type=DiagramType.C4_CONTEXT,
            context="Sistema de gestión bibliotecaria",
        )

        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].id, "VIS-DAS-01")
        self.assertEqual(findings[0].severity, "Alta")

    @patch("pathlib.Path.exists", return_value=True)
    @patch("pathlib.Path.read_bytes", return_value=b"fake_image_data")
    def test_analyze_image_with_empty_response(self, mock_read, mock_exists):
        analyzer = self._make_analyzer(
            response_text=json.dumps({"findings": []})
        )
        findings = analyzer.analyze_image(
            image_path=Path("/tmp/test.png"),
            diagram_type=DiagramType.UML_CLASS,
            context="",
        )
        self.assertEqual(findings, [])

    @patch("pathlib.Path.exists", return_value=True)
    @patch("pathlib.Path.read_bytes", return_value=b"fake_image_data")
    def test_analyze_image_malformed_json_returns_empty(self, mock_read, mock_exists):
        analyzer = self._make_analyzer(response_text="not json")
        findings = analyzer.analyze_image(
            image_path=Path("/tmp/test.png"),
            diagram_type=DiagramType.C4_CONTAINER,
            context="",
        )
        self.assertEqual(findings, [])

    def test_analyze_image_missing_file_returns_empty(self):
        analyzer = self._make_analyzer()
        findings = analyzer.analyze_image(
            image_path=Path("/nonexistent/file.png"),
            diagram_type=DiagramType.WIREFRAME,
            context="",
        )
        self.assertEqual(findings, [])

    @patch("pathlib.Path.exists", return_value=True)
    @patch("pathlib.Path.read_bytes", return_value=b"fake_image_data")
    def test_prompt_includes_diagram_type(self, mock_read, mock_exists):
        analyzer = self._make_analyzer()
        captured_prompts = []
        original = analyzer._generate_multimodal
        def capture(prompt, b64, mime):
            captured_prompts.append(prompt)
            return original(prompt, b64, mime)
        analyzer._generate_multimodal = capture

        analyzer.analyze_image(
            image_path=Path("/tmp/test.png"),
            diagram_type=DiagramType.C4_COMPONENT,
            context="Backend Spring Boot",
        )
        self.assertEqual(len(captured_prompts), 1)
        self.assertIn("c4_component", captured_prompts[0])
        self.assertIn("Backend Spring Boot", captured_prompts[0])

    @patch("pathlib.Path.exists", return_value=True)
    @patch("pathlib.Path.read_bytes", return_value=b"fake_image_data")
    def test_batch_analyze_calls_analyze_for_each(self, mock_read, mock_exists):
        analyzer = self._make_analyzer()
        images = [
            (Path("/tmp/a.png"), DiagramType.C4_CONTEXT, "ctx"),
            (Path("/tmp/b.png"), DiagramType.UML_CLASS, "uml"),
        ]
        results = analyzer.batch_analyze(images)

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0][0], Path("/tmp/a.png"))
        self.assertEqual(len(results[0][1]), 1)

    @patch("pathlib.Path.exists", side_effect=[False, True, True])
    @patch("pathlib.Path.read_bytes", return_value=b"fake_image_data")
    def test_batch_analyze_skips_missing_files(self, mock_read, mock_exists):
        analyzer = self._make_analyzer()
        images = [
            (Path("/nonexistent/a.png"), DiagramType.C4_CONTEXT, "ctx"),
            (Path("/tmp/b.png"), DiagramType.UML_CLASS, "uml"),
        ]
        results = analyzer.batch_analyze(images)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], Path("/tmp/b.png"))

    @patch("pathlib.Path.exists", return_value=True)
    @patch("pathlib.Path.read_bytes", return_value=b"fake_image_data")
    def test_severity_normalization(self, mock_read, mock_exists):
        analyzer = self._make_analyzer(
            response_text=json.dumps(
                {
                    "findings": [
                        {"id": "V1", "diagram_type": "c4_context", "description": "d", "severity": "critical", "page_reference": "p", "evidence": "e"},
                        {"id": "V2", "diagram_type": "c4_context", "description": "d", "severity": "high", "page_reference": "p", "evidence": "e"},
                        {"id": "V3", "diagram_type": "c4_context", "description": "d", "severity": "medium", "page_reference": "p", "evidence": "e"},
                        {"id": "V4", "diagram_type": "c4_context", "description": "d", "severity": "low", "page_reference": "p", "evidence": "e"},
                    ]
                }
            )
        )
        findings = analyzer.analyze_image(
            Path("/tmp/test.png"), DiagramType.C4_CONTEXT, ""
        )
        self.assertEqual(len(findings), 4)
        self.assertEqual(findings[0].severity, "Crítica")
        self.assertEqual(findings[1].severity, "Alta")
        self.assertEqual(findings[2].severity, "Media")
        self.assertEqual(findings[3].severity, "Baja")

    @patch("pathlib.Path.exists", return_value=True)
    @patch("pathlib.Path.read_bytes", side_effect=OSError("permission denied"))
    def test_analyze_image_read_error_returns_empty(self, mock_read, mock_exists):
        analyzer = self._make_analyzer()
        findings = analyzer.analyze_image(
            Path("/tmp/test.png"), DiagramType.C4_CONTEXT, ""
        )
        self.assertEqual(findings, [])

    def test_generate_multimodal_uses_gemini_model(self):
        """Verifica que se accede correctamente a self.gemini.model para llamadas multimodales."""
        mock_client = MagicMock()
        analyzer = ImageAnalyzer(gemini_client=mock_client)
        mock_response = MagicMock()
        mock_response.text = '{"findings": []}'
        mock_client.model.generate_content.return_value = mock_response

        result = analyzer._generate_multimodal("prompt", "b64data", "image/png")

        mock_client.model.generate_content.assert_called_once()
        self.assertEqual(result, '{"findings": []}')

    def test_generate_multimodal_fallback_when_no_model(self):
        """Verifica el fallback a generate() cuando no existe el atributo model."""
        mock_client = MagicMock()
        del mock_client.model
        analyzer = ImageAnalyzer(gemini_client=mock_client)
        mock_client.generate.return_value = '{"findings": []}'

        result = analyzer._generate_multimodal("prompt", "b64data", "image/png")

        mock_client.generate.assert_called_once()
        self.assertEqual(result, '{"findings": []}')


class TestNormalizeSeverity(unittest.TestCase):
    """Tests for severity normalization."""

    def test_critical_variants(self):
        self.assertEqual(ImageAnalyzer._normalize_severity("critical"), "Crítica")
        self.assertEqual(ImageAnalyzer._normalize_severity("CRITICAL"), "Crítica")
        self.assertEqual(ImageAnalyzer._normalize_severity("Critica"), "Crítica")

    def test_unknown_severity_passthrough(self):
        self.assertEqual(ImageAnalyzer._normalize_severity("Info"), "Info")


if __name__ == "__main__":
    unittest.main()
