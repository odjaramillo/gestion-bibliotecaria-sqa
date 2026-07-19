# UNIVERSIDAD CATÓLICA ANDRÉS BELLO

```
Facultad de Ingeniería — Escuela de Ingeniería Informática
Aseguramiento de la Calidad del Software — Prof. Ernesto Suárez — NRC: 25790
```

# REFLEXIÓN DE DESEMPEÑO DEL EQUIPO
## Criterio f) de la rúbrica de Fase 2 — roles, liderazgo y sinergia

**Proceso de aseguramiento sobre: Sistema de Gestión Bibliotecaria — Equipo 58-1**

---

## 1. Información del documento

| Campo | Valor |
|---|---|
| Documento | Reflexión de desempeño del equipo — organización, liderazgo, sinergia y evidencia por rol |
| Fase | Fase 2 — Técnicas Dinámicas (milestone homónimo del repositorio) |
| Versión | 1.0 |
| Estado | Emitido |
| Fecha de emisión | 2026-07-19 |
| Organización emisora | Equipo SQA T 11 — Proyecto 16 (Turno Tarde) |
| Elaborado por | Equipo SQA T 11 — rol de Líder General |
| Issue de trazabilidad | [#76](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/76) |

### 1.1 Propósito y ancla a la rúbrica

Este documento cierra el criterio **f) Organización del equipo y roles** de la rúbrica de Fase 2, cuyo nivel máximo exige «roles aplicados con **liderazgo**, **sinergia** y **reflexión sobre el desempeño**». Complementa al [Informe de Resultados de Pruebas de Fiabilidad](2026-07-19_informe-resultados-pruebas-fiabilidad.md) (INF-RES-001): aquel reporta qué se midió; este reporta **cómo se organizó el equipo para medirlo** y qué se aprendió del propio desempeño.

La unidad de análisis es el **rol**, no la persona: es la unidad que la rúbrica evalúa y la que la taxonomía del repositorio hace verificable de forma independiente. Toda la evidencia citada es pública y comprobable — cada issue, PR y commit enlazado existe en el repositorio.

### 1.2 Regla de evidencia

Toda cifra de este documento proviene del estado del repositorio al **19 de julio de 2026** y puede reverificarse con los filtros de etiquetas del repositorio (`is:issue label:rol:lider-tec`, etc.) y con el historial de commits (`git shortlog`). Los conteos son un corte previo a la apertura del PR de este propio documento.

---

## 2. Organización por roles

El enunciado define cinco roles. El equipo los operacionalizó como **etiquetas `rol:*` declaradas como código** en [`.github/labels.yml`](../../../.github/labels.yml) —sincronizadas por el workflow `sync-labels.yml`—, de modo que cada issue y cada PR declara el rol responsable:

| Rol del enunciado | Etiqueta | Descripción en la taxonomía |
|---|---|---|
| Líder General | `rol:lider-gral` | Líder General — coordinación y plan de aseguramiento |
| Analista de Pruebas y Tester | `rol:tester` | Analista de Pruebas / Tester — diseño y ejecución de pruebas |
| Escriba | `rol:escriba` | Escriba — documentación, auditoría y trazabilidad documental |
| Líder de Métricas | `rol:metricas` | Líder de Métricas — KPIs, dashboards y control estadístico |
| DevOp | `rol:lider-tec` | Líder Tecnológico / DevOp — ecosistema tecnológico e integración |

Los roles se ejercen sobre cuatro mecanismos, todos verificables:

1. **Etiquetas `rol:*`** en el 100% de los issues (46 de 46 al corte) y en 24 PRs.
2. **Autoría de commits y PRs**, visible en el historial y en la ficha de cada PR.
3. **Tablero GitHub Projects v2 #4**, con campo *Rol* y estado sincronizado desde las etiquetas por el workflow `pr-project.yml`.
4. **Milestone «Fase 2 — Técnicas Dinámicas»**, que agrupa todo el trabajo de la fase.

---

## 3. Evidencia de actividad por rol

Actividad registrada por rol al corte del 2026-07-19:

| Rol (etiqueta) | Issues | PRs |
|---|---|---|
| `rol:lider-tec` (DevOp) | 27 | 11 |
| `rol:escriba` | 8 | 2 |
| `rol:metricas` | 5 | 6 |
| `rol:tester` | 4 | 4 |
| `rol:lider-gral` | 2 | 1 |
| **Total** | **46** | **24** |

> Corte previo al PR de este documento. Reverificable con `is:issue label:rol:<rol>` y `is:pr label:rol:<rol>`.

La distribución **no es uniforme** y este documento no la presenta como si lo fuera: el rol tecnológico concentra el 59% de los issues y el 46% de los PRs. Esa asimetría se analiza en §6.

### 3.1 Qué es trabajo SQA y qué no

