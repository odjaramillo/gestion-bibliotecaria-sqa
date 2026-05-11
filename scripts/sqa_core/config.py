"""Shared configuration loader for SQA scripts."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SQAConfig:
    """Immutable configuration for SQA integrations."""

    jira_server: str
    jira_email: str
    jira_api_token: str
    confluence_url: str
    confluence_user: str
    confluence_token: str
    gemini_api_key: str
    sonarqube_url: str
    sonarqube_token: str
    modo: str
    project_root: Path
    documentacion_dir: Path
    reportes_dir: Path

    @property
    def dry_run(self) -> bool:
        """Modos 'reporte' y 'propuesta' son equivalentes a dry_run=True."""
        return self.modo in ("reporte", "propuesta")


def load_config(required_services: list[str] | None = None) -> SQAConfig:
    """Load and validate SQA configuration from environment variables.

    Args:
        required_services: Lista de servicios requeridos para este workflow.
            Opciones: 'jira', 'confluence', 'gemini', 'sonarqube'.
            Si es None, solo se requiere GEMINI_API_KEY.
    """
    if required_services is None:
        required_services = ["gemini"]

    all_vars: dict[str, str | None] = {
        "JIRA_SERVER": os.getenv("JIRA_SERVER"),
        "JIRA_EMAIL": os.getenv("JIRA_EMAIL"),
        "JIRA_API_TOKEN": os.getenv("JIRA_API_TOKEN"),
        "CONFLUENCE_URL": os.getenv("CONFLUENCE_URL"),
        "CONFLUENCE_USER": os.getenv("CONFLUENCE_USER"),
        "CONFLUENCE_TOKEN": os.getenv("CONFLUENCE_TOKEN"),
        "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
        "SONARQUBE_URL": os.getenv("SONARQUBE_URL"),
        "SONARQUBE_TOKEN": os.getenv("SONARQUBE_TOKEN"),
    }

    # Mapeo de servicio a variables requeridas
    service_vars: dict[str, list[str]] = {
        "jira": ["JIRA_SERVER", "JIRA_EMAIL", "JIRA_API_TOKEN"],
        "confluence": ["CONFLUENCE_URL", "CONFLUENCE_USER", "CONFLUENCE_TOKEN"],
        "gemini": ["GEMINI_API_KEY"],
        "sonarqube": ["SONARQUBE_URL", "SONARQUBE_TOKEN"],
    }

    missing: list[str] = []
    for svc in required_services:
        for var in service_vars.get(svc, []):
            if not all_vars[var]:
                missing.append(var)

    if missing:
        raise EnvironmentError(
            f"Variables de entorno faltantes para {required_services}: {', '.join(sorted(set(missing)))}"
        )

    modo = os.getenv("MODO", "reporte").lower()
    if modo not in ("reporte", "propuesta", "produccion"):
        raise EnvironmentError(
            f"MODO debe ser 'reporte', 'propuesta' o 'produccion', se obtuvo '{modo}'"
        )

    project_root = Path(__file__).resolve().parent.parent.parent
    documentacion_dir = project_root / "documentacion"
    reportes_dir = project_root / "sqa" / "reportes"

    return SQAConfig(
        jira_server=all_vars["JIRA_SERVER"] or "",
        jira_email=all_vars["JIRA_EMAIL"] or "",
        jira_api_token=all_vars["JIRA_API_TOKEN"] or "",
        confluence_url=all_vars["CONFLUENCE_URL"] or "",
        confluence_user=all_vars["CONFLUENCE_USER"] or "",
        confluence_token=all_vars["CONFLUENCE_TOKEN"] or "",
        gemini_api_key=all_vars["GEMINI_API_KEY"] or "",
        sonarqube_url=all_vars["SONARQUBE_URL"] or "",
        sonarqube_token=all_vars["SONARQUBE_TOKEN"] or "",
        modo=modo,
        project_root=project_root,
        documentacion_dir=documentacion_dir,
        reportes_dir=reportes_dir,
    )
