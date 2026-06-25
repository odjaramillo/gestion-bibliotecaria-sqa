# UNIVERSIDAD CATÓLICA ANDRÉS BELLO

```
Facultad de Ingeniería — Escuela de Ingeniería Informática
Aseguramiento de la Calidad del Software — Prof. Ernesto Suárez — NRC: 25790
```

# ESPECIFICACIÓN DE CASOS DE PRUEBA — FIABILIDAD
## (Test Case Specification — ISO/IEC/IEEE 29119-3:2021, cláusula 7.3)

**Proyecto evaluado: Sistema de Gestión Bibliotecaria — Equipo 58-1**

---

## 1. Información del documento (29119-3 §7.3.2)

### 1.1 Identificación única del documento
| Campo | Valor |
|---|---|
| Identificador | TCS-FIAB-001 |
| Versión | 1.0 |
| Estado | Borrador para revisión |
| Fecha de emisión | 2026-06-24 |

### 1.2 Organización emisora
Equipo SQA T 11 — Proyecto 16 (Turno Tarde). Autor: Analista de Pruebas (Oscar Jaramillo).

### 1.3 Autoridad de aprobación
Líder General del Equipo 11 (Alberto Rodriguez) — responsable de revisar y aprobar esta especificación antes de su entrega al equipo autor del SUT (Equipo 58-1). Revisor de métricas: Líder de Métricas (Edwin Li).

### 1.4 Historial de cambios
| Versión | Fecha | Descripción del cambio | Razón | Autor |
|---|---|---|---|---|
| 1.0 | 2026-06-24 | Creación. Síntesis de casos anclados al código desde `casos-de-prueba-adicionales(revisar).md`. Alcance: Madurez + Tolerancia a Fallos. | Realineación de Fase 2 a `objetivos.txt` | Equipo 11 |

---

## 2. Introducción (29119-3 §7.3.3)

### 2.1 Alcance
Esta especificación detalla los **ítems de cobertura de prueba** y los **casos de prueba** de las sub-características **Madurez** y **Tolerancia a Fallos** (ISO/IEC 25010:2023) del SUT.

- **Inclusiones:** lógica de negocio crítica de `PrestamoService` y `AmonestacionService`; manejo de entradas inválidas en endpoints REST y en el frontend Vue.
- **Exclusiones:** Disponibilidad y Capacidad de Recuperación (sub-características no seleccionadas); los casos de esas sub-características del documento fuente quedan archivados.
- **Supuestos:** código de producción congelado (el Equipo 11 especifica, el Equipo 58-1 implementa los `@Test`).
- **Limitaciones:** las celdas marcadas `[PLANIFICADO]` en la matriz de cobertura quedan en el plan exhaustivo pero sin caso ejecutable en esta iteración; la brecha se reporta, no se rellena con casos ficticios.

### 2.2 Referencias
- **Externas:** ISO/IEC/IEEE 29119-3:2021 (estructura de este documento); ISO/IEC/IEEE 29119-4:2021 (técnicas de diseño); ISO/IEC 25010:2023 (modelo de calidad); ISO/IEC 25023:2016 (métricas).
- **Internas:** PP-FIAB-001 (Plan de Pruebas); EST-FIAB-001 (Estrategia); `referencias/objetivos.txt` (marco de métricas); `2026-06-02_walkthrough-fiabilidad-sut-biblioteca.md` (base de prueba, hallazgos WT-01..WT-04); `casos-de-prueba-adicionales(revisar).md` (fuente de casos anclados al código).

> **Nota de origen:** el documento `Generacion de Casos de Pueba.md` (CT-FIA-01..24) se descartó como fuente de contenido por afirmar mecanismos inexistentes en el SUT (`@Transactional`, `@ControllerAdvice`, Resilience4j, `@Retryable`, clúster/failover, validación `@Min/@Positive`). Solo se conservó su formato (taxonomía de técnicas + métrica por caso).

