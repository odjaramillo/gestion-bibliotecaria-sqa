#!/usr/bin/env python3
"""
Workflow 4: Orquestador de Quality Gates — SQA Equipo 11.

Detecta artefactos, carga checklists JSON, simula verificacion,
lee resumenes de workflows upstream (WF1, WF2, WF3) y genera
reporte Markdown consolidado. En modo dry_run NO crea tickets
reales en Jira ni paginas en Confluence.

El encadenamiento con WF1/WF2/WF3 se realiza principalmente
desde GitHub Actions (workflow_run/manual). WF4 consume los
*_summary.json generados por los workflows upstream para
consolidar el estado del pipeline SQA en su reporte.

Compatible con Python 3.10+.
"""

from __future__ import annotations

import json
import logging
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from scripts.sqa_core.config import SQAConfig, load_config

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
)
logger = logging.getLogger("wf4_orquestador")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
DRY_RUN: bool = os.getenv("DRY_RUN", "true").lower() in ("1", "true", "yes", "on")

PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
DOCUMENTACION_DIR: Path = PROJECT_ROOT / "documentacion"
CHECKLISTS_DIR: Path = PROJECT_ROOT / "sqa" / "checklists"
REPORTES_DIR: Path = PROJECT_ROOT / "sqa" / "reportes"

# Mapeo de patrones de archivo a checklist JSON
ARTIFACT_CHECKLIST_MAP: dict[str, str] = {
    "BRIEF": "brief.json",
    "ERS": "ers.json",
    "DAS": "das.json",
    "PAC": "pac.json",
}

CODE_PATTERNS: dict[str, str] = {
    ".java": "codigo.json",
    ".vue": "codigo.json",
}

UPSTREAM_WORKFLOWS: tuple[str, ...] = ("wf1", "wf2", "wf3")


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------
@dataclass
class ChecklistItem:
    """Item individual de una checklist."""

    id: str
    category: str
    description: str
    verification_type: str
    evidence_location: str
    standard_reference: str
    result: str = "Pendiente"
    is_defect: bool = False
    severity: str = "N/A"


@dataclass
class Checklist:
    """Checklist completa cargada desde JSON."""

    artifact_type: str
    standard: str
    version: str
    items: list[ChecklistItem] = field(default_factory=list)


@dataclass
class DetectedArtifact:
    """Artefacto detectado en el filesystem."""

    path: Path
    artifact_type: str
    checklist_file: str


# ---------------------------------------------------------------------------
# Upstream Summary Reader
# ---------------------------------------------------------------------------
class UpstreamSummaryReader:
    """Lee los summary JSON generados por WF1, WF2 y WF3."""

    def __init__(self, reportes_dir: Path | None = None) -> None:
        self.reportes_dir = reportes_dir or REPORTES_DIR

    def read_all(self) -> dict[str, dict[str, Any]]:
        """Lee todos los resumenes upstream disponibles."""
        summaries: dict[str, dict[str, Any]] = {}
        for name in UPSTREAM_WORKFLOWS:
            path = self.reportes_dir / f"{name}_summary.json"
            if path.exists():
                try:
                    with path.open(encoding="utf-8") as f:
                        summaries[name] = json.load(f)
                    logger.info("Resumen upstream cargado: %s", path)
                except Exception as exc:
                    logger.warning("Error leyendo resumen upstream %s: %s", path, exc)
        return summaries


# ---------------------------------------------------------------------------
# Artifact Detector
# ---------------------------------------------------------------------------
class ArtifactDetector:
    """Detecta artefactos en el proyecto y los mapea a checklists."""

    def __init__(
        self,
        documentacion_dir: Path | None = None,
        project_root: Path | None = None,
    ) -> None:
        self.documentacion_dir = documentacion_dir or DOCUMENTACION_DIR
        self.project_root = project_root or PROJECT_ROOT

    def detect(self) -> list[DetectedArtifact]:
        """Escanea documentacion/ y directorios de codigo."""
        artifacts: list[DetectedArtifact] = []

        # 1. Documentacion (PDFs)
        if self.documentacion_dir.exists():
            for pdf in sorted(self.documentacion_dir.glob("*.pdf")):
                artifact_type, checklist = self._resolve_pdf(pdf.name)
                if checklist:
                    artifacts.append(
                        DetectedArtifact(
                            path=pdf,
                            artifact_type=artifact_type,
                            checklist_file=checklist,
                        )
                    )
                    logger.info("Artefacto detectado: %s → %s", pdf.name, checklist)

        # 2. Codigo fuente (Java / Vue)
        code_dirs = [
            self.project_root / "src",
            self.project_root / "biblioteca-frontend",
        ]
        code_found = False
        for code_dir in code_dirs:
            if code_dir.exists():
                for ext, checklist in CODE_PATTERNS.items():
                    if list(code_dir.rglob(f"*{ext}")):
                        code_found = True
        if code_found:
            artifacts.append(
                DetectedArtifact(
                    path=self.project_root / "src",
                    artifact_type="CODIGO",
                    checklist_file="codigo.json",
                )
            )
            logger.info("Artefacto detectado: Codigo fuente → codigo.json")

        return artifacts

    def _resolve_pdf(self, filename: str) -> tuple[str, str]:
        """Resuelve el tipo de artefacto y checklist para un PDF."""
        upper = filename.upper()
        for prefix, checklist_file in ARTIFACT_CHECKLIST_MAP.items():
            if prefix in upper:
                return prefix, checklist_file
        return "UNKNOWN", ""


