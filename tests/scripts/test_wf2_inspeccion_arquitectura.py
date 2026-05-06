"""Tests for scripts.wf2_inspeccion_arquitectura."""
from __future__ import annotations

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

if "fitz" not in sys.modules:
    sys.modules["fitz"] = MagicMock()

from scripts.wf2_inspeccion_arquitectura import WF2InspeccionArquitectura
from scripts.sqa_core.config import SQAConfig


class TestWF2InspeccionArquitectura(unittest.TestCase):
    """Tests for WF2 Inspeccion de Arquitectura."""

    def _make_config(
        self,
        dry_run: bool = True,
        documentacion_dir=None,
        reportes_dir=None,
    ) -> SQAConfig:
        return SQAConfig(
            jira_server="https://jira.example.com",
            jira_email="a@b.com",
            jira_api_token="tok",
            confluence_url="https://wiki.example.com",
            confluence_user="user",
            confluence_token="tok2",
            gemini_api_key="key",
            sonarqube_url="https://sonar.example.com",
            sonarqube_token="sonar_tok",
            dry_run=dry_run,
            project_root=MagicMock(),
            documentacion_dir=documentacion_dir or MagicMock(),
            reportes_dir=reportes_dir or MagicMock(),
        )

    @patch("scripts.wf2_inspeccion_arquitectura.extract_text_from_pdf")
    @patch("scripts.wf2_inspeccion_arquitectura.SonarQubeClient")
    @patch("scripts.wf2_inspeccion_arquitectura.GeminiClient")
    @patch("scripts.wf2_inspeccion_arquitectura.ConfluenceClient")
    @patch("scripts.wf2_inspeccion_arquitectura.JiraClient")
    @patch("scripts.wf2_inspeccion_arquitectura.write_summary_json")
    @patch("scripts.wf2_inspeccion_arquitectura.render_markdown_report")
    def test_happy_path_creates_artifacts(
        self,
        mock_render,
        mock_write_json,
        mock_jira_cls,
        mock_conf_cls,
        mock_gemini_cls,
        mock_sonar_cls,
        mock_extract,
    ):
        mock_doc_dir = MagicMock()
        mock_doc_dir.glob.return_value = [Path("documentacion/DAS.pdf")]
        config = self._make_config(dry_run=False, documentacion_dir=mock_doc_dir)

        mock_extract.return_value = "Diagrama C4: Contexto, Contenedores, Componentes."

        mock_sonar = MagicMock()
        mock_sonar.get_issues.return_value = {"issues": [{"key": "SONAR-1", "severity": "MAJOR"}]}
        mock_sonar.get_measures.return_value = {"component": {"measures": [{"metric": "code_smells", "value": "42"}]}}
        mock_sonar_cls.return_value = mock_sonar

        gemini_resp = (
            '[{"id":"ARCH-01","severity":"Alta","type":"task",'
            '"description":"Inconsistencia C4 detectada","component":"Backend"}]'
        )
        mock_gemini_cls.return_value.generate.return_value = gemini_resp

        mock_conf_cls.return_value.get_page_by_title.return_value = None
        mock_conf_cls.return_value.create_page.return_value = {"id": "PAGE-2"}

        mock_jira_cls.return_value.create_issue.return_value = MagicMock(key="SQA-10")

        wf2 = WF2InspeccionArquitectura(config)
        wf2.run()

        mock_extract.assert_called_once()
        mock_sonar.get_issues.assert_called_once()
        mock_sonar.get_measures.assert_called_once()
        mock_gemini_cls.return_value.generate.assert_called_once()
        mock_conf_cls.return_value.create_page.assert_called_once()
        self.assertEqual(mock_jira_cls.return_value.create_issue.call_count, 1)
        mock_write_json.assert_called_once()

    @patch("scripts.wf2_inspeccion_arquitectura.write_summary_json")
    def test_no_das_pdf_found_exits_early(self, mock_write_json):
        mock_doc_dir = MagicMock()
        mock_doc_dir.glob.return_value = []
        config = self._make_config(documentacion_dir=mock_doc_dir)

        wf2 = WF2InspeccionArquitectura(config)
        wf2.run()

        mock_write_json.assert_called_once()
        args = mock_write_json.call_args[1]
        self.assertEqual(args["status"], "failed")

    @patch("scripts.wf2_inspeccion_arquitectura.extract_text_from_pdf")
    @patch("scripts.wf2_inspeccion_arquitectura.SonarQubeClient")
    @patch("scripts.wf2_inspeccion_arquitectura.GeminiClient")
    @patch("scripts.wf2_inspeccion_arquitectura.ConfluenceClient")
    @patch("scripts.wf2_inspeccion_arquitectura.JiraClient")
    @patch("scripts.wf2_inspeccion_arquitectura.write_summary_json")
    def test_sonarqube_unreachable_aborts_inspection(
        self,
        mock_write_json,
        mock_jira_cls,
        mock_conf_cls,
        mock_gemini_cls,
        mock_sonar_cls,
        mock_extract,
    ):
        mock_doc_dir = MagicMock()
        mock_doc_dir.glob.return_value = [Path("documentacion/DAS.pdf")]
        config = self._make_config(documentacion_dir=mock_doc_dir)

        mock_extract.return_value = "Diagrama C4"
        mock_sonar_cls.return_value.get_issues.side_effect = Exception("Connection timeout")

        wf2 = WF2InspeccionArquitectura(config)
        wf2.run()

        mock_gemini_cls.return_value.generate.assert_not_called()
        mock_jira_cls.return_value.create_issue.assert_not_called()
        mock_conf_cls.return_value.create_page.assert_not_called()
        mock_write_json.assert_called_once()
        args = mock_write_json.call_args[1]
        self.assertEqual(args["status"], "failed")

    @patch("scripts.wf2_inspeccion_arquitectura.extract_text_from_pdf")
    @patch("scripts.wf2_inspeccion_arquitectura.SonarQubeClient")
    @patch("scripts.wf2_inspeccion_arquitectura.GeminiClient")
    @patch("scripts.wf2_inspeccion_arquitectura.ConfluenceClient")
    @patch("scripts.wf2_inspeccion_arquitectura.JiraClient")
    @patch("scripts.wf2_inspeccion_arquitectura.write_summary_json")
    def test_dry_run_skips_real_creation(
        self,
        mock_write_json,
        mock_jira_cls,
        mock_conf_cls,
        mock_gemini_cls,
        mock_sonar_cls,
        mock_extract,
    ):
        mock_doc_dir = MagicMock()
        mock_doc_dir.glob.return_value = [Path("documentacion/DAS.pdf")]
        config = self._make_config(dry_run=True, documentacion_dir=mock_doc_dir)

        mock_extract.return_value = "Diagrama C4"
        mock_sonar_cls.return_value.get_issues.return_value = {"issues": []}
        mock_sonar_cls.return_value.get_measures.return_value = {"component": {"measures": []}}
        mock_gemini_cls.return_value.generate.return_value = "[]"

        wf2 = WF2InspeccionArquitectura(config)
        wf2.run()

        mock_jira_cls.return_value.create_issue.assert_not_called()
        mock_conf_cls.return_value.create_page.assert_not_called()
        mock_write_json.assert_called_once()

    @patch("scripts.wf2_inspeccion_arquitectura.extract_text_from_pdf")
    @patch("scripts.wf2_inspeccion_arquitectura.SonarQubeClient")
    @patch("scripts.wf2_inspeccion_arquitectura.GeminiClient")
    @patch("scripts.wf2_inspeccion_arquitectura.ConfluenceClient")
    @patch("scripts.wf2_inspeccion_arquitectura.JiraClient")
    @patch("scripts.wf2_inspeccion_arquitectura.write_summary_json")
    def test_gemini_failure_logs_error(
        self,
        mock_write_json,
        mock_jira_cls,
        mock_conf_cls,
        mock_gemini_cls,
        mock_sonar_cls,
        mock_extract,
    ):
        mock_doc_dir = MagicMock()
        mock_doc_dir.glob.return_value = [Path("documentacion/DAS.pdf")]
        config = self._make_config(documentacion_dir=mock_doc_dir)

        mock_extract.return_value = "Diagrama C4"
        mock_sonar_cls.return_value.get_issues.return_value = {"issues": []}
        mock_sonar_cls.return_value.get_measures.return_value = {"component": {"measures": []}}
        mock_gemini_cls.return_value.generate.side_effect = Exception("Gemini quota exceeded")

        wf2 = WF2InspeccionArquitectura(config)
        wf2.run()

        mock_jira_cls.return_value.create_issue.assert_not_called()
        mock_conf_cls.return_value.create_page.assert_not_called()
        mock_write_json.assert_called_once()
        args = mock_write_json.call_args[1]
        self.assertEqual(args["status"], "failed")

    @patch("scripts.wf2_inspeccion_arquitectura.extract_text_from_pdf")
    @patch("scripts.wf2_inspeccion_arquitectura.SonarQubeClient")
    @patch("scripts.wf2_inspeccion_arquitectura.GeminiClient")
    @patch("scripts.wf2_inspeccion_arquitectura.ConfluenceClient")
    @patch("scripts.wf2_inspeccion_arquitectura.JiraClient")
    @patch("scripts.wf2_inspeccion_arquitectura.write_summary_json")
    def test_status_success_when_no_findings(
        self,
        mock_write_json,
        mock_jira_cls,
        mock_conf_cls,
        mock_gemini_cls,
        mock_sonar_cls,
        mock_extract,
    ):
        mock_doc_dir = MagicMock()
        mock_doc_dir.glob.return_value = [Path("documentacion/DAS.pdf")]
        config = self._make_config(dry_run=False, documentacion_dir=mock_doc_dir)

        mock_extract.return_value = "Diagrama C4"
        mock_sonar_cls.return_value.get_issues.return_value = {"issues": []}
        mock_sonar_cls.return_value.get_measures.return_value = {"component": {"measures": []}}
        mock_gemini_cls.return_value.generate.return_value = "[]"

        wf2 = WF2InspeccionArquitectura(config)
        wf2.run()

        args = mock_write_json.call_args[1]
        self.assertEqual(args["status"], "success")
        self.assertEqual(len(args["findings"]), 0)

    @patch("scripts.wf2_inspeccion_arquitectura.extract_text_from_pdf")
    @patch("scripts.wf2_inspeccion_arquitectura.SonarQubeClient")
    @patch("scripts.wf2_inspeccion_arquitectura.GeminiClient")
    @patch("scripts.wf2_inspeccion_arquitectura.ConfluenceClient")
    @patch("scripts.wf2_inspeccion_arquitectura.JiraClient")
    @patch("scripts.wf2_inspeccion_arquitectura.write_summary_json")
    def test_status_partial_when_findings_exist(
        self,
        mock_write_json,
        mock_jira_cls,
        mock_conf_cls,
        mock_gemini_cls,
        mock_sonar_cls,
        mock_extract,
    ):
        mock_doc_dir = MagicMock()
        mock_doc_dir.glob.return_value = [Path("documentacion/DAS.pdf")]
        config = self._make_config(dry_run=False, documentacion_dir=mock_doc_dir)

        mock_extract.return_value = "Diagrama C4"
        mock_sonar_cls.return_value.get_issues.return_value = {"issues": []}
        mock_sonar_cls.return_value.get_measures.return_value = {"component": {"measures": []}}
        mock_gemini_cls.return_value.generate.return_value = (
            '[{"id":"ARCH-02","severity":"Media","type":"task",'
            '"description":"Falta documentacion","component":"API"}]'
        )
        mock_jira_cls.return_value.create_issue.return_value = MagicMock(key="SQA-11")
        mock_conf_cls.return_value.create_page.return_value = {"id": "PAGE-3"}

        wf2 = WF2InspeccionArquitectura(config)
        wf2.run()

        args = mock_write_json.call_args[1]
        self.assertEqual(args["status"], "partial")
        self.assertEqual(len(args["findings"]), 1)

    @patch("scripts.wf2_inspeccion_arquitectura.extract_text_from_pdf")
    @patch("scripts.wf2_inspeccion_arquitectura.SonarQubeClient")
    @patch("scripts.wf2_inspeccion_arquitectura.GeminiClient")
    @patch("scripts.wf2_inspeccion_arquitectura.ConfluenceClient")
    @patch("scripts.wf2_inspeccion_arquitectura.JiraClient")
    @patch("scripts.wf2_inspeccion_arquitectura.write_summary_json")
    def test_jira_skips_baja_severity(
        self,
        mock_write_json,
        mock_jira_cls,
        mock_conf_cls,
        mock_gemini_cls,
        mock_sonar_cls,
        mock_extract,
    ):
        mock_doc_dir = MagicMock()
        mock_doc_dir.glob.return_value = [Path("documentacion/DAS.pdf")]
        config = self._make_config(dry_run=False, documentacion_dir=mock_doc_dir)

        mock_extract.return_value = "Diagrama C4"
        mock_sonar_cls.return_value.get_issues.return_value = {"issues": []}
        mock_sonar_cls.return_value.get_measures.return_value = {"component": {"measures": []}}
        mock_gemini_cls.return_value.generate.return_value = (
            '[{"id":"ARCH-03","severity":"Baja","type":"task",'
            '"description":"Mejora menor","component":"Frontend"}]'
        )
        mock_conf_cls.return_value.create_page.return_value = {"id": "PAGE-4"}

        wf2 = WF2InspeccionArquitectura(config)
        wf2.run()

        mock_jira_cls.return_value.create_issue.assert_not_called()
        args = mock_write_json.call_args[1]
        self.assertEqual(args["jira_keys"], [])

    @patch("scripts.wf2_inspeccion_arquitectura.ImageAnalyzer")
    @patch("scripts.wf2_inspeccion_arquitectura.extract_images_from_pdf")
    @patch("scripts.wf2_inspeccion_arquitectura.extract_page_texts_from_pdf")
    @patch("scripts.wf2_inspeccion_arquitectura.extract_text_from_pdf")
    @patch("scripts.wf2_inspeccion_arquitectura.SonarQubeClient")
    @patch("scripts.wf2_inspeccion_arquitectura.GeminiClient")
    @patch("scripts.wf2_inspeccion_arquitectura.ConfluenceClient")
    @patch("scripts.wf2_inspeccion_arquitectura.JiraClient")
    @patch("scripts.wf2_inspeccion_arquitectura.write_summary_json")
    def test_happy_path_with_visual_findings(
        self,
        mock_write_json,
        mock_jira_cls,
        mock_conf_cls,
        mock_gemini_cls,
        mock_sonar_cls,
        mock_extract,
        mock_page_texts,
        mock_extract_images,
        mock_analyzer_cls,
    ):
        mock_doc_dir = MagicMock()
        mock_doc_dir.glob.return_value = [Path("documentacion/DAS.pdf")]
        config = self._make_config(dry_run=False, documentacion_dir=mock_doc_dir)

        mock_extract.return_value = "Diagrama C4 de contexto"
        mock_sonar_cls.return_value.get_issues.return_value = {"issues": []}
        mock_sonar_cls.return_value.get_measures.return_value = {"component": {"measures": []}}
        mock_gemini_cls.return_value.generate.return_value = "[]"

        fake_image = Path("sqa/extracted_images/DAS_page1_img1.png")
        mock_extract_images.return_value = [fake_image]
        mock_page_texts.return_value = {1: "Diagrama de contexto"}

        mock_vf = MagicMock()
        mock_vf.id = "VIS-001"
        mock_vf.diagram_type.value = "c4_context"
        mock_vf.description = "Hallazgo visual"
        mock_vf.severity = "Alta"
        mock_vf.page_reference = "page 1"
        mock_vf.evidence = "evidencia"
        mock_analyzer_cls.return_value.batch_analyze.return_value = [
            (fake_image, [mock_vf])
        ]

        wf2 = WF2InspeccionArquitectura(config)
        wf2.run()

        mock_extract_images.assert_called_once()
        args = mock_write_json.call_args[1]
        self.assertIn("visual_findings", args)
        self.assertTrue(len(args["visual_findings"]) > 0)
        self.assertEqual(args["visual_findings"][0]["diagram_type"], "c4_context")
        self.assertEqual(args["visual_findings"][0]["severity"], "Alta")

    @patch("scripts.wf2_inspeccion_arquitectura.extract_images_from_pdf")
    @patch("scripts.wf2_inspeccion_arquitectura.extract_page_texts_from_pdf")
    @patch("scripts.wf2_inspeccion_arquitectura.extract_text_from_pdf")
    @patch("scripts.wf2_inspeccion_arquitectura.SonarQubeClient")
    @patch("scripts.wf2_inspeccion_arquitectura.GeminiClient")
    @patch("scripts.wf2_inspeccion_arquitectura.ConfluenceClient")
    @patch("scripts.wf2_inspeccion_arquitectura.JiraClient")
    @patch("scripts.wf2_inspeccion_arquitectura.write_summary_json")
    def test_empty_images_skips_visual_analysis(
        self,
        mock_write_json,
        mock_jira_cls,
        mock_conf_cls,
        mock_gemini_cls,
        mock_sonar_cls,
        mock_extract,
        mock_page_texts,
        mock_extract_images,
    ):
        mock_doc_dir = MagicMock()
        mock_doc_dir.glob.return_value = [Path("documentacion/DAS.pdf")]
        config = self._make_config(dry_run=True, documentacion_dir=mock_doc_dir)

        mock_extract.return_value = "Diagrama C4"
        mock_sonar_cls.return_value.get_issues.return_value = {"issues": []}
        mock_sonar_cls.return_value.get_measures.return_value = {"component": {"measures": []}}
        mock_gemini_cls.return_value.generate.return_value = "[]"
        mock_extract_images.return_value = []

        wf2 = WF2InspeccionArquitectura(config)
        wf2.run()

        args = mock_write_json.call_args[1]
        self.assertEqual(args["visual_findings"], [])

    @patch("scripts.wf2_inspeccion_arquitectura.extract_images_from_pdf")
    @patch("scripts.wf2_inspeccion_arquitectura.extract_page_texts_from_pdf")
    @patch("scripts.wf2_inspeccion_arquitectura.extract_text_from_pdf")
    @patch("scripts.wf2_inspeccion_arquitectura.SonarQubeClient")
    @patch("scripts.wf2_inspeccion_arquitectura.GeminiClient")
    @patch("scripts.wf2_inspeccion_arquitectura.ConfluenceClient")
    @patch("scripts.wf2_inspeccion_arquitectura.JiraClient")
    @patch("scripts.wf2_inspeccion_arquitectura.write_summary_json")
    def test_dry_run_generates_mock_visual_findings(
        self,
        mock_write_json,
        mock_jira_cls,
        mock_conf_cls,
        mock_gemini_cls,
        mock_sonar_cls,
        mock_extract,
        mock_page_texts,
        mock_extract_images,
    ):
        mock_doc_dir = MagicMock()
        mock_doc_dir.glob.return_value = [Path("documentacion/DAS.pdf")]
        config = self._make_config(dry_run=True, documentacion_dir=mock_doc_dir)

        mock_extract.return_value = "Diagrama C4"
        mock_sonar_cls.return_value.get_issues.return_value = {"issues": []}
        mock_sonar_cls.return_value.get_measures.return_value = {"component": {"measures": []}}
        mock_gemini_cls.return_value.generate.return_value = "[]"

        fake_image = Path("sqa/extracted_images/DAS_page1_img1.png")
        mock_extract_images.return_value = [fake_image]
        mock_page_texts.return_value = {1: "Página con diagrama"}

        wf2 = WF2InspeccionArquitectura(config)
        wf2.run()

        args = mock_write_json.call_args[1]
        self.assertEqual(len(args["visual_findings"]), 1)
        self.assertTrue(args["visual_findings"][0]["id"].startswith("VIS-MOCK"))
        self.assertEqual(args["visual_findings"][0]["severity"], "Baja")

    @patch("scripts.wf2_inspeccion_arquitectura.extract_images_from_pdf")
    @patch("scripts.wf2_inspeccion_arquitectura.extract_page_texts_from_pdf")
    @patch("scripts.wf2_inspeccion_arquitectura.extract_text_from_pdf")
    @patch("scripts.wf2_inspeccion_arquitectura.SonarQubeClient")
    @patch("scripts.wf2_inspeccion_arquitectura.GeminiClient")
    @patch("scripts.wf2_inspeccion_arquitectura.ConfluenceClient")
    @patch("scripts.wf2_inspeccion_arquitectura.JiraClient")
    @patch("scripts.wf2_inspeccion_arquitectura.write_summary_json")
    def test_visual_analysis_error_degrades_gracefully(
        self,
        mock_write_json,
        mock_jira_cls,
        mock_conf_cls,
        mock_gemini_cls,
        mock_sonar_cls,
        mock_extract,
        mock_page_texts,
        mock_extract_images,
    ):
        mock_doc_dir = MagicMock()
        mock_doc_dir.glob.return_value = [Path("documentacion/DAS.pdf")]
        config = self._make_config(dry_run=False, documentacion_dir=mock_doc_dir)

        mock_extract.return_value = "Diagrama C4"
        mock_sonar_cls.return_value.get_issues.return_value = {"issues": []}
        mock_sonar_cls.return_value.get_measures.return_value = {"component": {"measures": []}}
        mock_gemini_cls.return_value.generate.return_value = "[]"

        fake_image = Path("sqa/extracted_images/DAS_page1_img1.png")
        mock_extract_images.return_value = [fake_image]
        mock_page_texts.return_value = {1: "Página con diagrama"}

        wf2 = WF2InspeccionArquitectura(config)
        with patch.object(wf2, "_analyze_visuals", side_effect=Exception("Visual boom")):
            wf2.run()

        args = mock_write_json.call_args[1]
        self.assertEqual(args["visual_findings"], [])
        self.assertEqual(args["status"], "success")


if __name__ == "__main__":
    unittest.main()
