"""Workflow 1: Auditoria Estática de Requisitos (BRIEF/ERS).

Extrae texto de PDFs congelados, valida INVEST mediante Gemini,
genera una Matriz de Trazabilidad Inversa en Confluence,
y registra bugs en Jira.
"""
from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import Any

from scripts.sqa_core.clients import ConfluenceClient, GeminiClient, JiraClient
from scripts.sqa_core.config import SQAConfig, load_config
from scripts.sqa_core.pdf_text import chunk_text, extract_text_from_pdf
from scripts.sqa_core.reporting import render_markdown_report, write_summary_json

logger = logging.getLogger("wf1_auditoria_requisitos")

INVEST_PROMPT: str = (
    "Eres un auditor SQA experto en requisitos. Analiza el siguiente texto extraído "
    "de un documento de requisitos (BRIEF o ERS) y evalúa cada requisito bajo los "
    "criterios INVEST (Independent, Negotiable, Valuable, Estimable, Small, Testable). "
    "Devuelve ESTRICTAMENTE un array JSON con objetos que tengan estos campos: "
    '{"id":"string","severity":"Alta|Media|Baja","type":"bug|task",'
    '"description":"string","invest_criteria":"string"}. '
    "Si no hay defectos, devuelve un array vacío []."
)

CONFLUENCE_SPACE: str = "SQA"
CONFLUENCE_PARENT: str | None = None


class WF1AuditoriaRequisitos:
    """Orquesta la auditoría estática de requisitos."""

    def __init__(self, config: SQAConfig) -> None:
        self.config = config
        self.gemini = GeminiClient(config)
        self.confluence = ConfluenceClient(config)
        self.jira = JiraClient(config)

    def run(self) -> Path:
        """Ejecuta el flujo completo de WF1."""
        logger.info("=== WF1 Auditoria de Requisitos — Inicio ===")

        pdfs = self._detect_pdfs()
        if not pdfs:
            logger.warning("No se encontraron PDFs BRIEF/ERS en documentacion/")
            return self._write_summary(
                status="failed",
                artifacts=[],
                page_id=None,
                jira_keys=[],
                findings=[],
            )

        artifacts = [str(p) for p in pdfs]
        all_findings: list[dict[str, Any]] = []

        for pdf in pdfs:
            logger.info("Procesando %s", pdf.name)
            try:
                text = extract_text_from_pdf(pdf)
                chunks = chunk_text(text)
                findings = self._analyze_chunks(chunks, pdf.name)
                all_findings.extend(findings)
            except Exception as exc:
                logger.error("Error procesando %s: %s", pdf.name, exc)
                return self._write_summary(
                    status="failed",
                    artifacts=artifacts,
                    page_id=None,
                    jira_keys=[],
                    findings=[],
                )

        page_id: str | None = None
        jira_keys: list[str] = []

        if not self.config.dry_run:
            page_id = self._publish_matrix(artifacts, all_findings)
            jira_keys = self._create_jira_bugs(all_findings)
        else:
            logger.info("[DRY RUN] Omitiendo creación en Confluence/Jira")

        status = "success" if not all_findings else "partial"
        return self._write_summary(
            status=status,
            artifacts=artifacts,
            page_id=page_id,
            jira_keys=jira_keys,
            findings=all_findings,
        )

    def _detect_pdfs(self) -> list[Path]:
        """Detecta archivos BRIEF y ERS en documentacion/."""
        pdfs: list[Path] = []
        if self.config.documentacion_dir.exists():
            for pdf in sorted(self.config.documentacion_dir.glob("*.pdf")):
                upper = pdf.name.upper()
                if "BRIEF" in upper or "ERS" in upper:
                    pdfs.append(pdf)
        return pdfs

    def _analyze_chunks(self, chunks: list[str], filename: str) -> list[dict[str, Any]]:
        """Envía chunks a Gemini y parsea hallazgos."""
        findings: list[dict[str, Any]] = []
        for idx, chunk in enumerate(chunks):
            prompt = f"{INVEST_PROMPT}\n\nDocumento: {filename} (chunk {idx + 1}/{len(chunks)})\n\n{chunk}"
            try:
                raw = self.gemini.generate(prompt)
                data = json.loads(raw)
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict):
                            findings.append(item)
            except Exception as exc:
                logger.error("Error en análisis Gemini para %s chunk %d: %s", filename, idx, exc)
                raise
        return findings

    def _publish_matrix(
        self,
        artifacts: list[str],
        findings: list[dict[str, Any]],
    ) -> str | None:
        """Publica la Matriz de Trazabilidad Inversa en Confluence."""
        title = f"Matriz de Trazabilidad Inversa — {Path(artifacts[0]).name}"
        body = render_markdown_report(
            workflow="wf1",
            status="success" if not findings else "partial",
            artifacts=artifacts,
            findings=findings,
        )
        try:
            existing = self.confluence.get_page_by_title(CONFLUENCE_SPACE, title)
            if existing:
                logger.info("Actualizando página existente %s", existing["id"])
                version = existing.get("version", {}).get("number", 1)
                result = self.confluence.update_page(
                    existing["id"], version, title, body
                )
                return result.get("id")
            parent = CONFLUENCE_PARENT
            result = self.confluence.create_page(CONFLUENCE_SPACE, parent, title, body)
            return result.get("id")
        except Exception as exc:
            logger.error("Error publicando en Confluence: %s", exc)
            return None

    def _create_jira_bugs(self, findings: list[dict[str, Any]]) -> list[str]:
        """Crea o actualiza bugs en Jira para cada hallazgo de severidad Alta/Media."""
        keys: list[str] = []
        for finding in findings:
            if finding.get("severity") not in ("Alta", "Media"):
                continue
            external_id = f"SQA-WF1-{finding.get('id', 'REQ-??')}"
            summary = f"[WF1] {finding.get('id', 'REQ-??')} — {finding.get('invest_criteria', 'INVEST')}"
            description = (
                f"{finding.get('description', 'Sin descripción')}\n\n"
                f"Criterio INVEST: {finding.get('invest_criteria', 'N/A')}"
            )
            try:
                result = self.jira.upsert_issue(
                    external_id=external_id,
                    fields={
                        "project": {"key": "SQA"},
                        "summary": summary,
                        "description": description,
                        "issuetype": {"name": "Bug"},
                    },
                )
                if result.get("issue_key"):
                    keys.append(result["issue_key"])
            except Exception as exc:
                logger.error("Error creando bug en Jira: %s", exc)
        return keys

    def _write_summary(
        self,
        status: str,
        artifacts: list[str],
        page_id: str | None,
        jira_keys: list[str],
        findings: list[dict[str, Any]],
    ) -> Path:
        """Escribe el summary JSON en sqa/reportes/."""
        path = self.config.reportes_dir / "wf1_summary.json"
        return write_summary_json(
            path=path,
            workflow="wf1",
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
        logger.critical("Error de configuración: %s", exc)
        sys.exit(1)

    wf1 = WF1AuditoriaRequisitos(config)
    try:
        summary_path = wf1.run()
        print(f"\n[OK] WF1 completado. Summary: {summary_path}")
    except Exception as exc:
        logger.critical("Error fatal en WF1: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