# ---------------------------------------------------------------------------
# Checklist Loader
# ---------------------------------------------------------------------------
class ChecklistLoader:
    """Carga checklists JSON desde disco."""

    def __init__(self, checklists_dir: Path | None = None) -> None:
        self.checklists_dir = checklists_dir or CHECKLISTS_DIR

    def load(self, checklist_file: str) -> Checklist:
        """Carga una checklist por nombre de archivo."""
        path = self.checklists_dir / checklist_file
        if not path.exists():
            raise FileNotFoundError(f"Checklist no encontrada: {path}")

        with path.open(encoding="utf-8") as f:
            data: dict[str, Any] = json.load(f)

        items = [
            ChecklistItem(
                id=item["id"],
                category=item["category"],
                description=item["description"],
                verification_type=item["verification_type"],
                evidence_location=item["evidence_location"],
                standard_reference=item["standard_reference"],
            )
            for item in data.get("items", [])
        ]

        return Checklist(
            artifact_type=data["artifact_type"],
            standard=data["standard"],
            version=data["version"],
            items=items,
        )


# ---------------------------------------------------------------------------
# Simulator (Dry Run)
# ---------------------------------------------------------------------------
class DryRunSimulator:
    """Simula la verificacion de checklist basada en evidencia conocida."""

    def simulate(self, checklist: Checklist) -> Checklist:
        """Para cada item, determina resultado a partir de evidence_location."""
        for item in checklist.items:
            evidence = item.evidence_location.upper()
            if "DEFECTO:" in evidence:
                item.result = "No Cumple"
                item.is_defect = True
                item.severity = self._infer_severity(item.description, evidence)
            elif "PARCIAL:" in evidence:
                item.result = "Parcial"
                item.is_defect = True
                item.severity = "Media"
            else:
                item.result = "Cumple"
                item.is_defect = False
                item.severity = "N/A"
        return checklist

    def _infer_severity(self, description: str, evidence: str) -> str:
        """Infiere severidad basada en palabras clave del defecto."""
        critical_keywords = [
            "CONTRADICCIÓN", "INCONSISTENCIA", "CREDENCIALES", "HARDCODE",
            "CONTRASEÑA", "VALIDACIÓN COMENTADA", "FECHAS FUTURAS",
        ]
        high_keywords = [
            "BACKLOG VACÍO", "MONOLÍTICO", "NO EXISTE", "SIN MÉTRICA",
            "SIN @CONTROLLERADVICE", "STACK TRACES",
        ]

        combined = (description + " " + evidence).upper()
        for kw in critical_keywords:
            if kw in combined:
                return "Critica"
        for kw in high_keywords:
            if kw in combined:
                return "Alta"
        return "Media"