El repositorio separa limpiamente dos autorías: el **SUT** —`src/`, `biblioteca-frontend/`— es desarrollo del **Equipo 58-1**, auditado y congelado para este proceso; el **trabajo de aseguramiento** —`sqa/`, `.github/`— es del Equipo SQA T 11. La evidencia de la tabla corresponde al segundo universo: el equipo audita, no corrige el producto.

### 3.2 La automatización también deja autoría

Los bots del ecosistema (`SQA Automation`, `SQA Agent`) firman **73 commits** en el historial —sincronización de etiquetas y tablero, cálculo de KPIs, despliegues del dashboard—. Son la evidencia más directa del rol DevOp: la infraestructura no solo existe, **opera sola** y deja traza propia.

---

## 4. Liderazgo y coordinación

- **Issue-first como regla.** Ningún trabajo entra al repositorio sin un issue que lo trace. El ejemplo de mayor escala: los 17 hallazgos de la inspección estática de Fase 1 (D-002 a D-017) se registraron como issues [#38](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/38)–#54 antes de su adjudicación.
- **El PR como evidencia formal de revisión por pares (IEEE 730).** La plantilla de PR institucionaliza la revisión y nada entra a `main` sin ella. La revisión tiene dientes: del review del PR [#56](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/pull/56) nacieron los issues #57–#60, y el hardening posterior se ejecutó en el PR [#66](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/pull/66) (issues [#58](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/58), [#59](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/59)).
- **Las decisiones se registran como issues**, no como acuerdos de pasillo: la ratificación de métricas ([#24](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/24)), la implementación del nivel de aceptación ([#34](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/34)), la publicación de documentos ([#3](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/3)), la adjudicación de los hallazgos D-001/D-015 (PR [#61](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/pull/61)).
- **Milestone y etiquetas como tablero vivo.** El estado fluye por las etiquetas `estado:*` y el workflow lo propaga a los issues vinculados de cada PR: el tablero que audita el docente es el mismo dato que consumen las métricas de proceso.

---

## 5. Sinergia entre roles: los handoffs que produjo el proceso

La sinergia no se declara: se demuestra con entregas entre roles que quedaron registradas. Tres handoffs estructuraron la fase; un cuarto la cerró.

### 5.1 Tester → Métricas: el sign-off de las métricas declaradas

La ejecución de pruebas (rol `tester`) produjo la evidencia; el rol `metricas` la convirtió en valores ratificados. El sign-off de M-01, M-05 y M-06 se tramitó como issue [#24](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/24) y se cerró con el PR [#71](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/pull/71), fijando los umbrales del marco M-01..M-06. La métrica dejó de ser un número propuesto para ser un número **firmado**.

### 5.2 Inspección estática → Ejecución dinámica: la reclasificación de hallazgos

Los 17 hallazgos de Fase 1 alimentaron la base de prueba dinámica. La ejecución **refutó parcialmente** lo que la revisión en frío había anticipado: los manejadores por defecto de Spring devuelven HTTP 400/413 donde la inspección esperaba HTTP 500 por ausencia de `@RestControllerAdvice`. El hallazgo D-015 se reclasificó de Alta a Menor en el issue [#52](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/52), y la corrección arrastró a M-05: de la estimación inicial (44.4%) y el sobreajuste intermedio (61.1%) al **valor medido sobre ejecución: 55.6%** (10 de 18 condiciones controladas — [informe de resultados](2026-07-19_informe-resultados-pruebas-fiabilidad.md) §4). El proceso corrigió su propio diagnóstico en público.

### 5.3 Escriba → Líder Tecnológico: la publicación de los entregables

La documentación (rol `escriba`) solo es evidencia si es visible. El rol tecnológico montó el sitio de GitHub Pages ([#3](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/3), PR [#56](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/pull/56)) que publica los entregables desde un manifiesto curado. El handoff se ejerció hasta el último documento: el propio INF-RES-001 (PR [#73](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/pull/73)) quedó mergeado sin su entrada de manifiesto, y la omisión se detectó, se registró y se corrigió como issue [#74](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/74) — el proceso se audita a sí mismo.

### 5.4 Tester + DevOp: el nivel de aceptación

El cuarto nivel del plan —aceptación, ausente al inicio de la fase— se implementó con Playwright ([#34](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/34), PR [#68](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/pull/68)): diseño de casos del rol `tester`, workflow `ci-e2e.yml` del rol DevOp. Con él, los cuatro niveles del PP-FIAB-001 quedaron en ejecución.

---

## 6. Reflexión crítica sobre el desempeño

Se enuncia sin atenuantes, bajo la misma regla del [anexo de reflexión del ecosistema](../../anexos/reflexion-critica-ecosistema.md): cada afirmación puede rastrearse.

### 6.1 Qué funcionó

- **La trazabilidad total.** Hallazgo → issue etiquetado → rama → PR revisado → merge → métrica → publicación. La cadena no depende de la memoria de nadie: es el flujo de trabajo mismo. El 100% de issues con `rol:*` no es cosmético — es lo que hace posible este análisis por rol.
- **La honestidad de la métrica, aunque baje el número.** M-05 se publica en 55.6%, bajo su umbral del 80% y en rojo, después de dos correcciones; M-06 (75%) también queda bajo su umbral. El equipo prefirió un número incómodo y verdadero a un número cómodo. Cuando la ejecución refutó anticipos estáticos, el proceso reclasificó en lugar de sostener ([#52](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/52)).
- **El peer review como control real.** La doble revisión ciega del informe de resultados detectó tres defectos de cálculo y trazabilidad antes de la emisión; el review del sitio (PR [#56](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/pull/56)) dejó deuda registrada (#57–#60) en lugar de deuda escondida.

### 6.2 Qué costó

- **La concentración de conocimiento en pocos roles.** El rol tecnológico concentra el 59% de los issues y casi la mitad de los PRs: el mismo rol que montó el ecosistema ejecutó gran parte de la operación sobre él. Es un riesgo de continuidad que el equipo mitigó a medias convirtiendo el conocimiento en código y documentos versionados — pero la asimetría existe y la tabla de §3 la muestra sin maquillar.
- **El peer review como cuello de botella.** Con pocos roles con autoridad de revisión, los PRs esperan: la revisión rigurosa cuesta tiempo de cola. Es el precio aceptado de que la revisión sea un control y no un trámite, pero condicionó el ritmo de cierre de la fase.
- **La automatización del tablero sigue parcial** (issue [#11](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/11)): la columna *Status* y las etiquetas `estado:*` son dos fuentes de verdad para un mismo dato.

### 6.3 Lecciones aprendidas

1. **La evidencia por rol solo existe si la taxonomía se aplica siempre.** Un issue sin etiqueta es un agujero en la métrica de proceso; la disciplina de etiquetado es lo que convierte el historial en evidencia.
2. **Corregir la métrica duele una vez; sostenerla falsa cuesta todo el informe.** M-05 se corrigió dos veces a medida que mejoró la evidencia, y cada corrección aumentó la credibilidad del resultado final.
3. **Los handoffs hay que diseñarlos.** Las entregas entre roles más limpias fueron las que tenían un artefacto de frontera definido: el JSON de métricas entre tester y métricas; el manifiesto del sitio entre escriba y DevOp. Donde no hay artefacto de frontera, el handoff se degrada a conversación.

---

## 7. Cierre del criterio f)

La rúbrica exige para su nivel máximo «roles aplicados con liderazgo, sinergia y reflexión sobre desempeño». El mapa de este documento contra esa exigencia:

| Componente del criterio | Dónde se evidencia |
|---|---|
| Roles aplicados | §2 (operacionalización de los cinco roles) y §3 (actividad verificable por rol) |
| Liderazgo | §4 (issue-first, revisión IEEE 730, decisiones registradas, tablero vivo) |
| Sinergia | §5 (cuatro handoffs entre roles, con issues y PRs trazables) |
| Reflexión sobre el desempeño | §6 (qué funcionó, qué costó y lecciones — a nivel rol y proceso) |

El equipo declara el criterio **cerrado**, bajo la misma regla que rige el resto del proceso: cada afirmación de este documento puede comprobarse contra el repositorio público, sin credenciales y sin intermediarios.

---

## 8. Trazabilidad

- **Criterio de la rúbrica**: f) Organización del equipo y roles — Fase 2.
- **Documentos relacionados**: [Informe de Resultados de Pruebas de Fiabilidad](2026-07-19_informe-resultados-pruebas-fiabilidad.md) (INF-RES-001); [Reflexión crítica sobre el ecosistema tecnológico](../../anexos/reflexion-critica-ecosistema.md) (ANX-REF-001).
- **Issues citados**: [#3](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/3), [#11](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/11), [#24](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/24), [#34](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/34), [#38](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/38)–#54, [#52](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/52), #57–#60, [#58](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/58), [#59](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/59), [#74](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/74), [#76](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/76).
- **PRs citados**: [#56](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/pull/56), [#61](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/pull/61), [#66](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/pull/66), [#68](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/pull/68), [#71](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/pull/71), [#73](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/pull/73).
- **Evidencia cuantitativa**: etiquetas `rol:*` de [`.github/labels.yml`](../../../.github/labels.yml); historial de commits (`git shortlog`) para los bots de automatización.

---

## 9. Control de versiones

| Versión | Fecha | Autor | Cambios |
|---|---|---|---|
| 1.0 | 2026-07-19 | Equipo SQA T 11 — rol `lider-gral` | Emisión inicial (issue [#76](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/76)): organización y operacionalización de los cinco roles, evidencia de actividad por rol con corte verificable, liderazgo y coordinación, cuatro handoffs de sinergia trazables, reflexión crítica del desempeño y cierre del criterio f) de la rúbrica de Fase 2. |

---

*Reflexión de desempeño del equipo conforme al criterio f) de la rúbrica de Fase 2. Equipo SQA T 11 — emitida el 19 de julio de 2026. Cierre de la Fase 2.*