### 2.3 Convenciones de notación
| Prefijo | Significado |
|---|---|
| `TCOND-x#` | Condición de prueba (test condition) |
| `TCI-x#.#` | Ítem de cobertura de prueba (test coverage item) derivado de una condición por una técnica |
| `TC-FIAB-###` | Caso de prueba (ejercita uno o más TCI) |
| `WT-##` / `INC-WT-##` | Hallazgo del walkthrough / incidencia (GitHub Issue) asociada |
| `M-0#` | Métrica de `objetivos.txt` (ISO/IEC 25023) |

### 2.4 Glosario
- **TCI:** unidad mínima a cubrir, derivada de aplicar una técnica de 29119-4 a una condición de prueba.
- **Suite `regresion` / `defecto-conocido`:** clasificación de resultado definida en EST-FIAB-001 §5.

---

## 3. Matriz de cobertura técnica (plan exhaustivo)

Cruce sub-característica × técnica de diseño (ISO/IEC/IEEE 29119-4). Las celdas con TCI especificados llevan su condición de prueba; `[PLANIFICADO]` = en el plan, sin caso ejecutable en esta iteración.

| Sub-característica \ Técnica | Valores Límite | Partición Equiv. | Transición Estados | Basada en Escenarios | Sintaxis | Tablas de Decisión |
|---|---|---|---|---|---|---|
| **Madurez** | TCOND-M2 | TCOND-M1 | TCOND-M3 | TCOND-M4 | `[PLANIFICADO]` | TCOND-M5, TCOND-M6 |
| **Tolerancia a Fallos** | TCOND-T3 | TCOND-T1 | TCOND-T4 | `[PLANIFICADO]` | TCOND-T2 | TCOND-T5 |

---

## 4. Ítems de cobertura de prueba (29119-3 §7.3.4)

### 4.1 Madurez

**TCOND-M1 — Guardas de `PrestamoService.crearPrestamo` (Partición de equivalencia)** · Traza: `PrestamoService.java:29-64`

| TCI | Descripción | Partición | Prioridad |
|---|---|---|---|
| TCI-M1.1 | Usuario inexistente (`usuarioOpt.isEmpty()`, L31) | Inválida | Alta |
| TCI-M1.2 | Rol ≠ "USUARIO" (L34) | Inválida | Alta |
| TCI-M1.3 | ≥ 2 préstamos activos (L37) | Inválida | Alta |
| TCI-M1.4 | Usuario con amonestación no verificada (L40) | Inválida | Alta |
| TCI-M1.5 | Libro inexistente (L43) | Inválida | Alta |
| TCI-M1.6 | Libro con `cantidad < 1` (L45) | Inválida | Alta |
| TCI-M1.7 | Todos los datos válidos | Válida | Alta |

**TCOND-M2 — Tope de préstamos activos (Análisis de valores límite)** · Traza: `PrestamoService.java:36-37`

| TCI | Descripción | Prioridad |
|---|---|---|
| TCI-M2.1 | Frontera inferior: 1 préstamo activo (permite) | Media |
| TCI-M2.2 | Frontera: 2 préstamos activos (rechaza) | Media |
| TCI-M2.3 | Frontera superior: 3 préstamos activos (rechaza) | Baja |

**TCOND-M3 — Transición de estado e inventario (Transición de estados)** · Traza: `PrestamoService.java:56,60,78,82`

| TCI | Descripción | Prioridad |
|---|---|---|
| TCI-M3.1 | Transición `activo → finalizado` con devolución a tiempo; `cantidad` +1, sin amonestación | Alta |
| TCI-M3.2 | Sincronía de `cantidad`: −1 al prestar, +1 al devolver | Alta |

**TCOND-M4 — Escenario operativo completo (Basada en escenarios)** · Traza: flujo crear→devolver tarde→amonestación

| TCI | Descripción | Prioridad |
|---|---|---|
| TCI-M4.1 | Flujo completo sin fallas de integración de módulos | Media |
| TCI-M4.2 | Devolución tardía genera `Amonestacion` (monto 100.0, pagada=false, verificada=false), L87-96 | Media |

**TCOND-M5 — Guardas de `eliminarAmonestacion` (Tablas de decisión)** · Traza: `AmonestacionService.java:34-46`

