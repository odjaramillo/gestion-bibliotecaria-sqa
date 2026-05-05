# Matriz de Herramientas Tecnológicas — Fase 2: Pruebas Dinámicas
## Plan de Aseguramiento de la Calidad (PAC) — Sistema de Gestión Bibliotecaria
**Equipo SQA:** Equipo 11  
**SUT:** Código legado del Equipo 58-1 (Java 21 + Spring Boot 3.4.5 / Vue 3)  
**Documento:** Declaración de herramientas para el entregable "Infograma del Ecosistema Tecnológico"  
**Fase de ejecución:** Fase 2 (Shift-Right / Pruebas Dinámicas)  
**Restricción:** Código fuente heredado y documentación PDF en `/documentacion` son INTACTOS. Solo se auditan.

---

## 1. Resumen Ejecutivo

Este documento declara las herramientas tecnológicas que el Equipo SQA utilizará para demostrar el cumplimiento de los objetivos de calidad definidos en el PAC. Las selecciones se basan en:

- Alineación estricta con los **atributos y sub-características ISO 25010** definidos en el PAC.
- Compatibilidad con el **stack tecnológico existente** del SUT (Java 21, Spring Boot, Vue 3, MySQL).
- Integrabilidad con el **ecosistema CI/CD** (GitHub Actions) y las plataformas de reporte (Jira, Confluence).
- Criterio de preferencia por herramientas **"shift-left friendly"** (ejecutables en pipeline) sobre herramientas manuales o GUI-dependientes.

> **Nota metodológica:** Las herramientas declaradas en esta matriz serán ejecutadas en la Fase 2. En la Entrega 1 (Fase 1) solo se presenta esta planificación y la infraestructura base (pipelines, contenedores, configuración de herramientas).

---

## 2. Objetivos de Calidad del PAC (Referencia)

Los siguientes atributos y sub-características fueron definidos como objetivos de calidad en el PAC y son los ÚNICOS que esta matriz cubre:

### Calidad del Producto (ISO/IEC 25010)
1. **Adecuación Funcional**
   - Completitud funcional
2. **Fiabilidad**
   - Tolerancia a fallos
   - Capacidad de recuperación
3. **Mantenibilidad**
   - Capacidad para ser probado
   - Reusabilidad
   - Analizabilidad
