[TC-FIAB-023] - Ejecución de Préstamos bajo Carga Operativa Estándar
Hallazgo / Tipo: WT-01 | regresion
Subcaracterística (25010): Madurez
Técnica (29119): Partición de equivalencia
Descripción y Resultado Esperado: 1. Iniciar sesión con rol "BIBLIOTECARIO" (único rol con `hasAuthority("BIBLIOTECARIO")` permitido por `SecurityConfig` para `/api/prestar`). 2. Solicitar préstamo mediante el endpoint `/api/prestar` enviando `PrestamoRequest` (`correoUsuario`, `isbn`, `fechaPrestamo`). 3. Confirmar la operación en el frontend Vue. El sistema debe procesar la transacción sin generar excepciones ni degradación en el backend Spring Boot, demostrando estabilidad en un ciclo de ejecución repetitivo.
Datos de Prueba y Métricas (IEEE 1061): IDs de libros válidos [101, 102, 103]. Métrica: Tasa de Fallas (Rata de fallas), esperando 0 fallas observadas por hora de ejecución de la prueba.

[TC-FIAB-024] - Peticiones Concurrentes al Límite de la Configuración del Servidor
Hallazgo / Tipo: — (concurrencia) | regresion
Subcaracterística (25010): Madurez
Técnica (29119): Análisis de valores límite
Descripción y Resultado Esperado: 1. Configurar Spring Boot con un límite de hilos concurrentes estándar de Tomcat (ej. 200). 2. Enviar 199, 200 y 201 peticiones simultáneas de listado de libros a `/api/libros` desde el cliente. El sistema debe procesar hasta 200 y encolar o rechazar elegantemente la petición 201 sin que el servicio colapse.
Datos de Prueba y Métricas (IEEE 1061): 201 peticiones HTTP GET simultáneas a `/api/libros`. Métrica: Densidad de Defectos por módulo (evaluando fugas de memoria o interbloqueos en el controlador REST).

[TC-FIAB-025] - Procesamiento de Pagos Simulados de Amonestaciones
Hallazgo / Tipo: — (validación ausente) | defecto-conocido
Subcaracterística (25010): Madurez
Técnica (29119): Tablas de decisión
Descripción y Resultado Esperado: 1. Generar pagos simulados con combinaciones: (A) `metodoPago` válido + `comprobantePago` no vacío, (B) `metodoPago` vacío + `comprobantePago` provisto, (C) Entradas con caracteres especiales en el comprobante, (D) `amonestacionId` inexistente. El endpoint `PUT /api/amonestaciones-usuario/pagar` (`Controller.java:366-387`) NO valida `metodoPago` ni `comprobantePago` antes de persistir: acepta cualquier valor (incluido `null`, vacío o con caracteres de intento de inyección SQL), y siempre marca `pagada=true` siempre que el `amonestacionId` pertenezca al usuario autenticado. Comportamiento esperado por la ERS: rechazar inserciones incompletas; comportamiento actual documentado como defecto: persistir datos basura sin validación.
Datos de Prueba y Métricas (IEEE 1061): `metodoPago`: "Transferencia", `comprobantePago`: "REF-12345". Métrica: Exactitud computacional (porcentaje de transacciones simuladas procesadas según las reglas de negocio establecidas).

[TC-FIAB-026] - Ciclo de Vida de Préstamo y Reducción de Inventario
Hallazgo / Tipo: WT-01 | regresion
Subcaracterística (25010): Madurez
Técnica (29119): Pruebas de transición de estado
Descripción y Resultado Esperado: 1. Crear un registro de `Prestamo` para un libro específico mediante `/api/prestar` con `isbn` válido de 13 dígitos. 2. Cambiar el estado del préstamo siguiendo el flujo real implementado en `PrestamoService`: `"activo"` (al crear, `setEstado("activo")`, línea 56) -> `"finalizado"` (al devolver, `setEstado("finalizado")`, línea 78). 3. Validar que la variable `cantidad` del `Libro` disminuya al prestar (`libro.setCantidad(libro.getCantidad() - 1)`) y aumente al devolver (`libro.setCantidad(libro.getCantidad() + 1)`). La creación de `Amonestacion` al devolver tarde se evalúa como un caso independiente (no es un estado del préstamo, es una entidad separada generada condicionalmente). El sistema debe mantener la sincronía entre el estado del préstamo y el inventario real del libro.
Datos de Prueba y Métricas (IEEE 1061): ISBN: 978XXXXXXXXXX (13 dígitos, Cantidad inicial: 5). Transiciones de estado `"activo" -> "finalizado"` del préstamo en MySQL. Métrica: Cobertura de Transición de Estados (100% de transiciones válidas que afectan el stock verificadas sin fallas de concurrencia).