| TCI | Descripción | Prioridad |
|---|---|---|
| TCI-M5.1 | Rol ≠ BIBLIOTECARIO (L37) | Media |
| TCI-M5.2 | Amonestación inexistente (L42) | Media |
| TCI-M5.3 | Rol BIBLIOTECARIO + amonestación existe → elimina (L45) | Media |

**TCOND-M6 — Validación de pago de amonestación [DEFECTO] (Tablas de decisión)** · Traza: `Controller.java:366-387` · WT-02

| TCI | Descripción | Prioridad |
|---|---|---|
| TCI-M6.1 | `metodoPago` vacío + comprobante provisto → debería rechazar; actual: persiste | Alta |
| TCI-M6.2 | `metodoPago`/`comprobantePago` null → debería rechazar; actual: marca `pagada=true` | Alta |
| TCI-M6.3 | Comprobante con caracteres de inyección → debería sanitizar; actual: persiste tal cual | Media |

### 4.2 Tolerancia a Fallos

**TCOND-T1 — Manejo de fecha en `crearPrestamo` (Partición de equivalencia)** · Traza: `PrestamoService.java:47` · WT-01 / INC-WT-01

| TCI | Descripción | Partición | Prioridad |
|---|---|---|---|
| TCI-T1.1 | Fecha ISO 8601 válida (`"2026-06-24"`) | Válida | Alta |
| TCI-T1.2 | Fecha con formato no ISO (`"24-06-2026"`) → `DateTimeParseException` | Inválida | Alta |
| TCI-T1.3 | Fecha basura (`"99/99/9999"`) → `DateTimeParseException` | Inválida | Alta |
| TCI-T1.4 | Fecha `null` → `NullPointerException` | Inválida | Alta |

**TCOND-T2 — Payload REST malformado en `/api/prestar` (Pruebas de sintaxis)** · Traza: `Controller.java` POST préstamo · WT-02 / INC-WT-02

| TCI | Descripción | Prioridad |
|---|---|---|
| TCI-T2.1 | JSON con tipos incorrectos (`isbn` no numérico) → respuesta HTTP | Alta |
| TCI-T2.2 | JSON sintácticamente roto (llaves sin cerrar) → respuesta HTTP | Alta |

**TCOND-T3 — Tamaño de archivo multipart (Análisis de valores límite)** · Traza: `Controller.java:66-73`

| TCI | Descripción | Prioridad |
|---|---|---|
| TCI-T3.1 | Archivo 0.9 MB (bajo el default 1MB) → acepta | Media |
| TCI-T3.2 | Archivo 1.0 MB (en el límite) → acepta | Media |
| TCI-T3.3 | Archivo 1.1 MB (sobre el límite) → `MaxUploadSizeExceededException` | Media |

**TCOND-T4 — Rechazo de promesa async en frontend (Transición de estados)** · Traza: `PantallaLibro.vue`, `SolicitudVerificacionPago.vue` · WT-03 / INC-WT-03

| TCI | Descripción | Prioridad |
|---|---|---|
| TCI-T4.1 | Promesa Pendiente → Rechazada (red Offline) sin `.catch` ni `errorHandler` | Media |

**TCOND-T5 — Ausencia de frontera transaccional [DEFECTO] (Tablas de decisión)** · Traza: `PrestamoService.java:58,61` · WT-04 / INC-WT-04

| TCI | Descripción | Prioridad |
|---|---|---|
| TCI-T5.1 | Fallo entre los dos `save()` sin `@Transactional` → registro huérfano | Alta |

---

## 5. Casos de prueba (29119-3 §7.3.5)

> Cada caso incluye: identificador, objetivo, prioridad, trazabilidad (a TCI), precondiciones, entradas, resultado esperado y una columna **Resultado real** a completar en ejecución (§7.3.5.9).

