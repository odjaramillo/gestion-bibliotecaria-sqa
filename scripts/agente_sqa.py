"""
Agente de Auditoría Estática SQA — CMMI Nivel 5.

Evalúa requisitos en Jira bajo ISO/IEC/IEEE 29148 utilizando
Google Gemini como motor de inferencia y ejecuta transiciones
automáticas según el resultado de la evaluación.
"""

from __future__ import annotations

import json
import logging
import os
import sys
from dataclasses import dataclass
from typing import Any

import google.generativeai as genai
from jira import JIRA, Issue

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
)
logger = logging.getLogger("agente_sqa")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
JQL_QUERY: str = 'project = "BIB" AND status = "En Auditoría SQA"'

GEMINI_MODEL: str = "gemini-3.1-flash-lite-preview"

SQA_PROMPT: str = (
    "Eres un Auditor Estático SQA. Evalúa este requisito bajo ISO/IEC/IEEE 29148. "
    "Criterios: 1. No Ambigüedad. 2. Completitud. 3. Exhaustividad. "
    'Devuelve ESTRICTAMENTE JSON: '
    '{"aprobado": false, "dimension_defecto": "Ambigüedad", '
    '"hallazgo_estructurado": "[Observación]: <falla> -> '
    "[Justificación ISO 29148]: <norma> -> "
    '[Acción Correctiva]: <solución>"}. '
    'Si está perfecto, devuelve "aprobado": true.'
)

TRANSITION_READY_FOR_DEV: str = "Ready for Dev"
TRANSITION_REFINEMENT: str = "Refinement"


# ---------------------------------------------------------------------------
# Value Objects
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class AuditResult:
    """Resultado inmutable de la evaluación Gemini."""

    aprobado: bool
    dimension_defecto: str
    hallazgo_estructurado: str


@dataclass(frozen=True)
class JiraConfig:
    """Configuración de conexión a Jira."""

    server: str
    email: str
    api_token: str


@dataclass(frozen=True)
class GeminiConfig:
    """Configuración de conexión a Gemini."""

    api_key: str
    model: str = GEMINI_MODEL


# ---------------------------------------------------------------------------
# Environment Loader
# ---------------------------------------------------------------------------
class EnvironmentLoader:
    """Carga y valida variables de entorno requeridas (Zero-Trust)."""

    @staticmethod
    def load_jira_config() -> JiraConfig:
        server: str | None = os.getenv("JIRA_SERVER")
        email: str | None = os.getenv("JIRA_EMAIL")
        api_token: str | None = os.getenv("JIRA_API_TOKEN")

        missing: list[str] = []
        if not server:
            missing.append("JIRA_SERVER")
        if not email:
            missing.append("JIRA_EMAIL")
        if not api_token:
            missing.append("JIRA_API_TOKEN")

        if missing:
            raise EnvironmentError(
                f"Variables de entorno faltantes: {', '.join(missing)}"
            )

        return JiraConfig(server=server, email=email, api_token=api_token)  # type: ignore[arg-type]

    @staticmethod
    def load_gemini_config() -> GeminiConfig:
        api_key: str | None = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise EnvironmentError("Variable de entorno faltante: GEMINI_API_KEY")
        return GeminiConfig(api_key=api_key)


# ---------------------------------------------------------------------------
# Jira Gateway
# ---------------------------------------------------------------------------
class JiraGateway:
    """Encapsula todas las interacciones con la API de Jira."""

    def __init__(self, config: JiraConfig) -> None:
        self._client: JIRA = JIRA(
            server=config.server,
            basic_auth=(config.email, config.api_token),
        )

    def fetch_issues(self, jql: str) -> list[Issue]:
        """Ejecuta una consulta JQL y devuelve los issues encontrados."""
        try:
            issues: list[Issue] = self._client.search_issues(jql, maxResults=100)  # type: ignore[assignment]
            logger.info("Se encontraron %d issue(s) en auditoría.", len(issues))
            return issues
        except Exception as exc:
            logger.error("Error al consultar Jira: %s", exc)
            raise

    def transition_issue(self, issue: Issue, transition_name: str) -> None:
        """Ejecuta una transición de estado sobre un issue."""
        try:
            transitions: list[dict[str, Any]] = self._client.transitions(issue)
            target = next(
                (t for t in transitions if t["name"] == transition_name), None
            )
            if target is None:
                logger.warning(
                    "[%s] Transición '%s' no disponible. Transiciones válidas: %s",
                    issue.key,
                    transition_name,
                    [t["name"] for t in transitions],
                )
                return
            self._client.transition_issue(issue, target["id"])
            logger.info(
                "[%s] Transición ejecutada: '%s'.", issue.key, transition_name
            )
        except Exception as exc:
            logger.error(
                "[%s] Error en transición '%s': %s", issue.key, transition_name, exc
            )
            raise

    def add_comment(self, issue: Issue, body: str) -> None:
        """Agrega un comentario a un issue."""
        try:
            self._client.add_comment(issue, body)
            logger.info("[%s] Comentario agregado.", issue.key)
        except Exception as exc:
            logger.error("[%s] Error al agregar comentario: %s", issue.key, exc)
            raise