[TC-FIAB-027] - Carga de Reseñas con Interrupciones de Red
Hallazgo / Tipo: WT-03 | defecto-conocido
Subcaracterística (25010): Madurez
Técnica (29119): Grafos de causa-efecto
Descripción y Resultado Esperado: 1. Redactar reseña en el cliente Vue. 2. Enviar solicitud asíncrona a `/api/resenas` y simular interrupción de red (Causa 1) o lentitud extrema en el servidor (Causa 2). Documentar como `defecto-conocido` (relacionado con WT-03 / INC-WT-03) que el frontend Vue no cuenta con interceptor axios global ni `app.config.errorHandler` configurado, por lo que el rechazo de la promesa se propaga sin manejo uniforme, sin prevenir guardado duplicado y sin mostrar un mensaje de timeout controlado al usuario.
Datos de Prueba y Métricas (IEEE 1061): String de reseña de 500 caracteres, Latencia inducida en Axios de 30000ms. Métrica: Tolerancia al tiempo de respuesta (porcentaje de peticiones manejadas correctamente bajo estrés asíncrono sin generar un defecto visual).

[TC-FIAB-028] - Respuesta del Sistema ante Pérdida de Conexión a Base de Datos
Hallazgo / Tipo: WT-02 | defecto-conocido
Subcaracterística (25010): Disponibilidad
Técnica (29119): Partición de equivalencia
Descripción y Resultado Esperado: 1. Realizar peticiones a `/api/libros`. 2. Detener el servicio de MySQL intencionalmente (Partición inválida). 3. Repetir petición. Documentar como `defecto-conocido` (relacionado con WT-02 / INC-WT-02) que el proyecto NO contiene ninguna clase anotada con `@ControllerAdvice` ni `@RestControllerAdvice` (grep en `src/main/` retorna 0 coincidencias), por lo que Spring Boot responde con su comportamiento por defecto: HTTP 500 con el stacktrace completo de Java expuesto al cliente. Vue, al no tener interceptor axios para respuestas 5xx, queda en estado de carga o muestra la traza de error al usuario.
Datos de Prueba y Métricas (IEEE 1061): Petición GET normal vs Petición GET con daemon MySQL detenido (`sudo systemctl stop mysql`). Métrica: Índice de Disponibilidad Parcial (Manejo correcto de excepciones de infraestructura).

[TC-FIAB-029] - Comportamiento de Interfaz al Límite de la Sesión (JSESSIONID)
Hallazgo / Tipo: — (sesión) | regresion
Subcaracterística (25010): Disponibilidad
Técnica (29119): Análisis de valores límite
Descripción y Resultado Esperado: 1. Iniciar sesión y obtener la cookie `JSESSIONID`. 2. Configurar el timeout de sesión en Spring Boot a 15 minutos. 3. Realizar una petición a los 14m 59s, 15m 00s y 15m 01s. El sistema debe permitir la primera y rechazar las últimas con un código HTTP 401/403, forzando a Vue a redirigir automáticamente a la pantalla de login.
Datos de Prueba y Métricas (IEEE 1061): `server.servlet.session.timeout=15m`. Tiempos de inactividad: 899s, 900s, 901s. Métrica: Tasa de errores de interfaz (número de fallos de redirección / total de sesiones expiradas).

