"""Workflow 3: Generacion del Plan de Pruebas (PP+CP).

Lee los resumenes de WF1 y WF2, formula un Plan de Pruebas usando Gemini,
publica el plan en Confluence, crea casos de prueba en Jira,
y genera archivos esqueleto en sqa/test-automation/.
"""
from __future__ import annotations

import json
import logging
import subprocess
import sys
from pathlib import Path
from typing import Any

from scripts.sqa_core.clients import ConfluenceClient, GeminiClient, JiraClient
from scripts.sqa_core.config import SQAConfig, load_config
from scripts.sqa_core.reporting import render_markdown_report, write_summary_json

logger = logging.getLogger("wf3_generacion_pruebas")

TEST_PLAN_PROMPT: str = (
    "Eres un ingeniero SQA experto en planificacion de pruebas. Analiza los hallazgos "
    "de las auditorias anteriores (WF1: Requisitos y WF2: Arquitectura/Codigo) y genera "
    "un Plan de Pruebas con casos de prueba especificos. "
    "Devuelve ESTRICTAMENTE un array JSON con objetos que tengan estos campos: "
    '{"id":"string","type":"Funcional|No Funcional|Integracion|Regresion",'
    '"priority":"Alta|Media|Baja","title":"string","description":"string",'
    '"related_finding":"string"}. '
    "Si no hay hallazgos que requieran casos de prueba, devuelve un array vacio []."
)

CONFLUENCE_SPACE: str = "SQA"
CONFLUENCE_PARENT: str | None = None
JIRA_PROJECT_KEY: str = "SQA"


