# Informe de Revisión de Requisitos — Fase 1

| Campo | Valor |
|---|---|
| Documento | Informe de Revisión de Requisitos (Fase 1) — apéndice de `sqa/PACS.md` §5.1 |
| Identificador | INF-REV-001 |
| Versión | 1.0 |
| Fecha de emisión | 2026-07-13 |
| Estado | Emitido |
| Equipo SQA | Equipo 11 — Proyecto 16 |
| Artefactos revisados | BRIEF v1.1, ERS v1.2, DAS v1.5, código fuente (Equipo 58-1) |
| Instrumento aplicado | [`Checklists-Inspeccion-Estatica-v1.md`](Checklists-Inspeccion-Estatica-v1.md) v1.0 — 75 ítems |
| Estándares | ISO/IEC/IEEE 29148:2018 · ISO/IEC/IEEE 42010:2022 · ISO/IEC 25010 · IEEE 730-2014 |
| Issue | #32 |

---

## 1. Propósito

Este informe consolida los resultados de la **inspección estática** ejecutada por el Equipo 11 sobre los artefactos del Equipo 58-1 durante la Fase 1, y documenta las **correcciones incorporadas desde aquella entrega**.

Responde a dos exigencias formales:

- **Enunciado F1**, L115 y L335: *«Debe haber un plan de revisiones y un informe de revisiones»* — *«Entregable: Documento PACS con el apéndice del informe de revisiones»*.
- **Enunciado F2**, L53 (*Aspectos Complementarios*): *«El proyecto debe incluir el informe de revisión de requisitos correspondiente a la primera entrega. Este puede presentarse sin correcciones o con correcciones justificadas.»*

## 2. Nota de honestidad sobre este documento

Este informe **no es una revisión nueva**. La inspección se ejecutó en su momento: los 56 ítems aplicables fueron verificados contra los artefactos reales, con referencia de página, y los 17 defectos resultantes quedaron consignados en la tabla `RESUMEN DE DEFECTOS ENCONTRADOS` del instrumento.

Lo que **nunca ocurrió** —y es la deficiencia de proceso que este documento corrige— es que esos resultados **salieran del instrumento**. No se consolidaron en un informe, y no se registraron como hallazgos trazables: al 2026-07-12 el repositorio tenía **cero issues `tipo:hallazgo`**. El equipo revisó, encontró y anotó, pero no cerró la cadena de evidencia.

Ese es exactamente el tipo de brecha que el ecosistema actual está diseñado para impedir (ver [`anexos/reflexion-critica-ecosistema.md`](../anexos/reflexion-critica-ecosistema.md) §3).

---

## 3. Alcance y cobertura de la revisión

El instrumento declara **75 ítems**, distribuidos así:

| Checklist | Artefacto | Ítems | Ejecutados | Estándar rector |
|---|---|---|---|---|
| BRIEF | `BRIEF EQUIPO 58 1 - v1.1.pdf` | 8 | 8 | Prácticas de ingeniería de requisitos |
| ERS | `ERS Equipo 58 1 v.1.2.pdf` | 13 | 13 | ISO/IEC/IEEE 29148:2018 + ISO/IEC 25010 |
| DAS | `DAS Equipo 58-1 v1.5.pdf` | 19 | 19 | ISO/IEC/IEEE 42010:2022 + C4 |
| DAS — auditoría visual | Diagramas C4/UML | 4 | **0** | — |
| CÓDIGO | Java 21 / Spring Boot 3.4.5 / Vue 3 | 16 | 16 | ISO/IEC 25010 |
| **Subtotal — artefactos del Equipo 58-1** | | **60** | **56** | |
| PAC | PACS del propio Equipo 11 | 15 | — | IEEE 730-2014 |
| **Total del instrumento** | | **75** | | |

### Métrica — Cobertura de revisión

> **Cobertura de revisión = 56 / 60 = 93,3 %** de los ítems aplicables a los artefactos auditados.

