"""Tests for scripts.wf3_generacion_pruebas."""
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

from scripts.wf3_generacion_pruebas import WF3GeneracionPruebas
from scripts.sqa_core.config import SQAConfig


class TestWF3GeneracionPruebas(unittest.TestCase):
    """Tests for WF3 Generacion de Pruebas."""

    def _make_config(
        self,
        dry_run: bool = True,
        reportes_dir=None,
        project_root=None,
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
            project_root=project_root or MagicMock(),
            documentacion_dir=MagicMock(),
            reportes_dir=reportes_dir or MagicMock(),
        )

    def _make_wf1_summary(self) -> dict:
        return {
            "workflow": "wf1",
            "status": "partial",
            "findings": [
                {"id": "REQ-01", "severity": "Alta", "type": "bug", "description": "Ambiguo", "invest_criteria": "Specific"},
            ],
            "jira_keys": ["SQA-1"],
        }

    def _make_wf2_summary(self) -> dict:
        return {
            "workflow": "wf2",
            "status": "partial",
            "findings": [
                {"id": "ARCH-01", "severity": "Alta", "type": "task", "description": "Deuda tecnica", "component": "Backend"},
            ],
            "jira_keys": ["SQA-10"],
        }

    @patch("scripts.wf3_generacion_pruebas.GeminiClient")
    @patch("scripts.wf3_generacion_pruebas.ConfluenceClient")
    @patch("scripts.wf3_generacion_pruebas.JiraClient")
    @patch("scripts.wf3_generacion_pruebas.write_summary_json")
    @patch("scripts.wf3_generacion_pruebas.render_markdown_report")
    @patch("scripts.wf3_generacion_pruebas.subprocess.run")
    def test_happy_path_creates_all_artifacts(
        self,
        mock_subprocess,
        mock_render,
        mock_write_json,
        mock_jira_cls,
        mock_conf_cls,
        mock_gemini_cls,
    ):
        import json as _json
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            reportes_dir = Path(tmpdir) / "sqa" / "reportes"
            reportes_dir.mkdir(parents=True)
            project_root = Path(tmpdir)

            # Write upstream summaries
            (reportes_dir / "wf1_summary.json").write_text(
                _json.dumps(self._make_wf1_summary()), encoding="utf-8"
            )
            (reportes_dir / "wf2_summary.json").write_text(
                _json.dumps(self._make_wf2_summary()), encoding="utf-8"
            )

            config = self._make_config(dry_run=False, reportes_dir=reportes_dir, project_root=project_root)

            gemini_resp = _json.dumps([
                {"id": "TC-01", "type": "Funcional", "priority": "Alta",
                 "title": "Validar requisito REQ-01", "description": "Verificar claridad",
                 "related_finding": "REQ-01"},
            ])
            mock_gemini_cls.return_value.generate.return_value = gemini_resp

            mock_conf_cls.return_value.get_page_by_title.return_value = None
            mock_conf_cls.return_value.create_page.return_value = {"id": "PAGE-5"}

            mock_jira_cls.return_value.create_issue.return_value = MagicMock(key="SQA-20")

            wf3 = WF3GeneracionPruebas(config)
            wf3.run()

            mock_gemini_cls.return_value.generate.assert_called_once()
            mock_conf_cls.return_value.create_page.assert_called_once()
            self.assertEqual(mock_jira_cls.return_value.create_issue.call_count, 1)
            mock_write_json.assert_called_once()

            # Verify skeleton files were created
            test_auto_dir = project_root / "sqa" / "test-automation"
            self.assertTrue(test_auto_dir.exists())
            self.assertTrue((test_auto_dir / "README.md").exists())
            self.assertTrue((test_auto_dir / "test_backend_api.py").exists())

    @patch("scripts.wf3_generacion_pruebas.write_summary_json")
    def test_missing_both_summaries_fails_gracefully(self, mock_write_json):
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            reportes_dir = Path(tmpdir) / "sqa" / "reportes"
            reportes_dir.mkdir(parents=True)
            config = self._make_config(reportes_dir=reportes_dir)

            wf3 = WF3GeneracionPruebas(config)
            wf3.run()

            mock_write_json.assert_called_once()
            args = mock_write_json.call_args[1]
            self.assertEqual(args["status"], "failed")
            self.assertEqual(args["jira_keys"], [])

    @patch("scripts.wf3_generacion_pruebas.GeminiClient")
    @patch("scripts.wf3_generacion_pruebas.ConfluenceClient")
    @patch("scripts.wf3_generacion_pruebas.JiraClient")
    @patch("scripts.wf3_generacion_pruebas.write_summary_json")
    def test_gemini_failure_logs_error(
        self,
        mock_write_json,
        mock_jira_cls,
        mock_conf_cls,
        mock_gemini_cls,
    ):
        import json as _json
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            reportes_dir = Path(tmpdir) / "sqa" / "reportes"
            reportes_dir.mkdir(parents=True)
            project_root = Path(tmpdir)

            (reportes_dir / "wf1_summary.json").write_text(
                _json.dumps(self._make_wf1_summary()), encoding="utf-8"
            )
            (reportes_dir / "wf2_summary.json").write_text(
                _json.dumps(self._make_wf2_summary()), encoding="utf-8"
            )

            config = self._make_config(reportes_dir=reportes_dir, project_root=project_root)
            mock_gemini_cls.return_value.generate.side_effect = Exception("Gemini quota exceeded")

            wf3 = WF3GeneracionPruebas(config)
            wf3.run()

            mock_jira_cls.return_value.create_issue.assert_not_called()
            mock_conf_cls.return_value.create_page.assert_not_called()
            mock_write_json.assert_called_once()
            args = mock_write_json.call_args[1]
            self.assertEqual(args["status"], "failed")

    @patch("scripts.wf3_generacion_pruebas.GeminiClient")
    @patch("scripts.wf3_generacion_pruebas.ConfluenceClient")
    @patch("scripts.wf3_generacion_pruebas.JiraClient")
    @patch("scripts.wf3_generacion_pruebas.write_summary_json")
    @patch("scripts.wf3_generacion_pruebas.subprocess.run")
    def test_dry_run_skips_real_creation(
        self,
        mock_subprocess,
        mock_write_json,
        mock_jira_cls,
        mock_conf_cls,
        mock_gemini_cls,
    ):
        import json as _json
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            reportes_dir = Path(tmpdir) / "sqa" / "reportes"
            reportes_dir.mkdir(parents=True)
            project_root = Path(tmpdir)

            (reportes_dir / "wf1_summary.json").write_text(
                _json.dumps(self._make_wf1_summary()), encoding="utf-8"
            )
            (reportes_dir / "wf2_summary.json").write_text(
                _json.dumps(self._make_wf2_summary()), encoding="utf-8"
            )

            config = self._make_config(dry_run=True, reportes_dir=reportes_dir, project_root=project_root)
            mock_gemini_cls.return_value.generate.return_value = _json.dumps([])

            wf3 = WF3GeneracionPruebas(config)
            wf3.run()

            mock_jira_cls.return_value.create_issue.assert_not_called()
            mock_conf_cls.return_value.create_page.assert_not_called()
            mock_subprocess.assert_not_called()
            mock_write_json.assert_called_once()

    @patch("scripts.wf3_generacion_pruebas.GeminiClient")
    @patch("scripts.wf3_generacion_pruebas.ConfluenceClient")
    @patch("scripts.wf3_generacion_pruebas.JiraClient")
    @patch("scripts.wf3_generacion_pruebas.write_summary_json")
    @patch("scripts.wf3_generacion_pruebas.subprocess.run")
    def test_pr_creation_failure_preserves_artifacts(
        self,
        mock_subprocess,
        mock_write_json,
        mock_jira_cls,
        mock_conf_cls,
        mock_gemini_cls,
    ):
        import json as _json
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            reportes_dir = Path(tmpdir) / "sqa" / "reportes"
            reportes_dir.mkdir(parents=True)
            project_root = Path(tmpdir)

            (reportes_dir / "wf1_summary.json").write_text(
                _json.dumps(self._make_wf1_summary()), encoding="utf-8"
            )
            (reportes_dir / "wf2_summary.json").write_text(
                _json.dumps(self._make_wf2_summary()), encoding="utf-8"
            )

            config = self._make_config(dry_run=False, reportes_dir=reportes_dir, project_root=project_root)

            gemini_resp = _json.dumps([
                {"id": "TC-01", "type": "Funcional", "priority": "Alta",
                 "title": "Validar requisito", "description": "Desc",
                 "related_finding": "REQ-01"},
            ])
            mock_gemini_cls.return_value.generate.return_value = gemini_resp

            mock_conf_cls.return_value.get_page_by_title.return_value = None
            mock_conf_cls.return_value.create_page.return_value = {"id": "PAGE-6"}
            mock_jira_cls.return_value.create_issue.return_value = MagicMock(key="SQA-21")

            mock_subprocess.side_effect = Exception("gh: unauthorized")

            wf3 = WF3GeneracionPruebas(config)
            wf3.run()

            mock_conf_cls.return_value.create_page.assert_called_once()
            self.assertEqual(mock_jira_cls.return_value.create_issue.call_count, 1)
            mock_write_json.assert_called_once()
            args = mock_write_json.call_args[1]
            self.assertEqual(args["status"], "partial")

    @patch("scripts.wf3_generacion_pruebas.GeminiClient")
    @patch("scripts.wf3_generacion_pruebas.ConfluenceClient")
    @patch("scripts.wf3_generacion_pruebas.JiraClient")
    @patch("scripts.wf3_generacion_pruebas.write_summary_json")
    def test_no_upstream_findings_generates_plan(
        self,
        mock_write_json,
        mock_jira_cls,
        mock_conf_cls,
        mock_gemini_cls,
    ):
        import json as _json
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            reportes_dir = Path(tmpdir) / "sqa" / "reportes"
            reportes_dir.mkdir(parents=True)
            project_root = Path(tmpdir)

            empty_summary = {"workflow": "wf1", "status": "success", "findings": [], "jira_keys": []}
            (reportes_dir / "wf1_summary.json").write_text(
                _json.dumps(empty_summary), encoding="utf-8"
            )
            (reportes_dir / "wf2_summary.json").write_text(
                _json.dumps(empty_summary), encoding="utf-8"
            )

            config = self._make_config(dry_run=False, reportes_dir=reportes_dir, project_root=project_root)
            mock_gemini_cls.return_value.generate.return_value = "[]"

            mock_conf_cls.return_value.get_page_by_title.return_value = None
            mock_conf_cls.return_value.create_page.return_value = {"id": "PAGE-7"}

            wf3 = WF3GeneracionPruebas(config)
            wf3.run()

            mock_gemini_cls.return_value.generate.assert_called_once()
            mock_conf_cls.return_value.create_page.assert_called_once()
            mock_jira_cls.return_value.create_issue.assert_not_called()
            args = mock_write_json.call_args[1]
            self.assertEqual(args["status"], "success")

    @patch("scripts.wf3_generacion_pruebas.GeminiClient")
    @patch("scripts.wf3_generacion_pruebas.ConfluenceClient")
    @patch("scripts.wf3_generacion_pruebas.JiraClient")
    @patch("scripts.wf3_generacion_pruebas.write_summary_json")
    def test_missing_wf2_uses_wf1_only(
        self,
        mock_write_json,
        mock_jira_cls,
        mock_conf_cls,
        mock_gemini_cls,
    ):
        import json as _json
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            reportes_dir = Path(tmpdir) / "sqa" / "reportes"
            reportes_dir.mkdir(parents=True)
            project_root = Path(tmpdir)

            (reportes_dir / "wf1_summary.json").write_text(
                _json.dumps(self._make_wf1_summary()), encoding="utf-8"
            )
            # wf2_summary.json is missing

            config = self._make_config(dry_run=False, reportes_dir=reportes_dir, project_root=project_root)
            mock_gemini_cls.return_value.generate.return_value = "[]"

            mock_conf_cls.return_value.get_page_by_title.return_value = None
            mock_conf_cls.return_value.create_page.return_value = {"id": "PAGE-8"}

            wf3 = WF3GeneracionPruebas(config)
            wf3.run()

            mock_gemini_cls.return_value.generate.assert_called_once()
            mock_conf_cls.return_value.create_page.assert_called_once()
            args = mock_write_json.call_args[1]
            self.assertEqual(args["status"], "success")


if __name__ == "__main__":
    unittest.main()
