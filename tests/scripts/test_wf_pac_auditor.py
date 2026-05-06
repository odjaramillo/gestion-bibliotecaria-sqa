"""Tests for scripts.wf_pac_auditor module."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from scripts.wf_pac_auditor import (
    CRITICAL_ITEMS,
    ITEM_TO_SECTION,
    _audit,
    _parse_args,
    _parse_sections,
    _validate_section,
    main,
)


def _make_complete_pac() -> str:
    """Genera un PAC completo con todas las secciones válidas."""
    return (
        "## 1. Alcance y Propósito\n\n"
        "Este es el alcance del proyecto. Tiene suficiente contenido para ser válido y aprobado.\n"
        "\n"
        "## 2. Stack Tecnológico\n\n"
        "Backend: Java 21, Spring Boot 3.4.5. Frontend: Vue 3.2.13 con npm y webpack.\n"
        "\n"
        "## 3. Inventario de Artefactos\n\n"
        "Documentación: 2 PDFs. Código fuente: 10 archivos Java, 5 archivos Vue.\n"
        "\n"
        "## 4. Objetivos de Calidad\n\n"
        "Funcionalidad: 40, Fiabilidad: 30, Usabilidad: 30. Diferenciados de proceso.\n"
        "\n"
        "## 5. Gestión y Organización\n\n"
        "Roles: Alberto (Responsable), Oscar (Tecnología), Daniel (Funcional), Edwin (Métricas).\n"
        "\n"
        "## 6. Estándares Aplicables\n\n"
        "IEEE 730-2014, ISO/IEC 25010, ISO 12207, ISO/IEC 29148, ISO/IEC 42010.\n"
        "\n"
        "## 7. Herramientas Tecnológicas\n\n"
        "Ver matriz completa en sqa/PACS-Fase2-Herramientas.md con todas las fases.\n"
        "\n"
        "## 8. Métricas\n\n"
        "Densidad de Defectos = Defectos / Tamaño (KLOC). Cobertura de Revisiones al 100%.\n"
        "\n"
        "## 9. Análisis de Riesgos\n\n"
        "Riesgo de retraso en entregables: mitigación con checkpoints semanales.\n"
        "\n"
        "## 10. Cronograma\n\n"
        "Fase 1: 2026-05-01 a 2026-05-15. Fase 2: Pruebas Dinámicas con iteraciones.\n"
        "\n"
        "## 11. Gestión de Defectos\n\n"
        "Los defectos se gestionan mediante tickets en Jira con workflow de resolución.\n"
        "\n"
        "## 12. CI/CD\n\n"
        "Workflows de GitHub Actions: build.yml, test.yml, deploy.yml configurados.\n"
    )


def _make_checklist() -> dict:
    """Genera un checklist mínimo con los 15 ítems PAC."""
    return {
        "artifact_type": "PAC",
        "standard": "IEEE 730-2014",
        "version": "1.0",
        "items": [
            {"id": "PAC-01", "category": "Objetivos de Calidad (ISO/IEC 25010)"},
            {"id": "PAC-02", "category": "Objetivos de Calidad (ISO/IEC 25010)"},
            {"id": "PAC-03", "category": "Objetivos de Calidad (ISO/IEC 25010)"},
            {"id": "PAC-04", "category": "Gestión y Organización"},
            {"id": "PAC-05", "category": "Gestión y Organización"},
            {"id": "PAC-06", "category": "Gestión y Organización"},
            {"id": "PAC-07", "category": "Documentación, Estándares y Guías"},
            {"id": "PAC-08", "category": "Documentación, Estándares y Guías"},
            {"id": "PAC-09", "category": "Documentación, Estándares y Guías"},
            {"id": "PAC-10", "category": "Métricas y Control Estadístico"},
            {"id": "PAC-11", "category": "Métricas y Control Estadístico"},
            {"id": "PAC-12", "category": "Métricas y Control Estadístico"},
            {"id": "PAC-13", "category": "Ejecución y Cronograma"},
            {"id": "PAC-14", "category": "Ejecución y Cronograma"},
            {"id": "PAC-15", "category": "Ejecución y Cronograma"},
        ],
    }


class TestPACAuditor(unittest.TestCase):
    """Tests for PAC Auditor workflow."""

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.pac_path = Path(self.tmpdir.name) / "pac.md"
        self.checklist_path = Path(self.tmpdir.name) / "checklist.json"
        self.output_path = Path(self.tmpdir.name) / "report.json"

    def tearDown(self):
        self.tmpdir.cleanup()

    def _write_pac(self, content: str):
        self.pac_path.write_text(content, encoding="utf-8")

    def _write_checklist(self, data: dict):
        self.checklist_path.write_text(json.dumps(data), encoding="utf-8")

    def test_audit_complete_pac(self):
        """PAC completo → todos los ítems aprobados, estado APROBADO, código 0."""
        self._write_pac(_make_complete_pac())
        self._write_checklist(_make_checklist())
        report, exit_code = _audit(self.pac_path, self.checklist_path)

        self.assertEqual(report["estado"], "APROBADO")
        self.assertEqual(exit_code, 0)
        self.assertEqual(report["total_items"], 15)
        self.assertEqual(report["items_aprobados"], 15)
        self.assertEqual(report["items_pendientes"], 0)
        self.assertEqual(report["hallazgos"], [])
        self.assertEqual(report["cobertura"], "100.0%")
        self.assertEqual(
            report["secciones_completadas"],
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
        )
        self.assertEqual(report["secciones_pendientes"], [])

    def test_audit_missing_section(self):
        """Falta la sección 4 → PAC-01/02/03 pendientes."""
        pac = _make_complete_pac()
        pac = pac.replace(
            "## 4. Objetivos de Calidad\n\n"
            "Funcionalidad: 40, Fiabilidad: 30, Usabilidad: 30. Diferenciados de proceso.\n",
            "",
        )
        self._write_pac(pac)
        self._write_checklist(_make_checklist())
        report, exit_code = _audit(self.pac_path, self.checklist_path)

        pending_ids = {h["id"] for h in report["hallazgos"]}
        self.assertIn("PAC-01", pending_ids)
        self.assertIn("PAC-02", pending_ids)
        self.assertIn("PAC-03", pending_ids)
        self.assertIn(exit_code, {1, 2})

    def test_audit_placeholder(self):
        """Sección 5 contiene placeholder → PAC-04 pendiente."""
        pac = _make_complete_pac()
        pac = pac.replace(
            "## 5. Gestión y Organización\n\n"
            "Roles: Alberto (Responsable), Oscar (Tecnología), Daniel (Funcional), Edwin (Métricas).\n",
            "## 5. Gestión y Organización\n\n"
            "Roles: [COMPLETAR: definir roles con el líder del proyecto SQA]\n",
        )
        self._write_pac(pac)
        self._write_checklist(_make_checklist())
        report, exit_code = _audit(self.pac_path, self.checklist_path)

        pending_ids = {h["id"] for h in report["hallazgos"]}
        self.assertIn("PAC-04", pending_ids)

        pac04 = next(h for h in report["hallazgos"] if h["id"] == "PAC-04")
        self.assertIn("placeholder", pac04["motivo"].lower())

    def test_audit_empty_section(self):
        """Sección 5 con contenido insuficiente → al menos un ítem pendiente."""
        pac = _make_complete_pac()
        pac = pac.replace(
            "## 5. Gestión y Organización\n\n"
            "Roles: Alberto (Responsable), Oscar (Tecnología), Daniel (Funcional), Edwin (Métricas).\n",
            "## 5. Gestión y Organización\n\nok\n",
        )
        self._write_pac(pac)
        self._write_checklist(_make_checklist())
        report, exit_code = _audit(self.pac_path, self.checklist_path)

        pending_ids = {h["id"] for h in report["hallazgos"]}
        self.assertTrue(
            {"PAC-04", "PAC-05", "PAC-06"} & pending_ids,
            "Al menos un ítem de la sección 5 debe estar pendiente por contenido insuficiente",
        )

    def test_audit_critical_gap(self):
        """Falta PAC-01 (sección 4) → estado RECHAZADO, código 2, severidad Alta."""
        pac = _make_complete_pac()
        pac = pac.replace(
            "## 4. Objetivos de Calidad\n\n"
            "Funcionalidad: 40, Fiabilidad: 30, Usabilidad: 30. Diferenciados de proceso.\n",
            "",
        )
        self._write_pac(pac)
        self._write_checklist(_make_checklist())
        report, exit_code = _audit(self.pac_path, self.checklist_path)

        self.assertEqual(report["estado"], "RECHAZADO")
        self.assertEqual(exit_code, 2)

        pac01 = next((h for h in report["hallazgos"] if h["id"] == "PAC-01"), None)
        self.assertIsNotNone(pac01)
        self.assertEqual(pac01["severidad"], "Alta")

    def test_audit_report_format(self):
        """El reporte JSON cumple el contrato exacto de campos y tipos."""
        self._write_pac(_make_complete_pac())
        self._write_checklist(_make_checklist())
        report, _ = _audit(self.pac_path, self.checklist_path)

        required_keys = {
            "workflow",
            "fecha_ejecucion",
            "estado",
            "archivo_pac",
            "total_items",
            "items_aprobados",
            "items_pendientes",
            "cobertura",
            "hallazgos",
            "secciones_completadas",
            "secciones_pendientes",
        }
        self.assertEqual(set(report.keys()), required_keys)
        self.assertIsInstance(report["workflow"], str)
        self.assertIsInstance(report["fecha_ejecucion"], str)
        self.assertIsInstance(report["estado"], str)
        self.assertIsInstance(report["archivo_pac"], str)
        self.assertIsInstance(report["total_items"], int)
        self.assertIsInstance(report["items_aprobados"], int)
        self.assertIsInstance(report["items_pendientes"], int)
        self.assertIsInstance(report["cobertura"], str)
        self.assertIsInstance(report["hallazgos"], list)
        self.assertIsInstance(report["secciones_completadas"], list)
        self.assertIsInstance(report["secciones_pendientes"], list)

        for h in report["hallazgos"]:
            self.assertIn("id", h)
            self.assertIn("categoria", h)
            self.assertIn("estado", h)
            self.assertIn("motivo", h)
            self.assertIn("severidad", h)
            self.assertIsInstance(h["id"], str)
            self.assertIsInstance(h["categoria"], str)
            self.assertIsInstance(h["estado"], str)
            self.assertIsInstance(h["motivo"], str)
            self.assertIsInstance(h["severidad"], str)

    def test_audit_idempotence(self):
        """Dos ejecuciones sobre el mismo PAC producen resultados idénticos."""
        self._write_pac(_make_complete_pac())
        self._write_checklist(_make_checklist())
        report1, exit_code1 = _audit(self.pac_path, self.checklist_path)
        report2, exit_code2 = _audit(self.pac_path, self.checklist_path)

        self.assertEqual(exit_code1, exit_code2)
        r1 = {k: v for k, v in report1.items() if k != "fecha_ejecucion"}
        r2 = {k: v for k, v in report2.items() if k != "fecha_ejecucion"}
        self.assertEqual(r1, r2)

    def test_audit_cli_args(self):
        """Los argumentos de línea de comandos se parsean y aplican correctamente."""
        # Defaults
        args = _parse_args([])
        self.assertEqual(args.pac, "sqa/pac_generado.md")
        self.assertEqual(args.checklist, "sqa/checklists/pac.json")
        self.assertEqual(args.output, "sqa/reportes/wf_pac_audit.json")
        self.assertFalse(args.verbose)

        # Custom values
        args = _parse_args(
            [
                "--pac",
                "/tmp/pac.md",
                "--checklist",
                "/tmp/check.json",
                "--output",
                "/tmp/out.json",
                "--verbose",
            ]
        )
        self.assertEqual(args.pac, "/tmp/pac.md")
        self.assertEqual(args.checklist, "/tmp/check.json")
        self.assertEqual(args.output, "/tmp/out.json")
        self.assertTrue(args.verbose)

        # End-to-end via main()
        self._write_pac(_make_complete_pac())
        self._write_checklist(_make_checklist())

        captured = StringIO()
        with patch("sys.stdout", new=captured):
            exit_code = main(
                [
                    "--pac",
                    str(self.pac_path),
                    "--checklist",
                    str(self.checklist_path),
                    "--output",
                    str(self.output_path),
                    "--verbose",
                ]
            )

        self.assertEqual(exit_code, 0)
        self.assertTrue(self.output_path.exists())
        report = json.loads(self.output_path.read_text(encoding="utf-8"))
        self.assertEqual(report["estado"], "APROBADO")
        self.assertIn("Auditoría PAC", captured.getvalue())


class TestParseSections(unittest.TestCase):
    """Unit tests for _parse_sections helper."""

    def test_parse_single_section(self):
        content = "## 1. Title\n\nBody text here.\n"
        sections = _parse_sections(content)
        self.assertEqual(sections, {"1": "Body text here."})

    def test_parse_multiple_sections(self):
        content = "## 1. First\n\nFirst body.\n\n## 2. Second\n\nSecond body.\n"
        sections = _parse_sections(content)
        self.assertEqual(sections, {"1": "First body.", "2": "Second body."})

    def test_parse_with_subheadings(self):
        content = (
            "## 1. Title\n\n"
            "Text.\n\n"
            "### Sub\n\n"
            "More.\n\n"
            "## 2. Next\n\n"
            "Done.\n"
        )
        sections = _parse_sections(content)
        self.assertEqual(sections["1"], "Text.\n\n### Sub\n\nMore.")
        self.assertEqual(sections["2"], "Done.")


class TestValidateSection(unittest.TestCase):
    """Unit tests for _validate_section helper."""

    def test_valid_section(self):
        valid, reason = _validate_section(
            "This is more than fifty characters of content in the section body."
        )
        self.assertTrue(valid)
        self.assertIsNone(reason)

    def test_empty_section(self):
        valid, reason = _validate_section("")
        self.assertFalse(valid)
        self.assertIn("vacía", reason.lower())

    def test_short_section(self):
        valid, reason = _validate_section("Too short")
        self.assertFalse(valid)
        self.assertIn("insuficiente", reason.lower())

    def test_placeholder_section(self):
        valid, reason = _validate_section(
            "Some text [COMPLETAR: fill this] more text"
        )
        self.assertFalse(valid)
        self.assertIn("placeholder", reason.lower())
        self.assertIn("[COMPLETAR: fill this]", reason)


if __name__ == "__main__":
    unittest.main()
