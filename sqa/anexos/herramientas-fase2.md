# Matriz de Herramientas Tecnológicas — Anexo Técnico del PACS (Fase 2)
## Sistema de Gestión Bibliotecaria — Auditoría del Equipo 58-1

| Campo | Valor |
|---|---|
| Documento | Anexo técnico de herramientas — sub-doc de `sqa/PACS.md` §4.3 |
| Equipo SQA | Equipo 11 |
| SUT (Sistema Under Test) | Código del Equipo 58-1 (Java 21 + Spring Boot 3.4.5 / Vue 3) |
| Versión | 2.1 |
| Fecha | 2026-07-12 |
| Issue | #5 (regeneración v2.0, absorbido en PACS §4.3 — issue #6) |
| Restricción | Código fuente y documentación PDF en `/documentacion` son INTACTOS. Solo se auditan. |

> **Relación con el PACS**: este documento es el anexo técnico referenciado por [`sqa/PACS.md`](../PACS.md) §4.3. No es el PACS formal — es la matriz operativa de herramientas que el PACS absorbe por referencia.

**¿Qué es esto?**
Este documento declara las herramientas tecnológicas que el Equipo 11 utiliza para demostrar el cumplimiento de los objetivos de calidad definidos en el PAC. Incluye:
- **Fase 1 (Completa):** Inspección estática, auditoría con IA, análisis de documentos.
- **Fase 2 (En ejecución):** Pruebas dinámicas de Fiabilidad — unitarias, integración y sistema — sobre los 11 casos de `TCS-FIAB-001`, en una cadena de 5 PRs (`stacked-to-main`, issue #15).

---

## 1. Resumen Ejecutivo

Este documento declara las herramientas tecnológicas que el Equipo SQA utiliza para demostrar el cumplimiento de los objetivos de calidad definidos en el PAC. Las selecciones se basan en:

- Alineación estricta con las **sub-características de Fiabilidad de ISO/IEC 25010:2023** vigentes en [`referencias/objetivos.txt`](../referencias/objetivos.txt): **Madurez** y **Tolerancia a Fallos**.
- Compatibilidad con el **stack tecnológico existente** del SUT (Java 21, Spring Boot 3.4.5, Vue 3, MySQL en producción / H2 en CI).
- Integrabilidad con el **ecosistema 100% nativo de GitHub** (GitHub Actions, SonarCloud, GitHub Pages) — sin dependencias en plataformas externas de gestión documental o de incidencias.
- Criterio de preferencia por herramientas **"shift-left friendly"** (ejecutables en pipeline) sobre herramientas manuales o GUI-dependientes.

> **Nota metodológica:** la Fase 2 se ejecuta actualmente mediante una cadena de 5 Pull Requests encadenados (`stacked-to-main`, issue #15). El primero (configuración de JaCoCo y CI sobre H2) está abierto en PR #16; las suites de prueba correspondientes a los 11 casos de `TCS-FIAB-001` se incorporan en los PRs subsiguientes de la cadena.

---

## 2. Objetivos de Calidad del PAC (Referencia)

Los siguientes atributos y sub-características fueron definidos como objetivos de calidad en el PAC y son los ÚNICOS que esta matriz cubre:

### Calidad del Producto (ISO/IEC 25010:2023)
1. **Adecuación Funcional**
   - Completitud funcional
2. **Fiabilidad**
   - **Madurez** — grado en que el sistema satisface las necesidades de fiabilidad en operación normal (corrección de lógica crítica, ausencia de defectos, madurez de la suite de pruebas)
   - **Tolerancia a Fallos** — grado en que el sistema opera según lo previsto pese a fallos de software, incluyendo entradas inválidas
3. **Mantenibilidad**
   - Capacidad para ser probado
   - Reusabilidad
   - Analizabilidad
4. **Seguridad**
   - Confidencialidad
   - Integridad
   - Responsabilidad (trazabilidad)

> Las sub-características de Fiabilidad vigentes son **Madurez + Tolerancia a Fallos** (fuente: [`referencias/objetivos.txt`](../referencias/objetivos.txt)). La versión 1.0 de este anexo declaraba *Tolerancia a fallos + Capacidad de recuperación*; ese par fue reemplazado tras la revisión de `EST-FIAB-001` v2.0, que descarta *Capacidad de Recuperación* del alcance actual (ver §5 y §8).

### Calidad del Proceso (IEEE 730 / ISO/IEC 12207)
- Conformidad y Aseguramiento de los Procesos
- Gestión de Entornos e Infraestructura
- Medición y Mejora Continua
- Gestión de la Configuración y la Información

---

## 3. Matriz de Herramientas Declaradas

### 3.1 Calidad del Producto

| Atributo ISO 25010 | Sub-característica | Técnica de Prueba | Herramienta Declarada | Versión / Stack | Objetivo de Validación (SUT) | Justificación Técnica |
|---|---|---|---|---|---|---|
| **Adecuación Funcional** | Completitud funcional | Pruebas E2E / Sistema (UI) | **Playwright** | Node.js 20+, Chromium/Firefox/WebKit | Verificar que todos los flujos de usuario especificados existan y sean navegables: login, búsqueda de libros, préstamo, devolución, reserva, renovación. Evidencia con screenshots, videos y traces. | Vue 3 utiliza reactivity asíncrona. Selenium requiere sleeps explícitos y es propenso a flakiness. Playwright ofrece auto-wait, interceptación de red, y generación nativa de traces/videos publicables como artefactos de GitHub Actions. |
| **Adecuación Funcional** | Completitud funcional | Pruebas de Integración / API | **RestAssured** + **TestContainers** | Java 21, JUnit 5, Maven | Validar que TODOS los endpoints REST del backend respondan correctamente (crear lector, buscar libro, registrar préstamo, etc.). Validación de JSON schemas y códigos de estado HTTP. | RestAssured es código Java versionable en el repo, integrado con JUnit 5 y Maven Surefire (`mvn test`). TestContainers levanta un MySQL real en Docker durante los tests, eliminando mocks que generen falsos positivos. Postman no es adecuado para CI/CD automatizado. |
| **Fiabilidad** | Madurez — Corrección de lógica crítica y ausencia de defectos (M-01, M-02, M-03) | Pruebas unitarias (caja blanca) | **JUnit 5** + **Mockito** | JUnit Jupiter 5.10+, Mockito 5.x | Ejercitar los puntos de decisión de `PrestamoService.crearPrestamo/devolverPrestamo/renovarPrestamo` y `AmonestacionService.eliminarAmonestacion` (11 casos de `TCS-FIAB-001`, suites `regresion`/`defecto-conocido`). | JUnit 5 + Mockito son el estándar para aislar la capa de servicios; Mockito simula `PrestamoRepository`/`LibroRepository` para forzar condiciones de excepción controlada sin depender de una base de datos real. |
| **Fiabilidad** | Madurez — Cobertura de decisión/rama e instrucciones (M-02, M-04) | Cobertura de código + ejecución automatizada | **JaCoCo** + **Maven Surefire** | JaCoCo 0.8.12, Surefire 3.x | Medir cobertura de rama e instrucciones sobre `PrestamoService`/`AmonestacionService` (regla informativa `BRANCH ≥ 0.70`, `haltOnFailure=false`) y ejecutar las suites por `@Tag` en cada push. | JaCoCo genera el reporte XML/HTML consumido por `metricas/calcular_kpi.py`. Surefire ejecuta las suites `regresion` (gate) y `defecto-conocido` (informativa) e integra con `ci-tests.yml`. |
| **Fiabilidad** | Tolerancia a Fallos — Manejo de entradas inválidas (M-05) | Pruebas de integración (caja gris) | **Spring Boot Test** + **H2 Database** | Spring Boot Test 3.4.5, H2 2.x | Verificar que los endpoints rechacen entradas malformadas (fechas inválidas, cantidades negativas) sin excepción no controlada, ejercitando `@RestControllerAdvice` cuando exista. | `@SpringBootTest` + H2 in-memory (perfil `test`, `MODE=MySQL`) reproducen el stack real sin depender de un servicio MySQL en el runner de CI; ejecutan sobre la rama `simulacion-desarrollo`. |
| **Fiabilidad** | Tolerancia a Fallos — Prevención de estados inconsistentes (M-06) | Pruebas de sistema (caja negra) | **RestAssured** / **Postman** | RestAssured 5.x | Estimular endpoints ante operaciones críticas sin guarda de estado previa (inventario negativo, escritura parcial sin `@Transactional`). | RestAssured es código Java versionable, integrado a Maven/JUnit 5; complementa la verificación de precondiciones ya cubierta por las pruebas unitarias de Madurez. |
| **Mantenibilidad** | Capacidad para ser probado | Análisis ESTÁTICO + Cobertura de código | **JaCoCo** (cobertura) + **SonarCloud** (análisis estático) | Java 21, Maven | Medir el porcentaje de cobertura de pruebas sobre el código heredado. Un porcentaje bajo (< 40%) indica baja capacidad de prueba y alto riesgo de regresión. | JaCoCo genera reportes XML/HTML integrables con GitHub Actions y SonarCloud. SonarCloud calcula métricas de "testability" y "reliability". La cobertura es un proxy directo de "capacidad para ser probado". |
| **Mantenibilidad** | Reusabilidad | Análisis ESTÁTICO de arquitectura | **SonarCloud** (duplicación de código, acoplamiento) | Java 21 | Detectar lógica duplicada entre módulos (ej. préstamos vs. reservas). Medir acoplamiento entre paquetes. Identificar componentes candidatos a extracción y reutilización. | SonarCloud detecta duplicación a nivel de línea y bloque, e integra el reporte directamente en el PR vía `ci-static.yml`, sin requerir infraestructura propia. |
| **Mantenibilidad** | Analizabilidad | Análisis ESTÁTICO de complejidad | **SonarCloud** (complejidad ciclomática, cognitive complexity) + **Checkstyle** | Java 21 | Medir qué tan fácil es comprender y diagnosticar un componente. Complejidad ciclomática > 15 o cognitive complexity > 10 indican código difícil de analizar y modificar. | La complejidad ciclomática de McCabe es un indicador estándar de analizabilidad. Cognitive complexity (SonarCloud) mejora la precisión para estructuras modernas de Java. Checkstyle valida convenciones de nomenclatura y estructura. |
| **Seguridad** | Confidencialidad | Pruebas de penetración dinámica (DAST) + Pruebas de autorización | **OWASP ZAP** (DAST) + **Spring Security Test** | Java 21, Spring Security 6 | Intentar acceder a endpoints protegidos (`/api/prestamos`, `/api/admin/**`) sin token JWT o con token de rol incorrecto. Verificar que el sistema rechace accesos no autorizados (HTTP 401/403). | OWASP ZAP es el estándar open-source para DAST. Opera en modo daemon (`zap-baseline.py`) integrable en GitHub Actions. Spring Security Test permite validar la capa de autorización a nivel de pruebas unitarias de controllers con `@WithMockUser`. |
| **Seguridad** | Integridad | Pruebas de inyección + Validación de input | **OWASP ZAP** (SQL Injection, XSS) + **JUnit 5** (validaciones de bean) | Java 21, Spring Boot Validation | Inyectar payloads maliciosos (`' OR 1=1 --`, `<script>alert(1)</script>`) en campos de búsqueda y formularios. Verificar que Spring Data JPA utilice parámetros preparados y que Hibernate Validator rechace inputs inválidos. | ZAP automatiza la detección de SQLi y XSS en endpoints reales. JUnit 5 con `@Valid` y `MockMvc` valida que los DTOs rechacen datos corruptos antes de llegar a la capa de persistencia. |
| **Seguridad** | Responsabilidad (Trazabilidad) | Auditoría de logs + Validación de registros | **JUnit 5** + script Python de verificación de tabla de auditoría | Java 21, Python 3.10 | Verificar que cada acción crítica (préstamo, devolución, modificación de usuario) genere un registro inmutable en la tabla `auditoria` con timestamp, usuario, IP y acción realizada. | El backend debe persistir trazas. Los tests JUnit 5 validan que los servicios invoquen el logger de auditoría. Un script Python complementario verificará la consistencia de la tabla `auditoria` contra los logs de aplicación. |

Las filas de **Adecuación Funcional**, **Mantenibilidad** y **Seguridad** describen alcance planificado fuera del ciclo actual de Fiabilidad (issue #15); se mantienen como roadmap tecnológico del PAC, no como matriz activa de esta iteración.

### 3.2 Calidad del Proceso (IEEE 730 / ISO 12207)

| Proceso de Calidad | Actividad SQA | Herramienta / Tecnología | Objetivo | Justificación |
|---|---|---|---|---|
| **Gestión de Configuración** | Control de versiones y líneas base | **Git** + **GitHub** | Versionar código de pruebas, scripts SQA, configuraciones de pipeline y resultados de métricas. Tags para cada release del SUT. | Git es el estándar de facto. GitHub proporciona protección de ramas, PR reviews obligatorios, y releases documentadas. |
| **Gestión de Entornos e Infraestructura** | Reproducibilidad de entornos de prueba | **H2 Database** (in-memory, CI) + **Docker** (entornos locales) + **GitHub Actions Runners** | Levantar instancias reproducibles del SUT (backend + base de datos) en cada ejecución de pipeline, sin depender de un servicio MySQL externo en el runner. | H2 con perfil `test` (`MODE=MySQL`) elimina la fragilidad observada al combinar variables de entorno de un servicio MySQL con el perfil de pruebas (ver `ci-tests.yml`, issue #15 PR1). Docker sigue disponible para reproducción local con MySQL real. |
| **Medición y Mejora Continua** | Extracción y reporte de métricas | **SonarCloud API** + **JaCoCo** + `metricas/calcular_kpi.py` | Extraer métricas de calidad (cobertura, densidad de defectos, M-01..M-06) y publicar el dashboard automáticamente en GitHub Pages; registrar hallazgos de mejora como GitHub Issues (`tipo:hallazgo`/`tipo:defecto`). | SonarCloud expone métricas vía API REST integrada a `ci-static.yml`. `calcular_kpi.py` consolida los reportes de JaCoCo y Surefire en `reporte_kpi.json`, publicado por el workflow `pages-dashboard.yml`. GitHub Issues sustituye la gestión de tickets en plataformas externas. |
| **Conformidad y Aseguramiento** | Ejecución automatizada de pipelines | **GitHub Actions** (`.github/workflows/`) | Orquestar la ejecución secuencial de análisis estático, pruebas unitarias, pruebas de integración y análisis de seguridad en cada push o PR. | GitHub Actions es nativo del repositorio. Permite definir workflows YAML versionables, reutilizables, y con integración directa a GitHub Issues/PRs. |

---

## 4. Diagrama de Integración del Ecosistema

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           GITHUB ACTIONS (CI/CD)                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │   Build SUT  │→ │ SonarCloud   │→ │ JUnit 5 +    │→ │ Spring Boot  │   │
│  │   (Maven)    │  │  (SAST)      │  │ Mockito      │  │ Test + H2    │   │
│  │              │  │              │  │ (unitarias)  │  │ (integración)│   │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘   │
│         ↓                 ↓                 ↓                 ↓            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ RestAssured/ │  │   JaCoCo     │  │  Playwright  │  │   k6 (opt)   │   │
│  │  Postman     │  │ (BRANCH      │  │   (E2E)*     │  │  (Carga)*    │   │
│  │  (sistema)   │  │  ≥ 0.70)     │  │              │  │              │   │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘   │
│         ↓                 ↓                 ↓                 ↓            │
│                    ┌─────────────────────────────────────┐                  │
│                    │      SCRIPTS PYTHON (SQA Agent)     │                  │
│                    │  • Parsear resultados (JaCoCo XML,  │                  │
│                    │    Surefire XML)                     │                  │
│                    │  • Calcular métricas M-01..M-06       │                  │
│                    │    (`metricas/calcular_kpi.py`)       │                  │
│                    │  • Generar `reporte_kpi.json`         │                  │
│                    └─────────────────────────────────────┘                  │
│                               ↓                    ↓                        │
│                    ┌──────────────┐       ┌──────────────┐                  │
│                    │ GITHUB PAGES │       │ GITHUB ISSUES│                  │
│                    │  (Dashboard) │       │ (tipo:defecto│                  │
│                    │  de métricas)│       │  / hallazgo) │                  │
│                    └──────────────┘       └──────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────┘

* Playwright (E2E) y k6 (carga) son herramientas propuestas para iteraciones
  futuras fuera del alcance actual de Fiabilidad (issue #15); se declaran como
  roadmap tecnológico, no como parte de la matriz activa de esta iteración.
```

Todo el ecosistema es nativo de GitHub (Actions, SonarCloud, Pages, Issues); no depende de plataformas externas de gestión documental o de incidencias.

---

## 5. Declaración de Herramientas Descartadas

| Herramienta (sugerida genéricamente) | Razón de Descarte | Reemplazo Elegido |
|---|---|---|
| **Selenium** | Requiere sleeps explícitos, propenso a flakiness con Vue 3, sin generación nativa de traces/videos en CI. | **Playwright** |
| **Postman / Newman** (como única herramienta de sistema) | No es código versionable en el repo. Difícil de integrar con Maven/JUnit 5. Reportes limitados para CI. | **RestAssured** (con Postman como complemento manual exploratorio) |
| **JMeter** | GUI pesada, no es "CI-friendly". Reportes difíciles de parsear automáticamente. | **k6** (para futuras iteraciones de carga, fuera del alcance actual) |
| **Chaos Monkey for Spring Boot** | Sub-característica *Capacidad de Recuperación* descartada del alcance vigente en favor de Madurez (ver `EST-FIAB-001` v2.0 §8, nota de métricas retiradas). | Cobertura de decisión/rama (JaCoCo) + pruebas de excepción controlada (JUnit 5/Mockito) |
| **TestContainers para pruebas de integración de Fiabilidad** | El runner de CI no soporta un servicio MySQL estable junto al perfil `test` de Spring (conflicto de variables de entorno, ver issue #15 PR1). | **H2 Database** in-memory (`MODE=MySQL`); TestContainers se mantiene para pruebas de Adecuación Funcional (API) donde el conflicto no aplica. |
| **Pruebas Unitarias como medida de Mantenibilidad** | Las pruebas unitarias validan funcionalidad, no atributos de mantenibilidad (complejidad, acoplamiento, reusabilidad). | **SonarCloud + JaCoCo** (análisis estático + cobertura) |

---

## 6. Estado de Implementación

### Fase 1 — Infraestructura SQA (IMPLEMENTADA)

La Fase 1 está completa y aprobada. Todas las herramientas declaradas a continuación fueron desarrolladas, testeadas y documentadas por el Equipo 11.

| Actividad | Herramientas | Estado | Tests |
|---|---|---|---|
| Checklists de inspección estática | JSON + Python | Implementado | 71 ítems verificables |
| Auditoría de requisitos con IA (WF1) | Gemini multimodal | dry_run | 32 tests |
| Inspección arquitectónica (WF2) | Gemini + SonarCloud + Análisis visual | dry_run | 99 tests |
| Generación de plan de pruebas (WF3) | Gemini | dry_run | Cubierto |
| Orquestador de Quality Gates (WF4) | Python + GitHub Actions | dry_run | Cubierto |
| Extracción de imágenes de PDFs | PyMuPDF + Pillow | Implementado | Tests de extracción y conversión PNG |
| Análisis visual de diagramas | Gemini multimodal (C4/UML) | Integrado en WF2 | Tests de clasificación y análisis |
| Few-shot prompts | Constantes Python | Implementado | Tests de contenido de prompt |

**Total tests automatizados: 99 (100% pasando)**

### Fase 2 — Pruebas Dinámicas de Fiabilidad (EN EJECUCIÓN)

La Fase 2 está en ejecución mediante una cadena de 5 Pull Requests encadenados (`stacked-to-main`, issue #15). Estado actual:

| Orden | Actividad | Herramientas | Estado | Evidencia |
|---|---|---|---|---|
| PR 1/5 | Configuración de JaCoCo + migración de CI a H2 | `pom.xml` (JaCoCo check informativo, regla `BRANCH ≥ 0.70` en `PrestamoService`/`AmonestacionService`) + `ci-tests.yml` (sin servicio MySQL) | 🟢 Implementado (issue #15) | PR #16 (mergeado 2026-07-08) |
| — | Especificación de 11 casos de prueba | `TCS-FIAB-001` (JUnit 5 + Mockito, mapeados a M-01..M-06) | 🟢 Especificados | [`2026-06-24_especificacion-casos-prueba-fiabilidad.md`](../fase2/planificacion/2026-06-24_especificacion-casos-prueba-fiabilidad.md) — 11 filas `TC-FIAB-*` |
| PR 2-3/5 | Implementar pruebas unitarias e integración (Madurez + Tolerancia a Fallos) | JUnit 5, Mockito, Spring Boot Test, H2 | 🟢 Implementado | [`src/test/java/com/biblioteca/unit/`](../../src/test/java/com/biblioteca/unit) (5 clases, 15 métodos de prueba) e [`integration/`](../../src/test/java/com/biblioteca/integration) (4 clases, 4 métodos de prueba), ejecutadas por `ci-tests.yml` |
| PR 4/5 | Implementar pruebas de sistema | Spring Boot Test + MockMvc (desvío respecto de RestAssured / Postman, ver `PACS.md` §5.1) | 🟢 Implementado | [`src/test/java/com/biblioteca/system/`](../../src/test/java/com/biblioteca/system) (3 clases, 8 métodos de prueba) |
| PR 5/5 | Consolidar métricas M-01..M-06 y publicar dashboard | `metricas/calcular_kpi.py` → `reporte_kpi.json` + GitHub Pages (`pages-dashboard.yml`) | 🟢 Implementado | [Dashboard publicado](https://odjaramillo.github.io/gestion-bibliotecaria-sqa/), desplegado en cada push a `main` (issue #27, PR #28) |

> **Nota sobre los grupos de prueba**: la suite dinámica se ejecuta en dos universos `@Tag` — `regresion` (gate de integración, base de la cobertura JaCoCo y de M-03) y `defecto-conocido` (pruebas que codifican defectos reales del SUT congelado y fallan de forma esperada; se ejecutan de modo informativo). El desglose por clase está en [`sqa/PACS.md`](../PACS.md) §5.1.

El único nivel dinámico aún ausente es el de **aceptación** (Playwright), planificado en el [issue #34](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/34).

---

## 7. Glosario de Métricas M-01..M-06

Marco vigente de sub-características **Madurez + Tolerancia a Fallos** (ISO/IEC 25010:2023, medición ISO/IEC 25023:2016). Fuente primaria: [`referencias/objetivos.txt`](../referencias/objetivos.txt); la métrica M-04 (cobertura de instrucciones) extiende ese marco per `EST-FIAB-001` v2.0 §8, ya adoptada por los 11 casos de `TCS-FIAB-001`.

| ID | Métrica | Sub-característica | Fórmula | Umbral | Fuente |
|---|---|---|---|---|---|
| M-01 | Densidad de Defectos de Fiabilidad | Madurez — Ausencia de defectos | Defectos confirmados por ejecución / Módulos (o KLOC) bajo prueba | Bueno: 0–1.0 · Regular: 1.1–2.0 · Malo: > 2.0 [PROP] | `objetivos.txt` atributo 1.2 + `EST-FIAB-001` §8 |
| M-02 | Cobertura de Decisión/Rama | Madurez — Corrección de lógica crítica | (Ramas ejercitadas / Ramas totales en métodos críticos) × 100 | ≥ 70% [PROP] | `objetivos.txt` atributo 1.1 |
| M-03 | Tasa de Pruebas que Pasan | Madurez — Madurez de la suite | (Pruebas `regresion` exitosas / Pruebas `regresion` ejecutadas) × 100 | 100% en verde para integrar a `main` [PROP] | `objetivos.txt` atributo 1.3 |
| M-04 | Cobertura de Instrucciones JaCoCo | Madurez — soporte | (Instrucciones cubiertas / Total de instrucciones) × 100 | ≥ 60% [PROP] | `EST-FIAB-001` §8 (extiende `objetivos.txt`) |
| M-05 | Entradas Inválidas Controladas | Tolerancia a Fallos — Manejo de entradas inválidas | (Casos inválidos manejados sin excepción no controlada / Casos inválidos probados) × 100 | ≥ 80% [PROP] | `objetivos.txt` atributo 2.1 |
| M-06 | Operaciones con Guarda de Estado | Tolerancia a Fallos — Prevención de estados inconsistentes | (Operaciones críticas con validación de precondición / Operaciones críticas totales) × 100 | ≥ 80% [PROP] | `objetivos.txt` atributo 2.2 |

Fuente de datos por métrica: JaCoCo (M-02, M-04), Maven Surefire (M-01, M-03, M-05, M-06 vía suites `regresion`/`defecto-conocido`), revisión manual complementaria para M-06. Los umbrales marcados `[PROP]` son propuestas conservadoras a confirmar por el Líder de Métricas / Líder General.

> **Nota de consistencia**: esta numeración M-01..M-06 replica exactamente la de `EST-FIAB-001` v2.0 §8 y `PP-FIAB-001`, ya en uso por los 11 casos de `TCS-FIAB-001`. La tabla de `sqa/PACS.md` §5.2 usa una numeración distinta para las mismas seis métricas (asigna M-01 a Cobertura de Decisión y M-06 a Cobertura de Instrucciones); esa discrepancia es preexistente al alcance de esta regeneración — B-02 (issue #5) solo autoriza editar `PACS.md` §4.3 — y queda documentada como pendiente de corrección en una iteración posterior (ver apply-progress de `pacs-formal-consolidado-f1-f2`).

---

## 8. Control de Versiones

| Versión | Fecha | Autor | Cambios |
|---|---|---|---|
| 1.0 | 2026-05-06 | Equipo SQA | Declaración inicial de herramientas. Incluye Fase 1 (implementada) y Fase 2 (planificada, sub-características Tolerancia a fallos + Capacidad de recuperación). Documenta 99 tests pasando. Referencia plataformas externas de reporte (reemplazadas en v2.0). |
| 2.0 | 2026-07-08 | Equipo SQA | Regeneración (issue #5): sub-características Fiabilidad actualizadas a **Madurez + Tolerancia a Fallos** (ISO/IEC 25010:2023, alineado a `objetivos.txt`/`EST-FIAB-001`); matriz de herramientas de Fiabilidad reescrita (JUnit 5, Mockito, H2, JaCoCo, Maven Surefire, RestAssured/Postman, Spring Boot Test, GitHub Actions); diagrama de integración 100% nativo de GitHub; Fase 2 actualizada a **EN EJECUCIÓN** (issue #15, PR #16 abierto); glosario de métricas reemplazado por M-01..M-06 con fórmulas, umbrales `[PROP]` y fuentes; eliminadas todas las referencias a plataformas externas de reporte de incidencias y documentación. |
| 2.1 | 2026-07-12 | Equipo SQA | Sincronización del estado declarado con el repositorio (issue #33): roadmap de Fase 2 — PR 1/5 (mergeado), PR 2-3/5, PR 4/5 y PR 5/5 pasan a **🟢 Implementado**, con enlace a los tests y al dashboard; el nivel de sistema declara MockMvc como herramienta real (desvío respecto de RestAssured / Postman, registrado en `PACS.md` §5.1); nota sobre los universos `regresion` / `defecto-conocido`; aceptación (Playwright) queda como único nivel dinámico pendiente (issue #34). |

---

**Fin del Documento**
