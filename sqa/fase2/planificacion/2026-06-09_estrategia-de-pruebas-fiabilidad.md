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
| Versión | 1.0 |
| Fecha | 2026-06-09 |
| Equipo SQA | Equipo T 11 — Proyecto 16 (Turno Tarde) |
| Característica evaluada | Reliability — ISO/IEC 25010:2023 |
| Sub-características | Tolerancia a Fallos · Capacidad de Recuperación |
| Base de prueba | Walkthrough técnico 2026-06-02 (hallazgos WT-01..WT-06) |
| Autor del SUT | Br. Carlos Méndez (Equipo 58-1) |

---

## Tabla de Contenido

- [1. Propósito y Alcance](#1-propósito-y-alcance)
- [2. Justificación de Estándares Aplicados](#2-justificación-de-estándares-aplicados)
- [3. Enfoque por Sub-característica](#3-enfoque-por-sub-característica)
- [4. Niveles de Prueba](#4-niveles-de-prueba)
- [5. Política de Suites y Etiquetas](#5-política-de-suites-y-etiquetas)
- [6. Modelo de Autoría](#6-modelo-de-autoría)
- [7. Herramientas](#7-herramientas)
- [8. Métricas de Calidad](#8-métricas-de-calidad)

---

## 1. Propósito y Alcance

Esta Estrategia de Pruebas define el enfoque, los niveles, las técnicas y las restricciones que guían el diseño y la ejecución de las pruebas de **Fiabilidad** para el Sistema de Gestión Bibliotecaria (Equipo 58-1). Constituye el documento rector que da forma al Plan de Pruebas (PP-FIAB-001) y a todas las especificaciones de casos de prueba derivadas.

### 1.1 Objetivos estratégicos

1. Obtener evidencia objetiva y reproducible del comportamiento del sistema frente a condiciones de fallo, entradas malformadas y escenarios de recuperación, en cumplimiento de la característica *Reliability* de ISO/IEC 25010:2023.
2. Proveer al equipo de desarrollo (Br. Carlos Méndez, Equipo 58-1) especificaciones precisas de casos de prueba que le permitan implementar las suites JUnit 5 requeridas por el evaluador.
3. Establecer criterios de clasificación de resultados (suite `regresion` vs. suite `defecto-conocido`) coherentes con la restricción de código congelado del enunciado.

### 1.2 Alcance funcional

| Capa | Módulos en alcance |
|---|---|
| Backend — Servicios | `PrestamoService`, `LibroService`, `UsuarioService` |
| Backend — Controlador | `Controller.java` (métodos de préstamo, devolución, renovación, reseñas) |
| Backend — Configuración | `application.properties` (HikariCP, datasource) |
| Frontend — Componentes Vue | `PantallaLibro.vue`, `SolicitudVerificacionPago.vue`, `VerificarPago.vue`, `main.js` |

### 1.3 Fuera del alcance

- **Seguridad** (Confidencialidad, Integridad, Responsabilidad): cubierta por auditoría previa (Fase 1).
- **Mantenibilidad** (Analizabilidad, Reusabilidad, Capacidad para ser probado): cubierta por checklist COD-01..COD-06.
- **Adecuación Funcional**: tratada en suites E2E de Playwright separadas.
- Correcciones de código en producción (`src/main`, `biblioteca-frontend/src`): el código está congelado.

---

## 2. Justificación de Estándares Aplicados

| Estándar | Versión | Aplicación en esta estrategia |
|---|---|---|
| ISO/IEC 25010 | 2023 | Modelo de calidad que define las sub-características *Fault Tolerance* y *Recoverability* como objeto de evaluación. Estructura la selección de técnicas y los criterios de clasificación de hallazgos. |
| ISO/IEC/IEEE 29119-1 | 2022 | Conceptos y vocabulario de pruebas de software. Proporciona los términos base: ítem de prueba, base de prueba, nivel de prueba, técnica de diseño, criterio de entrada/salida. |
| ISO/IEC/IEEE 29119-2 | 2021 | Proceso de pruebas. Define el proceso de planificación (del que esta estrategia es la política de nivel superior) y las actividades de diseño, implementación, ejecución y reporte. |
| ISO/IEC/IEEE 29119-4 | 202x | Técnicas de diseño de pruebas. Justifica el uso de partición de equivalencia, análisis de valores límite e inyección de fallos como técnicas seleccionadas para esta estrategia. |
| ISO/IEC 25023 | 2016 | Medidas de calidad de producto. Proporciona las fórmulas de medición para *Fault Tolerance* y *Recoverability* que complementan las métricas IEEE 1061 del walkthrough. |
| IEEE 1061 | 1998 | Metodología de métricas de calidad. Base de las métricas M-01 (DDF), M-02 (CRC) y M-03 (FTR) heredadas del walkthrough y extendidas con métricas de ejecución. |
| ISO/IEC/IEEE 15289 | 2019 | Rige la estructura y el contenido del presente documento como artefacto de documentación de proceso de verificación. |

---

## 3. Enfoque por Sub-característica

La fiabilidad no se mide directamente con aserciones sobre un valor booleano: se **infiere** observando el comportamiento del sistema ante condiciones adversas controladas. Las dos sub-características de la norma requieren enfoques distintos.

### 3.1 Tolerancia a Fallos

**Definición (ISO/IEC 25010:2023):** Grado en que el sistema opera según lo previsto a pesar de la presencia de fallos de hardware o software.

**Técnicas empleadas:**

| Técnica | Descripción operacional | Hallazgos que cubre |
|---|---|---|
| **Inyección de fallos** | Configurar Mockito para lanzar `DateTimeParseException`, `DataAccessException` o `IOException` en el punto exacto donde el SUT debería capturarlas. Observar si el sistema propaga la excepción o la absorbe con respuesta controlada. | WT-01, WT-02 |
| **Partición de equivalencia** | Dividir el dominio de entradas en clases válidas e inválidas. Para fechas: formato ISO 8601 correcto (válida), cadena vacía (inválida), formato no estándar `dd-MM-yyyy` (inválida), `null` (inválida). | WT-01 |
| **Análisis de valores límite** | Probar los extremos de cada clase de equivalencia: fecha exactamente en el límite del rango aceptable, cadena de longitud 0 vs. 1 carácter, valores máximos de `Long` para IDs. | WT-01 |
| **Revisión de respuesta HTTP** | Con `MockMvc`, verificar que ante excepción no controlada el status devuelto sea 400 o 500 con cuerpo JSON de error, no stacktrace. Ausencia de `@RestControllerAdvice` debe producir 500 con stacktrace expuesto — ese comportamiento se documenta como caso `defecto-conocido`. | WT-02 |
| **Prueba de funciones async (frontend)** | Simular fallos de red con `jest.fn()` o Playwright interceptando la red. Verificar que el componente Vue muestre retroalimentación al usuario y no genere `unhandled promise rejection`. | WT-03 |

**Principio general:** los casos de prueba de Tolerancia a Fallos son de **caja blanca en nivel unitario** (se conocen las rutas de código con problema) y de **caja negra en nivel de sistema** (se estimula la interfaz HTTP sin conocimiento interno).

### 3.2 Capacidad de Recuperación

**Definición (ISO/IEC 25010:2023):** Grado en que el sistema puede recuperar datos directamente afectados y restablecer el estado deseado del sistema después de una interrupción o un fallo.

**Técnicas empleadas:**

| Técnica | Descripción operacional | Hallazgos que cubre |
|---|---|---|
| **Fallo a mitad de transacción** | En pruebas de integración con H2, lanzar una excepción artificial después del primer `save()` en métodos multi-entidad (`crearPrestamo`, `devolverPrestamo`). Sin `@Transactional`, la primera entidad queda persistida; con `@Transactional`, el rollback restaura el estado. | WT-04 |
| **Verificación de atomicidad** | Tras el fallo forzado, consultar directamente el repositorio H2 para confirmar que ninguna entidad parcial quedó persistida. | WT-04 |
| **Prueba de pool de conexiones** | Verificar que `application.properties` contenga las claves HikariCP mínimas. En una prueba de integración de Spring Boot, inyectar el `DataSource` y verificar que el `HikariConfig` tenga valores configurados (no defaults). | WT-05 |
| **Carga sostenida con JMeter** | Ejecutar un plan de carga con 50 usuarios concurrentes durante 3 minutos sobre los endpoints críticos (`POST /api/prestamos`, `PUT /api/prestamos/{id}/devolver`). Medir tasa de error, tiempo de respuesta p95 y p99. | WT-05, WT-06 |
| **Interceptor de axios ausente** | En prueba de sistema, interrumpir el backend y verificar el comportamiento del frontend. Sin interceptor, los errores 5xx no deben propagarse silenciosamente; el caso `defecto-conocido` documenta la ausencia de pantalla de fallback. | WT-06 |

---

## 4. Niveles de Prueba

| Nivel | Enfoque de caja | Sub-característica cubierta | Herramienta principal | Base de prueba |
|---|---|---|---|---|
| **Unitario** | Blanca | Tolerancia a Fallos | JUnit 5 + Mockito | WT-01, WT-02 (backend); WT-03 (frontend — jest/vitest) |
| **Integración** | Gris | Tolerancia a Fallos + Capacidad de Recuperación | JUnit 5 + H2 + Spring Boot Test | WT-01, WT-04 (atomicidad transaccional) |
| **Sistema** | Negra | Capacidad de Recuperación | JMeter + Spring Boot levantado con MySQL (perfil `test-system`) | WT-05 (pool), WT-06 (frontend degradación) |
| **Aceptación** | Negra | Tolerancia a Fallos + Capacidad de Recuperación | Revisión manual contra ERS §NFR-FIAB-* | Todos WT-01..WT-06 |

### 4.1 Pruebas unitarias (caja blanca)

Se construyen en `src/test/java/com/biblioteca/service/` y `src/test/java/com/biblioteca/controller/`. Cada test establece el contexto mínimo con Mockito (`@ExtendWith(MockitoExtension.class)`), inyecta dependencias mockeadas y verifica el comportamiento de la unidad bajo prueba. El uso de caja blanca está justificado porque los hallazgos WT-01 y WT-04 identifican líneas de código específicas.

### 4.2 Pruebas de integración (caja gris)

Se construyen con `@SpringBootTest(webEnvironment = RANDOM_PORT)` y perfil `test` (H2 in-memory). Prueban la interacción entre capas (Controller → Service → Repository) incluyendo la transaccionalidad JPA. El fallo a mitad de transacción se implementa con un `@MockBean` parcial que lanza excepción después del primer `save()`.

### 4.3 Pruebas de sistema (caja negra)

JMeter ejecuta planes de prueba (`sqa/fase2/jmeter/`) contra el sistema completo desplegado. MySQL real (perfil `system`). Los resultados se expresan como tasa de error (%) y tiempo de respuesta p95 (ms).

### 4.4 Pruebas de aceptación (caja negra)

El equipo SQA revisa los resultados de los niveles anteriores contra los requisitos no funcionales de la ERS. Un hallazgo que falla consistentemente en `defecto-conocido` se documenta como incidencia abierta.

---

## 5. Política de Suites y Etiquetas

El proyecto de pruebas JUnit 5 organiza todos los casos en dos suites exclusivas identificadas por anotación `@Tag`:

### Suite `regresion`

- **Propósito:** Pruebas que DEBEN pasar en el código actual tal como está. Constituyen el gate de CI.
- **Contenido:** Verificaciones de comportamiento observable y correcto según la ERS (flujos felices, validaciones básicas, comportamientos que el SUT sí implementa correctamente).
- **CI:** `mvn verify -Dgroups=regresion` — falla el pipeline si algún caso no pasa.
- **Nota:** Incluye los tests de `crearPrestamo` con datos correctos que sí persisten, login correcto, etc.

### Suite `defecto-conocido`

- **Propósito:** Pruebas que DOCUMENTAN un comportamiento defectuoso conocido. Se ejecutan en CI pero NO bloquean el pipeline.
- **Contenido:** Todo caso de prueba que exponga un hallazgo WT-01..WT-06. Cada método de test lleva `@Tag("defecto-conocido")` y en su Javadoc la referencia a la incidencia: `@see INC-WT-01`, `@see INC-WT-04`, etc.
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

## 6. Modelo de Autoría

La restricción del enunciado establece que el código de producción está congelado y que el equipo SQA no escribe código de prueba directamente en el repositorio del Equipo 58-1. El modelo opera así:

| Rol | Responsabilidad | Artefacto producido |
|---|---|---|
| **Equipo 11 — Analista de Pruebas** | Diseña y especifica los casos de prueba con nivel de detalle suficiente para que un desarrollador los implemente sin ambigüedad (datos de entrada, precondiciones, pasos, resultado esperado, etiqueta @Tag). | Especificaciones de casos de prueba (este doc + PP-FIAB-001) |
| **Equipo 11 — Líder de Métricas (Edwin Li)** | Define umbrales de métricas, revisa resultados JaCoCo y JMeter, calcula DDF/CRC/FTR de ejecución. | Informe de métricas (post-ejecución) |
| **Equipo 11 — Escriba (Samuel Artiles)** | Documenta hallazgos de ejecución como incidencias con referencia al hallazgo WT correspondiente. | Incidencias en Jira |
| **Br. Carlos Méndez (Equipo 58-1)** | Implementa los métodos `@Test` conforme a las especificaciones del Equipo 11. Configura `pom.xml` con H2, JaCoCo y Surefire. Crea la rama `simulacion-desarrollo` y ejecuta los sprints simulados. | Código de prueba en rama `simulacion-desarrollo` |

---

## 7. Herramientas

| Herramienta | Versión | Uso en esta estrategia | Consistencia con PACS-Fase2 |
|---|---|---|---|
| **JUnit 5** (Jupiter) | 5.10+ | Framework base para pruebas unitarias e integración. `@Tag`, `@ExtendWith`, `@SpringBootTest`. | Declarado como herramienta de fiabilidad en PACS §3.1 |
| **Mockito** | 5.x | Stubs y drivers: simula `PrestamoRepository`, `LibroRepository`, lanza excepciones controladas en el punto exacto. | Implícito en suites JUnit 5 del PACS |
| **H2 Database** | 2.x | Base de datos in-memory para pruebas de integración. Perfil `test` con `spring.datasource.url=jdbc:h2:mem:testdb`. | Implícito en TestContainers / integración del PACS |
| **JaCoCo** | 0.8.11+ | Cobertura de instrucciones y ramas. Objetivo: ≥ 60 % en clases bajo prueba. Reporte HTML en `target/site/jacoco/`. | Declarado explícitamente en PACS §3.1 y §7.1 |
| **Maven Surefire** | 3.x | Ejecución de tests por tag, generación de reportes XML. Integrado con JaCoCo. | Maven declarado en PACS §7.1 |
| **JMeter** | 5.6+ | Planes de carga para pruebas de sistema (Sprint 5). 50 usuarios concurrentes, rampa 30 s, duración 3 min. | Nota: PACS §5 lista JMeter como descartado para Completitud Funcional y propone k6; para Fiabilidad/carga, JMeter es la herramienta del enunciado y se usa aquí explícitamente. |
| **GitHub Actions** | — | Workflow `ci-fiabilidad.yml` en rama `simulacion-desarrollo`. Ejecuta `mvn verify` por sprint. | Declarado como orquestador en PACS §3.2 |
| **Spring Boot Test** | 3.4.5 | `@SpringBootTest`, `MockMvc`, `@MockBean` para pruebas de integración de capa web. | Stack del SUT (PACS §2.1) |

---

## 8. Métricas de Calidad

Las métricas se calculan al cierre de cada sprint de integración simulada y al final de la Fase 2. Las tres métricas heredadas del walkthrough (IEEE 1061) se complementan con cuatro métricas de ejecución.

| ID | Nombre | Atributo ISO 25010 | Fórmula | Rangos de calificación | Fuente de datos |
|---|---|---|---|---|---|
| M-01 | Densidad de Defectos de Fiabilidad (DDF) | Reliability | Hallazgos confirmados por ejecución / Módulos bajo prueba | Bueno: 0 – 1.0 · Regular: 1.1 – 2.0 · Malo: > 2.0 | Surefire (defecto-conocido) |
| M-02 | Cobertura de Revisión de Código (CRC) | Exhaustividad | (Módulos con al menos 1 caso de prueba / Total de módulos en alcance) × 100 | Bueno: 100 % · Regular: 80–99 % · Malo: < 80 % | JaCoCo class coverage |
| M-03 | First Time Right (FTR) de Fiabilidad | Reliability | (Módulos sin casos `defecto-conocido` fallando / Total módulos) × 100 | Bueno: > 70 % · Regular: 50–70 % · Malo: < 50 % | Surefire XML |
| M-04 | Cobertura de instrucciones JaCoCo | Capacidad para ser probado | (Instrucciones cubiertas / Total instrucciones) × 100 | Bueno: ≥ 60 % · Regular: 40–59 % · Malo: < 40 % | JaCoCo report |
| M-05 | Porcentaje de casos de tolerancia superados | Tolerancia a Fallos | (Casos `regresion` de tolerancia que pasan / Total casos `regresion` de tolerancia) × 100 | Bueno: ≥ 80 % · Regular: 60–79 % · Malo: < 60 % | Surefire (regresion) |
| M-06 | Tiempo de recuperación (MTTR de transacción) | Capacidad de Recuperación | Tiempo promedio desde fallo forzado hasta estado consistente verificado (ms) | Bueno: < 500 ms · Regular: 500–2000 ms · Malo: > 2000 ms | Logs JUnit (cronometrado en test) |
| M-07 | Tasa de error bajo carga | Capacidad de Recuperación | (Solicitudes con error / Total de solicitudes JMeter) × 100 | Bueno: < 2 % · Regular: 2–5 % · Malo: > 5 % | JMeter aggregate report |

> **Coherencia con walkthrough:** Los valores base de M-01, M-02 y M-03 obtenidos en el walkthrough (1.0 def/módulo, 100 %, 0 %) son el punto de partida. Las métricas de ejecución (M-04..M-07) complementan la evaluación con datos dinámicos que el walkthrough no podía proveer.

---

*Documento generado el 9 de junio de 2026 por el Equipo SQA 11 como parte de la Fase 2 del proceso de aseguramiento bajo ISO/IEC/IEEE 29119-2 y la característica Reliability de ISO/IEC 25010:2023.*
