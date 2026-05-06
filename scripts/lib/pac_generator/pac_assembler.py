"""PACAssembler: Ensambla todas las secciones en un documento PAC markdown.

Conforma el Plan de Aseguramiento de Calidad siguiendo la estructura
IEEE 730-2014, combinando secciones automáticas (derivadas del SUT)
con secciones manuales formateadas por Gemini.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from scripts.lib.pac_generator.config_reader import PacConfig


class PACAssembler:
    """Ensamblador determinista del documento PAC."""

    _MANUAL_SECTIONS = (
        "4. Objetivos de Calidad",
        "5. Gestión y Organización",
        "8. Métricas",
        "9. Análisis de Riesgos",
        "10. Cronograma",
    )

    def __init__(
        self,
        config: PacConfig,
        stack: dict[str, Any],
        artifacts: dict[str, Any],
        gemini_client: object,
    ) -> None:
        self.config = config
        self.stack = stack
        self.artifacts = artifacts
        self.gemini_client = gemini_client

    def generate(self) -> str:
        """Genera el documento PAC completo en markdown.

        Returns:
            Cadena markdown con las 13 secciones en orden fijo.
        """
        sections: list[str] = []

        sections.append(self._build_portada())
        sections.append(self._build_alcance())
        sections.append(self._build_stack())
        sections.append(self._build_inventario())
        sections.append(self._build_objetivos_calidad())
        sections.append(self._build_gestion_organizacion())
        sections.append(self._build_estandares())
        sections.append(self._build_herramientas())
        sections.append(self._build_metricas())
        sections.append(self._build_riesgos())
        sections.append(self._build_cronograma())
        sections.append(self._build_defectos())
        sections.append(self._build_cicd())

        return "\n\n".join(sections)

    # --- Auto sections -------------------------------------------------------

    def _build_portada(self) -> str:
        proyecto = self.config.proyecto
        backend = self.stack.get("backend", {})
        fecha = proyecto.get("fecha", "")
        lines = [
            "# Plan de Aseguramiento de Calidad (PAC)",
            "",
            "| Campo | Valor |",
            "|---|---|",
            f"| Proyecto | {proyecto.get('name', '')} |",
            f"| Versión | {proyecto.get('version', '')} |",
        ]
        if fecha:
            lines.append(f"| Fecha | {fecha} |")
        lines.append(
            f"| Backend | {backend.get('name', '')} {backend.get('version', '')} |"
        )
        frontend = self.stack.get("frontend", {})
        lines.append(
            f"| Frontend | {frontend.get('name', '')} {frontend.get('version', '')} |"
        )
        return "\n".join(lines)

    def _build_alcance(self) -> str:
        desc = self.config.proyecto.get("descripcion", "")
        backend = self.stack.get("backend", {})
        frontend = self.stack.get("frontend", {})
        stack_desc = (
            f"Backend: {backend.get('build_tool', '')} "
            f"({backend.get('java_version', '')}, {backend.get('spring_boot_version', '')}). "
            f"Frontend: {frontend.get('build_tool', '')} (Vue {frontend.get('vue_version', '')})."
        )
        return (
            f"## 1. Alcance y Propósito\n\n"
            f"{desc}\n\n"
            f"Stack tecnológico: {stack_desc}"
        )

    def _build_stack(self) -> str:
        backend = self.stack.get("backend", {})
        frontend = self.stack.get("frontend", {})
        lines = ["## 2. Stack Tecnológico", ""]
        lines.append("### Backend")
        lines.append(f"- **Build tool:** {backend.get('build_tool', '')}")
        lines.append(f"- **Java:** {backend.get('java_version', '')}")
        lines.append(f"- **Spring Boot:** {backend.get('spring_boot_version', '')}")
        deps = backend.get("dependencies", [])
        for dep in deps:
            lines.append(f"- {dep.get('artifactId', '')} ({dep.get('groupId', '')})")
        lines.append("")
        lines.append("### Frontend")
        lines.append(f"- **Build tool:** {frontend.get('build_tool', '')}")
        lines.append(f"- **Vue:** {frontend.get('vue_version', '')}")
        deps = frontend.get("dependencies", [])
        for dep in deps:
            lines.append(f"- {dep.get('name', '')} @{dep.get('version', '')}")
        return "\n".join(lines)

    def _build_inventario(self) -> str:
        docs = self.artifacts.get("documentation", [])
        java = self.artifacts.get("java_source", {})
        vue = self.artifacts.get("vue_source", {})
        lines = ["## 3. Inventario de Artefactos", ""]
        lines.append("### Documentación")
        if docs:
            for doc in docs:
                lines.append(f"- `{doc.get('filename', '')}`")
        else:
            lines.append("- No se detectaron documentos PDF.")
        lines.append("")
        lines.append("### Código Fuente")
        lines.append(
            f"- **Java:** {java.get('total_files', 0)} archivos, {java.get('total_loc', 0)} LOC"
        )
        lines.append(
            f"- **Vue:** {vue.get('total_files', 0)} archivos, {vue.get('total_loc', 0)} LOC"
        )
        return "\n".join(lines)

    def _build_estandares(self) -> str:
        path = Path("sqa/checklists/pac.json")
        categories: list[str] = []
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                seen: set[str] = set()
                for item in data.get("items", []):
                    cat = item.get("category", "")
                    if cat and cat not in seen:
                        seen.add(cat)
                        categories.append(cat)
            except Exception:
                pass
        lines = ["## 6. Estándares Aplicables", ""]
        if categories:
            for cat in categories:
                lines.append(f"- {cat}")
        else:
            lines.append("- IEEE 730-2014")
        return "\n".join(lines)

    def _build_herramientas(self) -> str:
        path = Path("sqa/PACS-Fase2-Herramientas.md")
        exists = path.exists()
        lines = ["## 7. Herramientas Tecnológicas", ""]
        if exists:
            lines.append(f"Ver matriz completa en `{path}`")
        else:
            lines.append("Matriz de herramientas no encontrada.")
        return "\n".join(lines)

    def _build_defectos(self) -> str:
        lines = [
            "## 11. Gestión de Defectos",
            "",
            "Los defectos se gestionan mediante tickets en Jira, siguiendo los workflows de resolución definidos por el equipo SQA.",
        ]
        return "\n".join(lines)

    def _build_cicd(self) -> str:
        workflows_dir = Path(".github/workflows")
        files: list[str] = []
        if workflows_dir.exists():
            files = sorted([p.name for p in workflows_dir.iterdir() if p.is_file()])
        lines = ["## 12. CI/CD", ""]
        lines.append("### Workflows de GitHub Actions")
        if files:
            for f in files:
                lines.append(f"- `{f}`")
        else:
            lines.append("- No se detectaron workflows.")
        return "\n".join(lines)

    # --- Manual sections (via Gemini) ----------------------------------------

    def _build_objetivos_calidad(self) -> str:
        directives = {
            "objetivos": self.config.objetivos_calidad,
        }
        content = self.gemini_client.format_section("4. Objetivos de Calidad", directives)
        return f"## 4. Objetivos de Calidad\n\n{content}"

    def _build_gestion_organizacion(self) -> str:
        directives = {
            "lider": self.config.lider,
            "roles": self.config.roles,
        }
        content = self.gemini_client.format_section("5. Gestión y Organización", directives)
        return f"## 5. Gestión y Organización\n\n{content}"

    def _build_metricas(self) -> str:
        directives = {
            "umbrales": self.config.umbrales,
        }
        content = self.gemini_client.format_section("8. Métricas", directives)
        return f"## 8. Métricas\n\n{content}"

    def _build_riesgos(self) -> str:
        directives = {
            "riesgos": self.config.riesgos,
        }
        content = self.gemini_client.format_section("9. Análisis de Riesgos", directives)
        return f"## 9. Análisis de Riesgos\n\n{content}"

    def _build_cronograma(self) -> str:
        directives = {
            "cronograma": self.config.cronograma,
        }
        content = self.gemini_client.format_section("10. Cronograma", directives)
        return f"## 10. Cronograma\n\n{content}"