### TC-FIAB-004 — Cobertura de las guardas de `crearPrestamo`
- **Objetivo:** ejercitar las particiones de `crearPrestamo` para cobertura de decisión.
- **Prioridad:** Alta · **Suite:** `regresion` · **Métrica:** M-02 (cobertura de decisión ≥ 70%)
- **Trazabilidad:** TCI-M1.1 … TCI-M1.7
- **Precondiciones:** contexto Spring perfil `test` (H2); repositorios mockeados (Mockito).
- **Entradas y resultados esperados:**

| # | TCI | Entrada | Resultado esperado | Resultado real |
|---|---|---|---|---|
| 1 | TCI-M1.1 | `correoUsuario` inexistente | `"Usuario no registrado."` | _(ejecución)_ |
| 2 | TCI-M1.2 | usuario rol `"BIBLIOTECARIO"` | `"Solo se pueden asociar préstamos a usuarios con rol USUARIO."` | |
| 3 | TCI-M1.3 | usuario con 2 activos | `"El usuario ya tiene 2 préstamos activos."` | |
| 4 | TCI-M1.4 | usuario con amonestación no verificada | `"El usuario tiene amonestaciones activas."` | |
| 5 | TCI-M1.5 | `isbn` inexistente | `"Libro no encontrado."` | |
| 6 | TCI-M1.6 | libro `cantidad = 0` | `"Libro no disponible para préstamo."` | |
| 7 | TCI-M1.7 | datos válidos | `"Préstamo registrado con éxito."` + `cantidad` −1 | |

### TC-FIAB-018 — Valor límite del tope de préstamos activos
- **Objetivo:** verificar la frontera de `prestamosActivos >= 2`. · **Prioridad:** Media · **Suite:** `regresion` · **Métrica:** M-02
- **Trazabilidad:** TCI-M2.1, TCI-M2.2, TCI-M2.3
- **Precondiciones:** usuario rol `USUARIO`, libro disponible, sin amonestaciones.
- **Entradas:** préstamos activos previos = {1, 2, 3}.
- **Resultado esperado:** 1 → permite; 2 → rechaza; 3 → rechaza. Frontera correcta = 2.

### TC-FIAB-019 — Transición de estado e inventario
- **Objetivo:** verificar `activo → finalizado` y sincronía de `cantidad`. · **Prioridad:** Alta · **Suite:** `regresion` · **Métrica:** M-02
- **Trazabilidad:** TCI-M3.1, TCI-M3.2
- **Precondiciones:** libro `cantidad = 5`; usuario válido.
- **Entradas/pasos:** crear préstamo (cantidad → 4, estado `activo`); devolver antes de `fechaLimite` (cantidad → 5, estado `finalizado`, sin amonestación).
- **Resultado esperado:** estado e inventario consistentes en cada transición.

### TC-FIAB-020 — Escenario operativo end-to-end
- **Objetivo:** verificar el flujo completo sin fallas de integración. · **Prioridad:** Media · **Suite:** `regresion` · **Métrica:** M-01, M-03
- **Trazabilidad:** TCI-M4.1, TCI-M4.2
- **Precondiciones:** BD poblada; usuario y libro válidos.
- **Entradas/pasos:** crear préstamo con `fechaPrestamo` tal que `fechaLimite < hoy` al devolver → devolver tarde.
- **Resultado esperado:** flujo completo sin excepción; amonestación por mora creada (monto 100.0, pagada=false, verificada=false); suite `regresion` verde.

### TC-FIAB-007 — Tabla de decisión de `eliminarAmonestacion`
- **Objetivo:** cubrir las 2 decisiones del método. · **Prioridad:** Media · **Suite:** `regresion` · **Métrica:** M-02
- **Trazabilidad:** TCI-M5.1, TCI-M5.2, TCI-M5.3
- **Precondiciones:** contexto de servicio con repositorio mockeado.
- **Entradas y resultados esperados:**

| rol = BIBLIOTECARIO | amonestación existe | Resultado esperado | Resultado real |
|---|---|---|---|
| No | — | `"Solo los bibliotecarios pueden eliminar amonestaciones."` | _(ejecución)_ |
| Sí | No | `"Amonestación no encontrada."` | |
| Sí | Sí | `"Amonestación eliminada con éxito."` + `deleteById` invocado | |

