# Anexo — Simulación de Integración Continua por Sprints del SUT

| Campo | Valor |
|---|---|
| Documento | Anexo reconciliador de la simulación de sprints del SUT (Equipo 58-1) sobre la rama `simulacion-desarrollo` — apéndice de `sqa/PACS.md` §4.5 y refinamiento de `sqa/fase2/dinamicas/2026-07-19_informe-resultados-pruebas-fiabilidad.md` §2.4 |
| Identificador | ANX-SIM-IC-001 |
| Versión | 1.1 |
| Fecha | 2026-07-19 |
| Equipo SQA | Equipo 11 — Proyecto 16 (rol `lider-tec` / `tester`) |
| Issue | #79 |
| Plan de pruebas ancla | [`sqa/fase2/planificacion/2026-06-09_plan-de-pruebas-fiabilidad.md`](../fase2/planificacion/2026-06-09_plan-de-pruebas-fiabilidad.md) §5.2 (cronograma) y §5.3 (workflow `ci-fiabilidad.yml`) |
| Estado | Emitido |

---

## 1. Propósito y alcance

El enunciado del proyecto (línea 32, criterio **e** Ecosistema tecnológico, nivel 5 de la rúbrica) exige al rol **DevOp** *simular una estrategia de integración continua* con el SUT, con **trazabilidad** y **reflexión crítica**. El plan PP-FIAB-001 §5.2 diseñó cinco sprints simulados (S0 skeleton → S4 sistema + Vue) sobre la rama `simulacion-desarrollo`, pero esa rama **nunca se ejecutó en su momento**: el código del Equipo 58-1 llegó completo a `main` y la bitácora por sprint quedó como un hueco de trazabilidad explícita — el propio [`INF-RES-001 §2.4`](../fase2/dinamicas/2026-07-19_informe-resultados-pruebas-fiabilidad.md) lo declara al consignar que el informe reporta el **estado consolidado sobre `main`**, no bitácoras por sprint.

Este anexo **reconcilia** ese desvío: recrea la rama `simulacion-desarrollo` con los cinco commits acumulativos y los tags `sprint-0`..`sprint-4`, ancla cada sprint a su commit, su tag, su `ci-fiabilidad` run real y los PRs/workflow runs del proyecto que lo acompañan, y **declara explícitamente** todos los desivíos conocidos. La rama simulada **no se mergea** a `main`: el SUT permanece congelado (PACS §6.1) y este anexo es la única vía por la que el docente audita la traza por sprint.

> **Relación con INF-RES-001 §2.4.** Este anexo **refina** la nota de §2.4, no la contradice. §2.4 describe la decisión de cierre (consolidar la evidencia en lugar de bitacorear por sprint) y los resultados consolidados; este anexo documenta, **a posteriori**, la traza por sprint que el plan PP-FIAB-001 §5.2 declaraba y que la decisión de §2.4 omitió materializar. El informe sigue siendo la fuente autorizada del estado del SUT; este anexo agrega la traza pedida por el plan.

---

## 2. La cadena de evidencia ancla cada sprint

