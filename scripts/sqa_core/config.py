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
    dry_run: bool
    project_root: Path
    documentacion_dir: Path
    reportes_dir: Path


def load_config() -> SQAConfig:
    """Load and validate SQA configuration from environment variables."""
    required: dict[str, str | None] = {
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

    missing = [k for k, v in required.items() if not v]
    if missing:
        raise EnvironmentError(
            f"Variables de entorno faltantes: {', '.join(missing)}"
        )

    dry_run = os.getenv("DRY_RUN", "true").lower() in ("1", "true", "yes", "on")

    project_root = Path(__file__).resolve().parent.parent.parent
    documentacion_dir = project_root / "documentacion"
    reportes_dir = project_root / "sqa" / "reportes"

    return SQAConfig(
        jira_server=required["JIRA_SERVER"],
        jira_email=required["JIRA_EMAIL"],
        jira_api_token=required["JIRA_API_TOKEN"],
        confluence_url=required["CONFLUENCE_URL"],
        confluence_user=required["CONFLUENCE_USER"],
        confluence_token=required["CONFLUENCE_TOKEN"],
        gemini_api_key=required["GEMINI_API_KEY"],
        sonarqube_url=required["SONARQUBE_URL"],
        sonarqube_token=required["SONARQUBE_TOKEN"],
        dry_run=dry_run,
        project_root=project_root,
        documentacion_dir=documentacion_dir,
        reportes_dir=reportes_dir,
    )
