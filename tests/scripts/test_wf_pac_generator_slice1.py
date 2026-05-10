"""Tests for scripts.lib.pac_generator modules (slice 1)."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import yaml

from scripts.lib.pac_generator.config_reader import (
    PacConfig,
    PacConfigError,
    read_config,
)
from scripts.lib.pac_generator.stack_discoverer import (
    parse_package_json,
    parse_pom,
)
from scripts.lib.pac_generator.artifact_inventory import (
    scan_documentation,
    scan_java_source,
    scan_vue_source,
)

FIXTURES_DIR = Path(__file__).parent / "fixtures"


class TestConfigReader(unittest.TestCase):
    """Tests for config_reader module."""

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmpdir.cleanup()

    def _write_config(self, data: dict) -> Path:
        path = Path(self.tmpdir.name) / "config.yaml"
        path.write_text(yaml.dump(data), encoding="utf-8")
        return path

    def test_read_valid_config(self):
        path = FIXTURES_DIR / "sample_pac_config.yaml"
        config = read_config(path)

        self.assertIsInstance(config, PacConfig)
        self.assertEqual(config.proyecto["name"], "Sistema de Prueba")
        self.assertEqual(config.proyecto["version"], "1.0.0")
        self.assertEqual(config.proyecto["descripcion"], "Proyecto de prueba para tests")

        self.assertEqual(config.lider["nombre"], "Ana López")
        self.assertEqual(config.lider["email"], "ana@ejemplo.com")
        self.assertEqual(config.lider["rol"], "Líder de Métricas")

        self.assertEqual(config.objetivos_calidad, {
            "funcionalidad": 40,
            "fiabilidad": 30,
            "usabilidad": 30,
        })

        self.assertEqual(config.roles, {
            "lider_metricas": "Ana López",
            "responsable_sqa": "Carlos Ruiz",
        })

        self.assertEqual(config.umbrales, {
            "cobertura_revisiones": 100.0,
            "densidad_defectos_max": 0.5,
        })

        self.assertEqual(len(config.riesgos), 1)
        self.assertEqual(config.riesgos[0]["descripcion"], "Retraso en entregables")
        self.assertEqual(config.riesgos[0]["mitigacion"], "Checkpoints semanales")
        self.assertEqual(config.riesgos[0]["aceptado"], False)

        self.assertEqual(len(config.cronograma), 1)
        self.assertEqual(config.cronograma[0]["fase"], "Fase 1")
        self.assertEqual(config.cronograma[0]["inicio"], "2026-05-01")
        self.assertEqual(config.cronograma[0]["fin"], "2026-05-15")
        self.assertEqual(config.cronograma[0]["entregables"], ["PAC aprobado"])

    def test_missing_file(self):
        fake_path = Path(self.tmpdir.name) / "nonexistent.yaml"
        with self.assertRaises(PacConfigError) as ctx:
            read_config(fake_path)
        self.assertIn("no encontrado", str(ctx.exception))

    def test_invalid_yaml(self):
        bad_path = Path(self.tmpdir.name) / "bad.yaml"
        bad_path.write_text("{ invalid yaml: [", encoding="utf-8")
        with self.assertRaises(PacConfigError) as ctx:
            read_config(bad_path)
        self.assertIn("Error de sintaxis YAML", str(ctx.exception))

    def test_missing_required_field(self):
        raw = yaml.safe_load((FIXTURES_DIR / "sample_pac_config.yaml").read_text())
        del raw["proyecto"]["version"]
        path = self._write_config(raw)
        with self.assertRaises(PacConfigError) as ctx:
            read_config(path)
        self.assertIn("version", str(ctx.exception))

    def test_invalid_weight_range(self):
        raw = yaml.safe_load((FIXTURES_DIR / "sample_pac_config.yaml").read_text())
        raw["objetivos_calidad"]["funcionalidad"] = 150
        path = self._write_config(raw)
        with self.assertRaises(PacConfigError) as ctx:
            read_config(path)
        self.assertIn("150", str(ctx.exception))

    def test_invalid_weight_type(self):
        raw = yaml.safe_load((FIXTURES_DIR / "sample_pac_config.yaml").read_text())
        raw["objetivos_calidad"]["funcionalidad"] = "alta"
        path = self._write_config(raw)
        with self.assertRaises(PacConfigError) as ctx:
            read_config(path)
        self.assertIn("str", str(ctx.exception))

    def test_empty_objetivos(self):
        raw = yaml.safe_load((FIXTURES_DIR / "sample_pac_config.yaml").read_text())
        raw["objetivos_calidad"] = {}
        path = self._write_config(raw)
        with self.assertRaises(PacConfigError) as ctx:
            read_config(path)
        self.assertIn("vacío", str(ctx.exception))

    def test_invalid_riesgo_aceptado(self):
        raw = yaml.safe_load((FIXTURES_DIR / "sample_pac_config.yaml").read_text())
        raw["riesgos"][0]["aceptado"] = "no"
        path = self._write_config(raw)
        with self.assertRaises(PacConfigError) as ctx:
            read_config(path)
        self.assertIn("bool", str(ctx.exception))

    def test_missing_cronograma_field(self):
        raw = yaml.safe_load((FIXTURES_DIR / "sample_pac_config.yaml").read_text())
        del raw["cronograma"][0]["fin"]
        path = self._write_config(raw)
        with self.assertRaises(PacConfigError) as ctx:
            read_config(path)
        self.assertIn("fin", str(ctx.exception))


class TestStackDiscoverer(unittest.TestCase):
    """Tests for stack_discoverer module."""

    def test_parse_pom_success(self):
        result = parse_pom(FIXTURES_DIR / "sample_pom.xml")

        self.assertEqual(result["artifact_id"], "biblioteca-backend")
        self.assertEqual(result["version"], "0.0.1-SNAPSHOT")
        self.assertEqual(result["name"], "gestion_bibliotecaria")
        self.assertEqual(result["description"], "Proyecto de prueba para StackDiscoverer")
        self.assertEqual(result["java_version"], "21")
        self.assertEqual(result["spring_boot_version"], "3.4.5")
        self.assertEqual(result["build_tool"], "Maven")

        deps = result["dependencies"]
        self.assertEqual(len(deps), 3)
        self.assertEqual(deps[0]["groupId"], "mysql")
        self.assertEqual(deps[0]["artifactId"], "mysql-connector-java")
        self.assertEqual(deps[0]["version"], "8.0.32")
        self.assertEqual(deps[1]["artifactId"], "spring-boot-starter-data-jpa")
        self.assertEqual(deps[2]["artifactId"], "spring-boot-starter-web")

    def test_parse_pom_not_found(self):
        with self.assertRaises(FileNotFoundError):
            parse_pom(Path("/nonexistent/pom.xml"))

    def test_parse_package_json_success(self):
        result = parse_package_json(FIXTURES_DIR / "sample_package.json")

        self.assertEqual(result["name"], "gestion-bibliotecaria")
        self.assertEqual(result["version"], "0.1.0")
        self.assertEqual(result["vue_version"], "3.2.13")
        self.assertEqual(result["build_tool"], "npm / vue-cli")

        deps = result["dependencies"]
        self.assertEqual(len(deps), 3)
        self.assertEqual(deps[0]["name"], "axios")
        self.assertEqual(deps[0]["version"], "1.9.0")
        self.assertEqual(deps[1]["name"], "core-js")
        self.assertEqual(deps[1]["version"], "3.8.3")
        self.assertEqual(deps[2]["name"], "vue")
        self.assertEqual(deps[2]["version"], "3.2.13")

        dev_deps = result["dev_dependencies"]
        self.assertEqual(len(dev_deps), 2)
        self.assertEqual(dev_deps[0]["name"], "@vue/cli-plugin-babel")
        self.assertEqual(dev_deps[0]["version"], "5.0.0")
        self.assertEqual(dev_deps[1]["name"], "@vue/cli-service")
        self.assertEqual(dev_deps[1]["version"], "5.0.0")

    def test_parse_package_json_not_found(self):
        with self.assertRaises(FileNotFoundError):
            parse_package_json(Path("/nonexistent/package.json"))

    def test_pom_dependencies_sorted(self):
        result = parse_pom(FIXTURES_DIR / "sample_pom.xml")
        artifact_ids = [d["artifactId"] for d in result["dependencies"]]
        self.assertEqual(artifact_ids, sorted(artifact_ids))

    def test_package_deps_sorted(self):
        result = parse_package_json(FIXTURES_DIR / "sample_package.json")
        dep_names = [d["name"] for d in result["dependencies"]]
        self.assertEqual(dep_names, sorted(dep_names))
        dev_names = [d["name"] for d in result["dev_dependencies"]]
        self.assertEqual(dev_names, sorted(dev_names))


class TestArtifactInventory(unittest.TestCase):
    """Tests for artifact_inventory module."""

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_scan_documentation(self):
        doc_dir = Path(self.tmpdir.name) / "documentacion"
        doc_dir.mkdir()
        (doc_dir / "b.pdf").write_text("pdf content", encoding="utf-8")
        (doc_dir / "a.pdf").write_text("pdf content", encoding="utf-8")
        (doc_dir / "readme.txt").write_text("txt content", encoding="utf-8")

        result = scan_documentation(doc_dir)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["filename"], "a.pdf")
        self.assertEqual(result[1]["filename"], "b.pdf")
        self.assertEqual(result[0]["path"], "documentacion/a.pdf")
        self.assertEqual(result[1]["path"], "documentacion/b.pdf")

    def test_scan_documentation_empty(self):
        doc_dir = Path(self.tmpdir.name) / "empty_docs"
        doc_dir.mkdir()
        result = scan_documentation(doc_dir)
        self.assertEqual(result, [])

    def test_scan_java_source(self):
        src_dir = Path(self.tmpdir.name) / "src"
        pkg1 = src_dir / "com" / "example"
        pkg1.mkdir(parents=True)
        (pkg1 / "Foo.java").write_text(
            "package com.example;\n\npublic class Foo {\n}\n",
            encoding="utf-8",
        )
        pkg2 = src_dir / "org" / "test"
        pkg2.mkdir(parents=True)
        (pkg2 / "Bar.java").write_text(
            "package org.test;\n\npublic class Bar {\n}\n",
            encoding="utf-8",
        )

        result = scan_java_source(src_dir)

        self.assertEqual(result["total_files"], 2)
        self.assertEqual(result["total_loc"], 6)
        self.assertEqual(len(result["packages"]), 2)

        self.assertEqual(result["packages"][0]["package"], "com.example")
        self.assertEqual(result["packages"][0]["files"], 1)
        self.assertEqual(result["packages"][0]["loc"], 3)

        self.assertEqual(result["packages"][1]["package"], "org.test")
        self.assertEqual(result["packages"][1]["files"], 1)
        self.assertEqual(result["packages"][1]["loc"], 3)

    def test_scan_java_source_empty(self):
        src_dir = Path(self.tmpdir.name) / "empty_src"
        src_dir.mkdir()
        result = scan_java_source(src_dir)
        self.assertEqual(result["total_files"], 0)
        self.assertEqual(result["total_loc"], 0)
        self.assertEqual(result["packages"], [])

    def test_scan_vue_source(self):
        src_dir = Path(self.tmpdir.name) / "vue_src"
        comp_dir = src_dir / "components"
        comp_dir.mkdir(parents=True)
        (comp_dir / "Hello.vue").write_text(
            "<template>\n  <div>Hello</div>\n</template>\n",
            encoding="utf-8",
        )
        view_dir = src_dir / "views"
        view_dir.mkdir(parents=True)
        (view_dir / "Home.vue").write_text(
            "<template>\n  <div>Home</div>\n</template>\n<script>\nexport default {}\n</script>\n",
            encoding="utf-8",
        )

        result = scan_vue_source(src_dir)

        self.assertEqual(result["total_files"], 2)
        self.assertEqual(result["total_loc"], 9)
        self.assertEqual(len(result["components"]), 2)

        self.assertEqual(result["components"][0]["component"], "components.Hello")
        self.assertEqual(result["components"][0]["loc"], 3)

        self.assertEqual(result["components"][1]["component"], "views.Home")
        self.assertEqual(result["components"][1]["loc"], 6)

    def test_scan_vue_source_empty(self):
        src_dir = Path(self.tmpdir.name) / "empty_vue"
        src_dir.mkdir()
        result = scan_vue_source(src_dir)
        self.assertEqual(result["total_files"], 0)
        self.assertEqual(result["total_loc"], 0)
        self.assertEqual(result["components"], [])


if __name__ == "__main__":
    unittest.main()
