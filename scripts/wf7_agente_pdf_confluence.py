#!/usr/bin/env python3
"""Workflow 7: Agente de Ingesta de PDFs a Confluence — SQA Equipo 11.

Lee archivos PDF de auditoría desde un directorio, extrae tablas de
defectos, genera páginas XHTML en Confluence bajo una jerarquía fija,
crea/actualiza tickets de Jira de forma idempotente, adjunta el PDF
original y genera un resumen JSON.

Compatible con Python 3.10+.
"""
from __future__ import annotations

import logging
import sys
import unicodedata
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from scripts.sqa_core.clients import ConfluenceClient, JiraClient
from scripts.sqa_core.config import SQAConfig, load_config
from scripts.sqa_core.pdf_auditoria import DocumentoAuditoria, ExtractorAuditoriaPdf
from scripts.sqa_core.reporting import escribir_resumen_ingesta_pdf
from scripts.sqa_core.xhtml_confluence import MetadataPagina, RenderizadorXhtmlConfluence

logger = logging.getLogger("wf7_agente_pdf_confluence")

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------
CONFLUENCE_SPACE: str = "SQA"
CONFLUENCE_ROOT_TITLE: str = "Auditorías SQA"
CONFLUENCE_PARENT_TITLE: str = "Ingesta PDFs SQA"


# ---------------------------------------------------------------------------
# Dataclass de resultado por PDF
# ---------------------------------------------------------------------------
@dataclass
class ResultadoPdf:
    """Resultado del procesamiento de un PDF individual."""

    pdf_name: str
    pdf_path: str
    status: str = "pending"
    confluence_page_id: str | None = None
    confluence_url: str | None = None
    jira_keys: list[str] = field(default_factory=list)
    defect_count: int = 0
    error_message: str | None = None
    timestamp: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "pdf_name": self.pdf_name,
            "pdf_path": self.pdf_path,
            "status": self.status,
            "confluence_page_id": self.confluence_page_id,
            "confluence_url": self.confluence_url,
            "jira_keys": self.jira_keys,
            "defect_count": self.defect_count,
            "error_message": self.error_message,
            "timestamp": self.timestamp,
        }


