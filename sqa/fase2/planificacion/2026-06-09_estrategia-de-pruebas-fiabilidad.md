# UNIVERSIDAD CATÓLICA ANDRÉS BELLO

```
Facultad de Ingeniería — Escuela de Ingeniería Informática
Aseguramiento de la Calidad del Software — Prof. Ernesto Suárez — NRC: 25790
```

# ESTRATEGIA DE PRUEBAS — FIABILIDAD (ISO/IEC 25010:2023)

**Proyecto evaluado: Sistema de Gestión Bibliotecaria — Equipo 58-1**

| Campo | Valor |
|---|---|
| Identificador | EST-FIAB-001 |
| Versión | 2.0 |
| Estado | Revisado |
| Fecha | 2026-06-24 |
| Organización emisora | Equipo SQA T 11 — Proyecto 16 (Turno Tarde) |
| Autoridad de aprobación | Líder General (Alberto Rodriguez) |
| Naturaleza (29119-3) | **Estrategia de prueba de proyecto** (tailoring específico del proyecto, no una *Organizational Test Strategy* A.2.3 válida para toda la organización). Provee los enunciados de estrategia que el Plan PP-FIAB-001 adapta en su §4. |
| Característica evaluada | Reliability — ISO/IEC 25010:2023 |
| Sub-características | Madurez · Tolerancia a Fallos |
| Base de prueba | Walkthrough técnico 2026-06-02 (hallazgos WT-01..WT-04) + objetivos.txt |
| Autor del SUT | Equipo 58-1 (autores del software) |

### Historial de cambios
| Versión | Fecha | Descripción del cambio | Razón | Autor |
|---|---|---|---|---|
| 1.0 | 2026-06-09 | Versión inicial (Tolerancia a Fallos · Capacidad de Recuperación; métricas IEEE 1061; ecosistema Jira/Confluence). | Planificación inicial Fase 2 | Equipo 11 |
| 2.0 | 2026-06-24 | Segunda sub-característica realineada a **Madurez** (`objetivos.txt`); métricas remapeadas a ISO/IEC 25023; referencias migradas a GitHub-native; declaración de naturaleza y campos de control de documento (29119-3). | Realineación + conformidad 29119-3 | Equipo 11 |

---

## Tabla de Contenido

