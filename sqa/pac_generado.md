# Plan de Aseguramiento de Calidad (PAC)

| Campo | Valor |
|---|---|
| Proyecto | Sistema de Gestión Bibliotecaria |
| Versión | 1.0.0 |
| Backend | gestion_bibliotecaria 0.0.1-SNAPSHOT |
| Frontend | gestion-bibliotecaria 0.1.0 |

## 1. Alcance y Propósito

### 1.1 Contexto del Proyecto
Sistema web para gestión de préstamos, catálogo y usuarios de una biblioteca. (Incluye administración de reseñas, comentarios y amonestaciones por retrasos [transacciones monetarias simuladas]).

El presente Plan de Aseguramiento de Calidad (PAC) aplica al Sistema Under Test (SUT) desarrollado por el equipo de desarrollo, y será auditado por el equipo SQA asignado. El objetivo es garantizar que todos los artefactos entregados cumplan con los estándares de calidad definidos y que el producto final sea confiable, mantenible y seguro.

### 1.2 Justificación de Negocio
La gestión bibliotecaria requiere un sistema robusto que permita:
- Controlar préstamos, devoluciones y reservas de material bibliográfico.
- Administrar catálogos de libros, revistas y recursos digitales.
- Gestionar usuarios, reseñas, comentarios y amonestaciones por retrasos.
- Garantizar la trazabilidad de operaciones críticas mediante auditoría.

Un fallo en este sistema impacta directamente la operatividad de la biblioteca y la satisfacción de sus usuarios, por lo que el aseguramiento de calidad no es opcional sino un requisito crítico de negocio.

### 1.3 Límites del Alcance (IN / OUT)

**Dentro del alcance (IN):**
- Documentación de requisitos (ERS), arquitectura (DAS) y brief del proyecto.
- Configuración de infraestructura CI/CD y pipelines de despliegue.
- Checklists de inspección estática, métricas de calidad y gestión de defectos.
- Plan de pruebas estáticas (Fase 1) y dinámicas (Fase 2).
- Stack tecnológico del SUT (Java, Spring Boot, Vue) para contexto de auditoría.

**Fuera del alcance (OUT):**
- Mantenimiento evolutivo del SUT post-entrega final.
- Pruebas de carga y estrés de alto volumen (planificadas para iteraciones futuras).
- Infraestructura de producción fuera del entorno Docker definido.
- Capacitación de usuarios finales del sistema bibliotecario.

### 1.4 Relación con Otros Documentos
Este documento se vincula directamente con los siguientes artefactos del proyecto:

| Documento | Versión | Relación con el PAC |
|---|---|---|
| ERS (Especificación de Requisitos de Software) | v1.2 | Base para auditoría de requisitos (WF1) y trazabilidad de pruebas. |
| DAS (Documento de Arquitectura de Software) | v1.5 | Base para inspección arquitectónica (WF2) y validación de decisiones de diseño. |
| Brief del Proyecto | v1.1 | Define contexto de negocio y restricciones que limitan el alcance del SQA. |
| Plan de Pruebas (PP) | — | Derivado del PAC; vincula cronograma con actividades de prueba dinámica. |
| Matriz de Herramientas | Fase 2 | Declara herramientas tecnológicas y justificación técnica por atributo ISO 25010. |

Stack tecnológico detectado: Backend: Maven (21, 3.4.5). Frontend: npm / vue-cli (Vue 3.2.13).

## 2. Stack Tecnológico

### 2.1 Backend
- **Build tool:** Maven
- **Java:** 21
- **Spring Boot:** 3.4.5
- lombok (org.projectlombok)
- mysql-connector-java (mysql)
- spring-boot-starter-data-jpa (org.springframework.boot)
- spring-boot-starter-security (org.springframework.boot)
- spring-boot-starter-test (org.springframework.boot)
- spring-boot-starter-web (org.springframework.boot)

**Justificación técnica:** Java 21 ofrece mejoras de rendimiento (generational ZGC, virtual threads estables) y soporte LTS extendido. Spring Boot 3.4.x aprovecha Jakarta EE 9+, requiriendo Java 17+ como baseline. Maven fue seleccionado como build tool estándar del equipo de desarrollo, garantizando reproducibilidad de builds mediante `pom.xml` versionado.

