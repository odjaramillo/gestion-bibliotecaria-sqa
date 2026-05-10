"""Tests for scripts.sqa_core.reporting."""
from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.sqa_core.reporting import render_markdown_report, write_summary_json


class TestRenderMarkdownReport(unittest.TestCase):
    """Tests for Markdown report rendering."""

    def test_includes_workflow_and_status(self):
        md = render_markdown_report(
            workflow="wf1",
            status="success",
            artifacts=["documentacion/BRIEF.pdf"],
            findings=[],
        )
        self.assertIn("# Reporte WF1", md)
        self.assertIn("**Estado:** success", md)

    def test_includes_findings_table(self):
        findings = [
            {"id": "REQ-01", "severity": "Alta", "type": "bug", "description": "Ambiguo"},
        ]
        md = render_markdown_report(
            workflow="wf1",
            status="partial",
            artifacts=["documentacion/ERS.pdf"],
            findings=findings,
        )
        self.assertIn("REQ-01", md)
        self.assertIn("Alta", md)
        self.assertIn("Ambiguo", md)

    def test_empty_findings_shows_no_defects(self):
        md = render_markdown_report(
            workflow="wf1",
            status="success",
            artifacts=["documentacion/BRIEF.pdf"],
            findings=[],
        )
        self.assertIn("No se detectaron defectos", md)


class TestWriteSummaryJson(unittest.TestCase):
    """Tests for JSON summary writing."""

    def test_writes_expected_contract(self):
        with TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "summary.json"
            write_summary_json(
                path=path,
                workflow="wf1",
                status="success",
                source_artifacts=["documentacion/BRIEF.pdf"],
                confluence_page_id="12345",
                jira_keys=["SQA-1"],
                findings=[{"id": "REQ-01", "severity": "Alta", "type": "bug"}],
            )
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(data["workflow"], "wf1")
            self.assertEqual(data["status"], "success")
            self.assertEqual(data["source_artifacts"], ["documentacion/BRIEF.pdf"])
            self.assertEqual(data["confluence_page_id"], "12345")
            self.assertEqual(data["jira_keys"], ["SQA-1"])
            self.assertEqual(len(data["findings"]), 1)
            self.assertIn("generated_at", data)

    def test_creates_parent_directories(self):
        with TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "nested" / "dir" / "summary.json"
            write_summary_json(
                path=path,
                workflow="wf1",
                status="success",
                source_artifacts=[],
                confluence_page_id=None,
                jira_keys=[],
                findings=[],
            )
            self.assertTrue(path.exists())


if __name__ == "__main__":
    unittest.main()