**Los 4 ítems no ejecutados** (`DAS-VIS-01` … `DAS-VIS-04`, auditoría visual de diagramas C4/UML) dependían del workflow **WF2 con análisis visual Gemini multimodal**, que **nunca salió de `dry_run`** y fue posteriormente desmantelado. Se declaran como **no ejecutados** en lugar de darse por cumplidos: el instrumento los previó, la herramienta no los produjo.

La checklist PAC (15 ítems) es una **auto-evaluación del PACS del Equipo 11**, no parte de la revisión de los artefactos del Equipo 58-1. Queda fuera del cómputo de cobertura de esta revisión.

---

## 4. Resultados

### 4.1 Resumen cuantitativo

| Artefacto | Ítems | Defectos | Tasa de no conformidad |
|---|---|---|---|
| BRIEF | 8 | 2 (1 confirmado + 1 falso positivo) | 12,5 % |
| **ERS** | **13** | **4** | **30,8 %** |
| DAS | 19 | 4 | 21,1 % |
| CÓDIGO | 16 | 7 | **43,8 %** |
| **Total** | **56** | **17 declarados → 16 válidos** | — |

### 4.2 Adjudicación de los 17 defectos declarados

| Estado | Cantidad | Detalle |
|---|---|---|
| ✅ Confirmados | **15** | Validados contra el artefacto; se sostienen |
| ⚠️ Falso positivo | **1** | D-001 — ver §4.4 |
| ⚠️ Refutado parcialmente en ejecución | **1** | D-015 — ver §5.2 |

### 4.3 Defectos críticos (5)

Los cinco son **confirmados** y ninguno fue refutado por la ejecución dinámica posterior.