- [1. Propósito y Alcance](#1-propósito-y-alcance)
- [2. Justificación de Estándares Aplicados](#2-justificación-de-estándares-aplicados)
- [3. Enfoque por Sub-característica](#3-enfoque-por-sub-característica)
- [4. Niveles de Prueba](#4-niveles-de-prueba)
- [5. Política de Suites y Etiquetas](#5-política-de-suites-y-etiquetas)
- [6. Modelo de Autoría y Grado de Independencia](#6-modelo-de-autoría-y-grado-de-independencia)
- [7. Herramientas y Automatización](#7-herramientas-y-automatización)
- [8. Métricas de Calidad](#8-métricas-de-calidad)
- [9. Gestión de Configuración e Incidencias](#9-gestión-de-configuración-e-incidencias)

---

## 1. Propósito y Alcance

Esta Estrategia de Pruebas define el enfoque, los niveles, las técnicas y las restricciones que guían el diseño y la ejecución de las pruebas de **Fiabilidad** para el Sistema de Gestión Bibliotecaria (Equipo 58-1). Constituye el documento rector que da forma al Plan de Pruebas (PP-FIAB-001) y a todas las especificaciones de casos de prueba derivadas.

### 1.1 Objetivos estratégicos

1. Obtener evidencia objetiva y reproducible del comportamiento del sistema en operación normal y frente a entradas malformadas, en cumplimiento de la característica *Reliability* de ISO/IEC 25010:2023, sub-características **Madurez** y **Tolerancia a Fallos**.
2. Proveer al equipo de desarrollo (Equipo 58-1) especificaciones precisas de casos de prueba que le permitan implementar las suites JUnit 5 requeridas por el evaluador.
3. Establecer criterios de clasificación de resultados (suite `regresion` vs. suite `defecto-conocido`) coherentes con la restricción de código congelado del enunciado.

### 1.2 Alcance funcional

| Capa | Módulos en alcance |
|---|---|
| Backend — Servicios | `PrestamoService`, `LibroService`, `UsuarioService`, `AmonestacionService` |
| Backend — Controlador | `Controller.java` (métodos de préstamo, devolución, renovación, reseñas) |
| Frontend — Componentes Vue | `PantallaLibro.vue`, `SolicitudVerificacionPago.vue`, `VerificarPago.vue`, `main.js` |

### 1.3 Fuera del alcance

- **Capacidad de Recuperación** y **Disponibilidad** (otras sub-características de Reliability): no seleccionadas para esta práctica conforme a `objetivos.txt`. Los hallazgos de recuperación detectados en el walkthrough (atomicidad transaccional) se reinterpretan como **defectos de Madurez** (estado inconsistente en operación normal), no como casos de recuperación.
- **Seguridad** (Confidencialidad, Integridad, Responsabilidad): cubierta por auditoría previa (Fase 1).
- **Mantenibilidad** (Analizabilidad, Reusabilidad, Capacidad para ser probado): cubierta por checklist COD-01..COD-06.
- **Adecuación Funcional**: tratada en suites E2E de Playwright separadas.
- Correcciones de código en producción (`src/main`, `biblioteca-frontend/src`): el código está congelado.

---

## 2. Justificación de Estándares Aplicados

| Estándar | Versión | Aplicación en esta estrategia |
|---|---|---|
| ISO/IEC 25010 | 2023 | Modelo de calidad que define las sub-características *Maturity* y *Fault Tolerance* como objeto de evaluación. Estructura la selección de técnicas y los criterios de clasificación de hallazgos. |
| ISO/IEC/IEEE 29119-1 | 2022 | Conceptos y vocabulario de pruebas de software. Proporciona los términos base: ítem de prueba, base de prueba, nivel de prueba, técnica de diseño, criterio de entrada/salida. |
| ISO/IEC/IEEE 29119-2 | 2021 | Proceso de pruebas. Define el proceso de planificación (del que esta estrategia es la política de nivel superior) y las actividades de diseño, implementación, ejecución y reporte. |
| ISO/IEC/IEEE 29119-3 | 2021 | Documentación de pruebas. Define las plantillas de Test Plan, Test Design Specification, Test Case Specification y Test Completion Report que estructuran el Plan de Pruebas y las especificaciones de casos derivadas. |
| ISO/IEC/IEEE 29119-4 | 2021 | Técnicas de diseño de pruebas. Justifica el uso de partición de equivalencia, análisis de valores límite, cobertura de decisión e inyección de fallos como técnicas seleccionadas para esta estrategia. |
| ISO/IEC 25023 | 2016 | Medidas de calidad de producto. Proporciona las fórmulas de medición para *Maturity* (cobertura de pruebas, densidad de defectos) y *Fault Tolerance* (evitación de fallos) que sustentan las métricas de esta estrategia. |
| ISO/IEC/IEEE 15289 | 2019 | Rige la estructura y el contenido del presente documento como artefacto de documentación de proceso de verificación. |

---

## 3. Enfoque por Sub-característica

La fiabilidad no se mide con una sola aserción booleana: se **infiere** observando el comportamiento del sistema en operación normal y ante condiciones adversas controladas. Las dos sub-características seleccionadas requieren enfoques distintos.

### 3.1 Tolerancia a Fallos

**Definición (ISO/IEC 25010:2023):** Grado en que el sistema opera según lo previsto a pesar de la presencia de fallos de hardware o software (incluyendo entradas inválidas).

**Técnicas empleadas:**

| Técnica | Descripción operacional | Hallazgos que cubre |
|---|---|---|
| **Inyección de fallos** | Configurar Mockito para lanzar `DateTimeParseException`, `DataAccessException` o `IOException` en el punto exacto donde el SUT debería capturarlas. Observar si el sistema propaga la excepción o la absorbe con respuesta controlada. | WT-01, WT-02 |
| **Partición de equivalencia** | Dividir el dominio de entradas en clases válidas e inválidas. Para fechas: formato ISO 8601 correcto (válida), cadena vacía (inválida), formato no estándar `dd-MM-yyyy` (inválida), `null` (inválida). | WT-01 |
| **Análisis de valores límite** | Probar los extremos de cada clase de equivalencia: fecha exactamente en el límite del rango aceptable, cadena de longitud 0 vs. 1 carácter, valores máximos de `Long` para IDs. | WT-01 |
| **Revisión de respuesta HTTP** | Con `MockMvc`, verificar que ante excepción no controlada el status devuelto sea 400 o 500 con cuerpo JSON de error, no stacktrace. Ausencia de `@RestControllerAdvice` debe producir 500 con stacktrace expuesto — ese comportamiento se documenta como caso `defecto-conocido`. | WT-02 |
| **Prueba de funciones async (frontend)** | Simular fallos de red con `jest.fn()` o Playwright interceptando la red. Verificar que el componente Vue muestre retroalimentación al usuario y no genere `unhandled promise rejection`. | WT-03 |

**Principio general:** los casos de prueba de Tolerancia a Fallos son de **caja blanca en nivel unitario** (se conocen las rutas de código con problema) y de **caja negra en nivel de sistema** (se estimula la interfaz HTTP sin conocimiento interno).

### 3.2 Madurez

**Definición (ISO/IEC 25010:2023):** Grado en que el sistema satisface las necesidades de fiabilidad en condiciones de operación normal.

A diferencia de Tolerancia a Fallos (que estimula condiciones adversas), Madurez se evidencia probando que la **lógica de negocio crítica se comporta correctamente en operación normal** y midiendo la **ausencia de defectos** sobre esa lógica. La unidad de evidencia es la cobertura de las decisiones del código y la densidad de defectos detectados.

**Técnicas empleadas:**

| Técnica | Descripción operacional | Elementos que cubre |
|---|---|---|
| **Cobertura de decisión/rama (caja blanca)** | Diseñar casos JUnit 5 que ejerciten cada rama de los métodos críticos: las 6 guardas de `crearPrestamo`, las 3 ramas de `devolverPrestamo`, las 4 de `renovarPrestamo`, las 2 de `eliminarAmonestacion`. Medir con JaCoCo la cobertura de ramas alcanzada (objetivo ≥ 70%). | `PrestamoService`, `AmonestacionService` |
| **Pruebas de operación normal (flujo correcto)** | Verificar que, con datos válidos, cada operación produce el resultado y el estado esperados (préstamo registrado, stock decrementado, devolución finalizada, amonestación por mora generada). Constituyen la suite `regresion`. | Servicios backend |
| **Análisis de densidad de defectos** | Contabilizar los defectos confirmados por ejecución sobre los módulos en alcance (defectos/KLOC o por clase). Los defectos de no-atomicidad (WT-04, mutaciones múltiples sin `@Transactional`) se reinterpretan aquí como **defectos de Madurez**: en operación normal con fallo parcial, el sistema deja estado inconsistente. | Servicios backend |
| **Madurez de la suite de pruebas** | Medir la tasa de pruebas `regresion` que pasan como indicador de la madurez del conjunto de pruebas y del código bajo prueba. | Suite completa |

**Principio general:** los casos de prueba de Madurez son predominantemente de **caja blanca en nivel unitario** (cobertura de decisiones sobre rutas de código conocidas) complementados con pruebas de **integración** (caja gris) que verifican la consistencia de estado entre capas.

---

## 4. Niveles de Prueba

| Nivel | Enfoque de caja | Sub-característica cubierta | Herramienta principal | Base de prueba |
|---|---|---|---|---|
| **Unitario** | Blanca | Madurez + Tolerancia a Fallos | JUnit 5 + Mockito + JaCoCo | WT-01, WT-02 (tolerancia); cobertura de decisión de servicios (madurez) |
| **Integración** | Gris | Madurez + Tolerancia a Fallos | JUnit 5 + H2 + Spring Boot Test | WT-01, WT-04 (consistencia de estado entre capas) |
| **Sistema** | Negra | Tolerancia a Fallos | Spring Boot levantado + cliente HTTP (Postman/RestAssured) | WT-02 (respuesta HTTP ante entrada inválida), WT-03 (degradación frontend) |
| **Aceptación** | Negra | Madurez + Tolerancia a Fallos | Revisión manual contra ERS §NFR-FIAB-* | Todos WT-01..WT-04 |

### 4.1 Pruebas unitarias (caja blanca)

Se construyen en `src/test/java/com/biblioteca/service/` y `src/test/java/com/biblioteca/controller/`. Cada test establece el contexto mínimo con Mockito (`@ExtendWith(MockitoExtension.class)`), inyecta dependencias mockeadas y verifica el comportamiento de la unidad bajo prueba. La cobertura de decisión sobre los métodos críticos es la evidencia primaria de Madurez; los casos de inyección de excepción cubren Tolerancia a Fallos.

### 4.2 Pruebas de integración (caja gris)

Se construyen con `@SpringBootTest(webEnvironment = RANDOM_PORT)` y perfil `test` (H2 in-memory). Prueban la interacción entre capas (Controller → Service → Repository), incluyendo la consistencia de estado tras operaciones multi-entidad. El fallo a mitad de operación se implementa con un `@MockBean` parcial que lanza excepción después del primer `save()`, evidenciando el defecto de no-atomicidad como defecto de Madurez.

### 4.3 Pruebas de sistema (caja negra)

Un cliente HTTP (Postman o RestAssured) estimula los endpoints REST del sistema desplegado y verifica el comportamiento ante entradas inválidas (códigos de estado y cuerpos de error), sin conocimiento de la implementación interna.

### 4.4 Pruebas de aceptación (caja negra)

El equipo SQA revisa los resultados de los niveles anteriores contra los requisitos no funcionales de la ERS. Un hallazgo que falla consistentemente en `defecto-conocido` se documenta como incidencia abierta (GitHub Issue).

---

## 5. Política de Suites y Etiquetas

El proyecto de pruebas JUnit 5 organiza todos los casos en dos suites exclusivas identificadas por anotación `@Tag`:

### Suite `regresion`

- **Propósito:** Pruebas que DEBEN pasar en el código actual tal como está. Constituyen el gate de CI y la evidencia de Madurez en operación normal.
- **Contenido:** Verificaciones de comportamiento observable y correcto según la ERS (flujos felices, validaciones básicas, comportamientos que el SUT sí implementa correctamente).
- **CI:** `mvn verify -Dgroups=regresion` — falla el pipeline si algún caso no pasa.
- **Nota:** Incluye los tests de `crearPrestamo` con datos correctos que sí persisten, login correcto, etc.

### Suite `defecto-conocido`

- **Propósito:** Pruebas que DOCUMENTAN un comportamiento defectuoso conocido. Se ejecutan en CI pero NO bloquean el pipeline.
- **Contenido:** Todo caso de prueba que exponga un hallazgo WT-01..WT-04. Cada método de test lleva `@Tag("defecto-conocido")` y en su Javadoc la referencia a la incidencia: `@see INC-WT-01`, `@see INC-WT-04`, etc.
- **CI:** `mvn verify -Dgroups=defecto-conocido -DfailIfNoTests=false` — siempre verde en el pipeline; los fallos se reportan en el resumen de Surefire.
- **Convención de Javadoc:**
  ```java
  /**
   * Verifica que PrestamoService.crearPrestamo propague DateTimeParseException
   * sin captura cuando la fecha viene en formato incorrecto.
   *
   * @see INC-WT-01
   * @tag defecto-conocido
   */
  ```

### Separación en pom.xml

```xml
<!-- Perfil CI regresion (gate) -->
<profile>
  <id>ci-regresion</id>
  <properties>
    <groups>regresion</groups>
  </properties>
</profile>

<!-- Perfil CI defecto-conocido (informativo) -->
<profile>
  <id>ci-defecto</id>
  <properties>
    <groups>defecto-conocido</groups>
    <failsafe.failIfNoSpecifiedTests>false</failsafe.failIfNoSpecifiedTests>
  </properties>
</profile>
```

---

## 6. Modelo de Autoría y Grado de Independencia

**Grado de independencia (29119-3 §A.2.3.b.iv):** la prueba la diseña un equipo (Equipo 11) **independiente** del equipo autor del SUT (Equipo 58-1). Es independencia organizativa plena: el equipo que asegura la calidad no es el que desarrolló el software, lo que maximiza la objetividad de los hallazgos.

La restricción del enunciado establece que el código de producción está congelado y que el equipo SQA no escribe código de prueba directamente en el repositorio del Equipo 58-1. El modelo opera así:

| Rol | Responsabilidad | Artefacto producido |
|---|---|---|
| **Equipo 11 — Analista de Pruebas** | Diseña y especifica los casos de prueba con nivel de detalle suficiente para que un desarrollador los implemente sin ambigüedad (datos de entrada, precondiciones, pasos, resultado esperado, etiqueta @Tag). | Especificaciones de casos de prueba (este doc + PP-FIAB-001) |
| **Equipo 11 — Líder de Métricas (Edwin Li)** | Define umbrales de métricas, revisa resultados JaCoCo, calcula densidad de defectos y cobertura de decisión de ejecución. | Informe de métricas (post-ejecución) |
| **Equipo 11 — Escriba (Samuel Artiles)** | Documenta hallazgos de ejecución como incidencias (GitHub Issues) con referencia al hallazgo WT correspondiente. | Incidencias en GitHub Issues |
| **Equipo 58-1 (autores del SUT)** | Implementa los métodos `@Test` conforme a las especificaciones del Equipo 11. Configura `pom.xml` con H2, JaCoCo y Surefire. Crea la rama `simulacion-desarrollo` y ejecuta los sprints simulados. | Código de prueba en rama `simulacion-desarrollo` |

---

## 7. Herramientas y Automatización

**Automatización (29119-3 §A.2.3.a.iv):** las pruebas unitarias y de integración se ejecutan automáticamente en CI (GitHub Actions, `ci-fiabilidad.yml`) en cada push a `simulacion-desarrollo`; JaCoCo genera la cobertura de rama; SonarCloud recibe los resultados. Las pruebas de sistema (caja negra) y las de frontend se ejecutan de forma manual/asistida (Postman/RestAssured, Playwright).

| Herramienta | Versión | Uso en esta estrategia | Consistencia con PACS-Fase2 |
|---|---|---|---|
| **JUnit 5** (Jupiter) | 5.10+ | Framework base para pruebas unitarias e integración. `@Tag`, `@ExtendWith`, `@SpringBootTest`. | Declarado como herramienta de fiabilidad en PACS §3.1 |
| **Mockito** | 5.x | Stubs y drivers: simula `PrestamoRepository`, `LibroRepository`, lanza excepciones controladas en el punto exacto. | Implícito en suites JUnit 5 del PACS |
| **H2 Database** | 2.x | Base de datos in-memory para pruebas de integración. Perfil `test` con `spring.datasource.url=jdbc:h2:mem:testdb`. | Implícito en TestContainers / integración del PACS |
| **JaCoCo** | 0.8.11+ | Cobertura de **decisión/rama** e instrucciones. Objetivo: ≥ 70% de decisión en clases bajo prueba (métrica primaria de Madurez). Reporte HTML en `target/site/jacoco/`. | Declarado explícitamente en PACS §3.1 y §7.1 |
| **Maven Surefire** | 3.x | Ejecución de tests por tag, generación de reportes XML. Integrado con JaCoCo. | Maven declarado en PACS §7.1 |
| **Postman / RestAssured** | — | Estímulo de endpoints REST en pruebas de sistema (caja negra) ante entradas inválidas. | Herramientas de prueba dinámica del PACS |
| **GitHub Actions** | — | Workflow `ci-fiabilidad.yml` en rama `simulacion-desarrollo`. Ejecuta `mvn verify` por sprint. | Declarado como orquestador en PACS §3.2 |
| **Spring Boot Test** | 3.4.5 | `@SpringBootTest`, `MockMvc`, `@MockBean` para pruebas de integración de capa web. | Stack del SUT (PACS §2.1) |

---

## 8. Métricas de Calidad

Las métricas se calculan al cierre de cada sprint de integración simulada y al final de la Fase 2, y son coherentes con el marco de `referencias/objetivos.txt` (ISO/IEC 25010 → ISO/IEC 25023). Los umbrales marcados [PROP] son propuestas conservadoras a confirmar por el Líder de Métricas / Líder General.

| ID | Nombre | Sub-característica / Atributo | Fórmula | Rangos de calificación | Fuente de datos |
|---|---|---|---|---|---|
| M-01 | Densidad de Defectos de Fiabilidad (DDF) | Madurez — Ausencia de defectos | Defectos confirmados por ejecución / Módulos (o KLOC) bajo prueba | Bueno: 0 – 1.0 · Regular: 1.1 – 2.0 · Malo: > 2.0 | Surefire (defecto-conocido) |
| M-02 | Cobertura de Decisión/Rama | Madurez — Corrección de lógica crítica | (Ramas ejercitadas / Ramas totales en métodos críticos) × 100 | Bueno: ≥ 70% [PROP] · Regular: 50–69% · Malo: < 50% | JaCoCo branch coverage |
| M-03 | Tasa de Pruebas que Pasan | Madurez — Madurez de la suite | (Pruebas `regresion` exitosas / Pruebas `regresion` ejecutadas) × 100 | Bueno: 100% [PROP] · Regular: 90–99% · Malo: < 90% | Surefire XML |
| M-04 | Cobertura de Instrucciones JaCoCo | Madurez — soporte | (Instrucciones cubiertas / Total instrucciones) × 100 | Bueno: ≥ 60% · Regular: 40–59% · Malo: < 40% | JaCoCo report |
| M-05 | Entradas Inválidas Controladas | Tolerancia a Fallos — Manejo de entradas inválidas | (Casos inválidos manejados sin excepción no controlada / Casos inválidos probados) × 100 | Bueno: ≥ 80% [PROP] · Regular: 60–79% · Malo: < 60% | Surefire (regresion + defecto-conocido) |
| M-06 | Operaciones con Guarda de Estado | Tolerancia a Fallos — Prevención de estados inconsistentes | (Operaciones críticas con validación de precondición / Operaciones críticas totales) × 100 | Bueno: ≥ 80% [PROP] · Regular: 60–79% · Malo: < 60% | Revisión + Surefire |

> **Coherencia con walkthrough:** los valores base de densidad de defectos y cobertura obtenidos en el walkthrough del 2026-06-02 son el punto de partida. Las métricas de ejecución (M-02..M-06) complementan la evaluación con datos dinámicos que el walkthrough no podía proveer.
>
> **Métricas retiradas en v2.0:** M-06 (MTTR de transacción) y M-07 (tasa de error bajo carga JMeter) de la versión 1.0 medían *Capacidad de Recuperación* y quedan fuera del alcance al sustituirse esa sub-característica por Madurez.

---

## 9. Gestión de Configuración e Incidencias

### 9.1 Gestión de configuración de los productos de trabajo de prueba (29119-3 §A.2.3.a.v)
Todos los artefactos de prueba (Plan, Estrategia, Especificación de casos, código `@Test`) se versionan en **Git**, en el repositorio público del proyecto. El código de prueba se integra en la rama `simulacion-desarrollo`; los documentos de planificación viven en `sqa/fase2/planificacion/`. Cada documento lleva identificador, versión, estado e historial de cambios (este encabezado). Las revisiones por pares se evidencian mediante Pull Requests (IEEE 730).

### 9.2 Gestión de incidencias (29119-3 §A.2.3.a.vi)
Las incidencias se registran como **GitHub Issues** (plantilla "Defecto F2"), con etiquetas canónicas `tipo:defecto`, `severidad:*`, `fase:fase-2`, `iso:*`. Cada incidencia traza al hallazgo WT de origen, al caso `defecto-conocido` que la ejercita y al comportamiento esperado según la ERS. El flujo de estado se gestiona en el tablero GitHub Projects #4 (Backlog → En Ejecución → En Revisión → Cerrado). El detalle operativo está en el Plan PP-FIAB-001 §7.

---

*Documento generado el 9 de junio de 2026, revisado el 24 de junio de 2026 por el Equipo SQA 11 como parte de la Fase 2 del proceso de aseguramiento bajo ISO/IEC/IEEE 29119-2/-3 y la característica Reliability (Madurez · Tolerancia a Fallos) de ISO/IEC 25010:2023.*