class WF3GeneracionPruebas:
    """Orquesta la generacion del plan de pruebas y casos de prueba."""

    def __init__(self, config: SQAConfig) -> None:
        self.config = config
        self.gemini = GeminiClient(config)
        self.confluence = ConfluenceClient(config)
        self.jira = JiraClient(config)

    def run(self) -> Path:
        """Ejecuta el flujo completo de WF3."""
        logger.info("=== WF3 Generacion de Pruebas — Inicio ===")

        upstream_data = self._read_upstream_summaries()
        if not upstream_data:
            logger.warning("No se encontraron resumenes de WF1 ni WF2")
            return self._write_summary(
                status="failed",
                artifacts=[],
                page_id=None,
                jira_keys=[],
                findings=[],
            )

        artifact_names = [f"sqa/reportes/{k}_summary.json" for k in upstream_data.keys()]

        try:
            test_cases = self._generate_test_plan(upstream_data)
        except Exception as exc:
            logger.error("Error generando plan de pruebas con Gemini: %s", exc)
            return self._write_summary(
                status="failed",
                artifacts=artifact_names,
                page_id=None,
                jira_keys=[],
                findings=[],
            )

        page_id: str | None = None
        jira_keys: list[str] = []
        pr_success = False

        if not self.config.dry_run:
            page_id = self._publish_test_plan(artifact_names, test_cases)
            jira_keys = self._create_jira_test_cases(test_cases)
        else:
            logger.info("[DRY RUN] Omitiendo creacion en Confluence/Jira")

        try:
            self._create_skeleton_files()
        except Exception as exc:
            logger.error("Error creando archivos esqueleto: %s", exc)

        if not self.config.dry_run:
            try:
                self._create_skeleton_pr()
                pr_success = True
            except Exception as exc:
                logger.error("Error creando PR esqueleto: %s", exc)

        status = self._resolve_status(test_cases, page_id, pr_success)
        return self._write_summary(
            status=status,
            artifacts=artifact_names,
            page_id=page_id,
            jira_keys=jira_keys,
            findings=test_cases,
        )

    def _read_upstream_summaries(self) -> dict[str, dict[str, Any]]:
        """Lee wf1_summary.json y wf2_summary.json si existen."""
        data: dict[str, dict[str, Any]] = {}
        for key in ("wf1", "wf2"):
            path = self.config.reportes_dir / f"{key}_summary.json"
            if path.exists():
                try:
                    with path.open(encoding="utf-8") as f:
                        data[key] = json.load(f)
                    logger.info("Resumen %s cargado: %s", key, path)
                except Exception as exc:
                    logger.warning("Error leyendo %s: %s", path, exc)
        return data

    def _generate_test_plan(
        self, upstream_data: dict[str, dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Envia hallazgos upstream a Gemini y parsea casos de prueba."""
        findings_text = ""
        for key, summary in upstream_data.items():
            findings = summary.get("findings", [])
            findings_text += f"\n--- {key.upper()} Findings ---\n"
            findings_text += json.dumps(findings, ensure_ascii=False)

        prompt = f"{TEST_PLAN_PROMPT}\n\n{findings_text}"
        raw = self.gemini.generate(prompt)
        data = json.loads(raw)
        test_cases: list[dict[str, Any]] = []
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    test_cases.append(item)
        return test_cases

    def _publish_test_plan(
        self,
        artifacts: list[str],
        test_cases: list[dict[str, Any]],
    ) -> str | None:
        """Publica el Plan de Pruebas en Confluence."""
        title = "Plan de Pruebas — Generado por WF3"
        body = render_markdown_report(
            workflow="wf3",
            status="success" if not test_cases else "partial",
            artifacts=artifacts,
            findings=test_cases,
        )
        try:
            existing = self.confluence.get_page_by_title(CONFLUENCE_SPACE, title)
            if existing:
                logger.info("Actualizando pagina existente %s", existing["id"])
                version = existing.get("version", {}).get("number", 1)
                result = self.confluence.update_page(
                    existing["id"], version, title, body
                )
                return result.get("id")
            result = self.confluence.create_page(
                CONFLUENCE_SPACE, CONFLUENCE_PARENT, title, body
            )
            return result.get("id")
        except Exception as exc:
            logger.error("Error publicando en Confluence: %s", exc)
            return None

    def _create_jira_test_cases(self, test_cases: list[dict[str, Any]]) -> list[str]:
        """Crea casos de prueba en Jira para cada item de prioridad Alta/Media."""
        keys: list[str] = []
        for tc in test_cases:
            if tc.get("priority") not in ("Alta", "Media"):
                continue
            summary = f"[WF3] {tc.get('id', 'TC-??')} — {tc.get('title', 'Caso de prueba')}"
            description = (
                f"{tc.get('description', 'Sin descripcion')}\n\n"
                f"Tipo: {tc.get('type', 'N/A')}\n"
                f"Prioridad: {tc.get('priority', 'N/A')}\n"
                f"Hallazgo relacionado: {tc.get('related_finding', 'N/A')}"
            )
            try:
                issue = self.jira.create_issue({
                    "project": {"key": JIRA_PROJECT_KEY},
                    "summary": summary,
                    "description": description,
                    "issuetype": {"name": "Task"},
                })
                keys.append(issue.key)
                logger.info("Caso de prueba creado: %s", issue.key)
            except Exception as exc:
                logger.error("Error creando caso de prueba en Jira: %s", exc)
        return keys

    def _create_skeleton_files(self) -> None:
        """Crea archivos esqueleto de automatizacion en sqa/test-automation/."""
        test_auto_dir = self.config.project_root / "sqa" / "test-automation"
        test_auto_dir.mkdir(parents=True, exist_ok=True)

        readme = test_auto_dir / "README.md"
        if not readme.exists():
            readme.write_text(
                "# Test Automation Suite\n\n"
                "Este directorio contiene la suite de automatizacion de pruebas "
                "generada por el ecosistema SQA (WF3).\n\n"
                "## Estructura\n\n"
                "- `test_backend_api.py` — Pruebas de API del backend Java\n"
                "- `test_frontend_e2e.py` — Pruebas E2E del frontend Vue\n\n"
                "## Instrucciones\n\n"
                "1. Completar los casos de prueba segun el Plan de Pruebas en Confluence\n"
                "2. Ejecutar con `python -m unittest discover -s sqa/test-automation`\n",
                encoding="utf-8",
            )

        backend_test = test_auto_dir / "test_backend_api.py"
        if not backend_test.exists():
            backend_test.write_text(
                '"""Esqueleto de pruebas de API para el backend."""\n'
                "from __future__ import annotations\n\n"
                "import unittest\n"
                "from unittest.mock import patch\n\n"
                "class TestBackendAPI(unittest.TestCase):\n"
                '    """Casos de prueba para la API REST del backend."""\n\n'
                "    def test_example_endpoint_returns_200(self):\n"
                '        """TODO: Implementar segun el Plan de Pruebas WF3."""\n'
                "        pass\n\n"
                "if __name__ == '__main__':\n"
                "    unittest.main()\n",
                encoding="utf-8",
            )

        frontend_test = test_auto_dir / "test_frontend_e2e.py"
        if not frontend_test.exists():
            frontend_test.write_text(
                '"""Esqueleto de pruebas E2E para el frontend."""\n'
                "from __future__ import annotations\n\n"
                "import unittest\n"
                "from unittest.mock import patch\n\n"
                "class TestFrontendE2E(unittest.TestCase):\n"
                '    """Casos de prueba end-to-end para el frontend Vue."""\n\n'
                "    def test_example_page_loads(self):\n"
                '        """TODO: Implementar segun el Plan de Pruebas WF3."""\n'
                "        pass\n\n"
                "if __name__ == '__main__':\n"
                "    unittest.main()\n",
                encoding="utf-8",
            )

        logger.info("Archivos esqueleto creados en %s", test_auto_dir)

    def _create_skeleton_pr(self) -> None:
        """Crea un PR esqueleto usando gh CLI si esta disponible."""
        try:
            result = subprocess.run(
                ["gh", "pr", "create", "--title", "[SQA] Test Automation Skeleton",
                 "--body", "Este PR esqueleto contiene la base de automatizacion de pruebas generada por WF3.",
                 "--base", "main"],
                capture_output=True,
                text=True,
                check=True,
                cwd=str(self.config.project_root),
            )
            logger.info("PR creado: %s", result.stdout.strip())
        except FileNotFoundError:
            logger.warning("gh CLI no esta instalado; omitiendo creacion de PR")
            raise
        except subprocess.CalledProcessError as exc:
            logger.error("Error creando PR con gh: %s", exc.stderr)
            raise

    def _resolve_status(
        self,
        test_cases: list[dict[str, Any]],
        page_id: str | None,
        pr_success: bool,
    ) -> str:
        """Determina el estado final del workflow.

        El estado se basa en los artefactos principales (Confluence/Jira).
        PR exitoso es secundario; su fallo se loguea pero no determina
        el status critico del workflow.
        """
        if not page_id:
            return "failed"
        if not test_cases:
            return "success"
        return "partial"

    def _write_summary(
        self,
        status: str,
        artifacts: list[str],
        page_id: str | None,
        jira_keys: list[str],
        findings: list[dict[str, Any]],
    ) -> Path:
        """Escribe el summary JSON en sqa/reportes/."""
        path = self.config.reportes_dir / "wf3_summary.json"
        return write_summary_json(
            path=path,
            workflow="wf3",
            status=status,
            source_artifacts=artifacts,
            confluence_page_id=page_id,
            jira_keys=jira_keys,
            findings=findings,
        )


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    )
    try:
        config = load_config()
    except EnvironmentError as exc:
        logger.critical("Error de configuracion: %s", exc)
        sys.exit(1)

    wf3 = WF3GeneracionPruebas(config)
    try:
        summary_path = wf3.run()
        print(f"\n[OK] WF3 completado. Summary: {summary_path}")
    except Exception as exc:
        logger.critical("Error fatal en WF3: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