[TC-FIAB-030] - Saturación del Pool de Conexiones a MySQL
Hallazgo / Tipo: WT-05 | defecto-conocido
Subcaracterística (25010): Disponibilidad
Técnica (29119): Tablas de decisión
Descripción y Resultado Esperado: 1. Documentar como `defecto-conocido` (relacionado con WT-05 / INC-WT-05) que `application.properties` NO contiene ninguna clave `spring.datasource.hikari.*`, por lo que HikariCP opera con todos sus valores por defecto (pool-size=10, connection-timeout=30000ms, etc.). 2. Observar y registrar el comportamiento real con la configuración por defecto: (A) 5 usuarios consultando simultáneamente -> Responde dentro del pool, (B) 10 usuarios consultando -> Responde al límite, (C) 15 usuarios requiriendo transacciones -> La petición 11 en adelante espera en cola; superado `connection-timeout` (30s), se obtiene `SQLTransientConnectionException` propagada al cliente. Sin control de pool, no se garantiza graceful degradation. Como trabajo futuro, agregar `spring.datasource.hikari.maximum-pool-size=N` y un test profile dedicado.
Datos de Prueba y Métricas (IEEE 1061): 15 peticiones pesadas simultáneas contra el pool por defecto de HikariCP (sin overrides en `application.properties`). Métrica: Tiempo de inactividad del servicio por agotamiento de recursos bajo defaults inseguros.

[TC-FIAB-031] - Carga Masiva de Préstamos sin Paginación (defecto-conocido)
Hallazgo / Tipo: — (paginación ausente) | defecto-conocido
Subcaracterística (25010): Disponibilidad
Técnica (29119): Partición de equivalencia
Descripción y Resultado Esperado: 1. Documentar como `defecto-conocido` que el proyecto NO implementa paginación: `PrestamoService.obtenerPrestamos()` retorna `List<Prestamo>` desde `findAll()` y no existe ningún `Pageable`, `Page<>` ni `PageRequest` en `src/main/`. 2. Poblar la tabla `prestamos` con 10,000 registros y emitir `GET /api/prestamos`. 3. Observar (Partición inválida) que el sistema SÍ carga los 10,000 registros en un único payload JSON, exponiendo todo a memoria RAM y al ancho de banda del cliente. Comportamiento esperado por la ERS: paginación nativa Spring Data; comportamiento actual: volcado completo. La paginación queda registrada como trabajo futuro (sustituir `findAll()` por un método que acepte `Pageable` y devolver `Page<Prestamo>`).
Datos de Prueba y Métricas (IEEE 1061): Tabla `prestamos` con 10,000 rows. Request a `GET /api/prestamos` (sin parámetros de paginación — los parámetros `?page=` y `?size=` son ignorados). Métrica: Degradación del rendimiento de concurrencia y consumo de memoria heap bajo volumen alto de BD, comparando p50/p95/p99 contra el baseline de 100 registros.

[TC-FIAB-032] - Carga y Renderizado Asíncrono de Imágenes de Libros
Hallazgo / Tipo: — (LONGBLOB) | defecto-conocido
Subcaracterística (25010): Disponibilidad
Técnica (29119): Grafos de causa-efecto
Descripción y Resultado Esperado: 1. Acceder al catálogo de libros en Vue (`GET /api/libros`). 2. Algunos libros tienen el campo `imagen` (columna real, definida como `LONGBLOB` en `Libro.java:39-40` y `schema.sql:25`) con valor `null` o con bytes corruptos no decodificables (Causa). La cadena base64 NO es una columna: la expone el método transitorio `getImagenBase64()` (`Libro.java:88-94`) que ante `imagen` nulo retorna `null`. 3. El frontend Vue debe interceptar el fallo de renderizado del origen de la imagen y aplicar una imagen por defecto/fallback (Efecto), manteniendo la cuadrícula del catálogo totalmente disponible y sin desbordamientos CSS. Documentar el comportamiento observado (¿hay fallback? ¿se rompe la grilla?).
Datos de Prueba y Métricas (IEEE 1061): Libro con `imagen = null` (no `imagen_base64`), Libro con `imagen` = array de bytes no decodificables (no JPEG/PNG). Métrica: Tasa de Fallas visuales (Imágenes rotas renderizadas vs resueltas por fallback).

