"""Tests for scripts.sqa_core.config."""
from __future__ import annotations

import os
import unittest
from unittest.mock import patch

from scripts.sqa_core.config import SQAConfig, load_config


class TestLoadConfig(unittest.TestCase):
    """Tests for load_config function."""

    def test_raises_when_jira_server_missing(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(EnvironmentError) as ctx:
                load_config()
            self.assertIn("JIRA_SERVER", str(ctx.exception))

    def test_raises_when_confluence_url_missing(self):
        env = {
            "JIRA_SERVER": "https://jira.example.com",
            "JIRA_EMAIL": "a@b.com",
            "JIRA_API_TOKEN": "tok",
            "GEMINI_API_KEY": "key",
        }
        with patch.dict(os.environ, env, clear=True):
            with self.assertRaises(EnvironmentError) as ctx:
                load_config()
            self.assertIn("CONFLUENCE_URL", str(ctx.exception))

    def test_returns_config_when_all_vars_present(self):
        env = {
            "JIRA_SERVER": "https://jira.example.com",
            "JIRA_EMAIL": "a@b.com",
            "JIRA_API_TOKEN": "tok",
            "CONFLUENCE_URL": "https://wiki.example.com",
            "CONFLUENCE_USER": "user",
            "CONFLUENCE_TOKEN": "tok2",
            "GEMINI_API_KEY": "key",
            "SONARQUBE_URL": "https://sonar.example.com",
            "SONARQUBE_TOKEN": "sonar_tok",
        }
        with patch.dict(os.environ, env, clear=True):
            config = load_config()
            self.assertIsInstance(config, SQAConfig)
            self.assertEqual(config.jira_server, "https://jira.example.com")
            self.assertEqual(config.confluence_url, "https://wiki.example.com")
            self.assertEqual(config.gemini_api_key, "key")
            self.assertEqual(config.sonarqube_url, "https://sonar.example.com")

    def test_dry_run_defaults_to_true(self):
        env = {
            "JIRA_SERVER": "https://jira.example.com",
            "JIRA_EMAIL": "a@b.com",
            "JIRA_API_TOKEN": "tok",
            "CONFLUENCE_URL": "https://wiki.example.com",
            "CONFLUENCE_USER": "user",
            "CONFLUENCE_TOKEN": "tok2",
            "GEMINI_API_KEY": "key",
            "SONARQUBE_URL": "https://sonar.example.com",
            "SONARQUBE_TOKEN": "sonar_tok",
        }
        with patch.dict(os.environ, env, clear=True):
            config = load_config()
            self.assertTrue(config.dry_run)

    def test_dry_run_false_when_set(self):
        env = {
            "JIRA_SERVER": "https://jira.example.com",
            "JIRA_EMAIL": "a@b.com",
            "JIRA_API_TOKEN": "tok",
            "CONFLUENCE_URL": "https://wiki.example.com",
            "CONFLUENCE_USER": "user",
            "CONFLUENCE_TOKEN": "tok2",
            "GEMINI_API_KEY": "key",
            "SONARQUBE_URL": "https://sonar.example.com",
            "SONARQUBE_TOKEN": "sonar_tok",
            "DRY_RUN": "false",
        }
        with patch.dict(os.environ, env, clear=True):
            config = load_config()
            self.assertFalse(config.dry_run)

    def test_project_paths_are_set(self):
        env = {
            "JIRA_SERVER": "https://jira.example.com",
            "JIRA_EMAIL": "a@b.com",
            "JIRA_API_TOKEN": "tok",
            "CONFLUENCE_URL": "https://wiki.example.com",
            "CONFLUENCE_USER": "user",
            "CONFLUENCE_TOKEN": "tok2",
            "GEMINI_API_KEY": "key",
            "SONARQUBE_URL": "https://sonar.example.com",
            "SONARQUBE_TOKEN": "sonar_tok",
        }
        with patch.dict(os.environ, env, clear=True):
            config = load_config()
            self.assertTrue(config.project_root.exists())
            self.assertTrue(str(config.documentacion_dir).endswith("documentacion"))
            self.assertTrue(str(config.reportes_dir).endswith("sqa/reportes"))


if __name__ == "__main__":
    unittest.main()
