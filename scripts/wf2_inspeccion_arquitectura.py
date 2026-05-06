"""Workflow 2: Inspeccion Arquitectonica y de Codigo (DAS + SonarQube).

Evalua el Documento de Arquitectura de Software (C4) y la calidad del
codigo fuente mediante SonarQube, genera un reporte de Deuda Tecnica
en Confluence, y crea tareas en Jira.
"""
from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import Any

from scripts.sqa_core.clients import ConfluenceClient, GeminiClient, JiraClient, SonarQubeClient
from scripts.sqa_core.config import SQAConfig, load_config
from scripts.sqa_core.image_analysis import DiagramType, ImageAnalyzer
from scripts.sqa_core.pdf_text import extract_images_from_pdf, extract_page_texts_from_pdf, extract_text_from_pdf
from scripts.sqa_core.reporting import render_markdown_report, write_summary_json

logger = logging.getLogger("wf2_inspeccion_arquitectura")

ARCHITECTURE_PROMPT: str = (
    "Eres un arquitecto SQA experto. Analiza el siguiente texto extraido "
    "de un Documento de Arquitectura de Software (DAS) basado en el modelo C4 "
    "y los hallazgos de SonarQube proporcionados. Evalua la consistencia entre "
    "la arquitectura documentada y el codigo real, e identifica deuda tecnica. "
    "Devuelve ESTRICTAMENTE un array JSON con objetos que tengan estos campos: "
    '{"id":"string","severity":"Alta|Media|Baja","type":"task|bug",'
    '"description":"string","component":"string"}. '
    "Si no hay hallazgos, devuelve un array vacio []."
)

CONFLUENCE_SPACE: str = "SQA"
CONFLUENCE_PARENT: str | None = None
SONAR_PROJECT_KEY: str = "gestion-bibliotecaria-sqa"
DAS_TEXT_MAX_LEN: int = 8000
SONAR_ISSUES_MAX_LEN: int = 4000
SONAR_MEASURES_MAX_LEN: int = 2000
SONAR_METRICS: list[str] = [
    "code_smells",
    "bugs",
    "vulnerabilities",
    "coverage",
    "duplicated_lines_density",
]