4. **Seguridad**
   - Confidencialidad
   - Integridad
   - Responsabilidad (trazabilidad)

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
| **Adecuación Funcional** | Completitud funcional | Pruebas E2E / Sistema (UI) | **Playwright** | Node.js 20+, Chromium/Firefox/WebKit | Verificar que todos los flujos de usuario especificados existan y sean navegables: login, búsqueda de libros, préstamo, devolución, reserva, renovación. Evidencia con screenshots, videos y traces. | Vue 3 utiliza reactivity asíncrona. Selenium requiere sleeps explícitos y es propenso a flakiness. Playwright ofrece auto-wait, interceptación de red, y generación nativa de traces/videos en CI, esenciales para reportes en Confluence. |
| **Adecuación Funcional** | Completitud funcional | Pruebas de Integración / API | **RestAssured** + **TestContainers** | Java 21, JUnit 5, Maven | Validar que TODOS los endpoints REST del backend respondan correctamente (crear lector, buscar libro, registrar préstamo, etc.). Validación de JSON schemas y códigos de estado HTTP. | RestAssured es código Java versionable en el repo, integrado con JUnit 5 y Maven Surefire (`mvn test`). TestContainers levanta un MySQL real en Docker durante los tests, eliminando mocks que generen falsos positivos. Postman no es adecuado para CI/CD automatizado. |
| **Fiabilidad** | Tolerancia a fallos | Pruebas de caos / Robustez | **Chaos Monkey for Spring Boot** (o tests de excepciones JUnit 5) | Spring Boot 3.4.5, Java 21 | Simular fallos de infraestructura (caída de conexión a MySQL, timeout de servicios). Verificar que el sistema loguee errores apropiadamente y no exponga stack traces o datos sensibles al usuario final. | Chaos Monkey es el estándar de facto para pruebas de caos en ecosistemas Spring Boot. Si la complejidad lo requiere, se complementará con tests JUnit 5 que inyecten `DataAccessException` y validen el comportamiento de los controllers. |
| **Fiabilidad** | Capacidad de recuperación | Pruebas de recuperación de datos | **JUnit 5** + **TestContainers** + script de verificación de consistencia | Java 21, MySQL 8.0 | Insertar un préstamo → forzar interrupción del contenedor MySQL → restablecer servicio → verificar que los datos afectados se recuperen o que el sistema detecte y reporte la inconsistencia. | TestContainers permite crear escenarios de "matar y revivir" la base de datos en segundos. Se valida tanto la persistencia de datos como la capacidad del sistema de reanudar operaciones sin corrupción. |
| **Mantenibilidad** | Capacidad para ser probado | Análisis ESTÁTICO + Cobertura de código | **JaCoCo** (cobertura) + **SonarQube** (análisis estático) | Java 21, Maven | Medir el porcentaje de cobertura de pruebas sobre el código heredado. Un porcentaje bajo (< 40%) indica baja capacidad de prueba y alto riesgo de regresión. | JaCoCo genera reportes XML/HTML integrables con GitHub Actions y SonarQube. SonarQube calcula métricas de "testability" y "reliability". La cobertura es un proxy directo de "capacidad para ser probado". |
| **Mantenibilidad** | Reusabilidad | Análisis ESTÁTICO de arquitectura | **SonarQube** (duplicación de código, acoplamiento) + **JDepend** (métricas de paquetes) | Java 21 | Detectar lógica duplicada entre módulos (ej. préstamos vs. reservas). Medir acoplamiento aferente (Ca) y eferente (Ce) entre paquetes. Identificar componentes candidatos a extracción y reutilización. | SonarQube detecta duplicación a nivel de línea y bloque. JDepend analiza la estructura de dependencias entre paquetes. Un alto acoplamiento eferente y bajo acoplamiento aferente indican baja reusabilidad. |
| **Mantenibilidad** | Analizabilidad | Análisis ESTÁTICO de complejidad | **SonarQube** (complejidad ciclomática, cognitive complexity) + **Checkstyle** | Java 21 | Medir qué tan fácil es comprender y diagnosticar un componente. Complejidad ciclomática > 15 o cognitive complexity > 10 indican código difícil de analizar y modificar. | La complejidad ciclomática de McCabe es un indicador estándar de analizabilidad. Cognitive complexity (SonarQube) mejora la precisión para estructuras modernas de Java. Checkstyle valida convenciones de nomenclatura y estructura. |
| **Seguridad** | Confidencialidad | Pruebas de penetración dinámica (DAST) + Pruebas de autorización | **OWASP ZAP** (DAST) + **Spring Security Test** | Java 21, Spring Security 6 | Intentar acceder a endpoints protegidos (`/api/prestamos`, `/api/admin/**`) sin token JWT o con token de rol incorrecto. Verificar que el sistema rechace accesos no autorizados (HTTP 401/403). | OWASP ZAP es el estándar open-source para DAST. Opera en modo daemon (`zap-baseline.py`) integrable en GitHub Actions. Spring Security Test permite validar la capa de autorización a nivel de pruebas unitarias de controllers con `@WithMockUser`. |
| **Seguridad** | Integridad | Pruebas de inyección + Validación de input | **OWASP ZAP** (SQL Injection, XSS) + **JUnit 5** (validaciones de bean) | Java 21, Spring Boot Validation | Inyectar payloads maliciosos (`' OR 1=1 --`, `<script>alert(1)</script>`) en campos de búsqueda y formularios. Verificar que Spring Data JPA utilice parámetros preparados y que Hibernate Validator rechace inputs inválidos. | ZAP automatiza la detección de SQLi y XSS en endpoints reales. JUnit 5 con `@Valid` y `MockMvc` valida que los DTOs rechacen datos corruptos antes de llegar a la capa de persistencia. |
| **Seguridad** | Responsabilidad (Trazabilidad) | Auditoría de logs + Validación de registros | **JUnit 5** + script Python de verificación de tabla de auditoría | Java 21, Python 3.10 | Verificar que cada acción crítica (préstamo, devolución, modificación de usuario) genere un registro inmutable en la tabla `auditoria` con timestamp, usuario, IP y acción realizada. | El backend debe persistir trazas. Los tests JUnit 5 validan que los servicios invoquen el logger de auditoría. Un script Python complementario verificará la consistencia de la tabla `auditoria` contra los logs de aplicación. |

