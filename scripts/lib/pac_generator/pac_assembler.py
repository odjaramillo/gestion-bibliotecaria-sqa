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
        desc = self.config.proyecto.get("descripcion", "").strip()
        backend = self.stack.get("backend", {})
        frontend = self.stack.get("frontend", {})
        stack_desc = (
            f"Backend: {backend.get('build_tool', '')} "
            f"({backend.get('java_version', '')}, {backend.get('spring_boot_version', '')}). "
            f"Frontend: {frontend.get('build_tool', '')} (Vue {frontend.get('vue_version', '')})."
        )
        lines = [
            "## 1. Alcance y Propósito",
            "",
            "### 1.1 Contexto del Proyecto",
            desc if desc else "Sistema web de gestión bibliotecaria.",
            "",
            "El presente Plan de Aseguramiento de Calidad (PAC) aplica al Sistema Under Test (SUT) desarrollado por el equipo de desarrollo, y será auditado por el equipo SQA asignado. El objetivo es garantizar que todos los artefactos entregados cumplan con los estándares de calidad definidos y que el producto final sea confiable, mantenible y seguro.",
            "",
            "### 1.2 Justificación de Negocio",
            "La gestión bibliotecaria requiere un sistema robusto que permita:",
            "- Controlar préstamos, devoluciones y reservas de material bibliográfico.",
            "- Administrar catálogos de libros, revistas y recursos digitales.",
            "- Gestionar usuarios, reseñas, comentarios y amonestaciones por retrasos.",
            "- Garantizar la trazabilidad de operaciones críticas mediante auditoría.",
            "",
            "Un fallo en este sistema impacta directamente la operatividad de la biblioteca y la satisfacción de sus usuarios, por lo que el aseguramiento de calidad no es opcional sino un requisito crítico de negocio.",
            "",
            "### 1.3 Límites del Alcance (IN / OUT)",
            "",
            "**Dentro del alcance (IN):**",
            "- Documentación de requisitos (ERS), arquitectura (DAS) y brief del proyecto.",
            "- Configuración de infraestructura CI/CD y pipelines de despliegue.",
            "- Checklists de inspección estática, métricas de calidad y gestión de defectos.",
            "- Plan de pruebas estáticas (Fase 1) y dinámicas (Fase 2).",
            "- Stack tecnológico del SUT (Java, Spring Boot, Vue) para contexto de auditoría.",
            "",
            "**Fuera del alcance (OUT):**",
            "- Mantenimiento evolutivo del SUT post-entrega final.",
            "- Pruebas de carga y estrés de alto volumen (planificadas para iteraciones futuras).",
            "- Infraestructura de producción fuera del entorno Docker definido.",
            "- Capacitación de usuarios finales del sistema bibliotecario.",
            "",
            "### 1.4 Relación con Otros Documentos",
            "Este documento se vincula directamente con los siguientes artefactos del proyecto:",
            "",
            "| Documento | Versión | Relación con el PAC |",
            "|---|---|---|",
            "| ERS (Especificación de Requisitos de Software) | v1.2 | Base para auditoría de requisitos (WF1) y trazabilidad de pruebas. |",
            "| DAS (Documento de Arquitectura de Software) | v1.5 | Base para inspección arquitectónica (WF2) y validación de decisiones de diseño. |",
            "| Brief del Proyecto | v1.1 | Define contexto de negocio y restricciones que limitan el alcance del SQA. |",
            "| Plan de Pruebas (PP) | — | Derivado del PAC; vincula cronograma con actividades de prueba dinámica. |",
            "| Matriz de Herramientas | Fase 2 | Declara herramientas tecnológicas y justificación técnica por atributo ISO 25010. |",
            "",
            f"Stack tecnológico detectado: {stack_desc}",
        ]
        return "\n".join(lines)

    def _build_stack(self) -> str:
        backend = self.stack.get("backend", {})
        frontend = self.stack.get("frontend", {})
        java_ver = backend.get("java_version", "")
        sb_ver = backend.get("spring_boot_version", "")
        bt = backend.get("build_tool", "")
        vue_ver = frontend.get("vue_version", "")
        ft_bt = frontend.get("build_tool", "")
        lines = [
            "## 2. Stack Tecnológico",
            "",
            "### 2.1 Backend",
            f"- **Build tool:** {bt}",
            f"- **Java:** {java_ver}",
            f"- **Spring Boot:** {sb_ver}",
        ]
        deps = backend.get("dependencies", [])
        for dep in deps:
            lines.append(f"- {dep.get('artifactId', '')} ({dep.get('groupId', '')})")
        lines += [
            "",
            "**Justificación técnica:** Java 21 ofrece mejoras de rendimiento (generational ZGC, virtual threads preview) y soporte LTS extendido. Spring Boot 3.4.x aprovecha Jakarta EE 9+, requiriendo Java 17+ como baseline. Maven fue seleccionado como build tool estándar del equipo de desarrollo, garantizando reproducibilidad de builds mediante `pom.xml` versionado.",
            "",
            "### 2.2 Frontend",
            f"- **Build tool:** {ft_bt}",
            f"- **Vue:** {vue_ver}",
        ]
        deps = frontend.get("dependencies", [])
        for dep in deps:
            lines.append(f"- {dep.get('name', '')} @{dep.get('version', '')}")
        lines += [
            "",
            "**Justificación técnica:** Vue 3 introduce la Composition API, mejor tree-shaking y rendimiento de reactividad con Proxy-based observation. El ecosistema npm/vue-cli facilita la integración con herramientas de prueba E2E como Playwright y la generación de bundles optimizados para despliegue.",
            "",
            "### 2.3 Matriz de Compatibilidad de Versiones",
            "",
            "| Componente | Versión Declarada | Versión Mínima Requerida | Estado |",
            "|---|---|---|---|",
            f"| Java JDK | {java_ver} | 17 | Compatible |",
            f"| Spring Boot | {sb_ver} | 3.2.x | Compatible |",
            f"| Vue.js | {vue_ver} | 3.0.0 | Compatible |",
            "| Node.js (build) | 20+ (LTS) | 18 | Compatible |",
            "| MySQL | 8.0 | 8.0 | Compatible |",
            "",
            "### 2.4 Entorno de Despliegue",
            "",
            "El SUT se despliega en contenedores Docker orchestrados mediante Docker Compose. La configuración garantiza:",
            "- Aislamiento de dependencias (backend, frontend, base de datos).",
            "- Reproducibilidad de entornos entre desarrollo, CI/CD y staging.",
            "- Escalabilidad horizontal del backend mediante balanceo de carga (futuro).",
            "",
            "| Entorno | Propósito | Infraestructura |",
            "|---|---|---|",
            "| Local | Desarrollo y pruebas unitarias | Docker Compose (dev profile) |",
            "| CI/CD | Validación automática en pipeline | GitHub Actions runners (ubuntu-latest) |",
            "| Staging | Validación pre-producción | Docker Compose (prod-like profile) |",
            "",
            "### 2.5 Stack de Seguridad",
            "",
            "El SUT incorpora las siguientes capas de seguridad:",
            "- **Spring Security 6:** Autenticación JWT, autorización basada en roles (`@PreAuthorize`), protección CSRF deshabilitada por API-only.",
            "- **Hibernate Validator:** Validación de inputs en DTOs mediante anotaciones (`@NotNull`, `@Size`, `@Email`).",
            "- **Spring Data JPA:** Uso de queries parametrizadas para mitigar SQL Injection.",
            "- **CORS configurado:** Orígenes permitidos restringidos al dominio del frontend.",
            "- **Auditoría:** Tabla `auditoria` con timestamp, usuario, IP y acción realizada para trazabilidad.",
        ]
        return "\n".join(lines)

    def _build_inventario(self) -> str:
        docs = self.artifacts.get("documentation", [])
        java = self.artifacts.get("java_source", {})
        vue = self.artifacts.get("vue_source", {})
        lines = [
            "## 3. Inventario de Artefactos",
            "",
            "### 3.1 Documentación del Proyecto",
            "",
            "La siguiente tabla lista los documentos detectados en `/documentacion`, su propósito y la fase de SQA en la que se auditan:",
            "",
        ]
        if docs:
            lines.append("| Documento | Propósito | Fase de Auditoría |")
            lines.append("|---|---|---|")
            doc_desc_map = {
                "BRIEF": "Contexto de negocio, objetivos y restricciones del proyecto.",
                "ERS": "Especificación funcional y no funcional de requisitos de software.",
                "DAS": "Decisiones arquitectónicas, vistas de diseño y patrones aplicados.",
                "Diagrama de Clases": "Modelo estático del dominio: entidades, relaciones y cardinalidades.",
                "Diagrama de contexto": "Vista C4 nivel 1 y 2: contexto del sistema, contenedores y componentes.",
            }
            for doc in docs:
                fname = doc.get("filename", "")
                desc = "Documento de proyecto."
                fase = "Fase 1 — Inspección estática"
                for key, val in doc_desc_map.items():
                    if key.upper() in fname.upper():
                        desc = val
                        break
                lines.append(f"| `{fname}` | {desc} | {fase} |")
        else:
            lines.append("- No se detectaron documentos PDF.")
        lines += [
            "",
            "### 3.2 Mapeo Artefacto → Estándar → Checklist",
            "",
            "| Artefacto | Estándar Aplicable | Checklist | Ruta |",
            "|---|---|---|---|",
            "| ERS | ISO/IEC/IEEE 29148:2018 | `sqa/checklists/ers.json` | `documentacion/ERS*.pdf` |",
            "| DAS | ISO/IEC/IEEE 42010:2022 | `sqa/checklists/das.json` | `documentacion/DAS*.pdf` |",
            "| Brief | Buenas prácticas SQA | `sqa/checklists/brief.json` | `documentacion/BRIEF*.pdf` |",
            "| PAC | IEEE 730-2014 | `sqa/checklists/pac.json` | `sqa/pac_generado.md` |",
        ]
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
        lines = [
            "## 6. Estándares Aplicables",
            "",
            "### 6.1 Descripción de Estándares",
            "",
            "El equipo SQA aplica los siguientes estándares internacionales para garantizar que cada artefacto del proyecto cumpla con criterios objetivos de calidad:",
            "",
        ]
        if categories:
            for cat in categories:
                desc = ""
                if "Objetivos de Calidad" in cat:
                    desc = "Define atributos de calidad del producto software (funcionalidad, fiabilidad, mantenibilidad, seguridad) y sub-características medibles. Asegura que los objetivos de calidad sean explícitos, medibles y verificables."
                elif "Gestión y Organización" in cat:
                    desc = "Establece roles, responsabilidades, estrategias de validación y verificación, y estructura de gobierno del equipo SQA. Garantiza que el aseguramiento de calidad sea una actividad planificada y no reactiva."
                elif "Documentación" in cat:
                    desc = "Norma la estructura, contenido y trazabilidad de documentos técnicos (ERS, DAS). Asegura que cada requisito y decisión arquitectónica esté identificable, rastreable y revisable."
                elif "Métricas" in cat:
                    desc = "Define principios para la medición de procesos y productos software. Establece que toda métrica debe tener definición operacional, fórmula, umbral objetivo y responsable de recolección."
                elif "Ejecución" in cat:
                    desc = "Vincula el PAC con el Plan de Pruebas (PP) y el cronograma del proyecto. Asegura que las actividades de SQA estén calendarizadas y que la gestión de defectos tenga un workflow definido."
                else:
                    desc = "Estándar aplicable según checklist del PAC."
                lines.append(f"- **{cat}:** {desc}")
        else:
            lines.append("- **IEEE 730-2014:** Estándar base para planes de aseguramiento de calidad. Define estructura, contenido mínimo y criterios de cumplimiento.")
        lines += [
            "",
            "### 6.2 Mapeo Artefacto → Estándar → Checklist",
            "",
            "| Artefacto | Estándar | Checklist | Nivel de Cumplimiento |",
            "|---|---|---|---|",
            "| ERS | ISO/IEC/IEEE 29148:2018 | `sqa/checklists/ers.json` | Obligatorio — 100% ítems verificables |",
            "| DAS | ISO/IEC/IEEE 42010:2022 | `sqa/checklists/das.json` | Obligatorio — 100% ítems verificables |",
            "| Brief | Buenas prácticas SQA | `sqa/checklists/brief.json` | Recomendado — contexto de negocio validado |",
            "| PAC | IEEE 730-2014 | `sqa/checklists/pac.json` | Obligatorio — auto-auditoría con wf6_auditor_pac.yml |",
            "",
            "### 6.3 Niveles de Cumplimiento",
            "",
            "- **Obligatorio:** El artefacto debe cumplir el 100% de los ítems críticos del checklist. Fallo en un ítem crítico implica rechazo del artefacto.",
            "- **Recomendado:** El artefacto debe cumplir al menos el 80% de los ítems no críticos. Los hallazgos se documentan como observaciones sin bloqueo de entrega.",
            "- **Informativo:** El artefacto se revisa para contexto pero no aplica checklist formal. Se utiliza para trazabilidad y justificación de alcance.",
        ]
        return "\n".join(lines)

    def _build_herramientas(self) -> str:
        path = Path("sqa/PACS-Fase2-Herramientas.md")
        exists = path.exists()
        lines = [
            "## 7. Herramientas Tecnológicas",
            "",
            "### 7.1 Categorización de Herramientas",
            "",
            "El equipo SQA utiliza un ecosistema de herramientas organizado por categoría funcional. A continuación se detallan las herramientas declaradas, su propósito y justificación técnica:",
            "",
            "#### Inspección Estática y Análisis de Documentos",
            "| Herramienta | Versión | Propósito | Justificación |",
            "|---|---|---|---|",
            "| **Python 3.10+** | 3.10 | Lenguaje base de scripts SQA | Tipado robusto, ecosistema maduro (PyMuPDF, Pillow, Requests), integración nativa con GitHub Actions. |",
            "| **PyMuPDF** | 1.24+ | Extracción de texto e imágenes de PDFs | Rendimiento superior frente a pdfminer; permite renderizado de páginas a PNG para análisis visual. |",
            "| **Pillow** | 10.0+ | Procesamiento de imágenes extraídas | Conversión, redimensión y normalización de imágenes antes de envío a modelos de visión (Gemini). |",
            "| **Google Gemini** | v1 (API) | Generación y análisis asistido por IA | Multimodal (texto + imagen); few-shot prompts configurables; acelera auditoría de requisitos y arquitectura. |",
            "",
            "#### Pruebas Dinámicas (Fase 2)",
            "| Herramienta | Versión | Propósito | Justificación |",
            "|---|---|---|---|",
            "| **Playwright** | 1.40+ | Pruebas E2E de UI | Auto-wait, interceptación de red, generación nativa de traces/videos en CI. Reemplaza a Selenium por menor flakiness con Vue 3. |",
            "| **RestAssured** | 5.3+ | Pruebas de integración API | Código Java versionable en repo; integrado con JUnit 5 y Maven Surefire. Reemplaza Postman/Newman en CI. |",
            "| **TestContainers** | 1.19+ | Bases de datos reales en tests | Levanta MySQL 8 en Docker durante tests; elimina mocks que generan falsos positivos. |",
            "| **OWASP ZAP** | 2.14+ | Pruebas de penetración DAST | Estándar open-source para análisis dinámico de seguridad. Integrable en GitHub Actions vía `zap-baseline.py`. |",
            "| **Spring Security Test** | 6.x | Pruebas de autorización unitarias | `@WithMockUser`, `MockMvc` y `@PreAuthorize` validables sin levantar el contexto completo. |",
            "| **JaCoCo** | 0.8.11+ | Cobertura de código | Reportes XML/HTML integrables con SonarQube y GitHub Actions. |",
            "| **SonarQube** | 10.x | Análisis estático SAST | Métricas de fiabilidad, mantenibilidad, deuda técnica y vulnerabilidades. API REST para extracción automatizada. |",
            "",
            "#### CI/CD y Automatización",
            "| Herramienta | Versión | Propósito | Justificación |",
            "|---|---|---|---|",
            "| **GitHub Actions** | — | Orquestación de pipelines | Nativo del repositorio; workflows YAML versionables; integración directa con PRs e issues. |",
            "| **Docker + Docker Compose** | 24+ | Reproducibilidad de entornos | Aislamiento de dependencias; entornos idénticos en local, CI y staging. |",
            "| **Maven** | 3.9+ | Build y dependencias del backend | Gestión declarativa de dependencias; plugins de calidad (Surefire, JaCoCo, Checkstyle). |",
            "",
            "#### Gestión de Calidad y Reportes",
            "| Herramienta | Versión | Propósito | Justificación |",
            "|---|---|---|---|",
            "| **Jira** | Cloud | Gestión de defectos y tareas | API REST para creación idempotente de tickets; trazabilidad de defectos por workflow y severidad. |",
            "| **Confluence** | Cloud | Documentación y reportes | Páginas con tablas, infografías y dashboards generados automáticamente por scripts Python. |",
            "",
            "### 7.2 Puntos de Integración entre Herramientas",
            "",
            "```",
            "GitHub Actions (trigger: push / workflow_dispatch)",
            "       │",
            "       ├─► Python Scripts (WF1-WF4) ──► Gemini API (análisis multimodal)",
            "       │",
            "       ├─► Maven Build ──► SonarQube SAST ──► JaCoCo (cobertura)",
            "       │",
            "       ├─► Docker Compose ──► TestContainers (MySQL) ──► RestAssured (API tests)",
            "       │",
            "       ├─► Playwright (E2E) ──► OWASP ZAP (DAST)",
            "       │",
            "       └─► ReportWriter (Python) ──► Jira (bugs) + Confluence (dashboards)",
            "```",
        ]
        if exists:
            lines.append(f"")
            lines.append(f"> **Referencia completa:** Ver matriz detallada en `{path}`.")
        return "\n".join(lines)

    def _build_defectos(self) -> str:
        lines = [
            "## 11. Gestión de Defectos",
            "",
            "### 11.1 Ciclo de Vida de un Defecto",
            "",
            "Todo hallazgo identificado durante las actividades de SQA sigue un ciclo de vida estructurado para garantizar trazabilidad y cierre controlado:",
            "",
            "```",
            "[OPEN] ──► [TRIAGE] ──► [ASSIGNED] ──► [FIX] ──► [VERIFY] ──► [CLOSED]",
            "   │           │              │            │           │",
            "   ▼           ▼              ▼            ▼           ▼",
            "REOPENED   REJECTED      REASSIGNED   REOPENED   REJECTED FIX",
            "```",
            "",
            "| Estado | Descripción | Responsable |",
            "|---|---|---|",
            "| **OPEN** | Defecto reportado inicialmente. | Auditor SQA |",
            "| **TRIAGE** | Validación de reproducibilidad, impacto y severidad. | Líder SQA |",
            "| **ASSIGNED** | Asignación a desarrollador con fecha objetivo de corrección. | Líder SQA |",
            "| **FIX** | Corrección implementada y commit vinculado al ticket. | Desarrollador |",
            "| **VERIFY** | Re-ejecución del caso de prueba / checklist que evidenció el defecto. | Auditor SQA |",
            "| **CLOSED** | Defecto verificado como corregido; evidencia documentada. | Auditor SQA |",
            "| **REOPENED** | La verificación falla; el defecto vuelve a FIX. | Auditor SQA |",
            "| **REJECTED** | El defecto no es válido (no reproducible, comportamiento esperado, duplicado). | Líder SQA |",
            "",
            "### 11.2 Clasificación por Severidad",
            "",
            "| Severidad | Definición | Ejemplo | SLA de Respuesta | SLA de Resolución |",
            "|---|---|---|---|---|",
            "| **Crítica** | Impide la operación del sistema o expone datos sensibles. | SQL Injection en endpoint de login; fallo de autenticación JWT. | 4 horas | 24 horas |",
            "| **Alta** | Funcionalidad principal afectada con workaround complejo. | Endpoint de préstamos devuelve 500 en escenario válido. | 8 horas | 48 horas |",
            "| **Media** | Funcionalidad secundaria afectada o workaround disponible. | Error de validación en campo opcional de comentarios. | 24 horas | 5 días hábiles |",
            "| **Baja** | Defecto cosmético, typo o inconsistencia menor. | Alineación incorrecta de botón en modal de reserva. | 48 horas | 10 días hábiles |",
            "",
            "### 11.3 Gestión de Defectos por Fase",
            "",
            "- **Fase 1 (Inspección Estática):** Los defectos se detectan mediante checklists JSON aplicados a documentos PDF (ERS, DAS, Brief). Se registran en Jira con etiqueta `sqa-fase1`. No requieren fix de código. El análisis de código fuente está planificado para Fase 2.",
            "- **Fase 2 (Pruebas Dinámicas):** Los defectos se detectan mediante pruebas E2E, API, seguridad y caos sobre el código fuente. Se registran en Jira con etiqueta `sqa-fase2` y vinculan el caso de prueba fallido (Playwright trace o RestAssured log)."
            "",
            "> **Nota sobre Segunda Entrega:** El análisis de defectos de código fuente mediante pruebas dinámicas (unitarias, integración, E2E, seguridad) está planificado para la **Segunda Entrega** (Fase 2: Pruebas Dinámicas). En la Primera Entrega se limita a inspección estática, auditoría documental y generación del plan de pruebas.",
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