class WF2InspeccionArquitectura:
    """Orquesta la inspeccion arquitectonica y de codigo."""

    def __init__(self, config: SQAConfig) -> None:
        self.config = config
        self.gemini = GeminiClient(config)
        self.confluence = ConfluenceClient(config)
        self.jira = JiraClient(config)
        self.sonar = SonarQubeClient(config)

    def run(self) -> Path:
        """Ejecuta el flujo completo de WF2."""
        logger.info("=== WF2 Inspeccion Arquitectonica — Inicio ===")

        das_pdf = self._detect_das_pdf()
        if not das_pdf:
            logger.warning("No se encontro PDF DAS en documentacion/")
            return self._write_summary(
                status="failed",
                artifacts=[],
                page_id=None,
                jira_keys=[],
                findings=[],
            )

        artifact = str(das_pdf)

        try:
            das_text = extract_text_from_pdf(das_pdf)
        except Exception as exc:
            logger.error("Error extrayendo texto de DAS: %s", exc)
            return self._write_summary(
                status="failed",
                artifacts=[artifact],
                page_id=None,
                jira_keys=[],
                findings=[],
            )

        sonar_data: dict[str, Any] = {}
        try:
            sonar_data = self._fetch_sonar_data()
        except Exception as exc:
            logger.error("Error conectando con SonarQube: %s", exc)
            return self._write_summary(
                status="failed",
                artifacts=[artifact],
                page_id=None,
                jira_keys=[],
                findings=[],
            )

        try:
            findings = self._analyze_with_gemini(das_text, sonar_data)
        except Exception as exc:
            logger.error("Error en analisis Gemini: %s", exc)
            return self._write_summary(
                status="failed",
                artifacts=[artifact],
                page_id=None,
                jira_keys=[],
                findings=[],
                visual_findings=[],
            )

        visual_inputs = self._collect_visual_inputs(das_pdf, das_text)
        visual_findings: list[dict[str, Any]] = []
        try:
            visual_findings = self._analyze_visuals(visual_inputs)
        except Exception as exc:
            logger.warning("Error en analisis visual (degradacion controlada): %s", exc)

        page_id: str | None = None
        jira_keys: list[str] = []

        if not self.config.dry_run:
            page_id = self._publish_tech_debt_report(artifact, findings)
            jira_keys = self._create_jira_tasks(findings)
        else:
            logger.info("[DRY RUN] Omitiendo creacion en Confluence/Jira")

        has_issues = bool(findings) or bool(visual_findings)
        status = "success" if not has_issues else "partial"
        all_artifacts = [artifact] + [str(img[0]) for img in visual_inputs]

        return self._write_summary(
            status=status,
            artifacts=all_artifacts,
            page_id=page_id,
            jira_keys=jira_keys,
            findings=findings,
            visual_findings=visual_findings,
        )

    def _detect_das_pdf(self) -> Path | None:
        """Detecta el archivo DAS en documentacion/."""
        if self.config.documentacion_dir.exists():
            for pdf in sorted(self.config.documentacion_dir.glob("*.pdf")):
                if "DAS" in pdf.name.upper():
                    return pdf
        return None

    def _fetch_sonar_data(self) -> dict[str, Any]:
        """Recupera issues y medidas desde SonarQube."""
        logger.info("Consultando SonarQube para proyecto %s", SONAR_PROJECT_KEY)
        issues = self.sonar.get_issues(SONAR_PROJECT_KEY)
        measures = self.sonar.get_measures(SONAR_PROJECT_KEY, SONAR_METRICS)
        return {"issues": issues, "measures": measures}

    def _analyze_with_gemini(
        self, das_text: str, sonar_data: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Envia DAS + SonarQube a Gemini y parsea hallazgos."""
        prompt = (
            f"{ARCHITECTURE_PROMPT}\n\n"
            f"--- DAS ---\n{das_text[:DAS_TEXT_MAX_LEN]}\n\n"
            f"--- SonarQube Issues ---\n{json.dumps(sonar_data.get('issues', {}), ensure_ascii=False)[:SONAR_ISSUES_MAX_LEN]}\n\n"
            f"--- SonarQube Measures ---\n{json.dumps(sonar_data.get('measures', {}), ensure_ascii=False)[:SONAR_MEASURES_MAX_LEN]}"
        )
        raw = self.gemini.generate(prompt)
        data = json.loads(raw)
        findings: list[dict[str, Any]] = []
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    findings.append(item)
        return findings

    def _publish_tech_debt_report(
        self,
        artifact: str,
        findings: list[dict[str, Any]],
    ) -> str | None:
        """Publica el Reporte de Deuda Tecnica en Confluence."""
        title = f"Deuda Tecnica — {Path(artifact).name}"
        body = render_markdown_report(
            workflow="wf2",
            status="success" if not findings else "partial",
            artifacts=[artifact],
            findings=findings,
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
            parent = CONFLUENCE_PARENT
            result = self.confluence.create_page(CONFLUENCE_SPACE, parent, title, body)
            return result.get("id")
        except Exception as exc:
            logger.error("Error publicando en Confluence: %s", exc)
            return None

    def _create_jira_tasks(self, findings: list[dict[str, Any]]) -> list[str]:
        """Crea tareas en Jira para cada hallazgo de severidad Alta/Media."""
        keys: list[str] = []
        for finding in findings:
            if finding.get("severity") not in ("Alta", "Media"):
                continue
            summary = f"[WF2] {finding.get('id', 'ARCH-??')} — {finding.get('component', 'Sistema')}"
            description = (
                f"{finding.get('description', 'Sin descripcion')}\n\n"
                f"Componente: {finding.get('component', 'N/A')}"
            )
            try:
                issue = self.jira.create_issue({
                    "project": {"key": "SQA"},
                    "summary": summary,
                    "description": description,
                    "issuetype": {"name": "Task"},
                })
                keys.append(issue.key)
                logger.info("Tarea creada: %s", issue.key)
            except Exception as exc:
                logger.error("Error creando tarea en Jira: %s", exc)
        return keys

    def _collect_visual_inputs(
        self,
        pdf_path: Path,
        das_text: str,
    ) -> list[tuple[Path, DiagramType, str]]:
        """Extrae imágenes del PDF y las clasifica para análisis visual."""
        output_dir = self.config.project_root / "sqa" / "extracted_images"
        try:
            image_paths = extract_images_from_pdf(pdf_path, output_dir)
        except Exception as exc:
            logger.warning("Error extrayendo imágenes de %s: %s", pdf_path, exc)
            return []

        if not image_paths:
            return []

        page_texts = extract_page_texts_from_pdf(pdf_path)
        inputs: list[tuple[Path, DiagramType, str]] = []
        for img_path in image_paths:
            page_num = 0
            parts = img_path.stem.split("_")
            for part in parts:
                if part.startswith("page"):
                    try:
                        page_num = int(part.replace("page", ""))
                    except ValueError:
                        pass
            page_text = page_texts.get(page_num, das_text[:500])
            diagram_type = self._classify_diagram_type(img_path, page_text)
            inputs.append((img_path, diagram_type, das_text[:1000]))
        return inputs

    def _classify_diagram_type(
        self,
        image_path: Path,
        page_text: str,
    ) -> DiagramType:
        """Clasifica el tipo de diagrama por nombre de archivo o texto de página."""
        name = image_path.name.lower()
        text = page_text.lower()
        if "context" in name or "contexto" in text:
            return DiagramType.C4_CONTEXT
        if "container" in name or "contenedor" in text:
            return DiagramType.C4_CONTAINER
        if "component" in name or "componente" in text:
            return DiagramType.C4_COMPONENT
        if "uml" in name or "clase" in text or "class" in text:
            return DiagramType.UML_CLASS
        if "wireframe" in name or "mockup" in text:
            return DiagramType.WIREFRAME
        return DiagramType.UNKNOWN

    def _analyze_visuals(
        self,
        visual_inputs: list[tuple[Path, DiagramType, str]],
    ) -> list[dict[str, Any]]:
        """Ejecuta análisis visual sobre las imágenes extraídas."""
        if not visual_inputs:
            return []

        if self.config.dry_run:
            logger.info("[DRY RUN] Generando hallazgos visuales simulados")
            return self._mock_visual_findings(visual_inputs)

        analyzer = ImageAnalyzer(self.gemini)
        results = analyzer.batch_analyze(visual_inputs)
        findings: list[dict[str, Any]] = []
        for img_path, visual_findings_list in results:
            for vf in visual_findings_list:
                findings.append({
                    "id": vf.id,
                    "diagram_type": vf.diagram_type.value,
                    "description": vf.description,
                    "severity": vf.severity,
                    "page_reference": vf.page_reference,
                    "evidence": vf.evidence,
                    "source_image": str(img_path),
                })
        return findings

    def _mock_visual_findings(
        self,
        visual_inputs: list[tuple[Path, DiagramType, str]],
    ) -> list[dict[str, Any]]:
        """Genera hallazgos visuales determinísticos para modo DRY_RUN."""
        findings: list[dict[str, Any]] = []
        for idx, (img_path, diagram_type, _ctx) in enumerate(visual_inputs, start=1):
            findings.append({
                "id": f"VIS-MOCK-{idx:03d}",
                "diagram_type": diagram_type.value,
                "description": f"[DRY RUN] Hallazgo simulado para {img_path.name}",
                "severity": "Baja",
                "page_reference": str(img_path),
                "evidence": "Generado en modo dry_run",
            })
        return findings

    def _write_summary(
        self,
        status: str,
        artifacts: list[str],
        page_id: str | None,
        jira_keys: list[str],
        findings: list[dict[str, Any]],
        visual_findings: list[dict[str, Any]] | None = None,
    ) -> Path:
        """Escribe el summary JSON en sqa/reportes/."""
        path = self.config.reportes_dir / "wf2_summary.json"
        return write_summary_json(
            path=path,
            workflow="wf2",
            status=status,
            source_artifacts=artifacts,
            confluence_page_id=page_id,
            jira_keys=jira_keys,
            findings=findings,
            visual_findings=visual_findings,
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

    wf2 = WF2InspeccionArquitectura(config)
    try:
        summary_path = wf2.run()
        print(f"\n[OK] WF2 completado. Summary: {summary_path}")
    except Exception as exc:
        logger.critical("Error fatal en WF2: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
