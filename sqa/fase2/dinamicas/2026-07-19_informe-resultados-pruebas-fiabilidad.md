# UNIVERSIDAD CATÓLICA ANDRÉS BELLO

```
Facultad de Ingeniería — Escuela de Ingeniería Informática
Aseguramiento de la Calidad del Software — Prof. Ernesto Suárez — NRC: 25790
```

# INFORME DE RESULTADOS DE PRUEBAS — FIABILIDAD
## (Test Completion Report — ISO/IEC/IEEE 29119-3:2021, cláusula 7.4)

**Proyecto evaluado: Sistema de Gestión Bibliotecaria — Equipo 58-1**

---

## 1. Información del documento (29119-3 §7.4.2)

| Campo | Valor |
|---|---|
| Identificador | INF-RES-001 |
| Versión | 1.0 |
| Estado | Emitido |
| Fecha de emisión | 2026-07-19 |
| Organización emisora | Equipo SQA T 11 — Proyecto 16 (Turno Tarde) |
| Autor | Analista de Pruebas — Oscar Jaramillo |
| Aprobado por | Líder General — Alberto Rodríguez |
| Revisor de métricas | Líder de Métricas (Equipo T 11) |

### 1.1 Historial de cambios
| Versión | Fecha | Descripción | Autor |
|---|---|---|---|
| 1.0 | 2026-07-19 | Emisión de cierre de Fase 2. Consolida los resultados de ejecución de los niveles unitario, de integración, de sistema y de aceptación; las incidencias trazadas al walkthrough; y las seis métricas de fiabilidad ratificadas (issue #24). | Equipo 11 |

---

## 2. Introducción (29119-3 §7.4.3)

### 2.1 Objeto
Este informe reporta los **resultados de la ejecución** de las pruebas dinámicas de fiabilidad (ISO/IEC 25010:2023 — *Madurez* y *Tolerancia a Fallos*) del Sistema de Gestión Bibliotecaria del Equipo 58-1, y evalúa si se cumplieron los objetivos de calidad y los criterios de salida del Plan de Pruebas PP-FIAB-001. Es el artefacto de cierre de la Fase 2.

### 2.2 Alcance
Cubre los cuatro niveles de prueba ejecutados sobre la característica Reliability: **unitario, de integración, de sistema y de aceptación**, con enfoques de caja blanca, gris y negra. Quedan fuera de alcance las sub-características *Disponibilidad* y *Capacidad de Recuperación* (no seleccionadas; ver §8 y el Anexo A de casos diferidos).

### 2.3 Referencias
- **Externas:** ISO/IEC/IEEE 29119-3:2021 (§7.4, estructura de este informe); ISO/IEC 25010:2023 (modelo de calidad); ISO/IEC 25023:2016 (métricas).
- **Internas:** PP-FIAB-001 (Plan de Pruebas), EST-FIAB-001 (Estrategia), TCS-FIAB-001 (Especificación de Casos), `2026-06-02_walkthrough-fiabilidad-sut-biblioteca.md` (base de prueba, hallazgos WT-01..WT-06), `referencias/objetivos.txt` (marco de métricas), `metricas/reporte_kpi.json` (métricas calculadas).

### 2.4 Base de la evidencia
Los resultados provienen de la ejecución automatizada en CI sobre `main`: reportes **Maven Surefire** (`target/surefire-reports/`) y **JaCoCo** (`target/site/jacoco/jacoco.xml`) para los niveles JVM, y **Playwright** (`biblioteca-frontend/tests/e2e/`, workflow `ci-e2e.yml`) para el nivel de aceptación. La ejecución es reproducible: los mismos artefactos alimentan el dashboard de métricas.

> **Nota sobre la simulación por sprints.** El PP-FIAB-001 §5.2 planifica la incorporación de pruebas en sprints simulados (0–4). Este informe reporta el **estado consolidado de ejecución** sobre `main` al cierre de la fase, no bitácoras por sprint: el equipo autor del SUT re-comprometió el código con las pruebas incorporadas y la suite completa se ejecuta hoy en verde (ver §9).

---

## 3. Resumen de la ejecución (29119-3 §7.4.4)

**Resultado global: 34 pruebas JVM ejecutadas — 0 fallos, 0 errores, 0 omitidas (100% verde)**, más **2 pruebas de aceptación** automatizadas con Playwright. Tasa de pruebas que pasan (M-03) = **100%**.

| Nivel | Enfoque | Clases | Pruebas | Resultado |
|---|---|---|---|---|
| Unitario | Caja blanca (JUnit 5 + Mockito) | 5 | 18 | ✅ 18/18 |
| Integración | Caja gris (Spring context + H2) | 4 | 7 | ✅ 7/7 |
| Sistema | Caja negra (MockMvc) | 3 | 8 | ✅ 8/8 |
| Smoke | Carga de contexto | 1 | 1 | ✅ 1/1 |
| **Subtotal JVM** | | **13** | **34** | **✅ 34/34** |
| Aceptación | Caja negra (Playwright, UI→backend real) | 2 specs | 2 | ✅ (ver §4.4) |

Todas las suites `regresion` (gate) pasan. Las suites `defecto-conocido` (informativas) ejecutan y **documentan** el comportamiento deficiente del SUT sin bloquear el pipeline (EST-FIAB-001 §5).

---

## 4. Resultados por nivel de prueba

### 4.1 Nivel unitario — 18 pruebas ✅ (caja blanca)

Aísla la lógica de negocio crítica de la capa Service con Mockito.

| Clase | Pruebas | Caso (TCS-FIAB-001) | TCI | Suite | Métrica |
|---|---|---|---|---|---|
| `PrestamoServiceCrearPrestamoTest` | 8 | TC-FIAB-004 | TCI-M1.1..M1.7 | regresion | M-02 |
| `PrestamosActivosLimiteTest` | 3 | TC-FIAB-018 | TCI-M2.1..M2.3 | regresion | M-02 |
| `EliminarAmonestacionTest` | 3 | TC-FIAB-007 | TCI-M5.1..M5.3 | regresion | M-02 |
| `ParseFechaValidaTest` | 1 | TC-FIAB-008 | TCI-T1.1 | regresion | M-03 |
| `ParseFechaInvalidaTest` | 3 | TC-FIAB-008 | TCI-T1.2..T1.4 | defecto-conocido | M-05 · WT-01 |

**Análisis (criterio b).** Las 8 pruebas de `crearPrestamo` ejercitan las siete particiones de sus guardas de precondición, dando cobertura de decisión sobre el método más crítico del SUT (M-02 = 60.7% en `PrestamoService`, 100% en `AmonestacionService`). Las tres pruebas de `ParseFechaInvalidaTest` **confirman en ejecución** el hallazgo WT-01: `LocalDate.parse` sin `try/catch` propaga `DateTimeParseException`/`NullPointerException` ante fecha malformada o nula (incidencia INC-WT-01). Son pruebas que pasan verificando el defecto: el valor esperado es la excepción no controlada.

### 4.2 Nivel de integración — 7 pruebas ✅ (caja gris)

Ejercita la colaboración entre servicios, repositorios y la persistencia H2 en contexto Spring.

| Clase | Pruebas | Caso | Suite | Métrica |
|---|---|---|---|---|
| `PagarAmonestacionTest` | 3 | TC-FIAB-025 | defecto-conocido | M-05 · TCOND-M6 |
| `PrestamoEstadoInventarioTest` | 2 | TC-FIAB-019 | regresion | M-02 |
| `PrestamoMoraAmonestacionTest` | 1 | TC-FIAB-020 | regresion | M-01, M-03 |
| `TransactionalGapTest` | 1 | TC-FIAB-022 | defecto-conocido | M-01 · WT-04 |

**Reflexión sobre integración (criterio c).** El escenario operativo end-to-end (`PrestamoMoraAmonestacionTest`, TC-FIAB-020) confirma que la cadena crear→devolver-tarde→amonestación integra sin fallas: la mora genera la `Amonestacion` esperada (monto 100.0, no pagada, no verificada). En contraste, `TransactionalGapTest` (TC-FIAB-022) **confirma el defecto WT-04**: inyectando un fallo entre los dos `save()` de `crearPrestamo` (sin `@Transactional`), el `Prestamo` queda huérfano y la `cantidad` no se restaura — pérdida de atomicidad ante fallo parcial (INC-WT-04, cuenta como defecto de fiabilidad en M-01). `PagarAmonestacionTest` confirma que `pagarAmonestacion` persiste sin validar `metodoPago`/`comprobantePago` — una de las entradas no controladas que alimenta **M-05**. *(El defecto propio de M-06 —`renovarPrestamo` decrementa inventario sin guarda de disponibilidad— no tiene clase de prueba dedicada; se sustenta en inspección de código, `PrestamoService.java:151-154`, no en un `@Test`.)*

### 4.3 Nivel de sistema — 8 pruebas ✅ (caja negra)

Estimula los endpoints REST vía `MockMvc`, sin conocimiento de la implementación.

| Clase | Pruebas | Caso | Suite | Métrica |
|---|---|---|---|---|
| `SecurityGatingTest` | 4 | SC-SEC-01 — gating de seguridad (issue #15) | regresion | M-03 |
| `PrestarJsonMalformadoTest` | 2 | TC-FIAB-011 | defecto-conocido | M-05 · WT-01/WT-02 |
| `MultipartLimitTest` | 2 | TC-FIAB-021 | defecto-conocido | M-05 |

**Análisis (criterio d — sistema).** Este nivel arrojó el resultado más instructivo del proceso: **la ejecución refutó dos defectos que la inspección estática había anticipado como HTTP 500**. (1) `PrestarJsonMalformadoTest` (TC-FIAB-011) demuestra que un JSON con tipo incorrecto produce **HTTP 400**, no 500: Jackson lanza `HttpMessageNotReadableException` y Spring la maneja por defecto, sin necesitar `@RestControllerAdvice`. El HTTP 500 real solo aparece cuando el JSON es válido pero el valor de `fechaPrestamo` no es parseable por `LocalDate.parse` (`PrestamoService.java:47`) — es decir, el mismo defecto WT-01 aflorando en la frontera de sistema, no el del `@RestControllerAdvice`. (2) `MultipartLimitTest` (TC-FIAB-021) demuestra que un archivo sobre 1 MB devuelve **HTTP 413 correcto**: `DefaultHandlerExceptionResolver` mapea `MaxUploadSizeExceededException` automáticamente desde Spring 5.1. Como hallazgo secundario, ese 413 se emite vía `sendError`, cuyo reenvío interno a `/error` pasa por el filtro de seguridad y, sin sesión, redirige a `/login` — el cliente no llega a ver el 413. (3) `SecurityGatingTest` verifica que el gating de autorización por rol responde según lo esperado. **Lección (criterio d + reflexión):** los manejadores por defecto de Spring son más robustos que lo que asumió la revisión en frío; el proceso reclasifica esos hallazgos en lugar de sostenerlos a la fuerza (ver §5 e issue #52). Esta corrección ajustó M-05 sobre la ejecución: de las condiciones de sintaxis JSON, solo el tipo incorrecto (T2.1) queda controlado (400), mientras la fecha no parseable (T2.2) sí escala a 500. El valor medido es **55.6%** (10 de 18 condiciones controladas), no la estimación inicial de 44.4% ni el sobreajuste intermedio de 61.1%.

### 4.4 Nivel de aceptación — 2 pruebas ✅ (Playwright, UI → backend real)

Cruza la frontera frontend Vue → backend Spring Boot real (MySQL), desde la perspectiva del usuario final. Único nivel que ejercita la aplicación integrada de punta a punta.

| Spec | Caso | Disposición | Métrica |
|---|---|---|---|
| `tc-fiab-043-prestamo-e2e.spec.js` | TC-FIAB-043 | regresion (aceptación) | M-01, M-03 |
| `tc-fiab-017-async-rejection.spec.js` | TC-FIAB-017 | defecto-conocido (aceptación) | M-05 · WT-03 |

**Validación de requisitos y análisis de aceptación (criterio d).** TC-FIAB-043 valida el requisito operativo central: un BIBLIOTECARIO registra y devuelve un préstamo accionando la interfaz, con confirmación visible y sin amonestación por mora en devolución a tiempo — el flujo end-to-end integra sin fallas (aceptado). TC-FIAB-017 ejercita, de forma reproducible, el rechazo de una promesa async ante pérdida de red: **confirma el defecto WT-03** (spinners no restaurados, sin mensaje al usuario). El nivel de aceptación reproduce por interfaz lo que TC-FIAB-020 verifica a nivel sistema, cerrando la trazabilidad UI↔backend exigida por PP-FIAB-001 §4.4.

---

## 5. Incidencias confirmadas por ejecución (29119-3 §7.4.4 — incident summary)

Cada caso `defecto-conocido` traza a una incidencia del walkthrough. La ejecución dinámica **confirmó** los hallazgos estáticos (no los refutó, salvo la nota de D-015 abajo):

| Incidencia | Hallazgo | Severidad | Confirmada por | Estado |
|---|---|---|---|---|
| INC-WT-01 | WT-01 — `LocalDate.parse` sin manejo de excepción | Alta | `ParseFechaInvalidaTest` (unitario); aflora también en `PrestarJsonMalformadoTest` (sistema) | ✅ Confirmada |
| INC-WT-02 (advice) | WT-02 — ausencia de `@RestControllerAdvice` → riesgo de stacktrace | Alta → **Menor** | `PrestarJsonMalformadoTest`, `MultipartLimitTest` | ⚠️ **Refutada parcialmente** (#52) |
| INC-WT-02 (pago) | WT-02 / TCOND-M6 — `pagarAmonestacion` persiste sin validar | Alta | `PagarAmonestacionTest` (integración) | ✅ Confirmada |
| INC-WT-03 | WT-03 — funciones async sin manejo de rechazo | Media | `tc-fiab-017-async-rejection` (aceptación) | ✅ Confirmada |
| INC-WT-04 | WT-04 — mutaciones múltiples sin `@Transactional` | Alta | `TransactionalGapTest` (integración) | ✅ Confirmada |

> **Nota de refutación parcial (D-015 / issue #52).** El hallazgo estático "ausencia de `@RestControllerAdvice`" anticipaba exposición de stacktrace vía HTTP 500. La ejecución lo **adjudicó en contra**: ante JSON con tipos incorrectos, Spring responde **HTTP 400** por su manejador por defecto de `HttpMessageNotReadableException`; ante multipart sobre el límite, `DefaultHandlerExceptionResolver` responde **HTTP 413** — ambos **sin** `@RestControllerAdvice` y sin filtrar la traza. El riesgo declarado no se materializó. El hallazgo no se elimina: se **reclasifica** de Alta a Menor (observación de mantenibilidad — el manejo de errores queda delegado al framework, sin política explícita, y los escenarios no cubiertos por los manejadores por defecto siguen sin control). Se registra con la misma formalidad que los confirmados: un proceso que solo publica los hallazgos que le dieron la razón no mide, selecciona.

---

## 6. Métricas de resultados (ISO/IEC 25023 — ratificadas, issue #24)

El estado *cumple/no cumple* lo calcula la herramienta (`metricas/calcular_kpi.py`) a partir del valor y el umbral; nunca se declara a mano.

| ID | Métrica | Valor | Umbral | Estado | Fuente |
|---|---|---|---|---|---|
| M-01 | Densidad de defectos de fiabilidad | 1.0 def/módulo | ≤ 1.0 | ✅ cumple | Declarada (walkthrough §5.2) |
| M-02 | Cobertura de decisión/rama | 60.7% | ≥ 50% | ✅ cumple | Automática (JaCoCo) |
| M-03 | Tasa de pruebas que pasan | 100% | ≥ 100% | ✅ cumple | Automática (Surefire) |
| M-04 | Cobertura de instrucciones | 38.1% | ≥ 30% | ✅ cumple | Automática (JaCoCo) |
| M-05 | Entradas inválidas controladas | 55.6% | ≥ 80% | ❌ no cumple | Declarada (ejecución + TCS-FIAB-001 §4) |
| M-06 | Operaciones con guarda de estado | 75.0% | ≥ 80% | ❌ no cumple | Declarada (objetivos.txt §2.2) |

**Lectura de las métricas.** Las métricas de la **suite** (M-02, M-03, M-04) cumplen: la cobertura y la tasa de aprobación son las esperadas para la fase. Las métricas del **producto** (M-05, M-06) **no cumplen, y ese es el resultado de la auditoría**: el SUT controla solo el 55.6% de las entradas inválidas probadas y una de cada cuatro operaciones críticas (`renovarPrestamo`, que decrementa inventario sin verificar disponibilidad) carece de guarda de estado. M-01 = 1.0 def/módulo se sitúa en el límite del rango aceptable; a nivel de defecto puntual (auditoría estática 2026-06-02) la densidad asciende a ~2.0. Ambas lecturas convergen en el veredicto: el SUT no integró la fiabilidad como característica intrínseca.

---

## 7. Trazabilidad ejecutada (síntesis)

Cadena completa **hallazgo → caso → clase de prueba → nivel → suite → métrica → resultado**, conforme a PP-FIAB-001 §6:

| Hallazgo/Objetivo | Caso | Clase ejecutada | Nivel | Suite | Métrica | Resultado |
|---|---|---|---|---|---|---|
| Cobertura Madurez | TC-FIAB-004/018/007 | `PrestamoServiceCrearPrestamoTest`, `PrestamosActivosLimiteTest`, `EliminarAmonestacionTest` | Unitario | regresion | M-02 | ✅ |
| WT-01 | TC-FIAB-008 | `ParseFechaValida/InvalidaTest` | Unitario | reg/def | M-03/M-05 | ✅ (defecto confirmado) |
| Madurez inventario | TC-FIAB-019 | `PrestamoEstadoInventarioTest` | Integración | regresion | M-02 | ✅ |
| Escenario operativo | TC-FIAB-020 | `PrestamoMoraAmonestacionTest` | Integración | regresion | M-01/M-03 | ✅ |
| Pago sin validar (TCOND-M6) | TC-FIAB-025 | `PagarAmonestacionTest` | Integración | defecto-conocido | M-05 | ✅ (defecto confirmado) |
| WT-04 | TC-FIAB-022 | `TransactionalGapTest` | Integración | defecto-conocido | M-01 | ✅ (defecto confirmado) |
| Sintaxis JSON | TC-FIAB-011 | `PrestarJsonMalformadoTest` | Sistema | defecto-conocido | M-05 | ⚠️ T2.1→400 (refuta advice); T2.2→500 (WT-01) |
| Multipart límite | TC-FIAB-021 | `MultipartLimitTest` | Sistema | defecto-conocido | M-05 | ⚠️ HTTP 413 — no materializado (§5) |
| Gating de seguridad | SC-SEC-01 (#15) | `SecurityGatingTest` | Sistema | regresion | M-03 | ✅ |
| Smoke | TC-FIAB-001 | `GestionBibliotecariaApplicationTests` | Smoke | regresion | M-03 | ✅ |
| Escenario por UI | TC-FIAB-043 | `tc-fiab-043-prestamo-e2e` | Aceptación | regresion | M-01/M-03 | ✅ |
| WT-03 | TC-FIAB-017 | `tc-fiab-017-async-rejection` | Aceptación | defecto-conocido | M-05 | ✅ (defecto confirmado) |

---

## 8. Desviaciones plan vs ejecutado (29119-3 §7.4.5)

- **Casos diferidos (13):** los casos de *Disponibilidad*, *Capacidad de Recuperación* y *Capacidad/carga* del documento fuente quedan diferidos y especificados en el Anexo A (`2026-06-24_casos-diferidos-fiabilidad.md`), fuera del alcance Madurez + Tolerancia declarado en §2.2. **La brecha se reporta, no se rellena con casos ficticios.**
- **Celdas `[PLANIFICADO]`:** la matriz de cobertura técnica de TCS-FIAB-001 §3 mantiene celdas planificadas sin caso ejecutable en esta iteración (p. ej. Sintaxis en Madurez, Escenarios en Tolerancia); permanecen en el plan exhaustivo.
- **Suite `defecto-conocido` informativa:** por decisión de estrategia (EST-FIAB-001 §5), estos casos no bloquean el gate; documentan el defecto de forma reproducible. Es una desviación deliberada, no una omisión.

---

## 9. Evaluación de criterios de salida (PP-FIAB-001 §5.2)

| Criterio de salida | Resultado |
|---|---|
| Suite `regresion` en verde para integrar a `main` | ✅ Cumplido — 0 fallos |
| Casos `defecto-conocido` ejecutados (informativos) | ✅ Cumplido — confirman INC-WT-01/02/03/04 |
| M-02 ≥ 50% en `PrestamoService` | ✅ Cumplido — 60.7% |
| M-03 = 100% | ✅ Cumplido |
| Niveles unitario, integración, sistema y aceptación implementados y en ejecución | ✅ Cumplido |

---

## 10. Conclusiones — ¿Se lograron los objetivos?

**Sí, se lograron los objetivos del proceso de aseguramiento.** El Equipo 11 planificó, ejecutó y documentó los cuatro niveles de prueba (unitario, integración, sistema y aceptación) con enfoques de caja blanca, gris y negra, sobre la característica Reliability del SUT, y el proceso está integrado y automatizado en el ecosistema de CI. La suite completa (34 pruebas JVM + 2 de aceptación) ejecuta en verde y de forma reproducible, y alimenta un dashboard de métricas ratificadas.

**Sobre la calidad del producto auditado, el veredicto es negativo y está sustentado.** La fiabilidad no fue integrada como característica intrínseca del Sistema de Gestión Bibliotecaria: las pruebas `defecto-conocido` confirmaron en ejecución los hallazgos de parsing de fecha (WT-01), pago sin validar (TCOND-M6), manejo async (WT-03) y ausencia de atomicidad transaccional (WT-04); y las métricas de producto M-05 (55.6%) y M-06 (75%) quedan por debajo de su umbral. La misma ejecución **adjudicó en contra** el riesgo de exposición de stacktrace por ausencia de `@RestControllerAdvice`, reclasificado de Alta a Menor (#52) — señal de que el proceso mide, no selecciona. Este resultado no es una falla del proceso de SQA — **es su hallazgo principal**: el proceso cumplió su función de diagnóstico, cuantificando y evidenciando la deuda de fiabilidad del SUT para su remediación por el Equipo 58-1 en iteraciones posteriores.

El valor del ejercicio reside precisamente en esa distinción: una suite de pruebas madura (M-02/M-03/M-04 en verde) que mide con honestidad un producto deficiente (M-05/M-06 en rojo), sin ajustar la vara para maquillar el resultado.

---

*Informe de Resultados de Pruebas conforme a ISO/IEC/IEEE 29119-3:2021 (§7.4), característica Reliability (Madurez · Tolerancia a Fallos) de ISO/IEC 25010:2023. Equipo SQA T 11 — emitido el 19 de julio de 2026. Cierre de la Fase 2.*