### TC-FIAB-025 — Pago de amonestación sin validación [defecto-conocido]
- **Objetivo:** documentar la persistencia sin validar `metodoPago`/`comprobantePago`. · **Prioridad:** Alta · **Suite:** `defecto-conocido` · **Métrica:** M-01, M-06
- **Trazabilidad:** TCI-M6.1, TCI-M6.2, TCI-M6.3 · `Controller.java:366-387` · WT-02
- **Precondiciones:** usuario autenticado con una amonestación propia.
- **Entradas y resultados:**

| metodoPago | comprobantePago | Esperado (ERS) | Actual (defecto) | Resultado real |
|---|---|---|---|---|
| `"Transferencia"` | `"REF-12345"` | acepta | acepta | _(ejecución)_ |
| vacío | provisto | rechaza | persiste | |
| `null` | `null` | rechaza | marca `pagada=true` | |
| inyección SQL | cualquiera | rechaza/sanitiza | persiste tal cual | |

### TC-FIAB-008 — Partición de la fecha en `crearPrestamo`
- **Objetivo:** verificar el manejo de fechas válidas e inválidas. · **Prioridad:** Alta · **Suite:** `regresion` (válida) + `defecto-conocido` (inválidas) · **Métrica:** M-05
- **Trazabilidad:** TCI-T1.1 … TCI-T1.4 · `PrestamoService.java:47` · WT-01 / INC-WT-01
- **Precondiciones:** usuario válido, libro disponible.
- **Entradas y resultados:**

| TCI | `fechaPrestamoStr` | Esperado (ERS) | Actual (defecto) | Resultado real |
|---|---|---|---|---|
| TCI-T1.1 | `"2026-06-24"` | procesa | procesa | _(ejecución)_ |
| TCI-T1.2 | `"24-06-2026"` | HTTP 400 / mensaje | `DateTimeParseException` | |
| TCI-T1.3 | `"99/99/9999"` | HTTP 400 / mensaje | `DateTimeParseException` | |
| TCI-T1.4 | `null` | mensaje controlado | `NullPointerException` | |

### TC-FIAB-011 — Sintaxis: payload JSON malformado [defecto-conocido]
- **Objetivo:** verificar la respuesta HTTP ante JSON roto / tipos incorrectos. · **Prioridad:** Alta · **Suite:** `defecto-conocido` · **Métrica:** M-05
- **Trazabilidad:** TCI-T2.1, TCI-T2.2 · WT-02 / INC-WT-02
- **Precondiciones:** endpoint `POST /api/prestar` desplegado.
- **Entradas:** `{"isbn": "no-es-isbn", "fechaPrestamo": "99/99/9999", "correoUsuario": "x"}` (DTO real `PrestamoRequest`; `idLibro` NO existe).
- **Resultado esperado (documentado):** sin `@RestControllerAdvice` (grep = 0) → HTTP 500 con stacktrace, en lugar de HTTP 400.

### TC-FIAB-021 — Valor límite del tamaño multipart [defecto-conocido]
- **Objetivo:** verificar la frontera del límite por defecto de subida (1MB). · **Prioridad:** Media · **Suite:** `defecto-conocido` · **Métrica:** M-05
- **Trazabilidad:** TCI-T3.1, TCI-T3.2, TCI-T3.3 · `Controller.java:66-73`
- **Precondiciones:** endpoint `POST /api/libros` (multipart) desplegado.
- **Entradas:** archivos binarios de 0.9 / 1.0 / 1.1 MB como parte `imagen`.
- **Resultado esperado (documentado):** 1.1 MB lanza `MaxUploadSizeExceededException`; sin `@RestControllerAdvice` → HTTP 500 en lugar de HTTP 413. Trabajo futuro: configurar `spring.servlet.multipart.max-file-size`.

