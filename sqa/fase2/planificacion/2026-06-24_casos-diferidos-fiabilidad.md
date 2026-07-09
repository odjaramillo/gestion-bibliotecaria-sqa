# ANEXO A — CASOS DE PRUEBA DIFERIDOS (FIABILIDAD)

```
Facultad de Ingeniería — Escuela de Ingeniería Informática
Aseguramiento de la Calidad del Software — Prof. Ernesto Suárez — NRC: 25790
```

## Información del anexo

| Campo | Valor |
|---|---|
| Identificador | ANX-FIAB-001 (Anexo A de TCS-FIAB-001) |
| Estado | Diferido — documentado |
| Fecha | 2026-07-09 |
| Origen | `casos-de-prueba-adicionales(revisar).md` (renombrado; consolidación issue #21) |

**Propósito.** Este anexo conserva la **especificación completa** de los 13 casos TC-FIAB **diferidos** en la consolidación del issue #21. Son casos válidos y bien especificados cuyas sub-características (Disponibilidad, Capacidad de Recuperación, Capacidad/concurrencia) quedan **fuera del alcance** declarado en TCS-FIAB-001 §2.1 (Madurez + Tolerancia a Fallos). No se implementan `@Test` en esta iteración, pero permanecen documentados con justificación y trazabilidad para que una iteración futura pueda replayearlos sin re-especificar. La disposición autoritativa está en **TCS-FIAB-001 §6.2**.

> **Casos absorbidos (no están en este anexo).** Los IDs fuente 013, 025, 026, 027, 033, 034, 035, 036 fueron re-especificados y anclados al código en **TCS-FIAB-001 §5** (mapeo en §6.2). Este anexo contiene únicamente los diferidos.

---

[TC-FIAB-023] - Ejecución de Préstamos bajo Carga Operativa Estándar
Disposición: DIFERIDO — dimensión de carga = Capacidad (fuera de alcance §2.1). La ruta funcional feliz ya está cubierta por TC-FIAB-020/019. Ref: TCS-FIAB-001 §6.2.
Hallazgo / Tipo: WT-01 | regresion
Subcaracterística (25010): Madurez
Técnica (29119): Partición de equivalencia
Descripción y Resultado Esperado: 1. Iniciar sesión con rol "BIBLIOTECARIO" (único rol con `hasAuthority("BIBLIOTECARIO")` permitido por `SecurityConfig` para `/api/prestar`). 2. Solicitar préstamo mediante el endpoint `/api/prestar` enviando `PrestamoRequest` (`correoUsuario`, `isbn`, `fechaPrestamo`). 3. Confirmar la operación en el frontend Vue. El sistema debe procesar la transacción sin generar excepciones ni degradación en el backend Spring Boot, demostrando estabilidad en un ciclo de ejecución repetitivo.
Datos de Prueba y Métricas (IEEE 1061): IDs de libros válidos [101, 102, 103]. Métrica: Tasa de Fallas (Rata de fallas), esperando 0 fallas observadas por hora de ejecución de la prueba.

[TC-FIAB-024] - Peticiones Concurrentes al Límite de la Configuración del Servidor
Disposición: DIFERIDO — concurrencia = Capacidad (fuera de alcance §2.1). Ref: TCS-FIAB-001 §6.2.
Hallazgo / Tipo: — (concurrencia) | regresion
Subcaracterística (25010): Madurez
Técnica (29119): Análisis de valores límite
Descripción y Resultado Esperado: 1. Configurar Spring Boot con un límite de hilos concurrentes estándar de Tomcat (ej. 200). 2. Enviar 199, 200 y 201 peticiones simultáneas de listado de libros a `/api/libros` desde el cliente. El sistema debe procesar hasta 200 y encolar o rechazar elegantemente la petición 201 sin que el servicio colapse.
Datos de Prueba y Métricas (IEEE 1061): 201 peticiones HTTP GET simultáneas a `/api/libros`. Métrica: Densidad de Defectos por módulo (evaluando fugas de memoria o interbloqueos en el controlador REST).

[TC-FIAB-028] - Respuesta del Sistema ante Pérdida de Conexión a Base de Datos
Disposición: DIFERIDO — Decisión issue #21 opción (b): sub-característica Disponibilidad fuera de alcance §2.1. Diferido con justificación registrada, sin implementar `@Test`. Ref: TCS-FIAB-001 §6.2.
Hallazgo / Tipo: WT-02 | defecto-conocido
Subcaracterística (25010): Disponibilidad
Técnica (29119): Partición de equivalencia
Descripción y Resultado Esperado: 1. Realizar peticiones a `/api/libros`. 2. Detener el servicio de MySQL intencionalmente (Partición inválida). 3. Repetir petición. Documentar como `defecto-conocido` (relacionado con WT-02 / INC-WT-02) que el proyecto NO contiene ninguna clase anotada con `@ControllerAdvice` ni `@RestControllerAdvice` (grep en `src/main/` retorna 0 coincidencias), por lo que Spring Boot responde con su comportamiento por defecto: HTTP 500 con el stacktrace completo de Java expuesto al cliente. Vue, al no tener interceptor axios para respuestas 5xx, queda en estado de carga o muestra la traza de error al usuario.
Datos de Prueba y Métricas (IEEE 1061): Petición GET normal vs Petición GET con daemon MySQL detenido (`sudo systemctl stop mysql`). Métrica: Índice de Disponibilidad Parcial (Manejo correcto de excepciones de infraestructura).

[TC-FIAB-029] - Comportamiento de Interfaz al Límite de la Sesión (JSESSIONID)
Disposición: DIFERIDO — sub-característica Disponibilidad fuera de alcance §2.1. Ref: TCS-FIAB-001 §6.2.
Hallazgo / Tipo: — (sesión) | regresion
Subcaracterística (25010): Disponibilidad
Técnica (29119): Análisis de valores límite
Descripción y Resultado Esperado: 1. Iniciar sesión y obtener la cookie `JSESSIONID`. 2. Configurar el timeout de sesión en Spring Boot a 15 minutos. 3. Realizar una petición a los 14m 59s, 15m 00s y 15m 01s. El sistema debe permitir la primera y rechazar las últimas con un código HTTP 401/403, forzando a Vue a redirigir automáticamente a la pantalla de login.
Datos de Prueba y Métricas (IEEE 1061): `server.servlet.session.timeout=15m`. Tiempos de inactividad: 899s, 900s, 901s. Métrica: Tasa de errores de interfaz (número de fallos de redirección / total de sesiones expiradas).

[TC-FIAB-030] - Saturación del Pool de Conexiones a MySQL
Disposición: DIFERIDO — sub-característica Disponibilidad/Capacidad fuera de alcance §2.1. Ref: TCS-FIAB-001 §6.2.
Hallazgo / Tipo: WT-05 | defecto-conocido
Subcaracterística (25010): Disponibilidad
Técnica (29119): Tablas de decisión
Descripción y Resultado Esperado: 1. Documentar como `defecto-conocido` (relacionado con WT-05 / INC-WT-05) que `application.properties` NO contiene ninguna clave `spring.datasource.hikari.*`, por lo que HikariCP opera con todos sus valores por defecto (pool-size=10, connection-timeout=30000ms, etc.). 2. Observar y registrar el comportamiento real con la configuración por defecto: (A) 5 usuarios consultando simultáneamente -> Responde dentro del pool, (B) 10 usuarios consultando -> Responde al límite, (C) 15 usuarios requiriendo transacciones -> La petición 11 en adelante espera en cola; superado `connection-timeout` (30s), se obtiene `SQLTransientConnectionException` propagada al cliente. Sin control de pool, no se garantiza graceful degradation. Como trabajo futuro, agregar `spring.datasource.hikari.maximum-pool-size=N` y un test profile dedicado.
Datos de Prueba y Métricas (IEEE 1061): 15 peticiones pesadas simultáneas contra el pool por defecto de HikariCP (sin overrides en `application.properties`). Métrica: Tiempo de inactividad del servicio por agotamiento de recursos bajo defaults inseguros.

[TC-FIAB-031] - Carga Masiva de Préstamos sin Paginación (defecto-conocido)
Disposición: DIFERIDO — sub-característica Disponibilidad/Capacidad fuera de alcance §2.1. Ref: TCS-FIAB-001 §6.2.
Hallazgo / Tipo: — (paginación ausente) | defecto-conocido
Subcaracterística (25010): Disponibilidad
Técnica (29119): Partición de equivalencia
Descripción y Resultado Esperado: 1. Documentar como `defecto-conocido` que el proyecto NO implementa paginación: `PrestamoService.obtenerPrestamos()` retorna `List<Prestamo>` desde `findAll()` y no existe ningún `Pageable`, `Page<>` ni `PageRequest` en `src/main/`. 2. Poblar la tabla `prestamos` con 10,000 registros y emitir `GET /api/prestamos`. 3. Observar (Partición inválida) que el sistema SÍ carga los 10,000 registros en un único payload JSON, exponiendo todo a memoria RAM y al ancho de banda del cliente. Comportamiento esperado por la ERS: paginación nativa Spring Data; comportamiento actual: volcado completo. La paginación queda registrada como trabajo futuro (sustituir `findAll()` por un método que acepte `Pageable` y devolver `Page<Prestamo>`).
Datos de Prueba y Métricas (IEEE 1061): Tabla `prestamos` con 10,000 rows. Request a `GET /api/prestamos` (sin parámetros de paginación — los parámetros `?page=` y `?size=` son ignorados). Métrica: Degradación del rendimiento de concurrencia y consumo de memoria heap bajo volumen alto de BD, comparando p50/p95/p99 contra el baseline de 100 registros.

[TC-FIAB-032] - Carga y Renderizado Asíncrono de Imágenes de Libros
Disposición: DIFERIDO — sub-característica Disponibilidad fuera de alcance §2.1. Ref: TCS-FIAB-001 §6.2.
Hallazgo / Tipo: — (LONGBLOB) | defecto-conocido
Subcaracterística (25010): Disponibilidad
Técnica (29119): Grafos de causa-efecto
Descripción y Resultado Esperado: 1. Acceder al catálogo de libros en Vue (`GET /api/libros`). 2. Algunos libros tienen el campo `imagen` (columna real, definida como `LONGBLOB` en `Libro.java:39-40` y `schema.sql:25`) con valor `null` o con bytes corruptos no decodificables (Causa). La cadena base64 NO es una columna: la expone el método transitorio `getImagenBase64()` (`Libro.java:88-94`) que ante `imagen` nulo retorna `null`. 3. El frontend Vue debe interceptar el fallo de renderizado del origen de la imagen y aplicar una imagen por defecto/fallback (Efecto), manteniendo la cuadrícula del catálogo totalmente disponible y sin desbordamientos CSS. Documentar el comportamiento observado (¿hay fallback? ¿se rompe la grilla?).
Datos de Prueba y Métricas (IEEE 1061): Libro con `imagen = null` (no `imagen_base64`), Libro con `imagen` = array de bytes no decodificables (no JPEG/PNG). Métrica: Tasa de Fallas visuales (Imágenes rotas renderizadas vs resueltas por fallback).

[TC-FIAB-037] - Caída del Backend durante Flujos Multi-paso
Disposición: DIFERIDO — recuperación de infraestructura (rollback nativo de MySQL) = Capacidad de Recuperación (fuera de alcance §2.1). Ref: TCS-FIAB-001 §6.2.
Hallazgo / Tipo: — (MySQL recovery) | regresion
Subcaracterística (25010): Tolerancia a Fallos
Técnica (29119): Grafos de causa-efecto
Descripción y Resultado Esperado: 1. El administrador emite un alta de múltiples libros o una amonestación compleja. 2. Inducir la finalización del proceso de Java (Kill pid) durante el guardado (Causa). Al reiniciar, MySQL debe haber bloqueado las transacciones incompletas y hecho rollback nativo (Efecto), previniendo inconsistencias en los datos.
Datos de Prueba y Métricas (IEEE 1061): `kill -9 <PID_JAVA>` durante transacción activa. Métrica: Cobertura de tolerancia a fallos a nivel de motor de base de datos.

[TC-FIAB-038] - Restauración ante Corrupción de Base de Datos
Disposición: DIFERIDO — sub-característica Capacidad de Recuperación fuera de alcance §2.1. Ref: TCS-FIAB-001 §6.2.
Hallazgo / Tipo: — (ddl-auto vs schema.sql) | regresion
Subcaracterística (25010): Capacidad de Recuperación
Técnica (29119): Partición de equivalencia
Descripción y Resultado Esperado: 1. Corromper la base de datos eliminando tablas críticas. Las tablas reales son `usuarios` (plural) según `schema.sql:6` y `@Table(name = "usuarios")` en `Usuario.java:6`; no `usuario`. 2. Documentar que `application.properties` tiene `spring.sql.init.mode`, `spring.sql.init.schema-locations` y `spring.sql.init.data-locations` comentados (líneas 18-20), por lo que `schema.sql` NO se ejecuta en el arranque del perfil por defecto. La estructura la crea JPA con `ddl-auto=update` (línea 13). 3. Como procedimiento válido de recuperación, usar un test profile (`application-test.properties`) con `ddl-auto=create-drop` que recrea el esquema desde el modelo JPA al iniciar y lo elimina al cerrar. La aplicación debe conectar y restablecer su estructura inicial funcionalmente.
Datos de Prueba y Métricas (IEEE 1061): Script `DROP TABLE usuarios;` (en el orden correcto de FKs: primero `amonestaciones`, `comentario_resena`, `resenas`, `prestamos`, `libros`, `usuarios`) seguido de reinicio con perfil de test `ddl-auto=create-drop`. Métrica: Tiempo Medio de Recuperación (MTTR), calculando el tiempo exacto en segundos desde el fallo hasta la disponibilidad de tablas.

[TC-FIAB-039] - Recuperación ante Exceso de Memoria Heap por Consultas Pesadas
Disposición: DIFERIDO — sub-característica Capacidad de Recuperación/Capacidad fuera de alcance §2.1. Ref: TCS-FIAB-001 §6.2.
Hallazgo / Tipo: — (heap OOM) | regresion
Subcaracterística (25010): Capacidad de Recuperación
Técnica (29119): Análisis de valores límite
Descripción y Resultado Esperado: 1. Arrancar la aplicación Java limitando deliberadamente la memoria (`-Xmx128m`). 2. Sobrecargar las peticiones pidiendo todos los libros con sus imágenes (columna `imagen` `LONGBLOB`, expuesta como `imagenBase64` por el getter transitorio de `Libro.java:88-94`) repetidamente hasta saturar el límite (128MB). 3. Evaluar si la aplicación se bloquea irreversiblemente o si el Garbage Collector de Java recupera la memoria tras cancelar las peticiones excedidas.
Datos de Prueba y Métricas (IEEE 1061): Peticiones en bucle continuo a `GET /api/libros` con payload de ~5MB. Argumento `-Xmx128m`. Métrica: Tasa de Recuperación Automática (Eventos de Garbage Collection exitosos vs caídas OOM).

[TC-FIAB-040] - Recuperación por Inicialización Fallida del Esquema
Disposición: DIFERIDO — sub-característica Capacidad de Recuperación fuera de alcance §2.1. Ref: TCS-FIAB-001 §6.2.
Hallazgo / Tipo: — (arranque) | regresion
Subcaracterística (25010): Capacidad de Recuperación
Técnica (29119): Tablas de decisión
Descripción y Resultado Esperado: 1. Modificar los parámetros `spring.datasource.url` con credenciales incorrectas o un host de MySQL inexistente. Decisión: Si la conexión a BD falla en el arranque, la aplicación Spring Boot debe detener su inicialización ordenadamente generando un log descriptivo de error de conexión, sin quedar colgada en un ciclo infinito de reintentos silenciosos.
Datos de Prueba y Métricas (IEEE 1061): Configuración `spring.datasource.password=wrong_pass`. Métrica: Tiempo de diagnóstico del fallo de arranque.

[TC-FIAB-041] - Recuperación ante 404 de Assets Estáticos del Frontend (hard refresh)
Disposición: DIFERIDO — sub-característica Capacidad de Recuperación fuera de alcance §2.1. Ref: TCS-FIAB-001 §6.2.
Hallazgo / Tipo: WT-03 | defecto-conocido
Subcaracterística (25010): Capacidad de Recuperación
Técnica (29119): Grafos de causa-efecto
Descripción y Resultado Esperado: 1. Sustituir el escenario original basado en `ChunkLoadError` (no aplicable: el proyecto Vue no tiene code-splitting, no usa `import()` dinámico, no tiene `vue-router` y `main.js` es un bootstrap de una línea sin chunks en el build de producción) por un escenario realista: desplegar una nueva versión del frontend y forzar al navegador a hard-refresh de rutas servidas como archivos estáticos. 2. Borrar o renombrar intencionadamente un asset (por ejemplo, un `app.<hash>.js` o un CSS) en el directorio `dist/` servido. Al recargar la página, el navegador solicitará un asset que el servidor ya no provee, obteniendo HTTP 404 (Causa). 3. Documentar como `defecto-conocido` (alineado con WT-03 / INC-WT-06) que el frontend no cuenta con un service worker, ni un interceptor axios, ni una vista de fallback específica para errores de carga de assets, por lo que el usuario queda con una pantalla blanca o con la traza del error en consola sin recuperación automática.
Datos de Prueba y Métricas (IEEE 1061): Eliminación/renombre de un asset estático crítico en `dist/` antes del hard refresh; observar respuesta HTTP 404 en Network y comportamiento de la SPA. Métrica: Tasa de recursos huérfanos del cliente recuperados exitosamente (esperado por la ERS: 100% con recuperación; observado: 0% por ausencia de service worker / fallback).

[TC-FIAB-042] - Persistencia de Estado Post-Caída de Servidor
Disposición: DIFERIDO — sub-característica Capacidad de Recuperación fuera de alcance §2.1. Ref: TCS-FIAB-001 §6.2.
Hallazgo / Tipo: — (sesión volátil) | regresion
Subcaracterística (25010): Capacidad de Recuperación
Técnica (29119): Pruebas de transición de estado
Descripción y Resultado Esperado: 1. Usuario autenticado posee una sesión activa (cookie `JSESSIONID` válida en su navegador). 2. Apagar y reiniciar el servidor Spring Boot abruptamente. 3. El usuario intenta navegar a una ruta protegida. El servidor reiniciado, al no tener la sesión en memoria (por defecto sin serialización externa), debe transicionar el estado del request a "No Autenticado" y forzar una redirección limpia sin generar errores 500.
Datos de Prueba y Métricas (IEEE 1061): Reinicio de servicio Spring Boot (`Ctrl+C` y `mvn spring-boot:run`). Cookie previamente válida en navegador. Métrica: Integridad de Reanudación de Estado (Manejo correcto de invalidación de estado volátil).