### 2.2 Frontend
- **Build tool:** npm / vue-cli
- **Vue:** 3.2.13
- axios @1.9.0
- core-js @3.8.3
- vue @3.2.13

**Justificación técnica:** Vue 3 introduce la Composition API, mejor tree-shaking y rendimiento de reactividad con Proxy-based observation. El ecosistema npm/vue-cli facilita la integración con herramientas de prueba E2E como Playwright y la generación de bundles optimizados para despliegue.

### 2.3 Matriz de Compatibilidad de Versiones

| Componente | Versión Declarada | Versión Mínima Requerida | Estado |
|---|---|---|---|
| Java JDK | 21 | 17 | Compatible |
| Spring Boot | 3.4.5 | 3.2.x | Compatible |
| Vue.js | 3.2.13 | 3.0.0 | Compatible |
| Node.js (build) | 20+ (LTS) | 18 | Compatible |
| MySQL | 8.0 | 8.0 | Compatible |

### 2.4 Entorno de Despliegue

El SUT se despliega en contenedores Docker orchestrados mediante Docker Compose. La configuración garantiza:
- Aislamiento de dependencias (backend, frontend, base de datos).
- Reproducibilidad de entornos entre desarrollo, CI/CD y staging.
- Escalabilidad horizontal del backend mediante balanceo de carga (futuro).

| Entorno | Propósito | Infraestructura |
|---|---|---|
| Local | Desarrollo y pruebas unitarias | Docker Compose (dev profile) |
| CI/CD | Validación automática en pipeline | GitHub Actions runners (ubuntu-latest) |
| Staging | Validación pre-producción | Docker Compose (prod-like profile) |

### 2.5 Stack de Seguridad

El SUT incorpora las siguientes capas de seguridad:
- **Spring Security 6:** Autenticación JWT, autorización basada en roles (`@PreAuthorize`), protección CSRF deshabilitada por API-only.
- **Hibernate Validator:** Validación de inputs en DTOs mediante anotaciones (`@NotNull`, `@Size`, `@Email`).
- **Spring Data JPA:** Uso de queries parametrizadas para mitigar SQL Injection.
- **CORS configurado:** Orígenes permitidos restringidos al dominio del frontend.
- **Auditoría:** Tabla `auditoria` con timestamp, usuario, IP y acción realizada para trazabilidad.

## 3. Inventario de Artefactos

### 3.1 Documentación del Proyecto

La siguiente tabla lista los documentos detectados en `/documentacion`, su propósito y la fase de SQA en la que se auditan:

| Documento | Propósito | Fase de Auditoría |
|---|---|---|
| `BRIEF EQUIPO 58 1 - v1.1.pdf` | Contexto de negocio, objetivos y restricciones del proyecto. | Fase 1 — Inspección estática |
| `DAS Equipo 58-1 v1.5.pdf` | Decisiones arquitectónicas, vistas de diseño y patrones aplicados. | Fase 1 — Inspección estática |
| `Diagrama de Clases UML - Equipo 58-1.pdf` | Modelo estático del dominio: entidades, relaciones y cardinalidades. | Fase 1 — Inspección estática |
| `ERS Equipo 58 1 v.1.2.pdf` | Especificación funcional y no funcional de requisitos de software. | Fase 1 — Inspección estática |
| `Equipo 58-1_ Diagrama de contexto, contenedores y componentes (6).pdf` | Vista C4 nivel 1 y 2: contexto del sistema, contenedores y componentes. | Fase 1 — Inspección estática |

### 3.2 Mapeo Artefacto → Estándar → Checklist

