#!/usr/bin/env python3
"""Workflow PAC Generator: Orquestador para generación semi-automatizada del PAC.

Este script coordina todos los componentes del generador PAC:
- Lee la configuración del líder (pac_config.yaml)
- Descubre el stack tecnológico desde pom.xml y package.json
- Inventaria artefactos (documentación, código fuente)
- Formatea secciones manuales con Gemini (opcional)
- Ensambla el documento PAC markdown
- Ejecuta chequeo de completitud
- Escribe reporte JSON de resumen
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Any

from scripts.lib.pac_generator.config_reader import PacConfigError, read_config
from scripts.lib.pac_generator.gemini_client import GeminiClient
from scripts.lib.pac_generator.pac_assembler import PACAssembler
from scripts.lib.pac_generator.report_writer import ReportWriter
from scripts.lib.pac_generator.stack_discoverer import parse_package_json, parse_pom
from scripts.lib.pac_generator.artifact_inventory import (
    scan_documentation,
    scan_java_source,
    scan_vue_source,
)


def _resolve_project_root() -> Path:
    """Resuelve la raíz del proyecto desde PROJECT_ROOT o la ubicación del script."""
    env_root = os.environ.get("PROJECT_ROOT")
    if env_root:
        return Path(env_root).resolve()
    return Path(__file__).resolve().parent.parent


def _discover_stack(project_root: Path) -> dict[str, Any]:
    """Descubre el stack backend y frontend."""
    stack: dict[str, Any] = {}
    pom_path = project_root / "pom.xml"
    try:
        stack["backend"] = parse_pom(pom_path)
    except FileNotFoundError:
        print(
            f"ADVERTENCIA: {pom_path} no encontrado. Continuando sin datos de backend.",
            file=sys.stderr,
        )
        stack["backend"] = {}

    package_json_path = project_root / "biblioteca-frontend" / "package.json"
    try:
        stack["frontend"] = parse_package_json(package_json_path)
    except FileNotFoundError:
        print(
            f"ADVERTENCIA: {package_json_path} no encontrado. "
            "Continuando sin datos de frontend.",
            file=sys.stderr,
        )
        stack["frontend"] = {}

    return stack


def _inventory_artifacts(project_root: Path) -> dict[str, Any]:
    """Inventaria artefactos de documentación y código fuente."""
    artifacts: dict[str, Any] = {}
    doc_dir = project_root / "documentacion"
    artifacts["documentation"] = scan_documentation(doc_dir)

    java_src = project_root / "src" / "main" / "java"
    artifacts["java_source"] = scan_java_source(java_src)

    vue_src = project_root / "biblioteca-frontend" / "src"
    artifacts["vue_source"] = scan_vue_source(vue_src)

    return artifacts


def _count_sections(pac_content: str) -> int:
    """Cuenta el total de secciones del PAC (portada + secciones numeradas)."""
    lines = pac_content.splitlines()
    numbered_sections = [line for line in lines if line.startswith("## ")]
    has_portada = any(
        line.startswith("# Plan de Aseguramiento de Calidad") for line in lines
    )
    return len(numbered_sections) + (1 if has_portada else 0)


def _find_placeholders(pac_content: str) -> list[str]:
    """Identifica líneas que contienen placeholders [COMPLETAR...]."""
    placeholders: list[str] = []
    for line in pac_content.splitlines():
        if "[COMPLETAR" in line:
            placeholders.append(line.strip())
    return placeholders


def main(argv: list[str] | None = None) -> int:
    """Punto de entrada del orquestador PAC.

    Returns:
        0 si el flujo completó (incluso parcialmente), 1 si la configuración es inválida.
    """
    parser = argparse.ArgumentParser(
        description="Genera el Plan de Aseguramiento de Calidad (PAC)"
    )
    parser.add_argument(
        "--config",
        default="sqa/templates/pac_config.yaml",
        help="Ruta al archivo de configuración pac_config.yaml",
    )
    parser.add_argument(
        "--output",
        default="sqa/pac_generado.md",
        help="Ruta de salida para el PAC generado",
    )
    parser.add_argument(
        "--no-gemini",
        action="store_true",
        help="Omitir formateo con Gemini y usar placeholders",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Generar pero no escribir archivos (imprime a stdout)",
    )
    args = parser.parse_args(argv)

    project_root = _resolve_project_root()
    config_path = project_root / args.config
    output_path = project_root / args.output

    # 1. Leer configuración
    try:
        config = read_config(config_path)
    except PacConfigError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    # 2. Descubrir stack
    stack = _discover_stack(project_root)

    # 3. Inventariar artefactos
    artifacts = _inventory_artifacts(project_root)

    # 4. Inicializar Gemini (o dummy si --no-gemini)
    if args.no_gemini:

        class _DummyGeminiClient:
            """Cliente dummy determinista para uso sin Gemini."""

            def format_section(self, section_name: str, directives: dict) -> str:
                return f"[FORMATEO GEMINI NO DISPONIBLE: {section_name}]"

        gemini_client: Any = _DummyGeminiClient()
    else:
        api_key = os.environ.get("GEMINI_API_KEY", "")
        gemini_client = GeminiClient(api_key)

    # 5. Ensamblar PAC
    assembler = PACAssembler(config, stack, artifacts, gemini_client)
    pac_content = assembler.generate()

    # 6. Chequeo de completitud
    sections_total = _count_sections(pac_content)
    placeholders = _find_placeholders(pac_content)
    placeholders_count = len(placeholders)

    status = "PARCIAL" if placeholders_count > 0 else "EXITOSO"

    issues: list[str] = []
    if not stack.get("backend"):
        issues.append("pom.xml no encontrado")
    if not stack.get("frontend"):
        issues.append("package.json no encontrado")
    issues.extend([f"Placeholder: {p}" for p in placeholders])

    # 7. Escribir PAC
    if not args.dry_run:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(pac_content, encoding="utf-8")
        print(f"PAC generado: {output_path}")
    else:
        print(pac_content)

    # 8. Escribir reporte (salvo en dry-run)
    if not args.dry_run:
        report_dir = project_root / "sqa" / "reportes"
        writer = ReportWriter(report_dir)
        report_path = writer.write_summary(
            pac_path=output_path,
            status=status,
            sections_total=sections_total,
            sections_auto=sections_total - 5,
            sections_manual=5,
            sections_completed=sections_total - placeholders_count,
            issues=issues,
        )
        print(f"Reporte generado: {report_path}")

    # 9. Resumen stdout
    print("\n=== Resumen PAC ===")
    print(f"Secciones totales: {sections_total}")
    print(f"Placeholders pendientes: {placeholders_count}")
    print(f"Estado: {status}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
