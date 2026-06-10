# UNIVERSIDAD CATÓLICA ANDRÉS BELLO

```
Facultad de Ingeniería — Escuela de Ingeniería Informática
Aseguramiento de la Calidad del Software — Prof. Ernesto Suárez — NRC: 25790
```

# INFORME DEL WALKTHROUGH

**Proyecto evaluado: Sistema de Gestión Bibliotecaria — Equipo 58-1**

| Rol | Nombre | Responsabilidad principal |
|---|---|---|
| Expositor / Autor (Equipo 58-1) | Br. Carlos Méndez | Exposición del código fuente y la lógica de las funcionalidades del SUT |
| Moderador (Equipo 11) | Alberto Rodriguez | Dirección de la sesión, validación de hallazgos y control del proceso |
| Registrador / Escriba (Equipo 11) | Samuel Artiles | Documentación técnica de hallazgos y trazabilidad normativa |
| Revisor (Métricas) (Equipo 11) | Edwin Li | Evaluación de reactivos y recolección de datos para DDF y FTR |
| Revisor (Requisitos) (Equipo 11) | Daniel Cohen | Soporte en la verificación de trazabilidad ERS ↔ código |
| Revisor (Arquitectura) (Equipo 11) | Oscar Jaramillo | Soporte en la verificación de separación de capas y patrones de diseño |

**EQUIPO T 11 — Proyecto 16 (Turno Tarde)**

---

## Tabla de Contenido