| Artefacto | Estándar Aplicable | Checklist | Ruta |
|---|---|---|---|
| ERS | ISO/IEC/IEEE 29148:2018 | `sqa/checklists/ers.json` | `documentacion/ERS*.pdf` |
| DAS | ISO/IEC/IEEE 42010:2022 | `sqa/checklists/das.json` | `documentacion/DAS*.pdf` |
| Brief | Buenas prácticas SQA | `sqa/checklists/brief.json` | `documentacion/BRIEF*.pdf` |
| PAC | IEEE 730-2014 | `sqa/checklists/pac.json` | `sqa/pac_generado.md` |

## 4. Objetivos de Calidad

[FORMATEO GEMINI NO DISPONIBLE: 4. Objetivos de Calidad]

## 5. Gestión y Organización

[FORMATEO GEMINI NO DISPONIBLE: 5. Gestión y Organización]

## 6. Estándares Aplicables

### 6.1 Descripción de Estándares

El equipo SQA aplica los siguientes estándares internacionales para garantizar que cada artefacto del proyecto cumpla con criterios objetivos de calidad:

- **Objetivos de Calidad (ISO/IEC 25010):** Define atributos de calidad del producto software (funcionalidad, fiabilidad, mantenibilidad, seguridad) y sub-características medibles. Asegura que los objetivos de calidad sean explícitos, medibles y verificables.
- **Gestión y Organización:** Establece roles, responsabilidades, estrategias de validación y verificación, y estructura de gobierno del equipo SQA. Garantiza que el aseguramiento de calidad sea una actividad planificada y no reactiva.
- **Documentación, Estándares y Guías:** Norma la estructura, contenido y trazabilidad de documentos técnicos (ERS, DAS). Asegura que cada requisito y decisión arquitectónica esté identificable, rastreable y revisable.
- **Métricas y Control Estadístico:** Define principios para la medición de procesos y productos software. Establece que toda métrica debe tener definición operacional, fórmula, umbral objetivo y responsable de recolección.
- **Ejecución y Cronograma:** Vincula el PAC con el Plan de Pruebas (PP) y el cronograma del proyecto. Asegura que las actividades de SQA estén calendarizadas y que la gestión de defectos tenga un workflow definido.

### 6.2 Mapeo Artefacto → Estándar → Checklist

| Artefacto | Estándar | Checklist | Nivel de Cumplimiento |
|---|---|---|---|
| ERS | ISO/IEC/IEEE 29148:2018 | `sqa/checklists/ers.json` | Obligatorio — 100% ítems verificables |
| DAS | ISO/IEC/IEEE 42010:2022 | `sqa/checklists/das.json` | Obligatorio — 100% ítems verificables |
| Brief | Buenas prácticas SQA | `sqa/checklists/brief.json` | Recomendado — contexto de negocio validado |
| PAC | IEEE 730-2014 | `sqa/checklists/pac.json` | Obligatorio — auto-auditoría con wf6_auditor_pac.yml |

### 6.3 Niveles de Cumplimiento

- **Obligatorio:** El artefacto debe cumplir el 100% de los ítems críticos del checklist. Fallo en un ítem crítico implica rechazo del artefacto.
- **Recomendado:** El artefacto debe cumplir al menos el 80% de los ítems no críticos. Los hallazgos se documentan como observaciones sin bloqueo de entrega.
- **Informativo:** El artefacto se revisa para contexto pero no aplica checklist formal. Se utiliza para trazabilidad y justificación de alcance.

## 7. Herramientas Tecnológicas

### 7.1 Categorización de Herramientas

El equipo SQA utiliza un ecosistema de herramientas organizado por categoría funcional. A continuación se detallan las herramientas declaradas, su propósito y justificación técnica:

#### Inspección Estática y Análisis de Documentos
| Herramienta | Versión | Propósito | Justificación |
|---|---|---|---|
| **Python 3.10+** | 3.10 | Lenguaje base de scripts SQA | Tipado robusto, ecosistema maduro (PyMuPDF, Pillow, Requests), integración nativa con GitHub Actions. |
| **PyMuPDF** | 1.24+ | Extracción de texto e imágenes de PDFs | Rendimiento superior frente a pdfminer; permite renderizado de páginas a PNG para análisis visual. |
| **Pillow** | 10.0+ | Procesamiento de imágenes extraídas | Conversión, redimensión y normalización de imágenes antes de envío a modelos de visión (Gemini). |
| **Google Gemini** | v1 (API) | Generación y análisis asistido por IA | Multimodal (texto + imagen); few-shot prompts configurables; acelera auditoría de requisitos y arquitectura. |