[TC-FIAB-033] - Entradas Malformadas en Endpoints Rest
Hallazgo / Tipo: WT-02 | defecto-conocido
Subcaracterística (25010): Tolerancia a Fallos
Técnica (29119): Partición de equivalencia
Descripción y Resultado Esperado: 1. Enviar un payload JSON a `/api/prestar` con tipos de datos incorrectos. El DTO real es `PrestamoRequest` (`PrestamoRequest.java:4-6`) con campos `correoUsuario` (String), `isbn` (Long de 13 dígitos) y `fechaPrestamo` (String ISO 8601 parseado por `LocalDate.parse` en `PrestamoService:47`). 2. Spring Boot no captura la `HttpMessageNotReadableException` porque no existe `@ControllerAdvice`/`@RestControllerAdvice` (mismo defecto WT-02 / INC-WT-02 que TC-FIAB-028): responde con HTTP 500 y stacktrace. Adicionalmente, `LocalDate.parse("99/99/9999")` propaga `DateTimeParseException` no envuelta (defecto WT-01 / INC-WT-01). Comportamiento esperado: HTTP 400 con mensaje amigable; comportamiento actual: HTTP 500 con stacktrace.
Datos de Prueba y Métricas (IEEE 1061): `{"isbn": "no-es-isbn", "fechaPrestamo": "99/99/9999", "correoUsuario": "x"}` (alineado al DTO `PrestamoRequest` real; el campo `idLibro` no existe en el DTO). Métrica: Densidad de Defectos de manejo de excepciones (Fallos capturados vs. Stacktraces propagados al cliente).

[TC-FIAB-034] - Carga de Imágenes Excesivas en Libros (multipart/form-data)
Hallazgo / Tipo: — (multipart sin tuning) | defecto-conocido
Subcaracterística (25010): Tolerancia a Fallos
Técnica (29119): Análisis de valores límite
Descripción y Resultado Esperado: 1. En el módulo de administración (`POST /api/libros`), el endpoint real (`Controller.java:66-73`) recibe `multipart/form-data` con un `Libro` como `@RequestPart("libro")` y la imagen como `@RequestPart(value = "imagen", required = false) MultipartFile imagen`. NO se envían cadenas base64: el binario va en la parte `imagen`. 2. Probar con archivos de imagen de 0.9MB, 1.0MB y 1.1MB. Spring Boot 3.x aplica el default `spring.servlet.multipart.max-file-size=1MB` (no hay overrides en `application.properties`), por lo que la carga de 1.1MB debe rechazarse con HTTP 500 (sin `@RestControllerAdvice` mapea `MaxUploadSizeExceededException` a HTTP 413). Comportamiento esperado: HTTP 413 Payload Too Large; comportamiento actual: HTTP 500 con stacktrace. Documentar el límite de 1MB como default y proponer, como trabajo futuro, configurar `spring.servlet.multipart.max-file-size` y `max-request-size` en un test profile.
Datos de Prueba y Métricas (IEEE 1061): Archivos binarios (`MultipartFile`) de 900KB, 1.0MB y 1.1MB enviados como parte `imagen` en `multipart/form-data` (no como string base64). Métrica: Tasa de fallas de Validación (Errores de desbordamiento de buffer o heap por request bajo el default de 1MB de Spring Boot 3.x).

[TC-FIAB-035] - Ausencia de Frontera Transaccional en `crearPrestamo` (defecto-conocido)
Hallazgo / Tipo: WT-04 | defecto-conocido
Subcaracterística (25010): Tolerancia a Fallos
Técnica (29119): Tablas de decisión
Descripción y Resultado Esperado: 1. Documentar como `defecto-conocido` (relacionado con WT-04 / INC-WT-04, en línea con TC-FIAB-013) que `PrestamoService` NO tiene ninguna anotación `@Transactional` (única presencia en el proyecto: `UsuarioService:92` y, aun allí, con el import incorrecto `jakarta.transaction.Transactional` documentado como INC-WT-04b). 2. Ejecutar el flujo `crearPrestamo(correoUsuario, isbn, fechaPrestamoStr)` y forzar una `RuntimeException` entre el `prestamoRepository.save(prestamo)` (línea 58) y el `libroRepository.save(libro)` (línea 61). 3. Observación esperada por la ejecución real: NO hay rollback automático; el `Prestamo` queda persistido como registro huérfano (cantidad del `Libro` no decrementada, estado inconsistente). Comportamiento esperado por la ERS: atomicidad transaccional; comportamiento actual: registros huérfanos. El defecto se documenta como riesgo conocido hasta que se agregue `@Transactional` de Spring.
Datos de Prueba y Métricas (IEEE 1061): Simulación de `RuntimeException` inyectada en el servicio entre los dos `save()`. Métrica: Índice de Corrupción de Datos (Número de registros huérfanos / Total de transacciones abortadas). Esperado por la ERS: 0; observado: 1 por cada aborto.