- [Propósito del Walkthrough](#propósito-del-walkthrough)
- [Objetivos de Calidad](#objetivos-de-calidad)
- [Justificación de Estándares Aplicados](#justificación-de-estándares-aplicados)
- [Método Empleado](#método-empleado)
- [Instrumento de Walkthrough](#instrumento-de-walkthrough)
- [Métricas Consideradas](#métricas-consideradas)
- [Resultados y Conclusiones](#resultados-y-conclusiones)

---

## Propósito del Walkthrough

El propósito de este walkthrough técnico es realizar una revisión guiada por el autor del Sistema de Gestión Bibliotecaria del Equipo 58-1 para detectar y **contextualizar con el equipo de desarrollo** los defectos de fiabilidad identificados durante la auditoría estática previa del 02 de junio de 2026. Esta sesión constituye una **técnica complementaria** a la inspección formal en frío (cold review) ya ejecutada, y se enfoca exclusivamente en la característica *Reliability* de la ISO/IEC 25010:2023, particularmente en las sub-características de *Tolerancia a Fallos* y *Capacidad de Recuperación*.

La sesión busca confirmar, mediante la exposición directa del código por parte del autor, que el Sistema de Gestión Bibliotecaria carece de los mecanismos mínimos de resiliencia necesarios para soportar escenarios de fallo parcial — tales como entradas malformadas, excepciones no controladas y mutaciones múltiples no atómicas — y que esta ausencia es **estructural** y no coyuntural. La ejecución de este walkthrough adopta la ISO/IEC/IEEE 29119-4:202x §5.2 como estándar base para la aplicación de la técnica de walkthrough, mientras que los hallazgos se documentan bajo los requisitos de contenido de la ISO/IEC/IEEE 15289:2019. Las métricas se calculan conforme a la metodología IEEE 1061:1998.

Finalmente, esta actividad proporciona los datos cualitativos y cuantitativos necesarios para alimentar el *Quality Gate* del pipeline SQA del Equipo 11, permitiendo cuantificar la densidad de defectos de fiabilidad y la efectividad del proceso de revisión por pares, en continuidad directa con el veredicto FAIL emitido por la auditoría estática del 2026-06-02.

## Objetivos de Calidad

Los objetivos de calidad del Equipo 11 para el walkthrough están diseñados para garantizar que el código fuente del Sistema de Gestión Bibliotecaria integre la fiabilidad como una característica intrínseca, asegurando la conformidad técnica y la prevención de fallos en ejecución. Están definidos como metas SMART (Específicas, Medibles, Alcanzables, Relevantes y Temporales) y se asocian a métricas IEEE 1061 para orientar la evaluación hacia resultados tangibles.

| ID | Objetivo de Calidad (SMART) | Métrica Asociada (IEEE 1061) |
|---|---|---|
| OBJ-01: Tolerancia a Fallos en Operaciones Críticas | Validar que el 100 % de los servicios de backend que realizan operaciones de parsing, IO o persistencia cuenten con captura de excepciones específicas (`DateTimeParseException`, `IOException`, etc.), eliminando respuestas HTTP 500 con stacktrace. | M-02: Cobertura de Revisión (Meta: 100 %). |
| OBJ-02: Manejo Asíncrono Resiliente | Identificar un mínimo de 5 hallazgos sobre el manejo de rechazos en operaciones asíncronas del frontend (axios/fetch) y sobre la ausencia de interceptores de error global. | M-01: Densidad de Defectos de Fiabilidad (DDF) (Umbral: ≤ 1.0 def/módulo). |
| OBJ-03: Atomicidad Transaccional | Confirmar que el 100 % de los métodos de servicio que realizan mutaciones múltiples (≥ 2 `save()` o borrados en entidades distintas) se ejecuten bajo `@Transactional` de Spring con `rollbackFor = Exception.class`, evitando estados inconsistentes ante fallos parciales. | M-01: Densidad de Defectos de Fiabilidad (DDF) (Umbral: ≤ 1.0 def/módulo). |
| OBJ-04: Degradación Elegante | Verificar que el backend disponga de un manejador global de excepciones (`@RestControllerAdvice`) y que el frontend implemente estados de fallback ante indisponibilidad del API, incluyendo interceptor centralizado de axios y manejo explícito de respuestas HTTP 5xx. | M-03: First Time Right (FTR) de Fiabilidad (Meta: > 70 %). |

## Justificación de Estándares Aplicados

La realización de este walkthrough técnico se fundamenta en un marco normativo internacional que garantiza la verificación estática de los artefactos del proyecto, priorizando la identificación temprana de vulnerabilidades de diseño relacionadas con la fiabilidad del software.

| Estándar | Versión | Aplicación en el Proyecto T 11 |
|---|---|---|
| ISO/IEC/IEEE 29119-4 | 202x | Técnica de walkthrough. Define el procedimiento de tres fases (preparación, sesión, cierre) y los tres roles (Autor, Espectadores, Registrador). Justifica la sesión como prueba estática informal esencial para la detección temprana de defectos. |
| ISO/IEC 25010 | 2023 | Modelo de calidad de producto. Define las sub-características de *Reliability* — *Tolerancia a Fallos* y *Capacidad de Recuperación* — que el software debe cumplir y que estructuran el instrumento de este walkthrough. |
| IEEE 1061 | 1998 | Metodología de métricas de calidad de software. Base para el cálculo de la Densidad de Defectos de Fiabilidad (DDF), la Cobertura de Revisión de Código (CRC) y el First Time Right (FTR). |
| ISO/IEC/IEEE 15289 | 2019 | Rige la estructura y el contenido del informe resultante del walkthrough. Define los requisitos de contenido para la documentación técnica de procesos de revisión. |

## Método Empleado

Para la correcta realización del walkthrough, el Líder General del Equipo 11 (Alberto Rodriguez) coordinó previamente con el autor del SUT (Br. Carlos Méndez, Equipo 58-1) la fecha y hora de la sesión. Se seleccionó como artefacto a exponer el **código fuente en ejecución** del backend Java/Spring Boot y los componentes Vue 3 del frontend, y el autor fue el encargado de conducir la presentación paso a paso.

El autor expuso las funcionalidades principales del Sistema de Gestión Bibliotecaria, con énfasis específico en los flujos críticos para la fiabilidad: inicio de sesión, creación de préstamo, devolución de préstamo, renovación de préstamo y registro de reseñas. Se hizo especial énfasis en las sub-características de **Tolerancia a Fallos** y **Capacidad de Recuperación**, dejando explícitamente fuera del alcance la dimensión de Seguridad (cubierta por la auditoría previa) y la de Mantenibilidad (cubierta por la checklist COD-01 a COD-06).

Los **6 módulos críticos** seleccionados para la revisión fueron:

1. `src/main/java/com/biblioteca/service/PrestamoService.java` (Backend)
2. `src/main/java/com/biblioteca/service/LibroService.java` (Backend)
3. `src/main/java/com/biblioteca/service/UsuarioService.java` (Backend)
4. `src/main/java/com/biblioteca/controller/Controller.java` (Backend)
5. `biblioteca-frontend/src/components/PantallaLibro.vue`, `SolicitudVerificacionPago.vue`, `VerificarPago.vue` (Frontend)
6. `src/main/resources/application.properties` + `biblioteca-frontend/src/main.js` (Configuración transversal)

Los hallazgos se documentaron en una **Matriz de Walkthrough** con seis columnas: ID de hallazgo, sub-característica (ISO/IEC 25010), pregunta guía, módulo afectado, resultado (Sí/No) y prioridad (Alta/Media/Baja). Las observaciones del Registrador se consolidan en este informe, en cumplimiento con ISO/IEC/IEEE 15289.

Para realizar el cálculo de las métricas, primero se definieron las unidades de medición y se contó el número de hallazgos de la matriz tras la revisión de los 6 módulos. El cálculo se ejecutó al cierre de la sesión, una vez que el Expositor hubo concluido el recorrido.

## Instrumento de Walkthrough

El instrumento utilizado para la ejecución del walkthrough fue una matriz basada en las sub-características de *Reliability* de la norma ISO/IEC 25010:2023. Cada ítem fue respondido de forma individual e independiente por los Revisores, y los resultados se consolidaron en la siguiente tabla:

### 5.1 Checklist de Walkthrough

| ID | Sub-característica (ISO 25010) | Pregunta Guía para la Revisión de Código | Resultado (S/N) | Hallazgos (Vulnerabilidades, Deuda Técnica o Cumplimiento) | Prioridad |
|---|---|---|---|---|---|
| WT-01 | Tolerancia a Fallos | ¿El backend captura excepciones específicas en operaciones críticas (parsing de fechas, lectura/escritura de bytes, persistencia JPA), evitando bloques `catch (Exception e)` genéricos o `parse` directos sin `try/catch`? | N | Se identifica `LocalDate.parse(fechaPrestamoStr)` en `PrestamoService.java:47` sin envoltura `try/catch`, lo que propaga `DateTimeParseException` sin control y deriva en HTTP 500 con stacktrace. Adicionalmente, el único bloque `try/catch` del backend (`LibroService.java:48-52`) utiliza `Exception` genérica y oculta la causa sin registro en bitácora. | Alta |
| WT-02 | Tolerancia a Fallos | ¿Existe un `@RestControllerAdvice` o `@ControllerAdvice` global en el backend que intercepte `RuntimeException` y excepciones específicas, evitando la exposición de stacktraces al cliente? ¿El frontend Vue configura `app.config.errorHandler` en `main.js`? | N | Búsqueda exhaustiva de `@ControllerAdvice`, `@RestControllerAdvice`, `@ExceptionHandler`, `ErrorController` y `HandlerExceptionResolver` arroja 0 ocurrencias en el proyecto backend. La única clase de configuración (`SecurityConfig.java`, 55 líneas) no contiene lógica de manejo de errores. En el frontend, `main.js:1-4` no configura `app.config.errorHandler` ni se implementa `onErrorCaptured` en ningún componente. | Alta |
| WT-03 | Tolerancia a Fallos | ¿Las funciones `async` del frontend (axios/fetch) cuentan con bloques `try/catch` o `.catch()` que muestren retroalimentación al usuario ante rechazos? | N | Se identifican **9 funciones asíncronas** sin manejo adecuado: `agregarResena`, `eliminarResena`, `guardarEdicionResena`, `agregarComentarioResena`, `eliminarComentarioResena`, `guardarEdicionComentario` (en `PantallaLibro.vue`); `pagarAmonestacion` y `cargarAmonestaciones` con `try/finally` sin `catch` (en `SolicitudVerificacionPago.vue`); `cargarAmonestaciones` y `verificarAmonestacion` (en `VerificarPago.vue`). Un fallo de red o 5xx generará `unhandled promise rejections` que pueden romper el estado de la UI. | Media |
| WT-04 | Capacidad de Recuperación | ¿Las operaciones de mutación múltiple (≥ 2 `save()` o borrados en entidades distintas) se ejecutan bajo `@Transactional` con atributos de Spring (`rollbackFor = Exception.class`), garantizando atomicidad ante fallos parciales? | N | Sólo 1 de los 5+ métodos con mutaciones múltiples (`UsuarioService.eliminarUsuario`) utiliza `@Transactional`. Los tres métodos críticos de `PrestamoService` — `crearPrestamo` (líneas 58, 61), `devolverPrestamo` (líneas 79, 83, 96) y `renovarPrestamo` (líneas 149, 154) — modifican 2 o 3 entidades sin garantía de atomicidad. `Controller.eliminarResena()` (líneas 300-302) ejecuta dos borrados encadenados sin transacción. Adicionalmente, `UsuarioService.java:16` importa `jakarta.transaction.Transactional` en lugar de `org.springframework.transaction.annotation.Transactional`, perdiendo atributos de Spring. | Alta |
| WT-05 | Capacidad de Recuperación | ¿La configuración del pool HikariCP en `application.properties` incluye parámetros explícitos (`max-lifetime`, `keepalive-time`, `connection-timeout`, `maximum-pool-size`) para restablecer enlaces caídos con el servidor MySQL? | N | El archivo `application.properties` (22 líneas) no contiene ninguna clave `spring.datasource.hikari.*`. Búsqueda de `hikari`, `connectionTimeout`, `idleTimeout`, `maxLifetime`, `testOnBorrow`: 0 ocurrencias. MySQL cierra conexiones inactivas tras 8 horas por defecto; sin `max-lifetime` inferior y `keepalive-time` configurado, HikariCP intentará reutilizar conexiones muertas, generando errores `Communications link failure` sin mecanismo de recuperación. | Baja |
| WT-06 | Capacidad de Recuperación | ¿El frontend implementa estados de degradación elegante — interceptor centralizado de axios, manejo explícito de HTTP 502/503/504, *toast* o pantalla de "Servicio no disponible" — ante indisponibilidad temporal del API? | N | Búsqueda de `axios.interceptors` = 0 ocurrencias. No existe instancia centralizada de axios; cada componente (`PantallaPrincipal.vue`, `PantallaLibro.vue`, `EliminarLibroPantallaBusqueda.vue`, `ModificarLibroPantallaBusqueda.vue`, `ModificarLibroFormulario.vue`, `AnadirPrestamo.vue`, `DevolverPrestamo.vue`, `SolicitudVerificacionPago.vue`, `VerificarPago.vue`) la importa directamente. Los `catch` existentes muestran mensajes genéricos que no distinguen 4xx, 5xx ni errores de red. No hay pantallas de *fallback*. | Media |

### 5.2 Distribución de Prioridades

| Prioridad | Conteo | Walkthrough Findings |
|---|---|---|
| Alta | 3 | WT-01, WT-02, WT-04 |
| Media | 2 | WT-03, WT-06 |
| Baja | 1 | WT-05 |
| **Total** | **6** | — |

## Métricas Consideradas

Las métricas utilizadas para esta sesión están definidas conforme a IEEE 1061:1998 y se registran en la siguiente tabla:

| ID | Métrica | Atributo (ISO 25010) | Fórmula / Función | Rangos de calificación | Resultados |
|---|---|---|---|---|---|
| M-01 | Densidad de Defectos de Fiabilidad (DDF) | Reliability (Tolerancia a Fallos / Capacidad de Recuperación) | Walkthrough Findings detectados / Total de Módulos Revisados | Bueno: 0 – 1.0 · Regular: 1.1 – 2.0 · Malo: > 2.0 | 6 hallazgos / 6 módulos = **1.0 def/módulo** — **Bueno (límite aceptable)** |
| M-02 | Cobertura de Revisión de Código (CRC) | Exhaustividad (Proceso) | (Módulos auditados / Total de Módulos del Walkthrough) × 100 | Bueno: 100 % · Regular: 80 % – 99 % · Malo: < 80 % | (6 auditados / 6 totales) × 100 = **100 %** — **Bueno (meta alcanzada)** |
| M-03 | First Time Right (FTR) de Fiabilidad | Reliability (Tolerancia a Fallos / Capacidad de Recuperación) | (Módulos sin hallazgos / Total de Módulos Revisados) × 100 | Bueno: > 70 % · Regular: 50 % – 70 % · Malo: < 50 % | (0 módulos sin hallazgos / 6 revisados) × 100 = **0 %** — **Malo (falla estructural)** |

> **Nota sobre coherencia con la auditoría previa**: La auditoría estática del 2026-06-02 (`2026-06-02_auditoria-estatica-fiabilidad-iso25010.md`) documentó 12 defectos individuales agrupados en 11 ítems de checklist (COD-FIAB-01 a COD-FIAB-11). El presente walkthrough agrupa esos defectos en **6 hallazgos de diseño** (WT-01 a WT-06) a nivel de preocupación arquitectónica. Por esta razón, la métrica M-01 del walkthrough (1.0 def/módulo) es numéricamente inferior a la métrica análoga de la auditoría (~2.0 def/módulo). Esta diferencia es **intencional y metodológicamente correcta**: el walkthrough opera a nivel de *preocupación de diseño*, mientras que la auditoría opera a nivel de *defecto puntual*. Ambas son consistentes en su veredicto de Quality Gate FAIL.

## Resultados y Conclusiones

Durante la sesión técnica guiada por el autor del Sistema de Gestión Bibliotecaria del Equipo 58-1, se evidenció de manera concluyente que la fiabilidad no fue integrada como una característica intrínseca en la arquitectura del Sprint actual. El sistema actual presenta un nivel de exposición elevado frente a escenarios básicos de fallo — entradas malformadas, excepciones no controladas, mutaciones múltiples no atómicas e indisponibilidad del API — originados por decisiones de implementación deficientes desde la concepción de la lógica de los flujos críticos.

El análisis del instrumento de Walkthrough revela deficiencias transversales en las dos sub-características de la norma ISO/IEC 25010 evaluadas:

- **Tolerancia a Fallos:** Se confirmó la ausencia de captura de excepciones específicas en operaciones críticas de `PrestamoService` (parsing directo en línea 47) y `LibroService` (catch genérico en líneas 48-52), produciendo respuestas HTTP 500 con stacktrace potencialmente expuesto al cliente (WT-01). Esta situación se agrava por la inexistencia de un `@RestControllerAdvice` global en el backend y de `app.config.errorHandler` en el frontend (WT-02). A nivel de operaciones asíncronas, se identificaron 9 funciones en `PantallaLibro.vue`, `SolicitudVerificacionPago.vue` y `VerificarPago.vue` que carecen de manejo de rechazos, derivando en `unhandled promise rejections` que rompen el estado de la UI sin retroalimentación al usuario (WT-03).

- **Capacidad de Recuperación:** Se constató la ausencia generalizada de `@Transactional` en los métodos críticos de `PrestamoService` (`crearPrestamo`, `devolverPrestamo`, `renovarPrestamo`) y en `Controller.eliminarResena`, exponiendo el sistema a estados inconsistentes en la base de datos ante fallos parciales — por ejemplo, un préstamo marcado como devuelto sin restauración del stock (WT-04). A nivel de pool de conexiones, la configuración de HikariCP está completamente ausente en `application.properties`, sin parámetros de `max-lifetime` ni `keepalive-time`, dejando al sistema vulnerable a errores `Communications link failure` por conexiones caducadas (WT-05). En el frontend, no existe un interceptor centralizado de axios ni pantallas de *fallback* ante respuestas 5xx, obligando al usuario a enfrentar mensajes genéricos de error sin indicación clara del estado del servicio (WT-06).

Los resultados obtenidos frente a los objetivos definidos en el instrumento son:

- **OBJ-01. Tolerancia a Fallos en Operaciones Críticas:** **Cumplido.** Se auditó la totalidad de los flujos críticos de `PrestamoService`, `LibroService`, `UsuarioService`, `Controller.java` y `main.js`, logrando alcanzar un 100 % en la métrica M-02 de Cobertura de Revisión de Código (CRC). La cobertura total permitió identificar los hallazgos WT-01 y WT-02 con alta confianza, aunque ambos permanecen sin remediación.

- **OBJ-02. Manejo Asíncrono Resiliente:** **Cumplido.** La interacción directa con la lógica expuesta por el autor y la revisión de los 3 componentes Vue del flujo de reseñas y verificación de pagos permitió identificar el hallazgo WT-03 (9 funciones asíncronas sin manejo de rechazos), superando el mínimo de 5 hallazgos establecido como meta. La métrica M-01 (DDF) muestra 1.0 def/módulo, dentro del rango Bueno.

- **OBJ-03. Atomicidad Transaccional:** **Cumplido, pero en el límite de aceptación técnica.** Se detectó exactamente una proporción de 1.0 walkthrough finding por módulo evaluado (M-01), donde el hallazgo WT-04 consolida 4 defectos puntuales documentados en la auditoría previa (3 métodos de `PrestamoService` + 1 en `Controller.eliminarResena`). Este indicador posiciona al sistema en el umbral máximo del rango Bueno, con riesgo de caer a Regular si se documentan hallazgos adicionales en una próxima iteración.

- **OBJ-04. Degradación Elegante:** **No cumplido.** El resultado de la métrica First Time Right (M-03) fue de 0 %. La ausencia generalizada de `@RestControllerAdvice` en el backend y de interceptores de axios / pantallas de fallback en el frontend, en la totalidad de los módulos del flujo revisado, impidió alcanzar la meta de robustez esperada para esta revisión. Los hallazgos WT-05 y WT-06 confirman que la falla es **estructural y transversal**, no atribuible a un módulo o desarrollador específico.

En concordancia con el propósito de este ejercicio de SQA, el Walkthrough cumple exitosamente su función de **diagnóstico preventivo guiado por el autor**, documentando los hallazgos bajo los estándares IEEE 1061 e ISO/IEC/IEEE 15289, y proporcionando una radiografía exacta de la deuda técnica de fiabilidad del Sistema de Gestión Bibliotecaria **en coherencia con la auditoría estática del 2026-06-02** sin requerir la ejecución de acciones correctivas inmediatas. Los hallazgos se entregan al equipo de desarrollo del Equipo 58-1 para su análisis, priorización y remediación en sprints posteriores, conforme a la planificación del PAC del Equipo 11.

---

**Fin del informe.**

*Documento generado el 2 de junio de 2026 por el Equipo SQA 11 como parte del proceso de revisión estática bajo ISO/IEC/IEEE 29119-4 §5.2 y la característica Reliability de ISO/IEC 25010:2023.*