#### Pruebas Dinámicas (Fase 2)
| Herramienta | Versión | Propósito | Justificación |
|---|---|---|---|
| **Playwright** | 1.40+ | Pruebas E2E de UI | Auto-wait, interceptación de red, generación nativa de traces/videos en CI. Reemplaza a Selenium por menor flakiness con Vue 3. |
| **RestAssured** | 5.3+ | Pruebas de integración API | Código Java versionable en repo; integrado con JUnit 5 y Maven Surefire. Reemplaza Postman/Newman en CI. |
| **TestContainers** | 1.19+ | Bases de datos reales en tests | Levanta MySQL 8 en Docker durante tests; elimina mocks que generan falsos positivos. |
| **OWASP ZAP** | 2.14+ | Pruebas de penetración DAST | Estándar open-source para análisis dinámico de seguridad. Integrable en GitHub Actions vía `zap-baseline.py`. |
| **Spring Security Test** | 6.x | Pruebas de autorización unitarias | `@WithMockUser`, `MockMvc` y `@PreAuthorize` validables sin levantar el contexto completo. |
| **JaCoCo** | 0.8.11+ | Cobertura de código | Reportes XML/HTML integrables con SonarQube y GitHub Actions. |
| **SonarQube** | 10.x | Análisis estático SAST | Métricas de fiabilidad, mantenibilidad, deuda técnica y vulnerabilidades. API REST para extracción automatizada. |

#### CI/CD y Automatización
| Herramienta | Versión | Propósito | Justificación |
|---|---|---|---|
| **GitHub Actions** | — | Orquestación de pipelines | Nativo del repositorio; workflows YAML versionables; integración directa con PRs e issues. |
| **Docker + Docker Compose** | 24+ | Reproducibilidad de entornos | Aislamiento de dependencias; entornos idénticos en local, CI y staging. |
| **Maven** | 3.9+ | Build y dependencias del backend | Gestión declarativa de dependencias; plugins de calidad (Surefire, JaCoCo, Checkstyle). |

#### Gestión de Calidad y Reportes
| Herramienta | Versión | Propósito | Justificación |
|---|---|---|---|
| **Jira** | Cloud | Gestión de defectos y tareas | API REST para creación idempotente de tickets; trazabilidad de defectos por workflow y severidad. |
| **Confluence** | Cloud | Documentación y reportes | Páginas con tablas, infografías y dashboards generados automáticamente por scripts Python. |

### 7.2 Puntos de Integración entre Herramientas

```
GitHub Actions (trigger: push / workflow_dispatch)
       │
       ├─► Python Scripts (WF1-WF4) ──► Gemini API (análisis multimodal)
       │
       ├─► Maven Build ──► SonarQube SAST ──► JaCoCo (cobertura)
       │
       ├─► Docker Compose ──► TestContainers (MySQL) ──► RestAssured (API tests)
       │
       ├─► Playwright (E2E) ──► OWASP ZAP (DAST)
       │
       └─► ReportWriter (Python) ──► Jira (bugs) + Confluence (dashboards)
```

> **Referencia completa:** Ver matriz detallada en `sqa/PACS-Fase2-Herramientas.md`.

## 8. Métricas

[FORMATEO GEMINI NO DISPONIBLE: 8. Métricas]

## 9. Análisis de Riesgos

[FORMATEO GEMINI NO DISPONIBLE: 9. Análisis de Riesgos]

## 10. Cronograma

[FORMATEO GEMINI NO DISPONIBLE: 10. Cronograma]

## 11. Gestión de Defectos

### 11.1 Ciclo de Vida de un Defecto

Todo hallazgo identificado durante las actividades de SQA sigue un ciclo de vida estructurado para garantizar trazabilidad y cierre controlado:

