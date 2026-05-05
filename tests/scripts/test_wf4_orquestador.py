"""Tests for scripts.wf4_orquestador."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock

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

from scripts.wf4_orquestador import (
    ArtifactDetector,
    DetectedArtifact,
    ReportGenerator,
    UpstreamSummaryReader,
    WF4Orchestrator,
)


class TestUpstreamSummaryReader(unittest.TestCase):
    """Tests for UpstreamSummaryReader."""

    def test_reads_all_available_summaries(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            reportes_dir = Path(tmpdir)
            for name in ("wf1", "wf2", "wf3"):
                (reportes_dir / f"{name}_summary.json").write_text(
                    json.dumps({"workflow": name, "status": "success", "findings": []}),
                    encoding="utf-8",
                )

            reader = UpstreamSummaryReader(reportes_dir)
            result = reader.read_all()

            self.assertEqual(set(result.keys()), {"wf1", "wf2", "wf3"})
            self.assertEqual(result["wf1"]["status"], "success")

    def test_missing_summaries_ignored(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            reportes_dir = Path(tmpdir)
            (reportes_dir / "wf1_summary.json").write_text(
                json.dumps({"workflow": "wf1", "status": "partial"}),
                encoding="utf-8",
            )

            reader = UpstreamSummaryReader(reportes_dir)
            result = reader.read_all()

            self.assertEqual(set(result.keys()), {"wf1"})

    def test_malformed_json_is_skipped(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            reportes_dir = Path(tmpdir)
            (reportes_dir / "wf1_summary.json").write_text("not json", encoding="utf-8")

            reader = UpstreamSummaryReader(reportes_dir)
            result = reader.read_all()

            self.assertEqual(result, {})


class TestReportGeneratorUpstream(unittest.TestCase):
    """Tests for ReportGenerator upstream integration."""

    def test_report_includes_upstream_section_when_summaries_present(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            reportes_dir = Path(tmpdir) / "reportes"
            reportes_dir.mkdir()

            gen = ReportGenerator(reportes_dir)
            artifacts = [
                DetectedArtifact(
                    path=Path("doc/BRIEF.pdf"),
                    artifact_type="BRIEF",
                    checklist_file="brief.json",
                )
            ]
            results = {}

            upstream = {
                "wf1": {
                    "workflow": "wf1",
                    "status": "partial",
                    "findings": [{"id": "REQ-01"}],
                    "source_artifacts": ["BRIEF.pdf"],
                },
            }

            path = gen.generate(artifacts, results, upstream_summaries=upstream)
            content = path.read_text(encoding="utf-8")

            self.assertIn("WF1", content)
            self.assertIn("partial", content)
            self.assertIn("REQ-01", content)
            self.assertIn("BRIEF.pdf", content)

    def test_report_has_no_upstream_section_when_summaries_empty(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            reportes_dir = Path(tmpdir) / "reportes"
            reportes_dir.mkdir()

            gen = ReportGenerator(reportes_dir)
            artifacts = [
                DetectedArtifact(
                    path=Path("doc/BRIEF.pdf"),
                    artifact_type="BRIEF",
                    checklist_file="brief.json",
                )
            ]
            results = {}

            path = gen.generate(artifacts, results, upstream_summaries={})
            content = path.read_text(encoding="utf-8")

            self.assertNotIn("Workflows Upstream", content)

    def test_dry_run_mode_mentions_simulation(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            reportes_dir = Path(tmpdir) / "reportes"
            reportes_dir.mkdir()

            gen = ReportGenerator(reportes_dir)
            artifacts = [
                DetectedArtifact(
                    path=Path("doc/BRIEF.pdf"),
                    artifact_type="BRIEF",
                    checklist_file="brief.json",
                )
            ]
            results = {}
            upstream = {
                "wf1": {"workflow": "wf1", "status": "success", "findings": []},
            }

            path = gen.generate(artifacts, results, upstream_summaries=upstream)
            content = path.read_text(encoding="utf-8")

            self.assertIn("DRY RUN", content)


class TestWF4OrchestratorIntegration(unittest.TestCase):
    """Integration tests for WF4Orchestrator with upstream summaries."""

    def _make_orchestrator(self, tmpdir: str, dry_run: bool = True) -> WF4Orchestrator:
        project_root = Path(tmpdir)
        documentacion_dir = project_root / "documentacion"
        checklists_dir = project_root / "sqa" / "checklists"
        reportes_dir = project_root / "sqa" / "reportes"
        documentacion_dir.mkdir(parents=True)
        checklists_dir.mkdir(parents=True)
        reportes_dir.mkdir(parents=True)

        # Create a dummy checklist
        checklist = {
            "artifact_type": "BRIEF",
            "standard": "ISO-25010",
            "version": "1.0",
            "items": [
                {
                    "id": "BR-01",
                    "category": "Requisitos",
                    "description": "El sistema debe tener login",
                    "verification_type": "Revision",
                    "evidence_location": "Seccion 3.1",
                    "standard_reference": "ISO-25010",
                }
            ],
        }
        (checklists_dir / "brief.json").write_text(json.dumps(checklist), encoding="utf-8")

        # Create a dummy PDF (just the file, content not used by detector)
        (documentacion_dir / "BRIEF.pdf").write_text("dummy", encoding="utf-8")

        config = MagicMock()
        config.dry_run = dry_run
        config.project_root = project_root
        config.documentacion_dir = documentacion_dir
        config.reportes_dir = reportes_dir

        return WF4Orchestrator(config)

    def test_orchestrator_reads_upstream_and_generates_report(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            orch = self._make_orchestrator(tmpdir)
            reportes_dir = orch.config.reportes_dir

            (reportes_dir / "wf1_summary.json").write_text(
                json.dumps(
                    {
                        "workflow": "wf1",
                        "status": "partial",
                        "findings": [{"id": "REQ-01", "severity": "Alta"}],
                        "source_artifacts": ["BRIEF.pdf"],
                        "jira_keys": ["SQA-1"],
                    }
                ),
                encoding="utf-8",
            )

            report_path = orch.run()
            content = report_path.read_text(encoding="utf-8")

            self.assertIn("WF1", content)
            self.assertIn("REQ-01", content)
            self.assertIn("SQA-1", content)

    def test_orchestrator_handles_missing_upstream_gracefully(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            orch = self._make_orchestrator(tmpdir)

            report_path = orch.run()
            content = report_path.read_text(encoding="utf-8")

            # Should still generate report for detected artifacts
            self.assertIn("BRIEF", content)
            self.assertTrue(report_path.exists())

    def test_orchestrator_reflects_all_three_workflows(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            orch = self._make_orchestrator(tmpdir)
            reportes_dir = orch.config.reportes_dir

            for i, name in enumerate(("wf1", "wf2", "wf3"), start=1):
                (reportes_dir / f"{name}_summary.json").write_text(
                    json.dumps(
                        {
                            "workflow": name,
                            "status": "success" if i == 1 else "partial",
                            "findings": [{"id": f"FIND-{i}", "severity": "Alta"}],
                            "source_artifacts": [f"{name}.pdf"],
                            "jira_keys": [f"SQA-{i}"],
                        }
                    ),
                    encoding="utf-8",
                )

            report_path = orch.run()
            content = report_path.read_text(encoding="utf-8")

            for name in ("WF1", "WF2", "WF3"):
                self.assertIn(name, content)

    def test_orchestrator_returns_none_when_no_artifacts(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            documentacion_dir = project_root / "documentacion"
            checklists_dir = project_root / "sqa" / "checklists"
            reportes_dir = project_root / "sqa" / "reportes"
            documentacion_dir.mkdir(parents=True)
            checklists_dir.mkdir(parents=True)
            reportes_dir.mkdir(parents=True)

            # No PDFs, no code dirs

            config = MagicMock()
            config.dry_run = True
            config.project_root = project_root
            config.documentacion_dir = documentacion_dir
            config.reportes_dir = reportes_dir

            orch = WF4Orchestrator(config)
            result = orch.run()
            self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