| Sprint | Commit (SHA corto) | Tag | `ci-fiabilidad` run (run real, en verde) | Contenido re-comprometido |
|---|---|---|---|---|
| **S0** skeleton CI | `2c28118` | `sprint-0` | [#29710403835](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/actions/runs/29710403835) | `pom.xml`; `application-test.properties` (H2 in-memory, `MODE=MySQL`); bootstrap `GestionBibliotecariaApplication` (luego migrada a `com.biblioteca` en S3); smoke test `GestionBibliotecariaApplicationTests`; `.github/workflows/ci-fiabilidad.yml` (NUEVO, §5.3). |
| **S1** Usuario + grafo JPA | `a19bda5` | `sprint-1` | [#29710462088](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/actions/runs/29710462088) | `UsuarioService` + `CustomUserDetailsService` + `SecurityConfig`; los **6 modelos** y **6 repositorios** JPA (grafo fuertemente conexo: `Prestamo↔Usuario/Libro/Amonestacion`, `Resena↔Libro/Usuario/ComentarioResena` — ver §4 desvio A). |
| **S2** LibroService | `94deb29` | `sprint-2` | [#29710476918](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/actions/runs/29710476918) | `LibroService` (registro con imagen, busqueda/modificacion por ISBN, DELETE con guarda BIBLIOTECARIO). |
| **S3** PrestamoService + 7 tests | `dbd2ee2` | `sprint-3` | [#29710541583](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/actions/runs/29710541583) | `PrestamoService` (crear / devolver / renovar / listar, hallazgos WT-01 y WT-04); `TestDataFactory`; **7 tests Prestamo** (5 unit con Mockito + 2 integration con `@SpringBootTest` H2). Bootstrap del SUT del Equipo 58-1 entra desde su paquete `com.biblioteca`. |
| **S4** services + Controller + frontend | `3c05025` | `sprint-4` | [#29710568145](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/actions/runs/29710568145) | `AmonestacionService` + `ResenaService` + `ComentarioResenaService`; 3 DTOs; `Controller` monolito (458 líneas, autowirea 6 services + 3 DTOs — ver §4 desvio B); 2 tests de Amonestacion + 3 tests de sistema (caja negra, `TestRestTemplate` + `MockMvc`); `biblioteca-frontend/` (Vue 3, 12 componentes, 2 specs Playwright). |

Los 5 runs reales del workflow dedicado (`ci-fiabilidad.yml`) están en verde sobre el push a `simulacion-desarrollo` con `mvn verify -Dgroups=regresion`. La suite `defecto-conocido` se ejecuta de forma informativa con `continue-on-error: true`, según §5.3 del plan. La rama y los tags están en `origin`:

```bash
# Reproducir la traza por sprint desde una copia local del repo
git fetch origin
git checkout simulacion-desarrollo
git log --oneline 2c28118~1..3c05025   # 5 commits S0..S4
git tag -l 'sprint-*'                  # sprint-0 sprint-1 sprint-2 sprint-3 sprint-4
```

### Progresión medida por sprint (datos de los 5 runs reales)

Los números de esta tabla se extrajeron el 2026-07-19 directamente de los 5 runs en verde del workflow `ci-fiabilidad` (conclusión `success` verificada vía `gh run view`). La **cantidad de tests** sale del resumen Surefire (`Tests run: N, Failures: 0, Errors: 0, Skipped: 0`) del paso *Ejecutar suite regresion (gate) con cobertura JaCoCo* del **log** de cada run. La **cobertura** sale de los counters globales `BRANCH` y `LINE` del `jacoco.xml` contenido en el **artifact** `jacoco-coverage-report` de cada run (`covered / (covered + missed)` sobre todo el código re-comprometido en ese sprint).

| Sprint | Commit / tag | Tests ejecutados (gate `regresion`) | Cobertura de ramas global | Cobertura de líneas global | Gate `regresion` | Run de CI |
|---|---|---|---|---|---|---|
| **S0** | `2c28118` / `sprint-0` | 1 (smoke) | — *(sin counter `BRANCH`: el código de S0 no contiene ramas)* | 1/3 = 33.3% | success | [#29710403835](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/actions/runs/29710403835) |
| **S1** | `a19bda5` / `sprint-1` | 1 (smoke — §4 desvío A) | 0/30 = 0.0% | 48/250 = 19.2% | success | [#29710462088](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/actions/runs/29710462088) |
| **S2** | `94deb29` / `sprint-2` | 1 (smoke — §4 desvío A) | 0/48 = 0.0% | 49/292 = 16.8% | success | [#29710476918](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/actions/runs/29710476918) |
| **S3** | `dbd2ee2` / `sprint-3` | 16 | 17/76 = 22.4% | 148/366 = 40.4% | success | [#29710541583](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/actions/runs/29710541583) |
| **S4** | `3c05025` / `sprint-4` | 23 | 34/158 = 21.5% | 236/601 = 39.3% | success | [#29710568145](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/actions/runs/29710568145) |

**Cómo leer la progresión.** La tabla evidencia el **crecimiento de la cobertura de pruebas sobre el SUT congelado** a medida que la simulación re-compromete código y tests: los tests del gate pasan de 1 → 1 → 1 → 16 → 23 y las ramas cubiertas en absoluto de 0 → 0 → 17 → 34. No es mejora del código — el SUT está congelado (TCS-FIAB-001 §2.1, PACS §6.1) — sino del arnés de pruebas que el Equipo 11 incorpora por sprint. Tres lecturas honestas:

1. **S1 y S2 son gates smoke.** Ejecutan únicamente el smoke test porque las suites de `UsuarioService` y `LibroService` (TC-FIAB-002/003 y TC-FIAB-005..007) no existen en el SUT del Equipo 58-1 — desvío A, ya declarado en §4. La cobertura de ramas de 0.0% con 30 y 48 ramas disponibles es la evidencia numérica de ese hueco, no un dato a maquillar.
2. **El porcentaje global no es monótono y no debería serlo.** La cobertura de líneas baja de 19.2% (S1) a 16.8% (S2) porque S2 agrega `LibroService` sin tests nuevos, y la de ramas baja de 22.4% (S3) a 21.5% (S4) porque S4 incorpora el `Controller` de 458 líneas y tres services adicionales más rápido de lo que agrega tests. El denominador (el código del SUT re-comprometido) crece en cada sprint; lo que crece sin excepción es el numerador absoluto — ramas cubiertas 0 → 0 → 17 → 34 — y la cantidad de tests — 1 → 1 → 1 → 16 → 23.
3. **Distinto alcance que la métrica M-02.** El dato de §3 (BRANCH = 0.60 sobre `com.biblioteca.service.PrestamoService`) es una cobertura **por clase**; esta tabla reporta la cobertura **global del reporte JaCoCo** de cada run. No se contradicen: miden cosas distintas.

---

## 3. Los PRs y workflow runs reales del proyecto que acompañan la simulación

La simulación de la IC no ocurrió en el vacío: el resto del ecosistema siguió su curso en `main` y dejó evidencia real con la que esta sección se ancla. La tabla lista los PRs y workflow runs que la rúbrica de la simulación cruza con el `simulacion-desarrollo`.

| PR | Workflow runs reales (sha / run id) | Lo que confirma del SUT o de la IC |
|---|---|---|
| [#1](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/pull/1) — ecosistema SQA GitHub-native | [ci-tests #29328065xxx](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/actions/workflows/ci-tests.yml) | Migración Jira+Confluence → GitHub-native (PACS §3). |
| [#3](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/3) — GitHub Pages para docs SQA | (issue, no PR directo) | Aprovisionamiento del slot de Pages ocupado por el dashboard — restricción L4 del anexo crítico. |
| [#4](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/pull/4) — realinea F2 a Madurez + Tolerancia | (histórico) | Decisión de reducir el alcance a dos sub-características, base del PP-FIAB-001. |
| [#12](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/pull/12) — publica dashboard en Pages | (histórico) | Único deploy de Pages compartido entre dashboard y sitio de documentos. |
| [#14](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/pull/14) — PACS consolidado F1+F2 | (histórico) | IEEE 730 §Clause 5 satisfecho; ancla §6.1 (SUT congelado). |
| [#16](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/pull/16) — config JaCoCo/CI (PR1/5) | ci-tests en `main` sobre `0.0.x` | Activación de la cobertura automatica. |
| [#17](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/pull/17) — PACS-Herramientas v2.0 | (histórico) | M-01..M-06 declarados. |
| [#18](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/pull/18) — suite unit F2 (PR2/5) | ci-tests en `main` | TC-FIAB-004/007/008/018 implementados (regresion). |
| [#19](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/pull/19) — suite integration F2 (PR3/5) | ci-tests en `main` | TC-FIAB-019/020/022/025 implementados. |
| [#20](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/pull/20) — suite system F2 (PR5/5) | ci-tests en `main` | TC-FIAB-011/021/01X. |
| [#22](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/pull/22) — consolidar TCS-FIAB-001 | (histórico) | 11 casos ratificados, 13 diferidos (ANX-FIAB-001). |
| [#23](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/pull/23) — enriquecer dashboard M-01..M-06 | pages-dashboard run [#2932400xxx](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/actions/workflows/pages-dashboard.yml) | Cobertura automatica publicada. |
| [#26](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/pull/26) — dashboard + meta única + métricas de proceso | pages-dashboard run | Reforma del dashboard, un único artefacto. |
| [#28](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/pull/28) — Pages auto en push a main | pages-dashboard run | Despliegue continuo del dashboard. |
| [#34](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/34) — implementar pruebas de aceptación con Playwright | ci-e2e [#29708835472](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/actions/runs/29708835472) y runs previos | Único nivel dinámico ausente en PP-FIAB-001. |
| [#55](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/pull/55) — INF-REV-001 F1 (apéndice PACS) | ci-static en PR | Inspección estática de ERS+DAS, 75 ítems. |
| [#56](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/pull/56) — publicar documentos SQA en el sitio | pages-dashboard run | Materialización del sitio `/docs` curado por `sqa/sitio/generar_docs.py`. |
| [#66](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/pull/66) — minimo privilegio en Pages + guard XSS | ci-static / ci-tests | Desvío de autocontención del sitio registrado en PACS §6.3. |
| [#68](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/pull/68) — pruebas de aceptación con Playwright | ci-e2e [#29708835472](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/actions/runs/29708835472) | tc-fiab-017-async-rejection + tc-fiab-043-prestamo-e2e. |
| [#71](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/pull/71) — ratificar M-01/M-05/M-06 en PACS | (issue #24 cerrado) | Métricas declaradas pasan a ratificadas; base de M-02 = 60.7%. |
| [#73](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/pull/73) — INF-RES-001 cierre F2 | ci-tests [#29705987185](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/actions/runs/29705987185) | Informe que este anexo refina (§2.4). |
| [#75](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/pull/75) — publicar INF-RES-001 en el dashboard | ci-tests [#29708663474](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/actions/runs/29708663474) | El informe queda enlazado desde el dashboard. |

> **Métrica por sprint (de la corrida real del workflow).** Cada run del `ci-fiabilidad` produjo un artefacto `jacoco-coverage-report` con el reporte JaCoCo de la corrida. Sobre la rama simulada, la cobertura del gate `regresion` se mantuvo: **S0 = 1 test** (smoke), **S1 = 1 test** (smoke, sin suite de Usuario porque TC-FIAB-002/003 no existen — §4 desvio A); **S2 = 1 test** (smoke, sin suite de Libro porque TC-FIAB-005/006/007 no existen — §4 desvio A); **S3 = 16 tests** en verde (5 unit Mockito de Prestamo + 2 integration + 8 unit de PrestamoServiceCrearPrestamo + 1 smoke; cobertura `PrestamoService` BRANCH = 0.60 contra umbral 0.70 — coincide con M-02 = 60.7% del INF-RES-001 §6); **S4 = 23 tests** en verde (suite completa del gate `regresion` del SUT del Equipo 58-1 re-comprometido; el warning de JaCoCo sobre `PrestamoService` persiste porque la regla `BRANCH >= 0.70` en `pom.xml` está con `haltOnFailure=false` y es solo informativa).

---

## 4. Desvíos declarados (todos)

Cada desvio se enumera con el identificador que el INF-RES-001 ya usa, y se ancla al commit, tag o workflow run que lo materializa en `simulacion-desarrollo`. **No se rellena con código nuevo** lo que el SUT del Equipo 58-1 no implementó: la honestidad de la simulación exige declarar el hueco, no taparlo.

### Desvío A — TC-FIAB-002 y TC-FIAB-003 nunca implementados

El plan PP-FIAB-001 §5.2 asignaba los casos `TC-FIAB-002..004` a S1 y `TC-FIAB-005..007` a S2 sobre los servicios `UsuarioService` y `LibroService` respectivamente. Esos casos **no existen** en el SUT del Equipo 58-1 re-comprometido en `simulacion-desarrollo`: el repositorio nunca recibió tests dedicados a la cobertura de decisión/rama de `UsuarioService` (TC-FIAB-002) ni de `LibroService` (TC-FIAB-003), y los 13 casos de `TCS-FIAB-001` restantes más `TC-FIAB-025` son los que se ejecutan. La consecuencia operativa es que **los gates de S1 y S2 quedan con un único test (el smoke)** — no hay regresión posible sobre los servicios de Usuario o Libro hasta S3, donde entran los tests de Prestamo, y S4, donde la suite completa de regresion cubre el Controller.

> **Materialización.** Tag `sprint-1` ([#29710462088](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/actions/runs/29710462088)): el run de `ci-fiabilidad` muestra `Tests run: 1` (el smoke). Tag `sprint-2` ([#29710476918](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/actions/runs/29710476918)): idem.

### Desvío B — `Controller` monolítico, no rebanable por dominio

El plan asumía (y así está escrito en la columna "código re-comprometido" de la tabla de §5.2) que S3 traería `Controller (préstamo)`. La realidad del SUT del Equipo 58-1 es que `Controller.java` es **un único `@RestController` de 458 líneas** que cubre los seis dominios: autowirea los 6 services + 3 DTOs, expone 25 endpoints REST, y la operación de borrado de reseñas (`eliminarResena`) encadena dos repositorios (`comentarioResenaRepository.deleteAll` + `resenaRepository.delete`) — hallazgo INC-WT-04c — sin `@Transactional`. **Un corte por dominio rompe la compilación**: si se intenta llevar a S3 solo los endpoints de `/api/prestar` y `/api/prestamos`, los imports del resto del Controller (Resena, ComentarioResena, Amonestacion) no resuelven. El plan, otra vez, asumía una granularidad que el SUT no admite. La entrada del Controller se hace **entera en S4** (commit `3c05025`, tag `sprint-4`).

### Desvío C — M-02 real 60.7% vs 70% planificado

El plan declaraba (PP-FIAB-001 §4.4) **M-02 ≥ 70%** como criterio de salida del plan completo. La ejecución real del SUT del Equipo 58-1 produce **M-02 = 60.7%** sobre `PrestamoService` (INF-RES-001 §6). En `simulacion-desarrollo` la métrica se reproduce: el warning del plugin JaCoCo en `mvn verify` indica `branches covered ratio is 0.60, but expected minimum is 0.70` sobre `com.biblioteca.service.PrestamoService`. El plugin no falla el build (la regla tiene `haltOnFailure=false` en `pom.xml`); el run queda en verde y la métrica queda por debajo del umbral planificado. **No se modifica `pom.xml`** para inflar la cobertura: el gap es lo que el SUT del Equipo 58-1 tiene hoy, no lo que el plan queria.

> **Materialización.** Cualquier run de `ci-fiabilidad` sobre el tip de `simulacion-desarrollo` (por ejemplo [#29710568145](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/actions/runs/29710568145)) muestra el warning en el log del job `test-fiabilidad`.

### Desvío D — La rama se creó hoy como ejecución tardía del plan

`simulacion-desarrollo` se creó el **2026-07-19** (fecha del push), no en el cronograma que PP-FIAB-001 §4.5 declaraba para la primera semana. El plan diseñaba 5 sprints ejecutados **antes** de la implementación del SUT por parte del Equipo 58-1; la realidad fue que el SUT llegó completo, INF-RES-001 §2.4 documentó la decisión de consolidar la evidencia en lugar de bitacorear por sprint, y la simulación se materializa **tarde** como ejercicio de trazabilidad retrospectiva. Esta materialización no contradice §2.4: la decisión de cierre sigue vigente (el SUT en `main` permanece congelado, INF-RES-001 sigue siendo la fuente autorizada del estado del SUT), y este anexo es el medio por el que la traza por sprint — pedida por el plan — queda disponible para auditoría.

### Desvío E — Bootstrap del SUT y la huella del Initializr

El `pom.xml` del Equipo 58-1 (re-comprometido en S0) conserva la huella del Spring Initializr: una clase `GestionBibliotecariaApplication` en el paquete `__1.spring_boot` (nombre que el Initializr asigna por convención cuando el nombre del proyecto empieza con dígito — el artifactId es `biblioteca-backend` con `groupId=58_1`). El SUT real del Equipo 58-1 tiene **dos** `@SpringBootApplication`: la legacy del Initializr y la real en `com.biblioteca`. La simulación replica la estructura: **S0** usa la legacy del Initializr para que el smoke levante; **S3** migra a la real en `com.biblioteca` cuando los tests de integración del Equipo 58-1 necesitan encontrar `@SpringBootConfiguration` por upward search desde `com.biblioteca.integration`. La coexistencia se documenta honestamente en el commit de S3.

### Desvío F — `defecto-conocido` como corrida informativa, no gate

`ci-fiabilidad.yml` ejecuta la suite `defecto-conocido` con `continue-on-error: true` (PP-FIAB-001 §5.3): es una corrida informativa que **no bloquea** el merge. Esto es la convención del SUT del Equipo 58-1 en `ci-tests.yml` y la decisión del equipo de no inflar el gate con defectos reales del SUT congelado (PACS §5.1, `anexos/reflexion-critica-ecosistema.md` §3.4). Los runs del workflow `ci-fiabilidad` están **verdes** sobre la combinación `regresion` + `defecto-conocido`; las pruebas con `@Tag("defecto-conocido")` se ejecutan, fallan como esperan (codificando defectos reales del SUT), y el job termina OK porque la falla es esperada.

### Desvío G — `biblioteca-frontend/` se versiona pero su suite Playwright no se ejecuta en el workflow

El frontend Vue 3 + Vue CLI 5 (12 componentes, 2 specs Playwright) entra **completo en S4** y se commitea, pero `ci-fiabilidad.yml` no incluye el job de Playwright: la suite end-to-end la corre `ci-e2e.yml` sobre `main` ([#29708835472](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/actions/runs/29708835472) y runs previos). Replicar `ci-e2e.yml` sobre `simulacion-desarrollo` exigiría un runner con navegadores y la duplicación del job; el plan no lo declara y el objetivo de la simulación (trazabilidad por sprint del SUT backend) se cumple con el frontend versionado en S4 y la suite e2e ejecutada contra `main` por su workflow natural.

---

## 5. Refinamiento de la nota de INF-RES-001 §2.4

INF-RES-001 §2.4 dice, textualmente:

> *"Nota sobre la simulación por sprints. El PP-FIAB-001 §5.2 planifica la incorporación de pruebas en sprints simulados (0–4). Este informe reporta el **estado consolidado de ejecución** sobre `main` al cierre de la fase, no bitácoras por sprint: el equipo autor del SUT re-comprometió el código con las pruebas incorporadas y la suite completa se ejecuta hoy en verde (ver §9)."*

Este anexo **no la contradice**. La lee como dos afirmaciones:

1. *El informe reporta el estado consolidado sobre `main`.* — **Verdadera, intacta**. INF-RES-001 sigue siendo la fuente autorizada del estado del SUT; los resultados de las 13 clases y 34 pruebas JVM, las seis métricas de fiabilidad ratificadas (M-01..M-06), las incidencias trazadas y la matriz de la §9 son el estado consolidado.
2. *No bitácoras por sprint.* — **Lo que este anexo refina**. La razón de la omisión (consolidación para reducir overhead) se mantiene; lo que se agrega es la traza por sprint materializada en `simulacion-desarrollo` y verificada por los 5 runs del `ci-fiabilidad`. La traza es evidencia del **proceso de planificación del SQA**, no del SUT mismo: el SUT no cambió, el plan se ejecutó tarde, y este anexo es la única forma de cerrar ese lazo sin reabrir nada en `main`.

> **Consecuencia para el lector del INF-RES-001.** Quien busque el **estado del SUT** lee INF-RES-001 §3..§6. Quien busque **la traza por sprint que el plan PP-FIAB-001 §5.2 declaraba y que la decisión de §2.4 no materializó** lee este anexo. Ambos documentos son complementarios y se citan mutuamente; no compiten por la misma evidencia.

---

## 6. Reflexión

La simulación de la IC del SUT en una rama con cinco sprints es, técnicamente, un **re-commit declarativo**: cada commit repite sobre `simulacion-desarrollo` lo que el SUT del Equipo 58-1 ya entregó consolidado a `main`. La diferencia no está en el código — está en el **cumplimiento del contrato de aseguramiento declarado en el plan**. El Equipo 11 diseñó PP-FIAB-001 §5.2 esperando que la entrega del SUT fuera incremental, y la realidad lo desmintió. Reconocerlo y registrarlo, en lugar de fingir que no pasó, es la diferencia entre un ecosistema SQA que mide y uno que se mide a sí mismo.

La simulación tardía no corrige el SUT ni reabre el informe; lo que hace es **completar la trazabilidad del plan** sobre la única rama en la que el plan se diseñó. Es una pieza de proceso honesta porque declara sus desivíos en lugar de maquillar el resultado. Y es, sobre todo, una decisión reversible: borrar la rama y los tags (`git push origin :simulacion-desarrollo && git push origin --delete sprint-0 sprint-1 sprint-2 sprint-3 sprint-4`) devuelve el repositorio al estado que tenía antes de este anexo, sin afectar `main` ni los workflows que la rúbrica audita como `main`-side.

La lección que el equipo extrae no es que el plan estaba mal diseñado: estaba **bien diseñado para un escenario que no se materializó**. La lección es que un ecosistema SQA que planifica sprints simulados debe tener un protocolo explícito para el caso en que el SUT llegue completo — y ese protocolo, ausente en PP-FIAB-001, es lo que INF-RES-001 §2.4 codificó por la vía del hecho y lo que este anexo ejecuta por la vía de la evidencia.

---

## 7. Trazabilidad

- **Plan ancla**: PP-FIAB-001 §4.5, §5.2, §5.3.
- **Informe refinado**: INF-RES-001 §2.4 (nota), §3 (resumen), §4 (niveles), §6 (métricas), §9 (veredicto).
- **Proposal**: engram topic `sdd/simulacion-sprints-sut/proposal` (obs #1530).
- **Spike de factibilidad**: engram topic `sdd/simulacion-sprints-sut/spike-factibilidad` (obs #1529) — mecánica de commits acumulativos verificada sobre worktree temporal.
- **Workflows reales** sobre la rama `simulacion-desarrollo`: [`ci-fiabilidad.yml`](../../.github/workflows/ci-fiabilidad.yml) — 5 runs en verde, URLs en §2.
- **Workflows reales** sobre `main` que ancla la IC existente: [`ci-tests.yml`](../../.github/workflows/ci-tests.yml), [`ci-static.yml`](../../.github/workflows/ci-static.yml), [`ci-e2e.yml`](../../.github/workflows/ci-e2e.yml), [`pages-dashboard.yml`](../../.github/workflows/pages-dashboard.yml).
- **PRs del proyecto**: #1, #3, #4, #12, #14, #16..#20, #22, #23, #26, #28, #34, #55, #56, #66, #68, #71, #73, #75 — ver §3.
- **Issues abiertos relevantes**: #24 (M-01/M-05/M-06 ratificadas — cerrado en #71), #11 (columna Status del tablero), #31 (cobertura JaCoCo → SonarCloud), #52 (reclasificación de D-015), #60 (sitio en camino crítico del deploy).
- **Rama y tags**: `simulacion-desarrollo` + `sprint-0`..`sprint-4` en `origin`, push incremental, **sin PR** a `main` (PACS §6.1: SUT congelado).

---

## 8. Control de versiones

| Versión | Fecha | Autor | Cambios |
|---|---|---|---|
| 1.0 | 2026-07-19 | Equipo SQA — rol `lider-tec` (`tester`) | Emisión del anexo reconciliador de la simulación de IC por sprints del SUT (issue #79): tabla Sprint→commit/tag/run real, PRs/workflow runs del proyecto ancla, declaración de los siete desivíos (TC-FIAB-002/003 nunca implementados, Controller monolítico no rebanable, M-02 60.7% vs 70% planificado, ejecución tardía del plan, bootstrap del Initializr, defecto-conocido informativo, frontend versionado pero e2e en `main`), refinamiento explícito de INF-RES-001 §2.4 y reflexión sobre el valor de la simulación declarativa. |
| 1.1 | 2026-07-19 | Equipo SQA — rol `metricas` | Incorporación de la subsección «Progresión medida por sprint» en §2: tabla con tests ejecutados (resumen Surefire del log de cada run) y cobertura global de ramas/líneas (counters `BRANCH`/`LINE` del `jacoco.xml` del artifact `jacoco-coverage-report`) extraídos de los 5 runs reales del workflow `ci-fiabilidad`, con lectura honesta de la no-monotonicidad del porcentaje global y referencias cruzadas a los desvíos A y C. |
