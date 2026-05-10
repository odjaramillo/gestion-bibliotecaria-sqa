"""Markdown and JSON report generation for SQA workflows."""
from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger("sqa_core.reporting")


def render_markdown_report(
    workflow: str,
    status: str,
    artifacts: list[str],
    findings: list[dict[str, Any]],
) -> str:
    """Render a Markdown report for a workflow execution."""
    lines: list[str] = []
    lines.append(f"# Reporte {workflow.upper()}\n")
    lines.append(f"**Estado:** {status}\n")
    lines.append(f"**Fecha:** {datetime.now(timezone.utc).isoformat()}\n")
    lines.append(f"**Artefactos analizados:** {len(artifacts)}\n")
    for art in artifacts:
        lines.append(f"- `{art}`\n")
    lines.append("\n")

    if findings:
        lines.append("## Hallazgos\n")
        lines.append("| ID | Severidad | Tipo | Descripción |\n")
        lines.append("|---|---|---|---|\n")
        for f in findings:
            desc = f.get("description", "").replace("|", "\\|")
            lines.append(
                f"| {f.get('id', 'N/A')} | {f.get('severity', 'N/A')} | "
                f"{f.get('type', 'N/A')} | {desc} |\n"
            )
        lines.append("\n")
    else:
        lines.append("> ✅ No se detectaron defectos.\n\n")

    lines.append("---\n")
    lines.append("*Generado automáticamente por el ecosistema SQA*\n")
    return "".join(lines)


def write_summary_json(
    path: Path,
    workflow: str,
    status: str,
    source_artifacts: list[str],
    confluence_page_id: str | None,
    jira_keys: list[str],
    findings: list[dict[str, Any]],
    visual_findings: list[dict[str, Any]] | None = None,
) -> Path:
    """Write a JSON summary following the SQA artifact contract."""
    path.parent.mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {
        "workflow": workflow,
        "status": status,
        "source_artifacts": source_artifacts,
        "confluence_page_id": confluence_page_id,
        "jira_keys": jira_keys,
        "findings": findings,
        "visual_findings": visual_findings or [],
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.info("Summary JSON escrito: %s", path)
    return path
