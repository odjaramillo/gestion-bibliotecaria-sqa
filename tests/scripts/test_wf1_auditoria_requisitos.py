"""Tests for scripts.wf1_auditoria_requisitos."""
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

from scripts.wf1_auditoria_requisitos import WF1AuditoriaRequisitos
from scripts.sqa_core.config import SQAConfig


class TestWF1AuditoriaRequisitos(unittest.TestCase):
    """Tests for WF1 Auditoria de Requisitos."""

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

    @patch("scripts.wf1_auditoria_requisitos.extract_text_from_pdf")
    @patch("scripts.wf1_auditoria_requisitos.chunk_text")
    @patch("scripts.wf1_auditoria_requisitos.GeminiClient")
    @patch("scripts.wf1_auditoria_requisitos.ConfluenceClient")
    @patch("scripts.wf1_auditoria_requisitos.JiraClient")
    @patch("scripts.wf1_auditoria_requisitos.write_summary_json")
    @patch("scripts.wf1_auditoria_requisitos.render_markdown_report")
    def test_happy_path_creates_artifacts(
        self,
        mock_render,
        mock_write_json,
        mock_jira_cls,
        mock_conf_cls,
        mock_gemini_cls,
        mock_chunk,
        mock_extract,
    ):
        # Setup mocks
        mock_doc_dir = MagicMock()
        mock_doc_dir.glob.return_value = [Path("documentacion/BRIEF.pdf"), Path("documentacion/ERS.pdf")]
        config = self._make_config(dry_run=False, documentacion_dir=mock_doc_dir)

        mock_extract.return_value = "Requisito: El sistema debe permitir préstamos."
        mock_chunk.return_value = ["chunk1"]

        gemini_resp = (
            '[{"id":"REQ-01","severity":"Alta","type":"bug",'
            '"description":"No es específico","invest_criteria":"Specific"}]'
        )
        mock_gemini_cls.return_value.generate.return_value = gemini_resp

        mock_conf_cls.return_value.get_page_by_title.return_value = None
        mock_conf_cls.return_value.create_page.return_value = {"id": "PAGE-1"}

        mock_jira_cls.return_value.create_issue.return_value = MagicMock(key="SQA-1")

        wf1 = WF1AuditoriaRequisitos(config)
        wf1.run()

        mock_extract.assert_called()
        mock_gemini_cls.return_value.generate.assert_called()
        mock_conf_cls.return_value.create_page.assert_called_once()
        self.assertEqual(mock_jira_cls.return_value.create_issue.call_count, 2)
        mock_write_json.assert_called_once()

    @patch("scripts.wf1_auditoria_requisitos.extract_text_from_pdf")
    @patch("scripts.wf1_auditoria_requisitos.GeminiClient")
    @patch("scripts.wf1_auditoria_requisitos.ConfluenceClient")
    @patch("scripts.wf1_auditoria_requisitos.JiraClient")
    @patch("scripts.wf1_auditoria_requisitos.write_summary_json")
    def test_no_pdfs_found_exits_early(
        self,
        mock_write_json,
        mock_jira_cls,
        mock_conf_cls,
        mock_gemini_cls,
        mock_extract,
    ):
        mock_doc_dir = MagicMock()
        mock_doc_dir.glob.return_value = []
        config = self._make_config(documentacion_dir=mock_doc_dir)

        wf1 = WF1AuditoriaRequisitos(config)
        wf1.run()

        mock_extract.assert_not_called()
        mock_gemini_cls.return_value.generate.assert_not_called()
        mock_conf_cls.return_value.create_page.assert_not_called()
        mock_jira_cls.return_value.create_issue.assert_not_called()
        mock_write_json.assert_called_once()
        args = mock_write_json.call_args[1]
        self.assertEqual(args["status"], "failed")

    @patch("scripts.wf1_auditoria_requisitos.extract_text_from_pdf")
    @patch("scripts.wf1_auditoria_requisitos.chunk_text")
    @patch("scripts.wf1_auditoria_requisitos.GeminiClient")
    @patch("scripts.wf1_auditoria_requisitos.ConfluenceClient")
    @patch("scripts.wf1_auditoria_requisitos.JiraClient")
    @patch("scripts.wf1_auditoria_requisitos.write_summary_json")
    def test_gemini_failure_logs_error(
        self,
        mock_write_json,
        mock_jira_cls,
        mock_conf_cls,
        mock_gemini_cls,
        mock_chunk,
        mock_extract,
    ):
        mock_doc_dir = MagicMock()
        mock_doc_dir.glob.return_value = [Path("documentacion/BRIEF.pdf")]
        config = self._make_config(documentacion_dir=mock_doc_dir)

        mock_extract.return_value = "text"
        mock_chunk.return_value = ["chunk1"]
        mock_gemini_cls.return_value.generate.side_effect = Exception("Gemini quota exceeded")

        wf1 = WF1AuditoriaRequisitos(config)
        wf1.run()

        mock_jira_cls.return_value.create_issue.assert_not_called()
        mock_conf_cls.return_value.create_page.assert_not_called()
        mock_write_json.assert_called_once()
        args = mock_write_json.call_args[1]
        self.assertEqual(args["status"], "failed")

    @patch("scripts.wf1_auditoria_requisitos.extract_text_from_pdf")
    @patch("scripts.wf1_auditoria_requisitos.chunk_text")
    @patch("scripts.wf1_auditoria_requisitos.GeminiClient")
    @patch("scripts.wf1_auditoria_requisitos.ConfluenceClient")
    @patch("scripts.wf1_auditoria_requisitos.JiraClient")
    @patch("scripts.wf1_auditoria_requisitos.write_summary_json")
    def test_dry_run_skips_real_creation(
        self,
        mock_write_json,
        mock_jira_cls,
        mock_conf_cls,
        mock_gemini_cls,
        mock_chunk,
        mock_extract,
    ):
        mock_doc_dir = MagicMock()
        mock_doc_dir.glob.return_value = [Path("documentacion/BRIEF.pdf")]
        config = self._make_config(dry_run=True, documentacion_dir=mock_doc_dir)

        mock_extract.return_value = "text"
        mock_chunk.return_value = ["chunk1"]
        mock_gemini_cls.return_value.generate.return_value = "[]"

        wf1 = WF1AuditoriaRequisitos(config)
        wf1.run()

        mock_jira_cls.return_value.create_issue.assert_not_called()
        mock_conf_cls.return_value.create_page.assert_not_called()
        mock_write_json.assert_called_once()


if __name__ == "__main__":
    unittest.main()