### 3.2 Calidad del Proceso (IEEE 730 / ISO 12207)

| Proceso de Calidad | Actividad SQA | Herramienta / Tecnología | Objetivo | Justificación |
|---|---|---|---|---|
| **Gestión de Configuración** | Control de versiones y líneas base | **Git** + **GitHub** | Versionar código de pruebas, scripts SQA, configuraciones de pipeline y resultados de métricas. Tags para cada release del SUT. | Git es el estándar de facto. GitHub proporciona protección de ramas, PR reviews obligatorios, y releases documentadas. |
| **Gestión de Entornos e Infraestructura** | Reproducibilidad de entornos de prueba | **Docker** + **Docker Compose** + **GitHub Actions Runners** | Levantar instancias idénticas del SUT (backend + frontend + MySQL) en cada ejecución de pipeline. | Docker garantiza que las pruebas corran en el mismo entorno en local y en CI. TestContainers (sobre Docker) gestiona el ciclo de vida de las dependencias. |
| **Medición y Mejora Continua** | Extracción y reporte de métricas | **SonarQube API** + **JaCoCo** + **Scripts Python** (Jira/Confluence API) | Extraer métricas de calidad (cobertura, deuda técnica, defectos) y publicar dashboards automáticos en Confluence. Crear tickets de mejora en Jira. | SonarQube expone métricas vía REST API. Scripts Python orquestan la recolección y transforman los datos a formatos Markdown/HTML para Confluence. Jira API crea tickets de tech-debt automatizados. |
| **Conformidad y Aseguramiento** | Ejecución automatizada de pipelines | **GitHub Actions** (`.github/workflows/`) | Orquestar la ejecución secuencial de análisis estático, pruebas unitarias, pruebas de integración, E2E, y análisis de seguridad en cada push o PR. | GitHub Actions es nativo del repositorio. Permite definir workflows YAML versionables, reutilizables, y con integración directa a GitHub Issues/PRs. |

---

## 4. Diagrama de Integración del Ecosistema (Mapeo para el Infograma)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           GITHUB ACTIONS (CI/CD)                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │   Build SUT  │→ │ SonarQube    │→ │ Unit Tests   │→ │ RestAssured  │   │
│  │   (Maven)    │  │ (SAST)       │  │ (JUnit 5)    │  │ + TestCont.  │   │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘   │
│         ↓                 ↓                 ↓                 ↓            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │  Playwright  │  │ OWASP ZAP    │  │   JaCoCo     │  │   k6 (opt)   │   │
│  │   (E2E)      │  │   (DAST)     │  │ (Cobertura)  │  │  (Carga)*    │   │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘   │
│         ↓                 ↓                 ↓                 ↓            │
│                    ┌─────────────────────────────────────┐                  │
│                    │      SCRIPTS PYTHON (SQA Agent)     │                  │
│                    │  • Parsear resultados (JSON/XML)    │                  │
│                    │  • Calcular métricas (Densidad      │                  │
│                    │    de Defectos, Cobertura)          │                  │
│                    │  • Generar Markdown/HTML            │                  │
│                    └─────────────────────────────────────┘                  │
│                               ↓                    ↓                        │
│                    ┌──────────────┐       ┌──────────────┐                  │
│                    │  CONFLUENCE  │       │    JIRA      │                  │
│                    │  (Reportes)  │       │ (Bugs/Tech   │                  │
│                    │              │       │    Debt)     │                  │
│                    └──────────────┘       └──────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────┘