# ---------------------------------------------------------------------------
# Gemini Evaluator
# ---------------------------------------------------------------------------
class GeminiEvaluator:
    """Evalúa requisitos utilizando Google Gemini."""

    def __init__(self, config: GeminiConfig) -> None:
        genai.configure(api_key=config.api_key)
        self._model = genai.GenerativeModel(
            model_name=config.model,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
            ),
        )

    def evaluate(self, requirement_text: str) -> AuditResult:
        """Envía el requisito a Gemini y parsea la respuesta JSON."""
        prompt: str = f"{SQA_PROMPT}\n\nRequisito a evaluar:\n{requirement_text}"

        try:
            response = self._model.generate_content(prompt)
            raw: str = response.text
        except Exception as exc:
            logger.error("Error en llamada a Gemini: %s", exc)
            raise

        try:
            data: dict[str, Any] = json.loads(raw)
        except json.JSONDecodeError as exc:
            logger.error("Respuesta de Gemini no es JSON válido: %s", raw)
            raise ValueError(f"JSON inválido de Gemini: {raw}") from exc

        return AuditResult(
            aprobado=bool(data.get("aprobado", False)),
            dimension_defecto=str(data.get("dimension_defecto", "")),
            hallazgo_estructurado=str(data.get("hallazgo_estructurado", "")),
        )


# ---------------------------------------------------------------------------
# SQA Orchestrator
# ---------------------------------------------------------------------------
class SQAOrchestrator:
    """Orquesta el flujo completo de auditoría estática."""

    def __init__(self, jira: JiraGateway, evaluator: GeminiEvaluator) -> None:
        self._jira = jira
        self._evaluator = evaluator

    def run(self) -> None:
        """Punto de entrada principal del agente."""
        issues: list[Issue] = self._jira.fetch_issues(JQL_QUERY)

        if not issues:
            logger.info("No hay issues pendientes de auditoría. Finalizando.")
            return

        for issue in issues:
            self._process_issue(issue)

        logger.info("Auditoría completada para %d issue(s).", len(issues))

    def _process_issue(self, issue: Issue) -> None:
        """Procesa un issue individual: evalúa y ejecuta la transición."""
        key: str = issue.key
        description: str = issue.fields.description or ""

        if not description.strip():
            logger.warning("[%s] Descripción vacía. Se omite la evaluación.", key)
            self._jira.add_comment(
                issue,
                "⚠️ *Auditoría SQA*: El requisito no tiene descripción. "
                "Se requiere contenido para evaluar.",
            )
            self._jira.transition_issue(issue, TRANSITION_REFINEMENT)
            return

        logger.info("[%s] Evaluando requisito…", key)

        try:
            result: AuditResult = self._evaluator.evaluate(description)
        except Exception as exc:
            logger.error("[%s] Fallo en evaluación: %s", key, exc)
            return

        if result.aprobado:
            self._handle_approval(issue)
        else:
            self._handle_rejection(issue, result)

    def _handle_approval(self, issue: Issue) -> None:
        """Maneja un requisito aprobado."""
        comment: str = (
            "✅ *Auditoría SQA Aprobada*\n\n"
            "El requisito cumple con los criterios de calidad "
            "ISO/IEC/IEEE 29148:\n"
            "- No Ambigüedad ✔\n"
            "- Completitud ✔\n"
            "- Exhaustividad ✔\n\n"
            "_Transición automática a Ready for Dev._"
        )
        self._jira.add_comment(issue, comment)
        self._jira.transition_issue(issue, TRANSITION_READY_FOR_DEV)
        logger.info("[%s] ✅ Requisito aprobado.", issue.key)

    def _handle_rejection(self, issue: Issue, result: AuditResult) -> None:
        """Maneja un requisito rechazado con defecto estructurado."""
        comment: str = (
            "❌ *Auditoría SQA — Defecto Detectado*\n\n"
            f"*Dimensión del Defecto:* {result.dimension_defecto}\n\n"
            f"*Hallazgo Estructurado:*\n{result.hallazgo_estructurado}\n\n"
            "_Transición automática a Refinement._"
        )
        self._jira.add_comment(issue, comment)
        self._jira.transition_issue(issue, TRANSITION_REFINEMENT)
        logger.info("[%s] ❌ Requisito rechazado: %s.", issue.key, result.dimension_defecto)


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------
def main() -> None:
    """Bootstrap del agente SQA."""
    logger.info("=== Agente de Auditoría Estática SQA — Inicio ===")

    try:
        jira_config: JiraConfig = EnvironmentLoader.load_jira_config()
        gemini_config: GeminiConfig = EnvironmentLoader.load_gemini_config()
    except EnvironmentError as exc:
        logger.critical("Error de configuración: %s", exc)
        sys.exit(1)

    jira_gw = JiraGateway(jira_config)
    evaluator = GeminiEvaluator(gemini_config)
    orchestrator = SQAOrchestrator(jira=jira_gw, evaluator=evaluator)

    try:
        orchestrator.run()
    except Exception as exc:
        logger.critical("Error fatal en el agente SQA: %s", exc)
        sys.exit(1)

    logger.info("=== Agente de Auditoría Estática SQA — Fin ===")


if __name__ == "__main__":
    main()