[TC-FIAB-036] - Interrupciones Asíncronas en Promesas del Cliente
Hallazgo / Tipo: WT-03 | defecto-conocido
Subcaracterística (25010): Tolerancia a Fallos
Técnica (29119): Pruebas de transición de estado
Descripción y Resultado Esperado: 1. En Vue, iniciar petición Axios asíncrona hacia el servidor. 2. Cambiar estado de red del navegador a "Offline" durante la promesa (Pendiente -> Rechazado). Documentar como `defecto-conocido` (relacionado con WT-03 / INC-WT-03) que las funciones asíncronas del frontend no cuentan con un manejo uniforme de rechazos: 9 funciones `async` fueron identificadas sin `.catch`/try-catch y `main.js` no configura `app.config.errorHandler`. Por lo tanto, el rechazo de la promesa puede propagarse como `Uncaught (in promise)`, los spinners de los botones pueden no restaurarse y el usuario no recibe un mensaje de fallo local controlado.
Datos de Prueba y Métricas (IEEE 1061): Latencia de red 5000ms. Estado: Offline forzado en DevTools. Métrica: Tasa de Excepciones No Controladas (Uncaught Promise Rejections en la consola de JS).

[TC-FIAB-037] - Caída del Backend durante Flujos Multi-paso
Hallazgo / Tipo: — (MySQL recovery) | regresion
Subcaracterística (25010): Tolerancia a Fallos
Técnica (29119): Grafos de causa-efecto
Descripción y Resultado Esperado: 1. El administrador emite un alta de múltiples libros o una amonestación compleja. 2. Inducir la finalización del proceso de Java (Kill pid) durante el guardado (Causa). Al reiniciar, MySQL debe haber bloqueado las transacciones incompletas y hecho rollback nativo (Efecto), previniendo inconsistencias en los datos.
Datos de Prueba y Métricas (IEEE 1061): `kill -9 <PID_JAVA>` durante transacción activa. Métrica: Cobertura de tolerancia a fallos a nivel de motor de base de datos.

[TC-FIAB-038] - Restauración ante Corrupción de Base de Datos
Hallazgo / Tipo: — (ddl-auto vs schema.sql) | regresion
Subcaracterística (25010): Capacidad de Recuperación
Técnica (29119): Partición de equivalencia
Descripción y Resultado Esperado: 1. Corromper la base de datos eliminando tablas críticas. Las tablas reales son `usuarios` (plural) según `schema.sql:6` y `@Table(name = "usuarios")` en `Usuario.java:6`; no `usuario`. 2. Documentar que `application.properties` tiene `spring.sql.init.mode`, `spring.sql.init.schema-locations` y `spring.sql.init.data-locations` comentados (líneas 18-20), por lo que `schema.sql` NO se ejecuta en el arranque del perfil por defecto. La estructura la crea JPA con `ddl-auto=update` (línea 13). 3. Como procedimiento válido de recuperación, usar un test profile (`application-test.properties`) con `ddl-auto=create-drop` que recrea el esquema desde el modelo JPA al iniciar y lo elimina al cerrar. La aplicación debe conectar y restablecer su estructura inicial funcionalmente.
Datos de Prueba y Métricas (IEEE 1061): Script `DROP TABLE usuarios;` (en el orden correcto de FKs: primero `amonestaciones`, `comentario_resena`, `resenas`, `prestamos`, `libros`, `usuarios`) seguido de reinicio con perfil de test `ddl-auto=create-drop`. Métrica: Tiempo Medio de Recuperación (MTTR), calculando el tiempo exacto en segundos desde el fallo hasta la disponibilidad de tablas.