* k6 es herramienta propuesta para iteraciones futuras de Eficiencia de Desempeño.
  No está en el PAC actual pero se declara como roadmap tecnológico.
```

---

## 5. Declaración de Herramientas Descartadas

| Herramienta (sugerida genéricamente) | Razón de Descarte | Reemplazo Elegido |
|---|---|---|
| **Selenium** | Requiere sleeps explícitos, propenso a flakiness con Vue 3, sin generación nativa de traces/videos en CI. | **Playwright** |
| **Postman / Newman** | No es código versionable en el repo. Difícil de integrar con Maven/JUnit 5. Reportes limitados para CI. | **RestAssured** |
| **JMeter** | GUI pesada, no es "CI-friendly". Reportes difíciles de parsear automáticamente. | **k6** (para futuras iteraciones de carga) |
| **Pruebas Unitarias como medida de Mantenibilidad** | Las pruebas unitarias validan funcionalidad, no atributos de mantenibilidad (complejidad, acoplamiento, reusabilidad). | **SonarQube + JaCoCo** (análisis estático + cobertura) |

---

## 6. Roadmap de Implementación (Fase 2)

| Orden | Actividad | Herramientas | Entregable en Confluence |
|---|---|---|---|
| 1 | Configurar análisis estático y cobertura | SonarQube + JaCoCo | Dashboard de Mantenibilidad (Complejidad, Duplicación, Cobertura) |
| 2 | Implementar pruebas de API | RestAssured + TestContainers | Reporte de Completitud Funcional (API) con % de endpoints cubiertos |
| 3 | Implementar pruebas E2E | Playwright | Reporte de Completitud Funcional (UI) con videos de flujos críticos |
| 4 | Ejecutar pruebas de seguridad | OWASP ZAP + Spring Security Test | Informe de Vulnerabilidades (DAST + SAST) |
| 5 | Ejecutar pruebas de fiabilidad | Chaos Monkey / TestContainers de recuperación | Informe de Tolerancia a Fallos y Recuperación |
| 6 | Consolidar métricas | Scripts Python | Informe de Pruebas (IP) con Densidad de Defectos y Cobertura de Revisiones |

---

## 7. Glosario de Métricas a Calcular

| Métrica | Fórmula | Herramienta Fuente | Propósito |
|---|---|---|---|
| **Densidad de Defectos** | Defectos Encontrados / Tamaño del SUT (KLOC o puntos de función) | SonarQube (LOC) + Jira (defectos) | Medir la calidad intrínseca del código heredado. |
| **Cobertura de Revisiones** | Artefactos Revisados / Artefactos Totales | GitHub (PRs) + Scripts SQA | Medir qué porcentaje del SUT ha sido auditado. |
| **Cobertura de Código** | Líneas Ejecutadas en Tests / Líneas Totales | JaCoCo | Medir la capacidad de prueba del código. |
| **Deuda Técnica** | Días estimados para remediar code smells | SonarQube | Medir el esfuerzo futuro requerido para mantener el SUT. |
| **Índice de Vulnerabilidades** | Vulnerabilidades Críticas + Altas / Total de dependencias | OWASP Dependency-Check + SonarQube | Medir el riesgo de seguridad del ecosistema. |

---

## 8. Control de Versiones

| Versión | Fecha | Autor | Cambios |
|---|---|---|---|
| 1.0 | 2026-05-04 | Equipo SQA | Declaración inicial de herramientas basada en análisis del stack del Equipo 58-1. |

---

**Fin del Documento**