### TC-FIAB-017 — Transición de promesa async en frontend [defecto-conocido]
- **Objetivo:** verificar el manejo de rechazo de promesas ante pérdida de red. · **Prioridad:** Media · **Suite:** `defecto-conocido` · **Métrica:** M-05
- **Trazabilidad:** TCI-T4.1 · WT-03 / INC-WT-03
- **Precondiciones:** cliente Vue en ejecución; petición Axios async en curso.
- **Entradas:** forzar red `Offline` en DevTools durante la promesa; latencia 5000 ms.
- **Resultado esperado (documentado):** 9 funciones `async` sin `.catch` y `main.js` sin `app.config.errorHandler` → `Uncaught (in promise)`, spinners no restaurados, sin mensaje al usuario.

### TC-FIAB-022 — Ausencia de frontera transaccional [defecto-conocido]
- **Objetivo:** documentar la pérdida de atomicidad ante fallo parcial. · **Prioridad:** Alta · **Suite:** `defecto-conocido` · **Métrica:** M-01, M-06
- **Trazabilidad:** TCI-T5.1 · `PrestamoService.java:58,61` · WT-04 / INC-WT-04
- **Precondiciones:** prueba de integración con H2; `@MockBean LibroRepository`.
- **Entradas:** inyectar `RuntimeException` entre `prestamoRepository.save(prestamo)` (L58) y `libroRepository.save(libro)` (L61).
- **Resultado esperado (documentado):** sin `@Transactional`, no hay rollback; `Prestamo` huérfano persiste, `cantidad` no decrementada. Índice de corrupción esperado = 0; observado = 1 por aborto.

---

## 6. Resumen de trazabilidad

| Caso | Sub-car. | TCI ejercitados | Técnica | Suite | WT / INC | Métrica |
|---|---|---|---|---|---|---|
| TC-FIAB-004 | Madurez | TCI-M1.1..M1.7 | PE | regresion | cobertura | M-02 |
| TC-FIAB-018 | Madurez | TCI-M2.1..M2.3 | AVL | regresion | — | M-02 |
| TC-FIAB-019 | Madurez | TCI-M3.1, M3.2 | TE | regresion | TC-026 | M-02 |
| TC-FIAB-020 | Madurez | TCI-M4.1, M4.2 | PBE | regresion | TC-023 | M-01, M-03 |
| TC-FIAB-007 | Madurez | TCI-M5.1..M5.3 | TD | regresion | cobertura | M-02 |
| TC-FIAB-025 | Madurez | TCI-M6.1..M6.3 | TD | defecto-conocido | WT-02 | M-01, M-06 |
| TC-FIAB-008 | Tolerancia | TCI-T1.1..T1.4 | PE | regresion/defecto | WT-01 / INC-WT-01 | M-05 |
| TC-FIAB-011 | Tolerancia | TCI-T2.1, T2.2 | PS | defecto-conocido | WT-02 / INC-WT-02 | M-05 |
| TC-FIAB-021 | Tolerancia | TCI-T3.1..T3.3 | AVL | defecto-conocido | TC-034 | M-05 |
| TC-FIAB-017 | Tolerancia | TCI-T4.1 | TE | defecto-conocido | WT-03 / INC-WT-03 | M-05 |
| TC-FIAB-022 | Tolerancia | TCI-T5.1 | TD | defecto-conocido | WT-04 / INC-WT-04 | M-01, M-06 |

### 6.1 Remapeo de métricas IEEE 1061 (fuente) → ISO/IEC 25023 (vigente)
| IEEE 1061 (documento fuente) | ISO/IEC 25023 (`objetivos.txt`) |
|---|---|
| Tasa de Excepciones No Manejadas | M-05 — Entradas inválidas controladas |
| Densidad de Defectos Críticos | M-01 — Densidad de defectos |
| Cobertura de Transición de Estados | M-02 — Cobertura de decisión |
| Índice de Corrupción de Datos | M-06 — Operaciones con guarda de estado |

**Casos fuera de alcance (Disponibilidad / Recuperación):** TC-FIAB-028..032 y 038..042 del documento fuente quedan archivados.

---

*Especificación de Casos de Prueba conforme a ISO/IEC/IEEE 29119-3:2021 (§7.3), característica Reliability (Madurez · Tolerancia a Fallos) de ISO/IEC 25010:2023. Equipo SQA 11 — 24 de junio de 2026.*