| ID | Artefacto | Defecto | Issue |
|---|---|---|---|
| **D-004** | ERS | HU5 — la regla de negocio dice «una amonestación a la vez»; el criterio de aceptación dice «una o varias». **No existe implementación correcta posible.** | [#41](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/41) |
| **D-007** | DAS | Decisiones ID-5 e ID-6 fechadas **después** de la emisión del documento. Imposibilidad temporal: el histórico no refleja las ediciones. | [#44](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/44) |
| **D-012** | CÓDIGO | `RegistroUsuario.vue:104` — la validación de contraseña está **comentada**. | [#49](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/49) |
| **D-013** | CÓDIGO | El backend **no valida** la complejidad de contraseña que la ERS exige. | [#50](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/50) |
| **D-014** | CÓDIGO | `application.properties` con `password=admin` **hardcodeado** y versionado. | [#51](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/51) |

**Lectura de los críticos.** D-012 y D-013 son el mismo defecto en dos capas: la política de contraseñas declarada en la ERS —8 caracteres, mayúscula, número, símbolo— **no se aplica en ninguna capa del sistema**. El requisito existe en el documento y en ningún otro lugar. Y el sistema **sí hashea correctamente** la contraseña al persistirla (`COD-07` ✅): protege criptográficamente una credencial que nunca debió aceptar.

### 4.4 El falso positivo — D-001

La tabla resumen del instrumento declara *«BRIEF — Backlog vacío — Alta»*. **El propio ítem `BRIEF-04` lo contradice**:

> ✅ Cumple: Sección 2 (Backlog) contiene imagen con User Story Map (5 épicas, 2 sprints, historias detalladas) — Pág. 5. **Nota:** El backlog está en formato visual/imagen, no en texto plano.

El backlog existe y está poblado. El «defecto» es un **artefacto del método de análisis** —extracción de texto sobre contenido que estaba en imagen—, no del documento auditado.

Se registra explícitamente como falso positivo ([#38](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/38)) en lugar de eliminarse en silencio. **Un instrumento de inspección que nunca produce falsos positivos no está siendo auditado.**

### 4.5 Índice completo de hallazgos

| ID | Artefacto | Ítem | Severidad | Estado | Issue |
|---|---|---|---|---|---|
| D-001 | BRIEF | BRIEF-04 | — | ⚠️ Falso positivo | [#38](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/38) |
| D-002 | BRIEF | BRIEF-06 | Menor | Confirmado | [#39](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/39) |
| D-003 | ERS | ERS-02 | Menor | Confirmado | [#40](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/40) |
| **D-004** | ERS | ERS-07 | 🔴 **Crítica** | Confirmado | [#41](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/41) |
| D-005 | ERS | ERS-09 | Observación | Confirmado | [#42](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/42) |
| D-006 | ERS | ERS-11/12/13 | Mayor | Confirmado | [#43](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/43) |
| **D-007** | DAS | DAS-05 | 🔴 **Crítica** | Confirmado | [#44](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/44) |
| D-008 | DAS | DAS-06 | Menor | Confirmado | [#45](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/45) |
| D-009 | DAS | DAS-13 | Menor | Confirmado | [#46](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/46) |
| D-010 | DAS | DAS-12/18/19 | Menor | Confirmado | [#47](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/47) |
| D-011 | CÓDIGO | COD-01/03 | Mayor | Confirmado | [#48](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/48) |
| **D-012** | CÓDIGO | COD-09 | 🔴 **Crítica** | Confirmado | [#49](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/49) |
| **D-013** | CÓDIGO | COD-08 | 🔴 **Crítica** | Confirmado | [#50](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/50) |
| **D-014** | CÓDIGO | COD-10 | 🔴 **Crítica** | Confirmado | [#51](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/51) |
| D-015 | CÓDIGO | COD-12 | Menor *(era Mayor)* | ⚠️ Refutado parcialmente | [#52](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/52) |
| D-016 | CÓDIGO | COD-06 | Observación | Confirmado | [#53](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/53) |
| D-017 | CÓDIGO | COD-13/14 | Menor | ✅ **Confirmado en ejecución** | [#54](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/54) |

---

## 5. Análisis — la Fase 2 dinámica adjudicó los hallazgos de la Fase 1

Aquí está el resultado más valioso de esta revisión, y no estaba disponible cuando se hizo la inspección: **la ejecución dinámica de la Fase 2 sometió a prueba varias hipótesis de defecto planteadas por la inspección estática de la Fase 1.**

La inspección estática produce **hipótesis**. La ejecución dinámica las **adjudica**. Algunas se confirman; otras se caen. Ambos resultados se publican.

### 5.1 Hallazgo confirmado — D-017

La inspección estática anticipó (`COD-13`):

> `PrestamoService` ejecuta `LocalDate.parse(fechaPrestamoStr)` **sin `try-catch`**.

La prueba `ParseFechaInvalidaTest` (grupo `defecto-conocido`, trazada a **WT-01 / INC-WT-01**) ejecutó el escenario, y **el defecto se materializó exactamente como fue anticipado**:

| Caso | Entrada | Resultado en ejecución |
|---|---|---|
| `TCI-T1.2` | formato `dd-MM-yyyy` | propaga `DateTimeParseException` **no controlada** |
| `TCI-T1.3` | cadena sin formato de fecha | propaga `DateTimeParseException` **no controlada** |
| `TCI-T1.4` | fecha `null` | propaga `NullPointerException` **no controlada** |

El ciclo queda cerrado de punta a punta:

> **inspección estática (F1) → hipótesis de defecto → prueba dinámica (F2) → defecto confirmado y ejecutable**

El defecto ya no es una afirmación en un documento: es **un test que corre en cada push y falla de forma esperada**. Es la forma más fuerte de evidencia que este proceso puede producir.

Lo mismo ocurre con `TransactionalGapTest`, que confirma en ejecución la ausencia de frontera transaccional anticipada por el walkthrough (**WT-04**) y consistente con **D-010** (`DAS-18`: la arquitectura no justifica cómo soporta la Fiabilidad). **No se documentó la tolerancia a fallos porque no se diseñó la tolerancia a fallos.**

### 5.2 Hallazgo refutado — D-015

La inspección estática afirmó (`COD-12`, severidad **Alta**):

> No existe `@ControllerAdvice` — **riesgo de exponer stack traces**.

La prueba `PrestarJsonMalformadoTest` (TC-FIAB-011) ejercitó el escenario concreto que el hallazgo anticipaba —un payload JSON malformado— y el veredicto fue **contrario**:

> `TCI-T2.1` — isbn con tipo incorrecto: **Spring maneja `HttpMessageNotReadableException` sin necesitar `@RestControllerAdvice`** (HTTP 400, **sin defecto**).

Spring Boot ya provee un manejador por defecto que responde `400 Bad Request` sin filtrar la traza. **El riesgo declarado no era el riesgo real.**

El hallazgo **no se elimina: se reclasifica**. La ausencia de una política explícita de manejo de errores sigue siendo una observación válida de mantenibilidad —el equipo delega el comportamiento al framework sin declararlo—, pero la severidad **Alta** era injustificada. Reclasificado a **Menor**.

**Un proceso de aseguramiento que solo publica los hallazgos que le dieron la razón no está midiendo: está seleccionando.**

---

## 6. Correcciones incorporadas desde la primera entrega

El enunciado de Fase 2 (L53) admite presentar este informe *«con correcciones justificadas»*. Se detallan a continuación las correcciones incorporadas, **todas verificables en el repositorio**.

### 6.1 Sobre el proceso de aseguramiento

| # | Corrección | Evidencia |
|---|---|---|
| C-01 | **Los hallazgos ahora son trazables.** Los 17 defectos de la inspección estática, que vivían únicamente dentro del instrumento, se registraron como issues `tipo:hallazgo` con severidad, área, estándar y estado. Antes de esta entrega el repositorio tenía **cero** issues de hallazgo. | Issues [#38](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/38)–[#54](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/54) |
| C-02 | **Se cerró el ciclo estático → dinámico.** Los hallazgos de la inspección se sometieron a prueba ejecutable; los confirmados quedaron codificados en la suite `defecto-conocido`, y el refutado se reclasificó. | §5 de este informe; `src/test/java/com/biblioteca/**` |
| C-03 | **Se declaran los ítems no ejecutados.** Los 4 ítems de auditoría visual (`DAS-VIS-*`) se reportan como **no ejecutados** en lugar de darse por cumplidos, y la cobertura de revisión se calcula en consecuencia (93,3 %, no 100 %). | §3 de este informe |
| C-04 | **Se declara el falso positivo.** D-001 se registra explícitamente como descartado, con su análisis. | Issue [#38](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/38) |

### 6.2 Sobre el ecosistema tecnológico

La corrección de fondo fue **desmantelar el ecosistema de la Fase 1 y construir otro**. El original —siete workflows de agentes sobre Gemini, un paquete `scripts/` completo, 99 tests automatizados— **nunca salió de `dry_run`**: los 99 tests probaban los agentes; **ninguno probaba el sistema bajo prueba**. Se optimizó la sofisticación de la herramienta y no la producción de evidencia.

El análisis completo, con la evidencia en el historial de commits, está en [`anexos/reflexion-critica-ecosistema.md`](../anexos/reflexion-critica-ecosistema.md) §2.

| # | Corrección | Evidencia |
|---|---|---|
| C-05 | **Ecosistema GitHub-native operativo**, con la cadena de evidencia registrada en la misma herramienta que custodia los artefactos (peer-review IEEE 730 vía Pull Request). | 6 workflows en `.github/workflows/` |
| C-06 | **PACS formal consolidado F1+F2** conforme a IEEE 730-2014 §Clause 5, con sus apéndices. | [`sqa/PACS.md`](../PACS.md) |
| C-07 | **Métricas medidas, no declaradas.** M-02/M-03/M-04 se derivan de artefactos reales de ejecución (JaCoCo, Surefire); las no medibles se marcan explícitamente como declaradas. | `sqa/metricas/`, dashboard publicado |
| C-08 | **Dashboard de métricas publicado y auto-desplegado** en cada push a `main`. | [Dashboard](https://odjaramillo.github.io/gestion-bibliotecaria-sqa/) |
| C-09 | **Infograma y reflexión crítica del ecosistema** incorporados como apéndices del PACS. | [ANX-ECO-001](../anexos/infograma-ecosistema.md), [ANX-REF-001](../anexos/reflexion-critica-ecosistema.md) |
| C-10 | **Estado declarado sincronizado con el repositorio.** Los documentos entregables declaraban como planificado trabajo ya implementado; se corrigió. | PACS v1.1, issue #33 |

### 6.3 Sobre las pruebas dinámicas

| # | Corrección | Evidencia |
|---|---|---|
| C-11 | **Tres de los cuatro niveles de prueba implementados y en ejecución**: unitaria (5 clases / 15 métodos), integración (4 / 4) y sistema (3 / 8). Aceptación permanece pendiente ([#34](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/34)). | `src/test/java/com/biblioteca/**`, `ci-tests.yml` |
| C-12 | **Los defectos se codifican como pruebas ejecutables.** El grupo `defecto-conocido` convierte cada defecto confirmado en un test que corre en cada push, sin destruir la señal del gate de regresión. | `ci-tests.yml`, `PACS.md` §5.1 |

---

## 7. Conclusiones

1. **La revisión se ejecutó y produjo resultados sustantivos**: 56 ítems verificados (93,3 % de cobertura), 17 defectos declarados, **5 críticos**, todos con evidencia y referencia de página.

2. **El defecto de proceso no estuvo en revisar, sino en no cerrar la cadena.** Los hallazgos no salieron del instrumento: no se consolidaron ni se registraron. Esa deficiencia es la que este informe corrige, y es la razón de existir del ecosistema actual.

3. **El artefacto más comprometido es el código** (43,8 % de no conformidad), con **cuatro de los cinco defectos críticos**, y tres de ellos concentrados en **seguridad**: la política de contraseñas de la ERS no se aplica en ninguna capa, y las credenciales de base de datos están hardcodeadas.

4. **El defecto más grave de la especificación es D-004**: HU5 se contradice a sí misma. No existe implementación correcta posible, y todo caso de prueba derivado hereda la contradicción.

5. **La inspección estática demostró su valor predictivo, y también sus límites.** D-017 se confirmó en ejecución exactamente como fue anticipado; D-015 fue refutado. Ambos resultados se publican con la misma formalidad. La evidencia manda, incluso cuando contradice al equipo que la produjo.

---

## 8. Trazabilidad

- **Apéndice de**: [`sqa/PACS.md`](../PACS.md) §5.1
- **Instrumento aplicado**: [`Checklists-Inspeccion-Estatica-v1.md`](Checklists-Inspeccion-Estatica-v1.md) v1.0 (75 ítems)
- **Artefactos revisados**: `documentacion/BRIEF EQUIPO 58 1 - v1.1.pdf`, `documentacion/ERS Equipo 58 1 v.1.2.pdf`, `documentacion/DAS Equipo 58-1 v1.5.pdf`, código fuente
- **Hallazgos registrados**: issues [#38](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/38) – [#54](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/54) (`tipo:hallazgo`)
- **Adjudicación dinámica**: `ParseFechaInvalidaTest`, `PrestarJsonMalformadoTest`, `TransactionalGapTest` (grupo `defecto-conocido`)
- **Contexto del ecosistema**: [`anexos/reflexion-critica-ecosistema.md`](../anexos/reflexion-critica-ecosistema.md)

---

## 9. Control de versiones

| Versión | Fecha | Autor | Cambios |
|---|---|---|---|
| 1.0 | 2026-07-13 | Equipo SQA — rol `escriba` | Emisión inicial (issue #32). Consolidación de la inspección estática de Fase 1: cobertura de revisión 93,3 % (56/60 ítems), 17 defectos adjudicados (15 confirmados, 1 falso positivo, 1 refutado en ejecución), 5 críticos. Registro de los hallazgos como issues trazables (#38–#54). Documentación de las correcciones incorporadas desde la primera entrega (C-01 … C-12). |
