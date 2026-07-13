# PACS formal consolidado F1+F2

| Campo | Valor |
|---|---|
| Documento | Plan de Aseguramiento de la Calidad del Software (PACS) |
| Identificador | PACS-CONSOLIDADO-001 |
| Versión | 1.2 |
| Fecha de emisión | 2026-07-12 |
| Estado | Emitido |
| Organización emisora | Equipo SQA T 11 — Proyecto 16 (Turno Tarde) |
| Autoridad de aprobación | Líder General (Alberto Rodriguez) |
| SUT (Sistema bajo prueba) | Sistema de Gestión Bibliotecaria — Equipo 58-1 (Java 21 + Spring Boot 3.4.5 / Vue 3) |
| Estándar estructural | IEEE Std 730-2014 §Clause 5 (SQAP Outline) |
| Issue de origen | [#6](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/6) |

## Tabla de contenido

- [§1. Propósito y alcance](#1-propósito-y-alcance)
- [§2. Definiciones y acrónimos](#2-definiciones-y-acrónimos)
- [§3. Documentos de referencia](#3-documentos-de-referencia)
- [§4. Visión general del plan SQA](#4-visión-general-del-plan-sqa)
  - [§4.1 Organización e independencia](#41-organización-e-independencia)
  - [§4.2 Riesgos de producto y de proyecto](#42-riesgos-de-producto-y-de-proyecto)
  - [§4.3 Herramientas](#43-herramientas)
  - [§4.4 Estándares, prácticas y convenciones](#44-estándares-prácticas-y-convenciones)
  - [§4.5 Esfuerzo, recursos y cronograma](#45-esfuerzo-recursos-y-cronograma)
- [§5. Actividades, resultados y tareas](#5-actividades-resultados-y-tareas)
  - [§5.1 Aseguramiento de producto](#51-aseguramiento-de-producto)
  - [§5.2 Aseguramiento de proceso](#52-aseguramiento-de-proceso)
- [§6. Consideraciones adicionales](#6-consideraciones-adicionales)
  - [§6.1 Revisión de contrato](#61-revisión-de-contrato)
  - [§6.2 Medición de calidad](#62-medición-de-calidad)
  - [§6.3 Dispensas y desviaciones](#63-dispensas-y-desviaciones)
  - [§6.4 Repetición de tareas](#64-repetición-de-tareas)
  - [§6.5 Riesgo de realizar el SQA](#65-riesgo-de-realizar-el-sqa)
  - [§6.6 Estrategia de comunicaciones](#66-estrategia-de-comunicaciones)
  - [§6.7 Proceso de no conformidades](#67-proceso-de-no-conformidades)
- [§7. Registros SQA](#7-registros-sqa)
  - [§7.1 Analizar, identificar, recopilar, archivar, mantener y disponer](#71-analizar-identificar-recopilar-archivar-mantener-y-disponer)
  - [§7.2 Disponibilidad de los registros](#72-disponibilidad-de-los-registros)
- [Control de versiones](#control-de-versiones)

---

## Prólogo

Este documento consolida en un único contenedor formal el Plan de Aseguramiento de la Calidad del Software (PACS) del Equipo 11 sobre el Sistema de Gestión Bibliotecaria del Equipo 58-1, integrando el trabajo de Fase 1 (técnicas estáticas sobre requisitos y arquitectura) y Fase 2 (técnicas estáticas a código y técnicas dinámicas sobre fiabilidad). Sigue la estructura mandatoria de IEEE Std 730-2014 §Clause 5, cuya conformidad — según §1.5.2 del propio estándar — se logra satisfaciendo los requisitos normativos ("shall") de esa cláusula.

Antes de esta versión, el ecosistema SQA disponía de aproximaciones parciales — la matriz de herramientas (`anexos/herramientas-fase2.md`, renombrada y absorbida como anexo técnico de este PACS), el reporte de migración (`REPORTE-ECOSISTEMA.md`) y el estado vivo del ecosistema (`ECOSISTEMA-ESTADO.md`) — pero ningún documento cumplía el rol de contenedor formal único. Esta versión (v1.0) resuelve esa ausencia estructural y ancla en un mismo lugar los apéndices pendientes de mayor peso en la rúbrica (infograma del ecosistema, reflexión crítica y dashboard de métricas de proceso), que se incorporarán como issues hijos de este documento.

La versión de Fase 1 entregada originalmente no contaba con un contenedor PACS conforme a IEEE 730. Esta versión mejora esa entrega al aportar la estructura normativa exigida, sin alterar el contenido técnico ya evaluado. Conforme al enunciado de Fase 2 (línea 54), un Plan de Aseguramiento de la Calidad que incorpore lo planificado en la primera entrega puede habilitar una reconsideración de la nota de Fase 1; este PACS aporta la evidencia estructural correspondiente — la decisión de reconsiderar queda a criterio exclusivo del docente.

---

## §1. Propósito y alcance

El propósito de este PACS es declarar, de forma centralizada y verificable, el conjunto de actividades, técnicas, herramientas, métricas, roles y registros que el Equipo 11 aplica para asegurar la calidad del Sistema de Gestión Bibliotecaria desarrollado por el Equipo 58-1, en las dos fases evaluadas del curso Aseguramiento de la Calidad del Software.

En **Fase 1**, el alcance cubre técnicas estáticas de inspección aplicadas sobre los artefactos de especificación y diseño del SUT: la Especificación de Requisitos de Software (ERS) y el Documento de Arquitectura de Software (DAS), mediante un checklist maestro de 75 ítems (`fase1/Checklists-Inspeccion-Estatica-v1.md`).

En **Fase 2**, el alcance se extiende a técnicas estáticas aplicadas directamente sobre el código fuente (walkthrough técnico guiado por el autor y auditoría asistida con IA) y a técnicas dinámicas centradas en la característica de calidad **Fiabilidad** (ISO/IEC 25010:2023), particularmente en las sub-características **Madurez** y **Tolerancia a Fallos**, sobre los servicios `PrestamoService`, `LibroService`, `UsuarioService` y `AmonestacionService` del backend.

Quedan fuera de alcance de este PACS: la reescritura de los documentos de Fase 2 ya entregados (se referencian tal cual desde §5.1), la implementación de las pruebas dinámicas en sí (bloqueador externo — ver §6.5), y la elaboración del infograma, la reflexión crítica y el dashboard automatizado, que son apéndices hijos anclados a este documento pero no forman parte de su contenido.

---

## §2. Definiciones y acrónimos

| Acrónimo | Significado | Referencia |
|---|---|---|
| SQA | Software Quality Assurance — Aseguramiento de la Calidad del Software | IEEE 730-2014 |
| SUT | System Under Test — Sistema bajo prueba (Gestión Bibliotecaria, Equipo 58-1) | Enunciados F1/F2 |
| PACS | Plan de Aseguramiento de la Calidad del Software (este documento) | IEEE 730-2014 §Clause 5 |
| SQAP | Software Quality Assurance Plan — nombre normativo de IEEE 730 para el PACS | IEEE 730-2014 |
| SQA records | Registros de aseguramiento de calidad (issues, PRs, reportes, actas) | IEEE 730-2014 §7 |
| PAA | Plan de Aseguramiento Académico — término del enunciado equivalente al PACS entregable | Enunciado F1 |
| GQM | Goal-Question-Metric — marco de definición de métricas de proceso | `metricas/calcular_kpi.py` |
| KPI | Key Performance Indicator — indicador clave calculado por sprint | `referencias/objetivos.txt` |
| RIE | Identificador de riesgo (Producto `RIE-P0N` / Proyecto `RIE-J0N`) | §4.2 de este documento |
| WT | Walkthrough Finding — hallazgo del walkthrough técnico (`WT-01`..`WT-06`) | `fase2/estaticas/2026-06-02_walkthrough-fiabilidad-sut-biblioteca.md` |

El marco vigente de métricas M-01..M-06 referidas en este glosario está definido íntegramente en [`referencias/objetivos.txt`](referencias/objetivos.txt).

---

## §3. Documentos de referencia

| Estándar / Documento | Versión | Ubicación |
|---|---|---|
| ERS — Especificación de Requisitos del Software (Equipo 58-1) | v1.2 | [`documentacion/ERS Equipo 58 1 v.1.2.pdf`](../documentacion/ERS%20Equipo%2058%201%20v.1.2.pdf) |
| DAS — Documento de Arquitectura de Software (Equipo 58-1) | v1.5 | [`documentacion/DAS Equipo 58-1 v1.5.pdf`](../documentacion/DAS%20Equipo%2058-1%20v1.5.pdf) |
| IEEE Std 730 | 2014 | [`referencias/IEEE 730/REFERENCIA-PARA-PACS.md`](referencias/IEEE%20730/REFERENCIA-PARA-PACS.md) (mapeo estructural, sin texto del estándar por licencia) |
| ISO/IEC 25010 | 2023 | Citado en [`referencias/objetivos.txt`](referencias/objetivos.txt) y en los documentos de Fase 2 |
| ISO/IEC/IEEE 29119-3 | 2021 | [`fase2/planificacion/2026-06-09_plan-de-pruebas-fiabilidad.md`](fase2/planificacion/2026-06-09_plan-de-pruebas-fiabilidad.md) |
| ISO/IEC/IEEE 12207 | 2008 | Citado en [`REPORTE-ECOSISTEMA.md`](REPORTE-ECOSISTEMA.md) (estándares de referencia) |
| ISO/IEC/IEEE 42010 | 2011 | Citado en [`REPORTE-ECOSISTEMA.md`](REPORTE-ECOSISTEMA.md) (estándares de referencia) |
| ISO/IEC/IEEE 15289 | 2019 | [`referencias/IEEE 730/REFERENCIA-PARA-PACS.md`](referencias/IEEE%20730/REFERENCIA-PARA-PACS.md) §4 y documentos de Fase 2 (estructura de contenido) |

---

## §4. Visión general del plan SQA

### §4.1 Organización e independencia

| Rol F1 | Rol F2 | Etiqueta `rol:*` | Responsable | Independencia |
|---|---|---|---|---|
| Líder General | Líder General | `rol:lider-gral` | Alberto Rodriguez | N/A — autoridad máxima del proceso SQA; aprueba entregables antes de la entrega al Equipo 58-1 |
| Líder Tecnológico | DevOp | `rol:lider-tec` | Oscar Jaramillo (F1) / Daniel Cohen (F2) | Media — mismo rol técnico, distinto responsable según la fase |
| Líder Funcional | — | *(sin etiqueta `rol:*` dedicada)* | Daniel Cohen (F1) | N/A — rol de dominio funcional; no genera artefactos SQA trazables por Pull Request |
| Líder de Métricas | Líder de Métricas | `rol:metricas` | Edwin Li | Alta — calcula y reporta M-01..M-06 sin intermediación del Líder General |
| Escriba | Escriba | `rol:escriba` | Samuel Artiles | Alta — documenta hallazgos de forma independiente de quien los origina |
| — | Analista de Pruebas / Tester | `rol:tester` | Oscar Jaramillo (F2) | Alta — diseña casos de prueba sin intervenir en la implementación del SUT |

> **Nota de trazabilidad de etiquetas**: las etiquetas `rol:*` de esta tabla son exactamente las cinco definidas y operativas en `.github/labels.yml` (`rol:lider-gral`, `rol:lider-tec`, `rol:tester`, `rol:metricas`, `rol:escriba`). El rol de Líder Funcional no cuenta con etiqueta dedicada porque no produce artefactos SQA versionados que requieran trazabilidad por Pull Request.

La independencia organizativa del proceso SQA se sostiene en la separación completa entre **Equipo 11 (SQA)**, responsable de diseñar, ejecutar y documentar las actividades de aseguramiento de calidad descritas en este PACS, y **Equipo 58-1 (autor SUT)**, responsable exclusivo de la implementación del Sistema de Gestión Bibliotecaria bajo prueba. Ningún integrante del Equipo 11 participa en el desarrollo del código de producción del SUT, y el código fuente permanece congelado durante la Fase 2 conforme a la restricción del enunciado (ver §6.1). Esta separación evita conflictos de interés entre quien construye el software y quien lo audita, y es consistente con la independencia organizativa exigida por IEEE 730-2014 §4.1.

### §4.2 Riesgos de producto y de proyecto

| ID | Origen | Descripción | Prob. | Impacto | Owner | Mitigación |
|---|---|---|---|---|---|---|
| RIE-P01 | Producto | `LocalDate.parse` sin guarda → excepción no controlada ante fecha inválida | Alta | Alto | Equipo 58-1 | TC-FIAB-008 (defecto-conocido), INC-WT-01 |
| RIE-P02 | Producto | Mutaciones múltiples sin `@Transactional` → estado inconsistente | Alta | Alto | Equipo 58-1 | TC-FIAB-022, INC-WT-04 |
| RIE-P03 | Producto | Ausencia de `@RestControllerAdvice` global → HTTP 500 con stacktrace expuesto | Media | Medio | Equipo 58-1 | TC-FIAB-011, INC-WT-02 |
| RIE-P04 | Producto | Pago de amonestación sin validación de entrada | Media | Medio | Equipo 58-1 | TC-FIAB-025 |
| RIE-J01 | Proyecto | El Equipo 58-1 no entrega el código de pruebas en el plazo del sprint (precondición técnica) | Media | Alto | Líder General | Escalar al profesor Ernesto Suárez; suspender el sprint hasta recibir la implementación |
| RIE-J02 | Proyecto | Incompatibilidad H2/MySQL: queries específicas de MySQL fallan en H2 | Media | Alto | Líder Tecnológico | Usar `MODE=MySQL`; aislar tests afectados con `@Disabled` |
| RIE-J03 | Proyecto | Cobertura de decisión insuficiente por lógica condicional compleja | Media | Medio | Líder de Métricas | Meta ≥ 50% al cierre del Sprint 3; ≥ 70% al cierre del Sprint 4 |
| RIE-J04 | Proyecto | Cronograma ajustado: 5 sprints simulados antes de la entrega | Alta | Alto | Líder General | Sprint 0 y 1 en paralelo la primera semana; Sprint 4 con subconjunto de casos de sistema si falta tiempo |
| RIE-J05 | Proyecto | Pruebas de frontend (Vue) no ejecutables en CI sin configuración adicional | Alta | Medio | Líder Tecnológico | TC-FIAB-017 como prueba manual con Playwright, con pasos de reproducción documentados |

**Mapeo de hallazgos del walkthrough a riesgos de producto** (fuente: [`fase2/estaticas/2026-06-02_walkthrough-fiabilidad-sut-biblioteca.md`](fase2/estaticas/2026-06-02_walkthrough-fiabilidad-sut-biblioteca.md)):

| WT | RIE asociado | Nota |
|---|---|---|
| WT-01 | RIE-P01 | Parsing de fecha sin guarda en `crearPrestamo` |
| WT-02 | RIE-P03 | Ausencia de `@RestControllerAdvice` global |
| WT-03 | *(sin RIE asignado)* | 9 funciones asíncronas del frontend sin manejo de rechazos — documentado como hallazgo suelto, ver §6.5 |
| WT-04 | RIE-P02 | Mutaciones múltiples sin `@Transactional` |
| WT-05 | *(riesgo latente, sin RIE asignado)* | Pool HikariCP sin parámetros de recuperación de conexión — ver §6.5 |
| WT-06 | *(riesgo latente, sin RIE asignado)* | Ausencia de degradación elegante en el frontend — ver §6.5 |

### §4.3 Herramientas

El Equipo 11 opera un ecosistema de aseguramiento 100% nativo de GitHub, resultado de la migración documentada en [`REPORTE-ECOSISTEMA.md`](REPORTE-ECOSISTEMA.md) §1. Las cuatro piezas centrales son:

1. **GitHub Issues** — registro de hallazgos (`tipo:hallazgo`), defectos (`tipo:defecto`) y auditorías, con plantillas dedicadas en `.github/ISSUE_TEMPLATE/`.
2. **GitHub Projects v2 (tablero #4)** — [tablero público](https://github.com/users/odjaramillo/projects/4) con campos Fase / Severidad / Rol y estado SQA (`Backlog → En Ejecución → En Revisión → Cerrado`).
3. **GitHub Actions** — orquestación de CI mediante seis workflows: `ci-static.yml`, `ci-tests.yml`, `ci-metricas.yml`, `sync-labels.yml`, `pr-project.yml`, `pages-dashboard.yml`.
4. **SonarCloud** — análisis estático continuo (bugs, vulnerabilidades, code smells, duplicación, deuda técnica) integrado a `ci-static.yml`.

Ningún componente del ecosistema depende de plataformas externas de gestión documental o de incidencias fuera de GitHub; el reemplazo del ecosistema previo se documenta históricamente en `REPORTE-ECOSISTEMA.md` §1.

El **esquema visual de integración** entre estas piezas —qué dispara qué, qué evidencia produce cada workflow y cómo esa evidencia termina publicada— es el apéndice [`anexos/infograma-ecosistema.md`](anexos/infograma-ecosistema.md) (ANX-ECO-001, issue #9). El infograma declara además los huecos conocidos del ecosistema, cada uno con su issue de seguimiento.

La matriz completa de herramientas declaradas por sub-característica de calidad (Madurez, Tolerancia a Fallos) vive como anexo técnico en [`anexos/herramientas-fase2.md`](anexos/herramientas-fase2.md) v2.1 (issue #5).

### §4.4 Estándares, prácticas y convenciones

| Estándar | Versión | Aplicación concreta en el proyecto |
|---|---|---|
| IEEE 730 | 2014 | Estructura mandatoria de este PACS (§Clause 5) |
| ISO/IEC 25010 | 2023 | Modelo de calidad de producto; sub-características Madurez y Tolerancia a Fallos |
| ISO/IEC/IEEE 29119-2 | 2021 | Procesos de prueba — Estrategia de Pruebas (`EST-FIAB-001`) |
| ISO/IEC/IEEE 29119-3 | 2021 | Documentación de prueba — Plan de Pruebas (`PP-FIAB-001`) y Especificación de Casos (`TCS-FIAB-001`) |
| ISO/IEC/IEEE 29119-4 | 202x (borrador referenciado por el walkthrough) | Técnica de walkthrough — procedimiento de tres fases y roles |
| ISO/IEC 25023 | 2016 | Métricas de calidad — fórmulas de M-01..M-06 |
| ISO/IEC/IEEE 15289 | 2019 | Estructura y contenido de los documentos SQA del proyecto |

### §4.5 Esfuerzo, recursos y cronograma

| Hito | Milestone | `due_on` | Issue / PR |
|---|---|---|---|
| Fase 1 — Técnicas Estáticas | [#1](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/milestone/1) | 2026-06-09 | Cierre de issue #6 |
| Fase 2 — Técnicas Dinámicas | [#2](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/milestone/2) | 2026-07-19 | PR #4 (mergeado) + PRs subsecuentes de esta cadena |
| Sprints simulados 0..4 | Dentro del milestone #2 | Ver tabla de sprints abajo | `PP-FIAB-001` §5.2 |
| Consolidación de este PACS | Interno (issue #6) | — | Estimación de 4-6 h de redacción |

Los **sprints 0..4** de integración simulada, definidos en [`fase2/planificacion/2026-06-09_plan-de-pruebas-fiabilidad.md`](fase2/planificacion/2026-06-09_plan-de-pruebas-fiabilidad.md) §5.2, son:

| Sprint | Foco | Criterio de salida |
|---|---|---|
| Sprint 0 | Skeleton de CI (`pom.xml`, H2/JaCoCo/Surefire, `ci-tests.yml`) | CI verde; regla de cobertura de rama configurada |
| Sprint 1 | `UsuarioService` / `UsuarioRepository` | Suite `regresion` de Usuario en verde |
| Sprint 2 | `LibroService` / `LibroRepository` | Suite `regresion` de Libro en verde |
| Sprint 3 | `PrestamoService` / `PrestamoRepository` / `Controller` (préstamo) | Suite `regresion` en verde; M-02 ≥ 50% en `PrestamoService` |
| Sprint 4 | `AmonestacionService`, reseñas, componentes Vue, sistema desplegable | Suite `regresion` en verde; M-02 ≥ 70% global |

---

## §5. Actividades, resultados y tareas

### §5.1 Aseguramiento de producto

| Tipo | Técnica | Herramienta | Entregable | Status |
|---|---|---|---|---|
| Estática | Inspección (checklist F1) | Checklist markdown (75 ítems) | [`fase1/Checklists-Inspeccion-Estatica-v1.md`](fase1/Checklists-Inspeccion-Estatica-v1.md) | ✅ Completado |
| Estática | Walkthrough (F2) | ISO/IEC/IEEE 29119-4 + matriz de hallazgos | [`fase2/estaticas/2026-06-02_walkthrough-fiabilidad-sut-biblioteca.md`](fase2/estaticas/2026-06-02_walkthrough-fiabilidad-sut-biblioteca.md) | ✅ Completado |
| Estática | Auditoría asistida con IA (F2) | ISO/IEC 25010, informe PDF | [`fase2/estaticas/2026-06-02_auditoria-estatica-fiabilidad-iso25010.pdf`](fase2/estaticas/2026-06-02_auditoria-estatica-fiabilidad-iso25010.pdf) | ✅ Completado |
| Dinámica | Unitaria | JUnit 5 + Mockito + JaCoCo | `PP-FIAB-001` §4.1 — [`src/test/java/com/biblioteca/unit/`](../src/test/java/com/biblioteca/unit) (5 clases, 15 métodos de prueba) | 🟢 Implementada — ejecutada por `ci-tests.yml`; cobertura en el [dashboard](https://odjaramillo.github.io/gestion-bibliotecaria-sqa/) |
| Dinámica | Integración | Spring Boot Test + H2 | `PP-FIAB-001` §4.2 — [`src/test/java/com/biblioteca/integration/`](../src/test/java/com/biblioteca/integration) (4 clases, 4 métodos de prueba) | 🟢 Implementada — ejecutada por `ci-tests.yml` |
| Dinámica | Sistema | Spring Boot Test + MockMvc (desvío respecto de Postman / RestAssured, ver nota abajo) | `PP-FIAB-001` §4.3 — [`src/test/java/com/biblioteca/system/`](../src/test/java/com/biblioteca/system) (3 clases, 8 métodos de prueba) | 🟢 Implementada — ejecutada por `ci-tests.yml` |
| Dinámica | Aceptación | Manual / Playwright | `PP-FIAB-001` §4.4 | 🟡 Planificada — único nivel dinámico ausente ([issue #34](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/34)) |

**Dos universos de prueba (`@Tag`).** La suite dinámica está deliberadamente partida en dos grupos JUnit 5, y el workflow `ci-tests.yml` los ejecuta por separado:

| Grupo `@Tag` | Rol | Clases |
|---|---|---|
| `regresion` | **Gate de integración**: debe estar en verde para integrar a `main`. Es el universo sobre el que se calculan la cobertura JaCoCo y M-03 (`-Dgroups=regresion`) | Unitaria: `ParseFechaValidaTest`, `PrestamosActivosLimiteTest`, `PrestamoServiceCrearPrestamoTest`, `EliminarAmonestacionTest` · Integración: `PrestamoEstadoInventarioTest`, `PrestamoMoraAmonestacionTest` · Sistema: `SecurityGatingTest` · Smoke: `GestionBibliotecariaApplicationTests` |
| `defecto-conocido` | **Evidencia de defecto**: pruebas que codifican defectos reales detectados en el SUT y que, por lo tanto, fallan de forma esperada. Se ejecutan de modo **informativo** y no tiñen el CI de rojo | Unitaria: `ParseFechaInvalidaTest` · Integración: `PagarAmonestacionTest`, `TransactionalGapTest` · Sistema: `MultipartLimitTest`, `PrestarJsonMalformadoTest` |

Esta partición no es deuda técnica: es el resultado esperado de la Fase 2 dinámica. Las pruebas `defecto-conocido` son la evidencia formal de que la ejecución dinámica **encontró defectos** en un SUT congelado (§6.1) que el Equipo 11 no puede corregir; se registran como tales y se miden aparte para que el gate de regresión siga siendo una señal fiable de no-regresión.

**Nota de desvío de herramienta (Sistema).** La versión 1.0 de este PACS declaraba *Postman / RestAssured* para el nivel de sistema. La implementación usa `@SpringBootTest` + `@AutoConfigureMockMvc` (MockMvc): ejercita el mismo contrato HTTP de extremo a extremo (rutas, códigos de estado, serialización JSON, gating de seguridad) dentro del mismo pipeline Maven/Surefire, sin exigir un servidor desplegado ni una herramienta externa al CI. El desvío queda registrado aquí conforme a §6.3.

Los hallazgos **WT-01, WT-02, WT-03, WT-04, WT-05 y WT-06** del walkthrough son la entrada primaria al registro de riesgos de producto (ver §4.2 de este documento). Los tres documentos dinámicos de Fase 2 (`EST-FIAB-001`, `PP-FIAB-001`, `TCS-FIAB-001`) no se duplican aquí; se referencian tal cual fueron entregados en PR #4.

### §5.2 Aseguramiento de proceso

| Actividad | Mecanismo | Evidencia | Frecuencia |
|---|---|---|---|
| Peer-review IEEE 730 sobre Pull Requests | Plantilla de PR (`.github/PULL_REQUEST_TEMPLATE.md`) + workflow `pr-project.yml` | Checklist de revisión por pares completo en cada PR | Cada Pull Request |
| Cálculo de métricas M-01..M-06 | `referencias/objetivos.txt` + fórmulas ISO/IEC 25023 | `metricas/calcular_kpi.py` → `reporte_kpi.json` (+ dashboard, ver §6.2) | Al cierre de cada sprint simulado (0..4) |
| Auditoría interna del PACS | Checklist de 12 ítems del issue #6 | Revisión del Pull Request que modifica `sqa/PACS.md` | Trimestral o por hito de milestone |
| Registro de proceso | GitHub Issues + Actions + Projects v2 #4 | Historial de issues, PRs y ejecuciones | Continuo |

**Métricas M-01..M-06 vigentes** (fuente: [`referencias/objetivos.txt`](referencias/objetivos.txt)):

| ID | Métrica | Sub-característica | Fórmula | Umbral |
|---|---|---|---|---|
| M-01 | Cobertura de decisión/rama sobre el SUT | Madurez — corrección de lógica crítica | (ramas ejercitadas / ramas totales) × 100 | ≥ 70% [PROP] |
| M-02 | Densidad de defectos | Madurez — ausencia de defectos | defectos detectados / KLOC (o por clase crítica) | Registrar y reducir; sin umbral de aprobación fijo [PROP] |
| M-03 | Tasa de pruebas que pasan | Madurez — madurez de la suite | (pruebas exitosas / pruebas ejecutadas) × 100 | 100% en verde para integrar a `main` [PROP] |
| M-04 | Entradas inválidas controladas | Tolerancia a Fallos — manejo de entradas inválidas | (casos inválidos manejados sin excepción no controlada / casos inválidos probados) × 100 | ≥ 80% [PROP] |
| M-05 | Operaciones con guarda de estado previa | Tolerancia a Fallos — prevención de estados inconsistentes | (operaciones críticas con validación de precondición / operaciones críticas totales) × 100 | ≥ 80% [PROP] |
| M-06 | Cobertura de instrucciones JaCoCo | Madurez — soporte | (instrucciones cubiertas / total de instrucciones) × 100 | ≥ 60% [PROP] |

> Los umbrales marcados `[PROP]` son propuestas conservadoras a confirmar por el Líder de Métricas / Líder General (ver `referencias/objetivos.txt`).

El **Pull Request** del repositorio constituye la evidencia formal de revisión por pares conforme a IEEE 730: cada PR incluye el checklist de peer-review del `.github/PULL_REQUEST_TEMPLATE.md`, que un revisor distinto del autor debe completar antes del merge. Los **checks del PACS mismo** (auditoría interna de este documento) se ejecutan con frecuencia **trimestral o en cada hito de milestone** (#1, #2), lo que ocurra primero.

---

## §6. Consideraciones adicionales

### §6.1 Revisión de contrato

El contrato de aseguramiento entre el Equipo 11 (SQA) y el Equipo 58-1 (autor del SUT) establece: el Equipo 11 diseña las especificaciones de prueba (`TCS-FIAB-001`) y las entrega al Equipo 58-1; el Equipo 58-1 implementa los `@Test` correspondientes en la rama `simulacion-desarrollo`; el código de producción del SUT permanece **congelado** durante toda la Fase 2, conforme a la restricción explícita del enunciado F2. Este contrato es la base operativa de la independencia declarada en §4.1.

### §6.2 Medición de calidad

La medición de calidad de proceso se apoya en tres piezas: (1) el marco de métricas M-01..M-06 de [`referencias/objetivos.txt`](referencias/objetivos.txt); (2) la cobertura de revisión por pares, calculada como PRs revisados / PRs abiertos; y (3) el flujo automatizado `metricas/calcular_kpi.py` → `reporte_kpi.json`, versionado en el repositorio y publicado como dashboard en GitHub Pages (https://odjaramillo.github.io/gestion-bibliotecaria-sqa/, workflow `pages-dashboard.yml`, refresco en cada push a `main` + cron semanal + on-demand).

### §6.3 Dispensas y desviaciones

Toda desviación documentada respecto de lo planificado en este PACS se registra como GitHub Issue con la etiqueta `estado:en-analisis`. La aplicación de la dispensa requiere aprobación explícita del Líder General antes de ejecutarse, y queda registrada en el historial del Pull Request asociado (si aplica). Ninguna desviación se aplica de forma silenciosa.

### §6.4 Repetición de tareas

Se repiten con la siguiente frecuencia: (1) los checks del PACS mismo, trimestralmente o por hito de milestone (§5.2); (2) el recálculo de M-01..M-06, al cierre de cada sprint simulado (0..4, §4.5); y (3) la re-ejecución de la suite `regresion`, en cada push a `main` / `develop` y en cada Pull Request hacia `main` (workflow `ci-tests.yml`, `-Dgroups=regresion`).

### §6.5 Riesgo de realizar el SQA

| # | Riesgo del proceso SQA | Mitigación |
|---|---|---|
| 1 | Bloqueador externo: la Fase 2 dinámica depende de que el Equipo 58-1 re-entregue el código con pruebas unitarias (enunciado F2, línea 55); sin esa entrega, `ci-tests.yml` no tiene qué ejecutar | Escalamiento formal vía RIE-J01 (§4.2); la documentación del PACS y las especificaciones de prueba avanzaron en paralelo sin depender del bloqueador. **Riesgo cerrado (2026-07-12)**: los niveles unitario, de integración y de sistema están implementados y en ejecución sobre `main` (§5.1) |
| 2 | Sub-características desactualizadas — riesgo ya materializado: la versión 1.0 del anexo de herramientas declaraba *Tolerancia a fallos + Capacidad de recuperación* como sub-características, abandonadas tras la realineación del equipo a *Madurez + Tolerancia a Fallos* (`referencias/objetivos.txt`) | Absorción y regeneración del anexo a v2.0 (issue #5, PR de seguimiento a este) |
| 3 | Sub-utilización del tablero Projects v2 #4 (issues que no avanzan por los estados definidos) | Revisión del tablero como parte del cierre de cada sprint (§5.2) |
| 4 | WT-03, WT-05 y WT-06 son hallazgos del walkthrough sin `RIE` formal asignado en el registro de riesgos de producto (§4.2); podrían perderse de vista si no se referencian explícitamente | Referenciados aquí y en la tabla de mapeo WT→RIE de §4.2 como riesgos latentes bajo seguimiento |

### §6.6 Estrategia de comunicaciones

| Canal | Propósito | Frecuencia |
|---|---|---|
| GitHub Issues | Reporte y seguimiento de hallazgos y defectos | Continuo, por hallazgo |
| GitHub Projects v2 (tablero #4) | Estado visual del avance SQA para el docente | Continuo, actualizado por movimiento de issue |
| Pull Requests | Peer-review IEEE 730 formal de cada entregable | Por entregable |
| Reuniones de cierre de sprint | Revisión de métricas M-01..M-06 y ajuste del plan | Al cierre de cada sprint simulado (0..4) |
| GitHub Pages (dashboard) | Publicación pública de métricas de proceso para el docente | Cada push a `main` + cron semanal (lunes 06:00 UTC) + manual on-demand |

### §6.7 Proceso de no conformidades

```
Hallazgo (walkthrough / auditoría / checklist de inspección)
    │
    ▼
1. GitHub Issue: etiqueta `tipo:hallazgo` (F1) o `tipo:defecto` (F2)
   + `severidad:*` + `area:*`
    │
    ▼
2. Asignación a responsable por etiqueta `rol:*` + entrada al tablero
   Projects v2 #4 en `estado:abierto`
    │
    ▼
3. ¿Aplica una corrección de código o de documento SQA?
    │
    ├─ Sí ──► 4a. Pull Request con checklist de peer-review IEEE 730
    │          completo (workflow `pr-project.yml` auto-etiqueta)
    │          ──► `estado:confirmado` ──► merge
    │
    └─ No ──► 4b. Se documenta como dispensa (waiver, ver §6.3) o
               queda registrado sin acción correctiva
    │
    ▼
5. `estado:cerrado` en Projects v2 #4 + cierre del Issue
```

Los **INC-WT-01, INC-WT-02, INC-WT-03 e INC-WT-04** (incidencias derivadas del walkthrough del 2026-06-02, ver §4.2) son la evidencia operativa vigente de este flujo: cada uno recorrió el registro como Issue, la asignación por rol y el tablero Projects v2 #4 conforme al diagrama anterior.

---

## §7. Registros SQA

### §7.1 Analizar, identificar, recopilar, archivar, mantener y disponer

- **Ubicación canónica**: el repositorio GitHub del proyecto es el SQA records store; todos los documentos versionados viven bajo la carpeta `sqa/`.
- **Convención de nombre**: los documentos con fecha de emisión siguen `YYYY-MM-DD_tipo-tema.md`, verificable contra archivos existentes como [`2026-06-09_plan-de-pruebas-fiabilidad.md`](fase2/planificacion/2026-06-09_plan-de-pruebas-fiabilidad.md) y [`2026-06-02_walkthrough-fiabilidad-sut-biblioteca.md`](fase2/estaticas/2026-06-02_walkthrough-fiabilidad-sut-biblioteca.md); los documentos "vivos" sin fecha en el nombre (`REPORTE-ECOSISTEMA.md`, `ECOSISTEMA-ESTADO.md`) usan mayúsculas descriptivas.
- **Retención**: durante toda la vida académica del proyecto, hasta la evaluación final de Fase 2 y una eventual reconsideración de nota.
- **Disposal**: no se eliminan registros; el historial de `git log` provee trazabilidad completa e inmutable de cualquier cambio, corrección o reemplazo de un documento.

### §7.2 Disponibilidad de los registros

| # | Canal | Mecanismo de acceso |
|---|---|---|
| 1 | Repositorio público | https://github.com/odjaramillo/gestion-bibliotecaria-sqa — issues, PRs y commits visibles sin ser colaborador |
| 2 | Actions runs | Pestaña *Actions* del repositorio — historial de `ci-static.yml`, `ci-tests.yml`, `sync-labels.yml`, `pr-project.yml`, `pages-dashboard.yml` |
| 3 | GitHub Projects v2 (tablero #4) | https://github.com/users/odjaramillo/projects/4 — tablero público |
| 4 | SonarCloud | Dashboard de métricas de código (bugs, cobertura, deuda técnica), enlazado desde `ci-static.yml` |
| 5 | GitHub Pages | https://odjaramillo.github.io/gestion-bibliotecaria-sqa/ — dashboard de métricas de proceso (issue #3), operativo desde PR #12 |

---

## Control de versiones

| Versión | Fecha | Autor | Cambios |
|---|---|---|---|
| 1.0 | 2026-07-07 | Oscar Jaramillo (Líder Tecnológico F1 / Analista de Pruebas F2) | Emisión inicial del PACS formal consolidado F1+F2, conforme a IEEE 730-2014 §Clause 5 (issue #6) |
| 1.1 | 2026-07-12 | Oscar Jaramillo (Líder Tecnológico F1 / Analista de Pruebas F2) | Sincronización del estado declarado con el repositorio (issue #33): §5.1 — niveles unitario, integración y sistema pasan a **🟢 Implementada** con enlace a los tests y al dashboard de cobertura; se documenta la partición `regresion` / `defecto-conocido` y el desvío de herramienta del nivel de sistema (MockMvc en lugar de Postman / RestAssured); aceptación permanece planificada (issue #34). §6.2 y §6.6 — el dashboard se refresca también en cada push a `main`. §6.4 — disparadores reales de `ci-tests.yml`. §6.5 — riesgo 1 (bloqueador externo de re-entrega de código) marcado como cerrado |
| 1.2 | 2026-07-12 | Oscar Jaramillo (Líder Tecnológico F1 / Analista de Pruebas F2) | Incorporación del **infograma del ecosistema tecnológico** como apéndice (issue #9, `anexos/infograma-ecosistema.md` — ANX-ECO-001), referenciado desde §4.3. Correcciones de hecho en §4.3: la orquestación declara **seis** workflows (faltaba `ci-metricas.yml`) y el anexo de herramientas se referencia en su versión vigente (v2.1). Se retira «cobertura» de las métricas atribuidas a SonarCloud: hoy el scan corre sin datos de cobertura (issue #31) |

---

**Fin del documento.**