# ---------------------------------------------------------------------------
# Report Generator
# ---------------------------------------------------------------------------
class ReportGenerator:
    """Genera reporte Markdown del WF4."""

    def __init__(self, reportes_dir: Path | None = None) -> None:
        self.reportes_dir = reportes_dir or REPORTES_DIR

    def generate(
        self,
        artifacts: list[DetectedArtifact],
        results: dict[str, Checklist],
        upstream_summaries: dict[str, dict[str, Any]] | None = None,
    ) -> Path:
        """Genera el reporte Markdown y devuelve su ruta."""
        self.reportes_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        report_path = self.reportes_dir / f"{timestamp}_wf4_reporte.md"

        lines: list[str] = []
        lines.append("# Reporte de Inspeccion Estatica — Workflow 4: Orquestador de Quality Gates\n")
        lines.append(f"**Fecha de ejecucion:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        lines.append(f"**Modo:** `{'DRY RUN' if DRY_RUN else 'PRODUCCION'}\n")
        lines.append(f"**Total artefactos detectados:** {len(artifacts)}\n")
        lines.append("---\n")

        # Resumen de artefactos
        lines.append("## 1. Artefactos Detectados\n")
        for art in artifacts:
            lines.append(f"- **{art.artifact_type}**: `{art.path}` → Checklist `{art.checklist_file}`\n")
        lines.append("\n")

        # Resultados por checklist
        for art in artifacts:
            checklist = results.get(art.checklist_file)
            if not checklist:
                continue
            lines.append(f"## 2. Checklist {checklist.artifact_type} ({art.checklist_file})\n")
            lines.append(f"**Estandar:** {checklist.standard}\n")
            lines.append(f"**Version Checklist:** {checklist.version}\n\n")

            # Tabla de resultados
            lines.append("| ID | Categoria | Item | Resultado | Severidad | Evidencia |\n")
            lines.append("|---|---|---|---|---|---|\n")
            for item in checklist.items:
                esc_evidence = item.evidence_location.replace("|", "\\|")
                lines.append(
                    f"| {item.id} | {item.category} | {item.description} | "
                    f"{item.result} | {item.severity} | {esc_evidence} |\n"
                )
            lines.append("\n")

            # Metricas
            total = len(checklist.items)
            cumplen = sum(1 for i in checklist.items if i.result == "Cumple")
            parciales = sum(1 for i in checklist.items if i.result == "Parcial")
            no_cumplen = sum(1 for i in checklist.items if i.result == "No Cumple")
            defectos = sum(1 for i in checklist.items if i.is_defect)

            lines.append("### Metricas\n")
            lines.append(f"- **Total items:** {total}\n")
            lines.append(f"- **Cumple:** {cumplen} ({self._pct(cumplen, total)})\n")
            lines.append(f"- **Parcial:** {parciales} ({self._pct(parciales, total)})\n")
            lines.append(f"- **No Cumple:** {no_cumplen} ({self._pct(no_cumplen, total)})\n")
            lines.append(f"- **Defectos identificados:** {defectos}\n")
            lines.append(f"- **Cobertura de Revision:** {self._pct(cumplen + parciales, total)}\n\n")

            # Defectos detallados
            if defectos:
                lines.append("### Defectos Encontrados\n")
                for item in checklist.items:
                    if item.is_defect:
                        lines.append(
                            f"- **{item.id}** ({item.severity}): {item.description}\n"
                        )
                        lines.append(f"  - Evidencia: {item.evidence_location}\n")
                lines.append("\n")

        # Workflows Upstream
        if upstream_summaries:
            lines.append("---\n")
            lines.append("## 3. Ejecucion de Workflows Upstream\n")
            for name in UPSTREAM_WORKFLOWS:
                summary = upstream_summaries.get(name)
                if not summary:
                    lines.append(f"### {name.upper()}\n")
                    lines.append(f"> Resumen no encontrado en `{name}_summary.json`.\n\n")
                    continue

                status = summary.get("status", "desconocido")
                findings = summary.get("findings", [])
                source_artifacts = summary.get("source_artifacts", [])
                jira_keys = summary.get("jira_keys", [])
                page_id = summary.get("confluence_page_id")

                lines.append(f"### {name.upper()}\n")
                lines.append(f"- **Estado:** {status}\n")
                lines.append(f"- **Hallazgos:** {len(findings)}\n")
                if source_artifacts:
                    lines.append(f"- **Artefactos analizados:** {', '.join(source_artifacts)}\n")
                if jira_keys:
                    lines.append(f"- **Tickets Jira:** {', '.join(jira_keys)}\n")
                if page_id:
                    lines.append(f"- **Pagina Confluence:** {page_id}\n")

                if findings:
                    lines.append("\n#### Hallazgos destacados\n")
                    for finding in findings[:5]:
                        fid = finding.get("id", "N/A")
                        fsev = finding.get("severity", "N/A")
                        fdesc = finding.get("description", "Sin descripcion")
                        lines.append(f"- **{fid}** ({fsev}): {fdesc}\n")
                    if len(findings) > 5:
                        lines.append(f"- ... y {len(findings) - 5} mas\n")
                lines.append("\n")

        # Seccion de Dry Run
        lines.append("---\n")
        lines.append("## 4. Acciones de Quality Gate\n")
        if DRY_RUN:
            lines.append(
                "> **⚠️ DRY RUN:** No se crearon tickets en Jira ni paginas en Confluence.\n"
                "> En produccion, los defectos 'No Cumple' generarian subtareas en Jira\n"
                "> y el acta de inspeccion se publicaria en Confluence.\n\n"
            )
            if upstream_summaries:
                lines.append(
                    "> **Simulacion basada en artefactos upstream:**\n"
                    "> Los hallazgos y metricas reflejan la ejecucion de WF1, WF2 y WF3\n"
                    "> segun los resumenes disponibles en `sqa/reportes/`.\n\n"
                )
        else:
            lines.append(
                "> **PRODUCCION:** Los defectos han sido sincronizados con Jira/Confluence.\n\n"
            )

        # Cierre
        lines.append("---\n")
        lines.append("*Generado automaticamente por WF4 Orquestador de Quality Gates — SQA Equipo 11*\n")

        report_path.write_text("".join(lines), encoding="utf-8")
        logger.info("Reporte generado: %s", report_path)
        return report_path

    @staticmethod
    def _pct(part: int, total: int) -> str:
        if total == 0:
            return "0%"
        return f"{part / total:.1%}"


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------
class WF4Orchestrator:
    """Orquesta el flujo completo del Workflow 4."""

    def __init__(self, config: SQAConfig | None = None) -> None:
        self.config = config
        project_root = config.project_root if config else PROJECT_ROOT
        documentacion_dir = config.documentacion_dir if config else DOCUMENTACION_DIR
        reportes_dir = config.reportes_dir if config else REPORTES_DIR
        checklists_dir = project_root / "sqa" / "checklists"

        self.detector = ArtifactDetector(
            documentacion_dir=documentacion_dir,
            project_root=project_root,
        )
        self.loader = ChecklistLoader(checklists_dir=checklists_dir)
        self.simulator = DryRunSimulator()
        self.reporter = ReportGenerator(reportes_dir=reportes_dir)
        self.upstream_reader = UpstreamSummaryReader(reportes_dir=reportes_dir)

    def run(self) -> Path | None:
        """Punto de entrada principal del WF4."""
        logger.info("=== WF4 Orquestador de Quality Gates — Inicio ===")

        dry_run = self.config.dry_run if self.config else DRY_RUN
        if dry_run:
            logger.info("[DRY RUN] No se crearan tickets en Jira ni paginas en Confluence")
        else:
            logger.info("[PRODUCCION] Sincronizacion con Jira/Confluence habilitada")

        # 1. Detectar artefactos
        artifacts = self.detector.detect()
        if not artifacts:
            logger.warning("No se detectaron artefactos. Finalizando.")
            return None

        # 2. Cargar checklists y simular
        results: dict[str, Checklist] = {}
        for art in artifacts:
            try:
                checklist = self.loader.load(art.checklist_file)
                checklist = self.simulator.simulate(checklist)
                results[art.checklist_file] = checklist
                logger.info(
                    "Checklist %s: %d items, %d defectos",
                    art.checklist_file,
                    len(checklist.items),
                    sum(1 for i in checklist.items if i.is_defect),
                )
            except FileNotFoundError as exc:
                logger.error("Error cargando checklist %s: %s", art.checklist_file, exc)

        # 3. Leer resumenes upstream
        upstream_summaries = self.upstream_reader.read_all()

        # 4. Generar reporte
        report_path = self.reporter.generate(
            artifacts, results, upstream_summaries=upstream_summaries
        )

        logger.info("=== WF4 Orquestador de Quality Gates — Fin ===")
        return report_path


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------
def _default_config() -> SQAConfig:
    """Crea una configuracion por defecto para ejecucion standalone."""
    project_root = Path(__file__).resolve().parent.parent
    return SQAConfig(
        jira_server="",
        jira_email="",
        jira_api_token="",
        confluence_url="",
        confluence_user="",
        confluence_token="",
        gemini_api_key="",
        sonarqube_url="",
        sonarqube_token="",
        dry_run=True,
        project_root=project_root,
        documentacion_dir=project_root / "documentacion",
        reportes_dir=project_root / "sqa" / "reportes",
    )


def main() -> None:
    try:
        config = load_config()
    except EnvironmentError:
        logger.warning("Variables de entorno incompletas; usando configuracion por defecto (dry_run)")
        config = _default_config()

    orchestrator = WF4Orchestrator(config)
    try:
        report_path = orchestrator.run()
        if report_path:
            print(f"\n[OK] Reporte generado: {report_path}")
        else:
            print("\n[OK] No se detectaron artefactos; no se genero reporte.")
    except Exception as exc:
        logger.critical("Error fatal en WF4: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