[TC-FIAB-039] - Recuperación ante Exceso de Memoria Heap por Consultas Pesadas
Hallazgo / Tipo: — (heap OOM) | regresion
Subcaracterística (25010): Capacidad de Recuperación
Técnica (29119): Análisis de valores límite
Descripción y Resultado Esperado: 1. Arrancar la aplicación Java limitando deliberadamente la memoria (`-Xmx128m`). 2. Sobrecargar las peticiones pidiendo todos los libros con sus imágenes (columna `imagen` `LONGBLOB`, expuesta como `imagenBase64` por el getter transitorio de `Libro.java:88-94`) repetidamente hasta saturar el límite (128MB). 3. Evaluar si la aplicación se bloquea irreversiblemente o si el Garbage Collector de Java recupera la memoria tras cancelar las peticiones excedidas.
Datos de Prueba y Métricas (IEEE 1061): Peticiones en bucle continuo a `GET /api/libros` con payload de ~5MB. Argumento `-Xmx128m`. Métrica: Tasa de Recuperación Automática (Eventos de Garbage Collection exitosos vs caídas OOM).

[TC-FIAB-040] - Recuperación por Inicialización Fallida del Esquema
Hallazgo / Tipo: — (arranque) | regresion
Subcaracterística (25010): Capacidad de Recuperación
Técnica (29119): Tablas de decisión
Descripción y Resultado Esperado: 1. Modificar los parámetros `spring.datasource.url` con credenciales incorrectas o un host de MySQL inexistente. Decisión: Si la conexión a BD falla en el arranque, la aplicación Spring Boot debe detener su inicialización ordenadamente generando un log descriptivo de error de conexión, sin quedar colgada en un ciclo infinito de reintentos silenciosos.
Datos de Prueba y Métricas (IEEE 1061): Configuración `spring.datasource.password=wrong_pass`. Métrica: Tiempo de diagnóstico del fallo de arranque.

[TC-FIAB-041] - Recuperación ante 404 de Assets Estáticos del Frontend (hard refresh)
Hallazgo / Tipo: WT-03 | defecto-conocido
Subcaracterística (25010): Capacidad de Recuperación
Técnica (29119): Grafos de causa-efecto
Descripción y Resultado Esperado: 1. Sustituir el escenario original basado en `ChunkLoadError` (no aplicable: el proyecto Vue no tiene code-splitting, no usa `import()` dinámico, no tiene `vue-router` y `main.js` es un bootstrap de una línea sin chunks en el build de producción) por un escenario realista: desplegar una nueva versión del frontend y forzar al navegador a hard-refresh de rutas servidas como archivos estáticos. 2. Borrar o renombrar intencionadamente un asset (por ejemplo, un `app.<hash>.js` o un CSS) en el directorio `dist/` servido. Al recargar la página, el navegador solicitará un asset que el servidor ya no provee, obteniendo HTTP 404 (Causa). 3. Documentar como `defecto-conocido` (alineado con WT-03 / INC-WT-06) que el frontend no cuenta con un service worker, ni un interceptor axios, ni una vista de fallback específica para errores de carga de assets, por lo que el usuario queda con una pantalla blanca o con la traza del error en consola sin recuperación automática.
Datos de Prueba y Métricas (IEEE 1061): Eliminación/renombre de un asset estático crítico en `dist/` antes del hard refresh; observar respuesta HTTP 404 en Network y comportamiento de la SPA. Métrica: Tasa de recursos huérfanos del cliente recuperados exitosamente (esperado por la ERS: 100% con recuperación; observado: 0% por ausencia de service worker / fallback).

[TC-FIAB-042] - Persistencia de Estado Post-Caída de Servidor
Hallazgo / Tipo: — (sesión volátil) | regresion
Subcaracterística (25010): Capacidad de Recuperación
Técnica (29119): Pruebas de transición de estado
Descripción y Resultado Esperado: 1. Usuario autenticado posee una sesión activa (cookie `JSESSIONID` válida en su navegador). 2. Apagar y reiniciar el servidor Spring Boot abruptamente. 3. El usuario intenta navegar a una ruta protegida. El servidor reiniciado, al no tener la sesión en memoria (por defecto sin serialización externa), debe transicionar el estado del request a "No Autenticado" y forzar una redirección limpia sin generar errores 500.
Datos de Prueba y Métricas (IEEE 1061): Reinicio de servicio Spring Boot (`Ctrl+C` y `mvn spring-boot:run`). Cookie previamente válida en navegador. Métrica: Integridad de Reanudación de Estado (Manejo correcto de invalidación de estado volátil).