"""Shared HTTP/API clients for SQA integrations with retry/backoff."""
from __future__ import annotations

import logging
import time
from typing import Any, Callable, TypeVar

import requests
from jira import JIRA

import google.generativeai as genai

from scripts.sqa_core.config import SQAConfig

logger = logging.getLogger("sqa_core.clients")

T = TypeVar("T")

DEFAULT_RETRIES = 3
DEFAULT_BACKOFF = 2.0


def _retry(
    fn: Callable[[], T],
    retries: int = DEFAULT_RETRIES,
    backoff: float = DEFAULT_BACKOFF,
) -> T:
    """Execute *fn* with exponential backoff on exception."""
    last_exc: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            return fn()
        except Exception as exc:
            last_exc = exc
            logger.warning("Retryable error (attempt %d/%d): %s", attempt, retries, exc)
            if attempt < retries:
                time.sleep(backoff * (2 ** (attempt - 1)))
    raise last_exc  # type: ignore[misc]


class JiraClient:
    """Wrapper around the Jira REST API with retry semantics."""

    def __init__(self, config: SQAConfig) -> None:
        self.config = config
        self.client = JIRA(
            server=config.jira_server,
            basic_auth=(config.jira_email, config.jira_api_token),
        )

    def search_issues(self, jql: str, max_results: int = 100) -> list[Any]:
        return _retry(lambda: self.client.search_issues(jql, maxResults=max_results))

    def create_issue(self, fields: dict[str, Any]) -> Any:
        return _retry(lambda: self.client.create_issue(fields=fields))

    def transition_issue(self, issue: Any, transition_name: str) -> None:
        def _transition() -> None:
            transitions = self.client.transitions(issue)
            target = next((t for t in transitions if t["name"] == transition_name), None)
            if target is None:
                raise ValueError(f"Transición '{transition_name}' no disponible")
            self.client.transition_issue(issue, target["id"])

        _retry(_transition)

    def add_comment(self, issue: Any, body: str) -> None:
        _retry(lambda: self.client.add_comment(issue, body))


class ConfluenceClient:
    """Lightweight Confluence REST client with retry semantics."""

    def __init__(self, config: SQAConfig) -> None:
        self.config = config
        self.base_url = config.confluence_url.rstrip("/")
        self.auth = (config.confluence_user, config.confluence_token)

    def _request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        url = f"{self.base_url}/rest/api{path}"
        headers = kwargs.pop("headers", {})
        headers.setdefault("Content-Type", "application/json")
        headers.setdefault("Accept", "application/json")

        def _call() -> requests.Response:
            resp = requests.request(method, url, auth=self.auth, headers=headers, **kwargs)
            resp.raise_for_status()
            return resp

        return _retry(_call)

    def get_page_by_title(self, space_key: str, title: str) -> dict[str, Any] | None:
        resp = self._request(
            "GET",
            "/content",
            params={"spaceKey": space_key, "title": title, "expand": "version"},
        )
        data = resp.json()
        results = data.get("results", [])
        return results[0] if results else None

    def create_page(
        self,
        space_key: str,
        parent_id: str | None,
        title: str,
        body: str,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "type": "page",
            "title": title,
            "space": {"key": space_key},
            "body": {"storage": {"value": body, "representation": "storage"}},
        }
        if parent_id:
            payload["ancestors"] = [{"id": parent_id}]
        resp = self._request("POST", "/content", json=payload)
        return resp.json()

    def update_page(
        self,
        page_id: str,
        version: int,
        title: str,
        body: str,
    ) -> dict[str, Any]:
        payload = {
            "type": "page",
            "title": title,
            "body": {"storage": {"value": body, "representation": "storage"}},
            "version": {"number": version + 1},
        }
        resp = self._request("PUT", f"/content/{page_id}", json=payload)
        return resp.json()


class GeminiClient:
    """Wrapper around Google Gemini API with retry semantics."""

    def __init__(self, config: SQAConfig) -> None:
        self.config = config
        genai.configure(api_key=config.gemini_api_key)
        self.model = genai.GenerativeModel(
            model_name="gemini-3.1-flash-lite-preview",
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
            ),
        )

    def generate(self, prompt: str) -> str:
        def _call() -> str:
            response = self.model.generate_content(prompt)
            return response.text

        return _retry(_call)


class SonarQubeClient:
    """Lightweight SonarQube REST client with retry semantics."""

    def __init__(self, config: SQAConfig) -> None:
        self.config = config
        self.base_url = config.sonarqube_url.rstrip("/")
        self.token = config.sonarqube_token

    def _request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        url = f"{self.base_url}/api{path}"
        headers = kwargs.pop("headers", {})
        headers.setdefault("Authorization", f"Bearer {self.token}")

        def _call() -> requests.Response:
            resp = requests.request(method, url, headers=headers, **kwargs)
            resp.raise_for_status()
            return resp

        return _retry(_call)

    def get_issues(self, project_key: str) -> dict[str, Any]:
        resp = self._request(
            "GET",
            "/issues/search",
            params={"componentKeys": project_key, "resolved": "false"},
        )
        return resp.json()

    def get_measures(self, project_key: str, metric_keys: list[str]) -> dict[str, Any]:
        resp = self._request(
            "GET",
            "/measures/component",
            params={"component": project_key, "metricKeys": ",".join(metric_keys)},
        )
        return resp.json()