# ---------------------------------------------------------------------------
# Workflow
# ---------------------------------------------------------------------------
class WF7AgentePdfConfluence:
    """Orquesta la ingesta de PDFs de auditoría a Confluence y Jira."""

    def __init__(self, config: SQAConfig) -> None:
        self.config = config
        self.confluence = ConfluenceClient(config)
        self.jira = JiraClient(config)
        self.extractor = ExtractorAuditoriaPdf()
        self.renderer = RenderizadorXhtmlConfluence()

    # ------------------------------------------------------------------
    # Público
    # ------------------------------------------------------------------
    def run(
        self,
        directorio_pdfs: str | Path,
        dry_run: bool = False,
    ) -> Path:
        """Ejecuta el flujo completo de ingesta de PDFs.

        Args:
            directorio_pdfs: Directorio que contiene los PDFs de auditoría.
            dry_run: Si es ``True``, simula sin mutar APIs externas.

        Returns:
            Ruta al archivo JSON de resumen.
        """
        effective_dry_run = dry_run or self.config.dry_run
        if effective_dry_run:
            logger.info("=== WF5 Agente PDF→Confluence — DRY RUN ===")
        else:
            logger.info("=== WF5 Agente PDF→Confluence — PRODUCCIÓN ===")

        dir_path = Path(directorio_pdfs)
        pdfs = self._detectar_pdfs(dir_path)
        if not pdfs:
            logger.warning("No se encontraron PDFs en %s", dir_path)
            resultados: list[dict[str, Any]] = []
            return self._escribir_resumen(resultados)

        # Asegurar jerarquía de páginas en Confluence
        parent_id = self._asegurar_jerarquia(dry_run=effective_dry_run)

        resultados_pdf: list[ResultadoPdf] = []
        for pdf in pdfs:
            resultado = self._procesar_pdf(pdf, parent_id, dry_run=effective_dry_run)
            resultados_pdf.append(resultado)

        resultados = [r.to_dict() for r in resultados_pdf]
        return self._escribir_resumen(resultados)

    # ------------------------------------------------------------------
    # Detección
    # ------------------------------------------------------------------
    def _detectar_pdfs(self, dir_path: Path) -> list[Path]:
        """Detecta archivos PDF ordenados alfabéticamente."""
        if not dir_path.exists():
            logger.warning("Directorio no existe: %s", dir_path)
            return []
        return sorted(dir_path.glob("*.pdf"))

    # ------------------------------------------------------------------
    # Jerarquía Confluence
    # ------------------------------------------------------------------
    def _asegurar_jerarquia(self, dry_run: bool) -> str | None:
        """Asegura que existan la página raíz y la página padre.

        Returns:
            ID de la página padre ("Ingesta PDFs SQA") o ``None`` en dry-run.
        """
        if dry_run:
            logger.info("[DRY RUN] Simulando creación de jerarquía Confluence")
            return None

        root_id = self._asegurar_pagina(
            title=CONFLUENCE_ROOT_TITLE,
            parent_id=None,
        )
        parent_id = self._asegurar_pagina(
            title=CONFLUENCE_PARENT_TITLE,
            parent_id=root_id,
        )
        return parent_id

    def _asegurar_pagina(self, title: str, parent_id: str | None) -> str:
        """Obtiene una página por título o la crea si no existe.

        Returns:
            ID de la página.
        """
        existing = self.confluence.get_page_by_title(CONFLUENCE_SPACE, title)
        if existing:
            logger.info("Página existente '%s': %s", title, existing["id"])
            return existing["id"]

        body = f"<p>Página generada automáticamente por WF5.</p>"
        result = self.confluence.create_page(
            CONFLUENCE_SPACE,
            parent_id,
            title,
            body,
        )
        page_id = result.get("id")
        logger.info("Página creada '%s': %s", title, page_id)
        return page_id

    # ------------------------------------------------------------------
    # Procesamiento individual de PDF
    # ------------------------------------------------------------------
    def _procesar_pdf(
        self,
        pdf: Path,
        parent_id: str | None,
        dry_run: bool,
    ) -> ResultadoPdf:
        """Procesa un único PDF: extrae, renderiza, publica y sincroniza Jira."""
        resultado = ResultadoPdf(
            pdf_name=pdf.name,
            pdf_path=str(pdf),
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

        try:
            logger.info("Procesando PDF: %s", pdf.name)

            # 1. Extraer tablas
            documento = self.extractor.extraer(pdf)
            resultado.defect_count = len(documento.filas_con_defecto())

            # 2. Renderizar XHTML inicial
            xhtml = self.renderer.renderizar(
                documento, jira_server=self.config.jira_server
            )

            # 3. Publicar/actualizar página Confluence
            page_id = self._publicar_pagina(
                pdf, documento, xhtml, parent_id, dry_run
            )
            resultado.confluence_page_id = page_id
            if page_id and self.config.confluence_url:
                resultado.confluence_url = (
                    f"{self.config.confluence_url.rstrip('/')}/"
                    f"pages/viewpage.action?pageId={page_id}"
                )

            if not dry_run and not page_id:
                raise RuntimeError("No se pudo obtener page_id de Confluence")

            # 4. Subir adjunto PDF original
            if page_id and not dry_run:
                self.confluence.upload_attachment(pdf, page_id)
                logger.info("Adjunto subido: %s → %s", pdf.name, page_id)

            # 5. Sincronizar defectos con Jira
            tickets: dict[str, str] = {}
            if not dry_run and page_id:
                tickets = self._sincronizar_jira(documento, page_id, dry_run)
                resultado.jira_keys = list(tickets.values())

            # 6. Re-renderizar con enlaces Jira y actualizar página
            if page_id and tickets and not dry_run:
                xhtml_final = self.renderer.renderizar(
                    documento, tickets=tickets, jira_server=self.config.jira_server
                )
                existing = self.confluence.get_page_by_title(
                    CONFLUENCE_SPACE, self._titulo_pagina(pdf)
                )
                if existing:
                    version = existing.get("version", {}).get("number", 1)
                    self.confluence.update_page(
                        existing["id"],
                        version,
                        self._titulo_pagina(pdf),
                        xhtml_final,
                    )
                    logger.info(
                        "Página actualizada con tickets Jira: %s", page_id
                    )

            resultado.status = "success"
            logger.info("PDF procesado exitosamente: %s", pdf.name)

        except Exception as exc:
            resultado.status = "failed"
            resultado.error_message = str(exc)
            logger.error("Error procesando %s: %s", pdf.name, exc)

        return resultado

    # ------------------------------------------------------------------
    # Publicación Confluence
    # ------------------------------------------------------------------
    def _publicar_pagina(
        self,
        pdf: Path,
        documento: DocumentoAuditoria,
        xhtml: str,
        parent_id: str | None,
        dry_run: bool,
    ) -> str | None:
        """Crea o actualiza la página de Confluence para un PDF.

        Returns:
            ID de la página o ``None``.
        """
        title = self._titulo_pagina(pdf)

        if dry_run:
            logger.info("[DRY RUN] Crearía/actualizaría página '%s'", title)
            return None

        # Validar XHTML antes de enviar
        if not self.renderer.validar_xhtml(xhtml):
            logger.warning("XHTML inválido para %s; enviando de todos modos", pdf.name)

        existing = self.confluence.get_page_by_title(CONFLUENCE_SPACE, title)
        if existing:
            logger.info("Actualizando página existente '%s': %s", title, existing["id"])
            version = existing.get("version", {}).get("number", 1)
            result = self.confluence.update_page(
                existing["id"], version, title, xhtml
            )
            page_id = result.get("id")
            if not page_id:
                raise RuntimeError("Confluence update_page no devolvió page_id")
            return page_id

        result = self.confluence.create_page(
            CONFLUENCE_SPACE, parent_id, title, xhtml
        )
        page_id = result.get("id")
        if not page_id:
            raise RuntimeError("Confluence create_page no devolvió page_id")
        logger.info("Página creada '%s': %s", title, page_id)
        return page_id

    @staticmethod
    def _titulo_pagina(pdf: Path) -> str:
        """Genera el título determinista de la página para un PDF."""
        return pdf.stem

    # ------------------------------------------------------------------
    # Sincronización Jira
    # ------------------------------------------------------------------
    def _sincronizar_jira(
        self,
        documento: DocumentoAuditoria,
        page_id: str,
        dry_run: bool,
    ) -> dict[str, str]:
        """Crea o actualiza tickets de Jira para cada defecto.

        Returns:
            Mapa ``{fila_id: issue_key}``.
        """
        tickets: dict[str, str] = {}
        pdf_slug = self._slug_pdf(documento.nombre)
        confluence_url = f"{self.config.confluence_url.rstrip('/')}/pages/viewpage.action?pageId={page_id}"

        for fila in documento.filas_con_defecto():
            external_id = f"SQA-PDF-{pdf_slug}-{fila.id}"
            summary = f"[PDF] {documento.nombre} — {fila.id}"
            description = (
                f"Métrica: {fila.metrica}\n"
                f"Criterio: {fila.criterio}\n"
                f"Resultado: {fila.resultado}\n"
                f"Observación: {fila.observacion}\n\n"
                f"PDF origen: {documento.pdf_path}\n"
                f"Página Confluence: {confluence_url}"
            )

            result = self.jira.upsert_issue(
                external_id=external_id,
                fields={
                    "project": {"key": "SQA"},
                    "summary": summary,
                    "description": description,
                    "issuetype": {"name": "Bug"},
                },
            )
            action = result.get("action", "error")
            issue_key = result.get("issue_key")

            if action == "error":
                raise RuntimeError(
                    f"Jira upsert_issue devolvió error para {external_id}"
                )
            if issue_key:
                tickets[fila.id] = issue_key
                logger.info(
                    "Jira %s: %s para external_id=%s",
                    action,
                    issue_key,
                    external_id,
                )

        return tickets

    @staticmethod
    def _slug_pdf(nombre: str) -> str:
        """Genera un slug seguro a partir del nombre del PDF."""
        slug = (
            unicodedata.normalize("NFKD", nombre)
            .encode("ASCII", "ignore")
            .decode("ASCII")
        )
        slug = slug.replace(" ", "_").replace("-", "_")
        return slug.upper()

    # ------------------------------------------------------------------
    # Resumen
    # ------------------------------------------------------------------
    def _escribir_resumen(self, resultados: list[dict[str, Any]]) -> Path:
        """Escribe el JSON de resumen en ``sqa/reportes/wf5_summary.json``."""
        output_path = self.config.reportes_dir / "wf7_summary.json"
        return escribir_resumen_ingesta_pdf(resultados, output_path)


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------
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

    project_root = config.project_root
    pdfs_dir = project_root / "sqa" / "pdfs"

    wf7 = WF7AgentePdfConfluence(config)
    try:
        summary_path = wf7.run(directorio_pdfs=pdfs_dir, dry_run=False)
        print(f"\n[OK] WF7 completado. Summary: {summary_path}")
    except Exception as exc:
        logger.critical("Error fatal en WF7: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
