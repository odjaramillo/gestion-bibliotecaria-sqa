"""Tests for scripts.sqa_core.clients."""
from __future__ import annotations

import sys
import unittest
from unittest.mock import MagicMock, patch

# Mock missing third-party modules before importing SQA code
for _mod in ("jira", "requests"):
    if _mod not in sys.modules:
        sys.modules[_mod] = MagicMock()

# google.generativeai is a submodule — mock the parent and submodule chain
if "google" not in sys.modules:
    sys.modules["google"] = MagicMock()
if "google.generativeai" not in sys.modules:
    sys.modules["google.generativeai"] = MagicMock()

from scripts.sqa_core.clients import (
    ConfluenceClient,
    GeminiClient,
    JiraClient,
    SonarQubeClient,
)
from scripts.sqa_core.config import SQAConfig


class TestJiraClient(unittest.TestCase):
    """Tests for JiraClient wrapper."""

    def _make_config(self) -> SQAConfig:
        return SQAConfig(
            jira_server="https://jira.example.com",
            jira_email="a@b.com",
            jira_api_token="tok",
            confluence_url="https://wiki.example.com",
            confluence_user="user",
            confluence_token="tok2",
            gemini_api_key="key",
            sonarqube_url="https://sonar.example.com",
            sonarqube_token="sonar_tok",
            dry_run=True,
            project_root=MagicMock(),
            documentacion_dir=MagicMock(),
            reportes_dir=MagicMock(),
        )

    @patch("scripts.sqa_core.clients.JIRA")
    def test_initializes_with_config_credentials(self, mock_jira_cls):
        config = self._make_config()
        client = JiraClient(config)
        mock_jira_cls.assert_called_once_with(
            server="https://jira.example.com",
            basic_auth=("a@b.com", "tok"),
        )
        self.assertIs(client.client, mock_jira_cls.return_value)

    @patch("scripts.sqa_core.clients.JIRA")
    def test_search_issues_delegates_to_client(self, mock_jira_cls):
        config = self._make_config()
        client = JiraClient(config)
        mock_issue = MagicMock()
        client.client.search_issues.return_value = [mock_issue]
        result = client.search_issues('project = "T1"')
        client.client.search_issues.assert_called_once_with('project = "T1"', maxResults=100)
        self.assertEqual(result, [mock_issue])

    @patch("scripts.sqa_core.clients.JIRA")
    def test_create_issue_delegates_to_client(self, mock_jira_cls):
        config = self._make_config()
        client = JiraClient(config)
        mock_issue = MagicMock()
        client.client.create_issue.return_value = mock_issue
        result = client.create_issue({
            "project": {"key": "SQA"},
            "summary": "Bug",
            "issuetype": {"name": "Bug"},
        })
        self.assertEqual(result, mock_issue)


class TestConfluenceClient(unittest.TestCase):
    """Tests for ConfluenceClient wrapper."""

    def _make_config(self) -> SQAConfig:
        return SQAConfig(
            jira_server="https://jira.example.com",
            jira_email="a@b.com",
            jira_api_token="tok",
            confluence_url="https://wiki.example.com",
            confluence_user="user",
            confluence_token="tok2",
            gemini_api_key="key",
            sonarqube_url="https://sonar.example.com",
            sonarqube_token="sonar_tok",
            dry_run=True,
            project_root=MagicMock(),
            documentacion_dir=MagicMock(),
            reportes_dir=MagicMock(),
        )

    @patch("scripts.sqa_core.clients.requests.request")
    def test_get_page_by_title_makes_get_request(self, mock_request):
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = {
            "results": [{"id": "12345", "title": "Test Page"}]
        }
        config = self._make_config()
        client = ConfluenceClient(config)
        result = client.get_page_by_title("SPACE", "Test Page")
        self.assertEqual(result["id"], "12345")
        mock_request.assert_called_once()
        args = mock_request.call_args
        self.assertEqual(args[0][0], "GET")

    @patch("scripts.sqa_core.clients.requests.request")
    def test_create_page_makes_post_request(self, mock_request):
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = {"id": "67890"}
        config = self._make_config()
        client = ConfluenceClient(config)
        result = client.create_page("SPACE", "Parent", "Title", "<p>Body</p>")
        self.assertEqual(result["id"], "67890")
        args = mock_request.call_args
        self.assertEqual(args[0][0], "POST")

    @patch("scripts.sqa_core.clients.requests.request")
    def test_update_page_makes_put_request(self, mock_request):
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = {"id": "12345"}
        config = self._make_config()
        client = ConfluenceClient(config)
        result = client.update_page("12345", 2, "Title", "<p>New Body</p>")
        self.assertEqual(result["id"], "12345")
        args = mock_request.call_args
        self.assertEqual(args[0][0], "PUT")


class TestGeminiClient(unittest.TestCase):
    """Tests for GeminiClient wrapper."""

    def _make_config(self) -> SQAConfig:
        return SQAConfig(
            jira_server="https://jira.example.com",
            jira_email="a@b.com",
            jira_api_token="tok",
            confluence_url="https://wiki.example.com",
            confluence_user="user",
            confluence_token="tok2",
            gemini_api_key="key",
            sonarqube_url="https://sonar.example.com",
            sonarqube_token="sonar_tok",
            dry_run=True,
            project_root=MagicMock(),
            documentacion_dir=MagicMock(),
            reportes_dir=MagicMock(),
        )

    @patch("scripts.sqa_core.clients.genai")
    def test_initializes_with_api_key(self, mock_genai):
        config = self._make_config()
        client = GeminiClient(config)
        mock_genai.configure.assert_called_once_with(api_key="key")
        self.assertIsNotNone(client.model)

    @patch("scripts.sqa_core.clients.genai")
    def test_generate_returns_text(self, mock_genai):
        mock_model = MagicMock()
        mock_model.generate_content.return_value.text = "Result"
        mock_genai.GenerativeModel.return_value = mock_model
        config = self._make_config()
        client = GeminiClient(config)
        result = client.generate("prompt")
        self.assertEqual(result, "Result")
        mock_model.generate_content.assert_called_once_with("prompt")


class TestSonarQubeClient(unittest.TestCase):
    """Tests for SonarQubeClient wrapper."""

    def _make_config(self) -> SQAConfig:
        return SQAConfig(
            jira_server="https://jira.example.com",
            jira_email="a@b.com",
            jira_api_token="tok",
            confluence_url="https://wiki.example.com",
            confluence_user="user",
            confluence_token="tok2",
            gemini_api_key="key",
            sonarqube_url="https://sonar.example.com",
            sonarqube_token="sonar_tok",
            dry_run=True,
            project_root=MagicMock(),
            documentacion_dir=MagicMock(),
            reportes_dir=MagicMock(),
        )

    @patch("scripts.sqa_core.clients.requests.request")
    def test_get_issues_makes_authenticated_get(self, mock_request):
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = {"issues": []}
        config = self._make_config()
        client = SonarQubeClient(config)
        result = client.get_issues("my-project")
        self.assertEqual(result, {"issues": []})
        args = mock_request.call_args
        self.assertEqual(args[0][0], "GET")
        self.assertIn("sonar_tok", args[1]["headers"].get("Authorization", ""))


if __name__ == "__main__":
    unittest.main()
