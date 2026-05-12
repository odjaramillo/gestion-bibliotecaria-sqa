"""Tests para scripts.wf7_agente_pdf_confluence."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import MagicMock, patch

# Mockear dependencias de terceros antes de importar módulos SQA
for _mod in ("jira", "requests"):
    if _mod not in sys.modules:
        sys.modules[_mod] = MagicMock()

if "google" not in sys.modules:
    sys.modules["google"] = MagicMock()
if "google.generativeai" not in sys.modules:
    sys.modules["google.generativeai"] = MagicMock()

if "fitz" not in sys.modules:
    sys.modules["fitz"] = MagicMock()

from scripts.sqa_core.config import SQAConfig
from scripts.wf7_agente_pdf_confluence import (
    CONFLUENCE_PARENT_TITLE,
    CONFLUENCE_ROOT_TITLE,
    ResultadoPdf,
    WF7AgentePdfConfluence,
)


class TestWF7AgentePdfConfluence(unittest.TestCase):
    """Tests de integración mockeada para WF7."""

    def _make_config(self, tmpdir: str, dry_run: bool = True) -> SQAConfig:
        project_root = Path(tmpdir)
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
            modo="reporte" if dry_run else "produccion",
            project_root=project_root,
            documentacion_dir=project_root / "documentacion",
            reportes_dir=project_root / "sqa" / "reportes",
        )

    def _make_workflow(self, tmpdir: str, dry_run: bool = True) -> WF7AgentePdfConfluence:
        config = self._make_config(tmpdir, dry_run)
        wf = WF7AgentePdfConfluence(config)
        return wf

    # ------------------------------------------------------------------
    # Dry-run
    # ------------------------------------------------------------------
    def test_dry_run_no_llama_apis_externas(self):
        with TemporaryDirectory() as tmpdir:
            pdfs_dir = Path(tmpdir) / "pdfs"
            pdfs_dir.mkdir()
            (pdfs_dir / "auditoria_test.pdf").write_text("dummy", encoding="utf-8")

            wf = self._make_workflow(tmpdir, dry_run=True)
            wf.confluence = MagicMock()
            wf.jira = MagicMock()

            with patch("scripts.wf7_agente_pdf_confluence.ExtractorAuditoriaPdf.extraer") as mock_extraer:
                mock_doc = MagicMock()
                mock_doc.nombre = "auditoria_test"
                mock_doc.pdf_path = str(pdfs_dir / "auditoria_test.pdf")
                mock_doc.filas_con_defecto.return_value = []
                mock_doc.filas = []
                mock_extraer.return_value = mock_doc

                summary_path = wf.run(directorio_pdfs=pdfs_dir, dry_run=True)

            self.assertTrue(summary_path.exists())
            wf.confluence.create_page.assert_not_called()
            wf.confluence.upload_attachment.assert_not_called()
            wf.jira.upsert_issue.assert_not_called()

    # ------------------------------------------------------------------
    # Jerarquía
    # ------------------------------------------------------------------
    def test_crea_jerarquia_cuando_no_existe(self):
        with TemporaryDirectory() as tmpdir:
            wf = self._make_workflow(tmpdir, dry_run=False)
            wf.confluence = MagicMock()
            wf.confluence.get_page_by_title.return_value = None
            wf.confluence.create_page.side_effect = [
                {"id": "ROOT-1"},
                {"id": "PARENT-1"},
            ]

            parent_id = wf._asegurar_jerarquia(dry_run=False)

            self.assertEqual(parent_id, "PARENT-1")
            # Dos llamadas: root + parent
            self.assertEqual(wf.confluence.create_page.call_count, 2)
            # Primera llamada crea la raíz
            args_root = wf.confluence.create_page.call_args_list[0]
            self.assertEqual(args_root[0][2], CONFLUENCE_ROOT_TITLE)
            # Segunda llamada crea el padre bajo la raíz
            args_parent = wf.confluence.create_page.call_args_list[1]
            self.assertEqual(args_parent[0][1], "ROOT-1")
            self.assertEqual(args_parent[0][2], CONFLUENCE_PARENT_TITLE)

    def test_reusa_jerarquia_existente(self):
        with TemporaryDirectory() as tmpdir:
            wf = self._make_workflow(tmpdir, dry_run=False)
            wf.confluence = MagicMock()
            wf.confluence.get_page_by_title.side_effect = [
                {"id": "ROOT-1", "version": {"number": 1}},
                {"id": "PARENT-1", "version": {"number": 1}},
            ]

            parent_id = wf._asegurar_jerarquia(dry_run=False)

            self.assertEqual(parent_id, "PARENT-1")
            wf.confluence.create_page.assert_not_called()

    # ------------------------------------------------------------------
    # Defectos → Jira
    # ------------------------------------------------------------------
    def test_sincroniza_defectos_con_jira(self):
        with TemporaryDirectory() as tmpdir:
            wf = self._make_workflow(tmpdir, dry_run=False)
            wf.jira = MagicMock()
            wf.jira.upsert_issue.return_value = {
                "action": "created",
                "issue_key": "SQA-99",
            }

            mock_fila = MagicMock()
            mock_fila.id = "REQ-01"
            mock_fila.metrica = "Cobertura"
            mock_fila.criterio = ">80%"
            mock_fila.resultado = "FALLA"
            mock_fila.observacion = "Baja"
            mock_fila.es_defecto = True

            mock_doc = MagicMock()
            mock_doc.nombre = "Auditoria_Test"
            mock_doc.pdf_path = "/fake.pdf"
            mock_doc.filas_con_defecto.return_value = [mock_fila]

            tickets = wf._sincronizar_jira(mock_doc, "PAGE-1", dry_run=False)

            self.assertEqual(tickets, {"REQ-01": "SQA-99"})
            wf.jira.upsert_issue.assert_called_once()
            args = wf.jira.upsert_issue.call_args
            self.assertEqual(args[1]["external_id"], "SQA-PDF-AUDITORIA_TEST-REQ-01")
            fields = args[1]["fields"]
            self.assertEqual(fields["project"]["key"], "SQA")
            self.assertEqual(fields["issuetype"]["name"], "Bug")

    def test_dry_run_no_sincroniza_jira(self):
        with TemporaryDirectory() as tmpdir:
            wf = self._make_workflow(tmpdir, dry_run=True)
            wf.jira = MagicMock()

            mock_doc = MagicMock()
            mock_doc.nombre = "Auditoria_Test"
            mock_doc.pdf_path = "/fake.pdf"
            mock_doc.filas_con_defecto.return_value = []

            tickets = wf._sincronizar_jira(mock_doc, "PAGE-1", dry_run=True)

            self.assertEqual(tickets, {})
            wf.jira.upsert_issue.assert_not_called()

    # ------------------------------------------------------------------
    # Resiliencia: un PDF falla, los demás continúan
    # ------------------------------------------------------------------
    def test_continua_cuando_un_pdf_falla(self):
        with TemporaryDirectory() as tmpdir:
            pdfs_dir = Path(tmpdir) / "pdfs"
            pdfs_dir.mkdir()
            (pdfs_dir / "ok.pdf").write_text("dummy", encoding="utf-8")
            (pdfs_dir / "bad.pdf").write_text("dummy", encoding="utf-8")

            wf = self._make_workflow(tmpdir, dry_run=False)
            wf.confluence = MagicMock()
            wf.confluence.get_page_by_title.return_value = None
            wf.confluence.create_page.return_value = {"id": "PAGE-OK"}
            wf.jira = MagicMock()
            wf.jira.upsert_issue.return_value = {
                "action": "created",
                "issue_key": "SQA-1",
            }

            call_count = [0]

            def _extraer_side_effect(pdf_path):
                call_count[0] += 1
                if "bad" in str(pdf_path):
                    raise ValueError("PDF corrupto")
                mock_doc = MagicMock()
                mock_doc.nombre = "ok"
                mock_doc.pdf_path = str(pdf_path)
                mock_doc.filas_con_defecto.return_value = []
                mock_doc.filas = []
                return mock_doc

            with patch(
                "scripts.wf7_agente_pdf_confluence.ExtractorAuditoriaPdf.extraer"
            ) as mock_extraer:
                mock_extraer.side_effect = _extraer_side_effect
                summary_path = wf.run(directorio_pdfs=pdfs_dir, dry_run=False)

            data = json.loads(summary_path.read_text(encoding="utf-8"))
            self.assertEqual(data["total_pdfs_processed"], 2)
            self.assertEqual(data["successful"], 1)
            self.assertEqual(data["failed"], 1)

            pdf_results = {p["pdf_name"]: p for p in data["pdfs"]}
            self.assertEqual(pdf_results["ok.pdf"]["status"], "success")
            self.assertEqual(pdf_results["bad.pdf"]["status"], "failed")
            self.assertIn("PDF corrupto", pdf_results["bad.pdf"]["error_message"])

    # ------------------------------------------------------------------
    # Resumen JSON
    # ------------------------------------------------------------------
    def test_genera_resumen_json_correcto(self):
        with TemporaryDirectory() as tmpdir:
            pdfs_dir = Path(tmpdir) / "pdfs"
            pdfs_dir.mkdir()
            (pdfs_dir / "test.pdf").write_text("dummy", encoding="utf-8")

            wf = self._make_workflow(tmpdir, dry_run=True)
            wf.confluence = MagicMock()
            wf.jira = MagicMock()

            with patch("scripts.wf7_agente_pdf_confluence.ExtractorAuditoriaPdf.extraer") as mock_extraer:
                mock_doc = MagicMock()
                mock_doc.nombre = "test"
                mock_doc.pdf_path = str(pdfs_dir / "test.pdf")
                mock_doc.filas_con_defecto.return_value = []
                mock_doc.filas = []
                mock_extraer.return_value = mock_doc

                summary_path = wf.run(directorio_pdfs=pdfs_dir, dry_run=True)

            self.assertTrue(summary_path.exists())
            data = json.loads(summary_path.read_text(encoding="utf-8"))
            self.assertEqual(data["total_pdfs_processed"], 1)
            self.assertEqual(data["successful"], 1)
            self.assertEqual(data["failed"], 0)
            self.assertIn("execution_date", data)
            self.assertEqual(len(data["pdfs"]), 1)
            self.assertEqual(data["pdfs"][0]["pdf_name"], "test.pdf")
            self.assertEqual(data["pdfs"][0]["status"], "success")
            self.assertEqual(data["pdfs"][0]["defect_count"], 0)
            self.assertIn("timestamp", data["pdfs"][0])

    # ------------------------------------------------------------------
    # Sin PDFs
    # ------------------------------------------------------------------
    def test_sin_pdfs_genera_resumen_vacio(self):
        with TemporaryDirectory() as tmpdir:
            pdfs_dir = Path(tmpdir) / "pdfs"
            pdfs_dir.mkdir()

            wf = self._make_workflow(tmpdir, dry_run=True)
            summary_path = wf.run(directorio_pdfs=pdfs_dir, dry_run=True)

            data = json.loads(summary_path.read_text(encoding="utf-8"))
            self.assertEqual(data["total_pdfs_processed"], 0)
            self.assertEqual(data["successful"], 0)
            self.assertEqual(data["failed"], 0)
            self.assertEqual(data["pdfs"], [])

    # ------------------------------------------------------------------
    # Adjunto
    # ------------------------------------------------------------------
    def test_sube_adjunto_en_modo_produccion(self):
        with TemporaryDirectory() as tmpdir:
            pdfs_dir = Path(tmpdir) / "pdfs"
            pdfs_dir.mkdir()
            pdf_path = pdfs_dir / "test.pdf"
            pdf_path.write_text("dummy", encoding="utf-8")

            wf = self._make_workflow(tmpdir, dry_run=False)
            wf.confluence = MagicMock()
            wf.confluence.get_page_by_title.return_value = None
            wf.confluence.create_page.return_value = {"id": "PAGE-1"}
            wf.jira = MagicMock()
            wf.jira.upsert_issue.return_value = {
                "action": "created",
                "issue_key": "SQA-1",
            }

            with patch("scripts.wf7_agente_pdf_confluence.ExtractorAuditoriaPdf.extraer") as mock_extraer:
                mock_doc = MagicMock()
                mock_doc.nombre = "test"
                mock_doc.pdf_path = str(pdf_path)
                mock_doc.filas_con_defecto.return_value = []
                mock_doc.filas = []
                mock_extraer.return_value = mock_doc

                wf.run(directorio_pdfs=pdfs_dir, dry_run=False)

            wf.confluence.upload_attachment.assert_called_once_with(
                pdf_path, "PAGE-1"
            )

    # ------------------------------------------------------------------
    # Re-renderizado con tickets
    # ------------------------------------------------------------------
    def test_actualiza_pagina_con_enlaces_jira(self):
        with TemporaryDirectory() as tmpdir:
            pdfs_dir = Path(tmpdir) / "pdfs"
            pdfs_dir.mkdir()
            pdf_path = pdfs_dir / "test.pdf"
            pdf_path.write_text("dummy", encoding="utf-8")

            wf = self._make_workflow(tmpdir, dry_run=False)
            wf.confluence = MagicMock()
            wf.confluence.get_page_by_title.side_effect = [
                None,  # raíz no existe
                None,  # padre no existe
                None,  # primera búsqueda para crear página PDF
                {"id": "PAGE-1", "version": {"number": 1}},  # segunda para update con tickets
            ]
            wf.confluence.create_page.return_value = {"id": "PAGE-1"}
            wf.jira = MagicMock()
            wf.jira.upsert_issue.return_value = {
                "action": "created",
                "issue_key": "SQA-101",
            }

            with patch("scripts.wf7_agente_pdf_confluence.ExtractorAuditoriaPdf.extraer") as mock_extraer:
                mock_fila = MagicMock()
                mock_fila.id = "REQ-01"
                mock_fila.metrica = "M1"
                mock_fila.criterio = "C1"
                mock_fila.resultado = "FALLA"
                mock_fila.observacion = "Obs"
                mock_fila.es_defecto = True

                mock_doc = MagicMock()
                mock_doc.nombre = "test"
                mock_doc.pdf_path = str(pdf_path)
                mock_doc.filas_con_defecto.return_value = [mock_fila]
                mock_doc.filas = [mock_fila]
                mock_extraer.return_value = mock_doc

                wf.run(directorio_pdfs=pdfs_dir, dry_run=False)

            # Debe llamar a update_page para re-renderizar con tickets
            wf.confluence.update_page.assert_called_once()
            update_args = wf.confluence.update_page.call_args
            self.assertEqual(update_args[0][0], "PAGE-1")

    # ------------------------------------------------------------------
    # Propagación de errores
    # ------------------------------------------------------------------
    def test_marca_pdf_como_fallido_si_confluence_falla(self):
        with TemporaryDirectory() as tmpdir:
            pdfs_dir = Path(tmpdir) / "pdfs"
            pdfs_dir.mkdir()
            (pdfs_dir / "test.pdf").write_text("dummy", encoding="utf-8")

            wf = self._make_workflow(tmpdir, dry_run=False)
            wf.confluence = MagicMock()
            wf.confluence.get_page_by_title.side_effect = [
                {"id": "ROOT-1"},
                {"id": "PARENT-1"},
                None,
            ]
            wf.confluence.create_page.side_effect = Exception("Confluence timeout")
            wf.jira = MagicMock()

            with patch("scripts.wf7_agente_pdf_confluence.ExtractorAuditoriaPdf.extraer") as mock_extraer:
                mock_doc = MagicMock()
                mock_doc.nombre = "test"
                mock_doc.pdf_path = str(pdfs_dir / "test.pdf")
                mock_doc.filas_con_defecto.return_value = []
                mock_doc.filas = []
                mock_extraer.return_value = mock_doc

                summary_path = wf.run(directorio_pdfs=pdfs_dir, dry_run=False)

            data = json.loads(summary_path.read_text(encoding="utf-8"))
            self.assertEqual(data["failed"], 1)
            pdf_results = {p["pdf_name"]: p for p in data["pdfs"]}
            self.assertEqual(pdf_results["test.pdf"]["status"], "failed")
            self.assertIn("Confluence timeout", pdf_results["test.pdf"]["error_message"])

    def test_marca_pdf_como_fallido_si_jira_falla(self):
        with TemporaryDirectory() as tmpdir:
            pdfs_dir = Path(tmpdir) / "pdfs"
            pdfs_dir.mkdir()
            (pdfs_dir / "test.pdf").write_text("dummy", encoding="utf-8")

            wf = self._make_workflow(tmpdir, dry_run=False)
            wf.confluence = MagicMock()
            wf.confluence.get_page_by_title.return_value = None
            wf.confluence.create_page.return_value = {"id": "PAGE-1"}
            wf.jira = MagicMock()
            wf.jira.upsert_issue.return_value = {"action": "error", "issue_key": None}

            with patch("scripts.wf7_agente_pdf_confluence.ExtractorAuditoriaPdf.extraer") as mock_extraer:
                mock_fila = MagicMock()
                mock_fila.id = "REQ-01"
                mock_fila.metrica = "M1"
                mock_fila.criterio = "C1"
                mock_fila.resultado = "FALLA"
                mock_fila.observacion = "Obs"
                mock_fila.es_defecto = True

                mock_doc = MagicMock()
                mock_doc.nombre = "test"
                mock_doc.pdf_path = str(pdfs_dir / "test.pdf")
                mock_doc.filas_con_defecto.return_value = [mock_fila]
                mock_doc.filas = [mock_fila]
                mock_extraer.return_value = mock_doc

                summary_path = wf.run(directorio_pdfs=pdfs_dir, dry_run=False)

            data = json.loads(summary_path.read_text(encoding="utf-8"))
            self.assertEqual(data["failed"], 1)
            pdf_results = {p["pdf_name"]: p for p in data["pdfs"]}
            self.assertEqual(pdf_results["test.pdf"]["status"], "failed")
            self.assertIn(
                "Jira upsert_issue devolvió error",
                pdf_results["test.pdf"]["error_message"],
            )

    def test_idempotencia_dos_ejecuciones_no_duplican_jira(self):
        with TemporaryDirectory() as tmpdir:
            pdfs_dir = Path(tmpdir) / "pdfs"
            pdfs_dir.mkdir()
            (pdfs_dir / "test.pdf").write_text("dummy", encoding="utf-8")

            wf = self._make_workflow(tmpdir, dry_run=False)
            wf.confluence = MagicMock()
            wf.confluence.get_page_by_title.return_value = None
            wf.confluence.create_page.return_value = {"id": "PAGE-1"}
            wf.jira = MagicMock()
            wf.jira.upsert_issue.return_value = {
                "action": "created",
                "issue_key": "SQA-101",
            }

            with patch("scripts.wf7_agente_pdf_confluence.ExtractorAuditoriaPdf.extraer") as mock_extraer:
                mock_fila = MagicMock()
                mock_fila.id = "REQ-01"
                mock_fila.metrica = "M1"
                mock_fila.criterio = "C1"
                mock_fila.resultado = "FALLA"
                mock_fila.observacion = "Obs"
                mock_fila.es_defecto = True

                mock_doc = MagicMock()
                mock_doc.nombre = "test"
                mock_doc.pdf_path = str(pdfs_dir / "test.pdf")
                mock_doc.filas_con_defecto.return_value = [mock_fila]
                mock_doc.filas = [mock_fila]
                mock_extraer.return_value = mock_doc

                summary_path_1 = wf.run(directorio_pdfs=pdfs_dir, dry_run=False)
                summary_path_2 = wf.run(directorio_pdfs=pdfs_dir, dry_run=False)

            data1 = json.loads(summary_path_1.read_text(encoding="utf-8"))
            data2 = json.loads(summary_path_2.read_text(encoding="utf-8"))
            self.assertEqual(data1["total_pdfs_processed"], 1)
            self.assertEqual(data2["total_pdfs_processed"], 1)

            calls = wf.jira.upsert_issue.call_args_list
            self.assertEqual(len(calls), 2)
            self.assertEqual(calls[0][1]["external_id"], calls[1][1]["external_id"])

    # ------------------------------------------------------------------
    # Utilidades
    # ------------------------------------------------------------------
    def test_titulo_pagina_desde_pdf(self):
        pdf = Path("/fake/Auditoria_DAS_Test_SQA11.pdf")
        self.assertEqual(
            WF7AgentePdfConfluence._titulo_pagina(pdf),
            "Auditoria_DAS_Test_SQA11",
        )

    def test_slug_pdf_normaliza_correctamente(self):
        self.assertEqual(
            WF7AgentePdfConfluence._slug_pdf("Auditoría DAS"),
            "AUDITORIA_DAS",
        )
        self.assertEqual(
            WF7AgentePdfConfluence._slug_pdf("test-file_v2"),
            "TEST_FILE_V2",
        )


class TestResultadoPdf(unittest.TestCase):
    """Tests para la dataclass ResultadoPdf."""

    def test_to_dict_contiene_todos_los_campos(self):
        r = ResultadoPdf(
            pdf_name="test.pdf",
            pdf_path="/tmp/test.pdf",
            status="success",
            confluence_page_id="123",
            confluence_url="https://wiki.example.com",
            jira_keys=["SQA-1"],
            defect_count=2,
            timestamp="2026-01-01T00:00:00Z",
        )
        d = r.to_dict()
        self.assertEqual(d["pdf_name"], "test.pdf")
        self.assertEqual(d["confluence_page_id"], "123")
        self.assertEqual(d["jira_keys"], ["SQA-1"])
        self.assertEqual(d["defect_count"], 2)


if __name__ == "__main__":
    unittest.main()