```
[OPEN] ──► [TRIAGE] ──► [ASSIGNED] ──► [FIX] ──► [VERIFY] ──► [CLOSED]
   │           │              │            │           │
   ▼           ▼              ▼            ▼           ▼
REOPENED   REJECTED      REASSIGNED   REOPENED   REJECTED FIX
```

| Estado | Descripción | Responsable |
|---|---|---|
| **OPEN** | Defecto reportado inicialmente. | Auditor SQA |
| **TRIAGE** | Validación de reproducibilidad, impacto y severidad. | Líder SQA |
| **ASSIGNED** | Asignación a desarrollador con fecha objetivo de corrección. | Líder SQA |
| **FIX** | Corrección implementada y commit vinculado al ticket. | Desarrollador |
| **VERIFY** | Re-ejecución del caso de prueba / checklist que evidenció el defecto. | Auditor SQA |
| **CLOSED** | Defecto verificado como corregido; evidencia documentada. | Auditor SQA |
| **REOPENED** | La verificación falla; el defecto vuelve a FIX. | Auditor SQA |
| **REJECTED** | El defecto no es válido (no reproducible, comportamiento esperado, duplicado). | Líder SQA |

### 11.2 Clasificación por Severidad

| Severidad | Definición | Ejemplo | SLA de Respuesta | SLA de Resolución |
|---|---|---|---|---|
| **Crítica** | Impide la operación del sistema o expone datos sensibles. | SQL Injection en endpoint de login; fallo de autenticación JWT. | 4 horas | 24 horas |
| **Alta** | Funcionalidad principal afectada con workaround complejo. | Endpoint de préstamos devuelve 500 en escenario válido. | 8 horas | 48 horas |
| **Media** | Funcionalidad secundaria afectada o workaround disponible. | Error de validación en campo opcional de comentarios. | 24 horas | 5 días hábiles |
| **Baja** | Defecto cosmético, typo o inconsistencia menor. | Alineación incorrecta de botón en modal de reserva. | 48 horas | 10 días hábiles |

### 11.3 Gestión de Defectos por Fase

- **Fase 1 (Inspección Estática):** Los defectos se detectan mediante checklists JSON aplicados a documentos PDF (ERS, DAS, Brief). Se registran en Jira con etiqueta `sqa-fase1`. No requieren fix de código. El análisis de código fuente está planificado para Fase 2.
- **Fase 2 (Pruebas Dinámicas):** Los defectos se detectan mediante pruebas E2E, API, seguridad y caos sobre el código fuente. Se registran en Jira con etiqueta `sqa-fase2` y vinculan el caso de prueba fallido (Playwright trace o RestAssured log).
> **Nota sobre Segunda Entrega:** El análisis de defectos de código fuente mediante pruebas dinámicas (unitarias, integración, E2E, seguridad) está planificado para la **Segunda Entrega** (Fase 2: Pruebas Dinámicas). En la Primera Entrega se limita a inspección estática, auditoría documental y generación del plan de pruebas.

## 12. CI/CD

### Workflows de GitHub Actions
| Workflow | Nombre | Trigger | Jobs |
|---|---|---|---|
| `auditoria_sqa.yml` | Auditoría Estática SQA | workflow_dispatch | auditoria-sqa |
| `wf1_auditoria_requisitos.yml` | WF1 — Auditoría Estática de Requisitos | workflow_dispatch, push | wf1-auditoria-requisitos |
| `wf2_inspeccion_arquitectura.yml` | WF2 — Inspeccion Arquitectonica y de Codigo | workflow_dispatch, push | wf2-inspeccion-arquitectura |
| `wf3_generacion_pruebas.yml` | WF3 — Generacion del Plan de Pruebas | workflow_dispatch, push | wf3-generacion-pruebas |
| `wf4_orquestador.yml` | WF4 — Orquestador de Quality Gates | workflow_dispatch, pull_request | wf4-quality-gates |
| `wf5_generador_pac.yml` | WF5 — Generador de PAC | workflow_dispatch | wf5-generador-pac |
| `wf6_auditor_pac.yml` | WF6 — Auditor de PAC | workflow_dispatch | wf6-auditor-pac |