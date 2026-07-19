# Especificación de Casos de Prueba Dinámicos (Refactorizado)
**Norma:** ISO/IEC/IEEE 29119-3
**Alcance Estricto:** Fiabilidad (Tolerancia a Fallos y Capacidad de Recuperación)
**Alineado con:** Hallazgos Estáticos WT-01 al WT-06

---

### ID del Caso: CP-001
**Nivel y Enfoque:** Sistema / Caja Negra
**Combinación:** Tolerancia a fallos + Análisis de Valores Límite
**Objetivo:** DESTRUCTIVO. Violar el límite de la regla de negocio creando el tercer préstamo activo en simultáneo para corromper el validador.
**Precondiciones:** El usuario existe en BD y tiene exactamente 2 préstamos activos (límite máximo).
**Datos de Entrada:** `correoUsuario` = "tester@ucab.edu", `isbn` = 9781234567897, `fechaPrestamoStr` = "2026-07-12"
**Pasos de Ejecución:**
1. Autenticarse con rol USUARIO y obtener token.
2. Interceptar la petición de red.
3. Enviar un POST a `/api/prestar` con el payload de entrada.
4. Repetir la misma petición POST en menos de 50ms usando hilos concurrentes para provocar una condición de carrera.
**Resultados Esperados:** El sistema DEBE rechazar la petición con HTTP 400 y el mensaje "El usuario ya tiene 2 préstamos activos." SIN crear el tercer préstamo ni generar un error 500.
**Criterios de Aceptación:** El registro en BD muestra `countByUsuarioIdAndFechaDevolucionIsNull` = 2.
**Trazabilidad:** `PrestamoService.crearPrestamo()` (líneas 36-37) y `Controller.registrarPrestamo()`.

---

### ID del Caso: CP-002 (Refactorizado - E2E Frontend)
**Nivel y Enfoque:** Sistema (E2E) / Caja Negra
**Combinación:** Tolerancia a Fallos + Pruebas de Escenario (Scenario Testing)
**Objetivo:** DESTRUCTIVO. Evidenciar la falta de manejo de promesas asíncronas en el frontend forzando un error 500 desde el backend.
**Precondiciones:** Aplicación Vue levantada y conectada al backend. Autenticado como usuario.
**Datos de Entrada:** Texto de reseña válido.
**Pasos de Ejecución:**
1. Navegar a `PantallaLibro.vue` en el frontend.
2. Interceptar la petición de red (ej. Burp Suite) y forzar que el backend responda con HTTP 500 a la petición POST de crear reseña.
3. Hacer clic en "Enviar Reseña".
4. Observar el comportamiento de la Interfaz de Usuario y la consola.
**Resultados Esperados:** La prueba confirmará el hallazgo estático: la UI colapsa o se queda en estado de carga infinita sin mostrar ninguna alerta ni retroalimentación. En la consola se registrará un `unhandled promise rejection` debido a la falta de un bloque `try/catch`.
**Criterios de Aceptación:** El tester documenta el cuelgue visual y la excepción no manejada en consola.
**Trazabilidad:** Frontend (`PantallaLibro.vue`, función `agregarResena`). Hallazgos WT-03 y WT-06.

---

### ID del Caso: CP-003 (Refactorizado - E2E Integrado)
**Nivel y Enfoque:** Sistema (E2E) / Caja Negra
**Combinación:** Tolerancia a fallos + Partición de Equivalencia
**Objetivo:** DESTRUCTIVO. Inyectar una fecha malformada desde el frontend para provocar un error de parsing y evaluar el colapso en cadena de ambas capas.
**Precondiciones:** API y Frontend desplegados. Autenticado en el sistema.
**Datos de Entrada:** `fechaPrestamoStr` = "9999-99-99" (Formato de fecha inválido).
**Pasos de Ejecución:**
1. Interceptar el request desde el navegador antes de enviarlo al backend al crear un préstamo.
2. Modificar el JSON inyectando el valor anómalo.
3. Inspeccionar la respuesta HTTP y el estado del frontend tras liberar la petición.
**Resultados Esperados:** Alineado con la realidad del código: el backend fallará en `LocalDate.parse()` arrojando un HTTP 500 con el *stacktrace* expuesto (por falta de try/catch, WT-01). El frontend, al recibir el 500, no lo atrapará de forma centralizada (sin `app.config.errorHandler`), rompiendo el flujo visual y generando una promesa rechazada no manejada.
**Criterios de Aceptación:** Se evidencia y registra el HTTP 500 con *stacktrace* (DateTimeParseException) y el colapso silencioso del cliente.
**Trazabilidad:** `PrestamoService.crearPrestamo()` (línea 47) y frontend Vue. Hallazgos WT-01 y WT-02.

---

### ID del Caso: CP-004
**Nivel y Enfoque:** Integración / Caja Gris
**Combinación:** Tolerancia a fallos + Adivinación de Errores (Error Guessing)
**Objetivo:** DESTRUCTIVO. Explotar la lógica de devolución para incrementar falsamente el inventario de libros (Ataque de Doble Gasto).
**Precondiciones:** Préstamo ID 5 activo. Libro ID 10 con `cantidad` = 5.
**Datos de Entrada:** `prestamoId` = 5.
**Pasos de Ejecución:**
1. Abrir dos terminales paralelas (o usar JMeter).
2. Ejecutar simultáneamente `POST /api/prestamos/devolver?prestamoId=5` en ambas terminales.
**Resultados Esperados:** La primera petición retorna "Préstamo devuelto con éxito." (cantidad a 6). La segunda DEBE retornar "El préstamo ya fue devuelto." y NO aumentar la cantidad a 7.
**Criterios de Aceptación:** Al consultar la BD, el libro ID 10 tiene `cantidad` = 6, y la BD no tiene registros inconsistentes.
**Trazabilidad:** `PrestamoService.devolverPrestamo()` (líneas 72-74 y 81-83).

---

### ID del Caso: CP-005
**Nivel y Enfoque:** Integración / Caja Blanca
**Combinación:** Capacidad de Recuperación + Análisis de Flujo de Datos
**Objetivo:** DESTRUCTIVO. Romper el flujo de la transacción a la mitad para validar si el sistema deja datos corruptos o huérfanos.
**Precondiciones:** Contexto de Spring cargado. Mock inyectado en `libroRepository` forzado a arrojar `DataAccessException`.
**Datos de Entrada:** Petición válida para crear préstamo.
**Pasos de Ejecución:**
1. Llamar a `PrestamoService.crearPrestamo`.
2. La línea 58 (`prestamoRepository.save`) guarda el préstamo en BD.
3. La línea 61 (`libroRepository.save`) arroja la excepción programada.
**Resultados Esperados:** La prueba VA A FALLAR exponiendo el defecto arquitectónico. Como el método no tiene la anotación `@Transactional`, el sistema no tiene capacidad de recuperación (rollback). El préstamo queda guardado, pero el libro no se descuenta.
**Criterios de Aceptación:** El tester reporta el hallazgo crítico (INC) exigiendo control transaccional inmediato.
**Trazabilidad:** `PrestamoService.crearPrestamo()` (líneas 58 a 61). Hallazgo WT-04.

---

### ID del Caso: CP-006
**Nivel y Enfoque:** Integración / Caja Negra
**Combinación:** Tolerancia a fallos + Transición de Estados (State Transition Testing)
**Objetivo:** DESTRUCTIVO. Forzar una transición de estado ilegal en la máquina de estados del préstamo.
**Precondiciones:** Préstamo ID 8 en estado "activo" (aún no devuelto). Autenticado como "BIBLIOTECARIO".
**Datos de Entrada:** `id` = 8.
**Pasos de Ejecución:**
1. Validar en BD que el préstamo está activo (`fechaDevolucion` es NULL).
2. Enviar petición PUT directa a `/api/prestamos/8/renovar`.
**Resultados Esperados:** El sistema debe impedir la transición del estado "activo" al estado "renovado" saltándose el estado intermedio "finalizado". Debe retornar HTTP 400.
**Criterios de Aceptación:** El préstamo mantiene su `fechaLimite` original y su estado no se altera.
**Trazabilidad:** `PrestamoService.renovarPrestamo()` (líneas 132-134).

---

### ID del Caso: CP-007 (Refactorizado - E2E Frontend)
**Nivel y Enfoque:** Sistema (E2E) / Caja Negra
**Combinación:** Capacidad de Recuperación + Pruebas de Transición de Estados
**Objetivo:** DESTRUCTIVO. Simular una caída temporal de la red del cliente para evaluar la existencia de degradación elegante (*fallback*).
**Precondiciones:** Frontend Vue levantado. Pantalla `VerificarPago.vue` cargada.
**Datos de Entrada:** Clic de usuario.
**Pasos de Ejecución:**
1. Desconectar la conexión a internet de la máquina cliente (modo offline).
2. Intentar hacer clic en el botón para ejecutar la función asíncrona `verificarAmonestacion`.
3. Reconectar la red tras 10 segundos y observar si el sistema se recupera.
**Resultados Esperados:** Al no existir un interceptor global ni bloques `.catch()` (WT-03), el frontend no mostrará ninguna pantalla de "Servicio no disponible" ni un toast de error. La promesa no manejada romperá el estado interno del componente, el cual no podrá recuperarse visualmente al volver la conexión sin un refresco manual de la página.
**Criterios de Aceptación:** El tester demuestra la falta de pantallas de error explícitas ante indisponibilidad de red.
**Trazabilidad:** Frontend (`VerificarPago.vue`, `verificarAmonestacion`). Hallazgos WT-03 y WT-06.

---

### ID del Caso: CP-008
**Nivel y Enfoque:** Aceptación / Caja Negra
**Combinación:** Capacidad de Recuperación + Pruebas Aleatorias (Fuzzing)
**Objetivo:** DESTRUCTIVO. Ahogar el parseo JSON del backend inyectando payloads gigantescos.
**Precondiciones:** API ejecutándose en entorno Beta.
**Datos de Entrada:** Petición con cuerpo JSON mutado: `{ "texto": "A" * 10000000 }` (10MB).
**Pasos de Ejecución:**
1. Generar payload de 10MB.
2. Autenticarse como usuario normal.
3. Enviar PUT a `/api/resenas/1` con el payload destructivo.
**Resultados Esperados:** El servidor web debe interceptar la petición por exceso de tamaño (`Payload Too Large`) recuperándose sin colapsar el servicio para los demás usuarios.
**Criterios de Aceptación:** Retorna HTTP 413, los logs advierten el rechazo, y el consumo de RAM del servidor se normaliza.
**Trazabilidad:** `Controller.editarResena()` (línea 258).

---

### ID del Caso: CP-009 (Refactorizado - E2E Frontend)
**Nivel y Enfoque:** Sistema (E2E) / Caja Negra
**Combinación:** Tolerancia a Fallos + Adivinación de Errores (Error Guessing)
**Objetivo:** DESTRUCTIVO. Apagar el backend abruptamente para evidenciar la falta de interceptores globales ante respuestas 5xx.
**Precondiciones:** Frontend y Backend ejecutándose.
**Datos de Entrada:** Navegación hacia `SolicitudVerificacionPago.vue`.
**Pasos de Ejecución:**
1. Apagar el servicio de Backend (`kill -9` al proceso de Spring Boot).
2. Navegar en el frontend a la ruta que monta `SolicitudVerificacionPago.vue`, forzando el disparo de `cargarAmonestaciones`.
3. Revisar el comportamiento de la interfaz ante el fallo de conexión.
**Resultados Esperados:** La función `cargarAmonestaciones` (que solo usa `try/finally` sin `catch`) fallará. Al no haber interceptor global en axios ni manejadores de error, la UI quedará en blanco o en carga perpetua, fallando catastróficamente de forma silenciosa para el usuario.
**Criterios de Aceptación:** Se evidencia la falta de mensajes genéricos amigables o redirecciones ante la caída total del API.
**Trazabilidad:** Frontend (`SolicitudVerificacionPago.vue`, `main.js`). Hallazgos WT-02, WT-03 y WT-06.

---

### ID del Caso: CP-010
**Nivel y Enfoque:** Sistema / Caja Gris
**Combinación:** Tolerancia a fallos + Pruebas de Escenario
**Objetivo:** DESTRUCTIVO. Eliminar un perfil de usuario con dependencias duras activas para corromper la integridad referencial.
**Precondiciones:** Usuario "MOROSO" con 1 préstamo sin devolver.
**Datos de Entrada:** Petición DELETE autenticada por "MOROSO".
**Pasos de Ejecución:**
1. Iniciar sesión como "MOROSO".
2. Enviar DELETE a `/api/usuarios`.
3. Intentar consultar el préstamo o el libro asociado en la BD.
**Resultados Esperados:** La prueba va a exponer OTRA FALLA ARQUITECTÓNICA. En el `Controller` (línea 186) se llama a `usuarioService.eliminarUsuario` de forma directa sin comprobaciones en cascada previas, lo que arrojará un error 500 por violación de *foreign key constraint* (o dejará huérfanos).
**Criterios de Aceptación:** La prueba expone el defecto. El tester reporta el hallazgo por falta de validación antes del DELETE.
**Trazabilidad:** `Controller.eliminarPerfil()` (línea 182-188).

---

### ID del Caso: CP-011
**Nivel y Enfoque:** Integración / Caja Gris
**Combinación:** Tolerancia a fallos + Adivinación de Errores
**Objetivo:** Someter al sistema a un fallo de dependencia (lentitud extrema en la BD) para verificar si el hilo de ejecución de Tomcat se bloquea.
**Precondiciones:** Base de datos detrás de un proxy (Toxiproxy) configurado para inyectar latencia de 30s.
**Datos de Entrada:** Petición POST válida a `/api/prestamos/devolver`.
**Pasos de Ejecución:**
1. Configurar la dependencia para demorar 30 segundos.
2. Ejecutar la petición HTTP.
**Resultados Esperados:** El sistema DEBE aplicar un timeout a nivel de consulta (ej. configurando query.timeout en JPA) para no dejar el hilo bloqueado 30 segundos.
**Criterios de Aceptación:** La API aborta y responde en < 500ms. El hilo del servidor no queda secuestrado.
*(Nota: Si esto falla, levantará un nuevo defecto no cubierto por el Walkthrough).*
**Trazabilidad:** Configuración JPA / Timeout.

---

### ID del Caso: CP-012 (Refactorizado - Alineado con WT-02 y WT-05)
**Nivel y Enfoque:** Integración / Caja Blanca
**Combinación:** Capacidad de Recuperación + Pruebas de Recuperación (Disaster Recovery Testing)
**Objetivo:** DESTRUCTIVO. Asesinar el motor de BD en plena transacción concurrente para validar el impacto real de la falta de configuración del pool HikariCP.
**Precondiciones:** Aplicación web levantada y conectada.
**Datos de Entrada:** Peticiones concurrentes GET a `/api/libros`.
**Pasos de Ejecución:**
1. Lanzar script de JMeter con 20 hilos concurrentes.
2. Detener forzosamente el motor de base de datos (`sudo systemctl stop postgres`).
3. Evaluar los responses recibidos por los clientes.
4. Reiniciar la base de datos tras 15 segundos e inyectar nueva carga.
**Resultados Esperados:** Tal como dicta la auditoría: durante la caída el sistema fallará exponiendo un HTTP 500 con el *stacktrace* (por falta de `@ControllerAdvice`, WT-02). Al reiniciar la BD, las nuevas peticiones seguirán fallando con "Communications link failure" ya que HikariCP no tiene configurado `max-lifetime` ni `keepalive-time` (WT-05) y no recuperará las conexiones muertas.
**Criterios de Aceptación:** Se documentan los *stacktraces* filtrados al cliente y el estado irrecuperable del pool de conexiones.
**Trazabilidad:** `application.properties`, `@ControllerAdvice`. Hallazgos WT-02 y WT-05.

---

### ID del Caso: CP-013 (Refactorizado - E2E Frontend)
**Nivel y Enfoque:** Sistema (E2E) / Caja Negra
**Combinación:** Capacidad de Recuperación + Pruebas Aleatorias (Monkey Testing UI)
**Objetivo:** DESTRUCTIVO. Bombardear una acción asíncrona de mutación en la UI bajo alta latencia para evidenciar la inconsistencia por ausencia de atomicidad transaccional combinada con falta de manejo de promesas.
**Precondiciones:** Frontend corriendo. Throttling de red activado (Fast 3G).
**Datos de Entrada:** Clics rápidos consecutivos ("doble envío") en eliminar reseña.
**Pasos de Ejecución:**
1. Activar throttling en devtools.
2. En `PantallaLibro.vue`, presionar repetidamente el botón eliminar reseña 5 veces antes de que resuelva el primer click.
**Resultados Esperados:** Por la falta de deshabilitación de estado (loading) y de manejo en el bloque `.catch()` (WT-03), se despacharán 5 peticiones. El backend fallará en la concurrencia (evidenciando la falla de transacciones WT-04) devolviendo errores que se transformarán en `unhandled promise rejections` en Vue. La UI quedará con datos corrompidos (fantasma) irrecuperables hasta hacer F5.
**Criterios de Aceptación:** Se evidencia que la interfaz permite concurrencia destructiva cliente-servidor sin recuperación automática.
**Trazabilidad:** Frontend (`PantallaLibro.vue`), Backend `eliminarResena`. Hallazgos WT-03 y WT-04.

---

### ID del Caso: CP-014
**Nivel y Enfoque:** Sistema / Caja Blanca
**Combinación:** Tolerancia a fallos + Análisis de Valores Límite
**Objetivo:** DESTRUCTIVO. Forzar un cálculo injusto en penalizaciones aprovechando la debilidad en el manejo de zonas horarias y milisegundos de medianoche.
**Precondiciones:** Préstamo activo con `fechaLimite` = "2026-07-15" (sin hora). Servidor en UTC, tester en UTC-4.
**Datos de Entrada:** Petición POST a `/api/prestamos/devolver` en el límite de medianoche.
**Pasos de Ejecución:**
1. Modificar reloj del cliente a 23:59:59 del 15 de julio local.
2. Retener paquete HTTP y liberarlo para que llegue al servidor a las 00:00:01 del 16 de julio (UTC).
3. Validar si se genera amonestación.
**Resultados Esperados:** Exponer el defecto arquitectónico. Al usar `LocalDate.now()` en la línea 76, el software ignora el `ZoneId` y latencias. El servidor creerá equivocadamente que el usuario devolvió tarde, generándole una amonestación de 100$.
**Criterios de Aceptación:** Prueba demuestra fallo en límite horario, generando INC para migrar a `Instant.now()`.
**Trazabilidad:** `PrestamoService.devolverPrestamo()` (líneas 76 y 86-87).

---

### ID del Caso: CP-015
**Nivel y Enfoque:** Unitario / Caja Blanca
**Combinación:** Tolerancia a Fallos + Cobertura de Ramas (Branch Testing)
**Objetivo:** DESTRUCTIVO. Evidenciar la vulnerabilidad en el parseo de fechas forzando una rama de excepción no controlada.
**Precondiciones:** Entorno de pruebas configurado con JUnit 5. Clase `PrestamoService` instanciada.
**Datos de Entrada:** `fechaPrestamoStr` = "fecha-invalida" (string no parseable a LocalDate).
**Pasos de Ejecución:**
1. Crear una instancia de prueba para `PrestamoService`.
2. Usar `assertThrows(DateTimeParseException.class, () -> { ... })` en JUnit.
3. Invocar el método `crearPrestamo()` pasando la fecha inválida directamente como argumento.
**Resultados Esperados:** Como se documentó en el hallazgo WT-01, al carecer de un bloque `try/catch` específico, la ejecución de la instrucción `LocalDate.parse()` arrojará un `DateTimeParseException` que no será atrapado por el servicio, haciendo que la excepción burbujee y rompa la ejecución.
**Criterios de Aceptación:** El test de JUnit pasa exitosamente al asertar la excepción arrojada. El reporte de JaCoCo demuestra la cobertura de la rama de error expuesta.
**Trazabilidad:** `PrestamoService.crearPrestamo()` (línea 47). Hallazgo WT-01.

---

### ID del Caso: CP-016
**Nivel y Enfoque:** Unitario / Caja Blanca
**Combinación:** Capacidad de Recuperación + Pruebas de Flujo de Datos (Data Flow Testing)
**Objetivo:** DESTRUCTIVO. Provocar un fallo en el segundo guardado de una mutación múltiple para confirmar la ausencia de atomicidad (falta de rollback).
**Precondiciones:** Clase `PrestamoService` instanciada con mocks de Mockito (`@Mock` en `prestamoRepository` y `libroRepository`).
**Datos de Entrada:** Parámetros válidos para invocar `crearPrestamo()`.
**Pasos de Ejecución:**
1. Configurar Mockito: `when(libroRepository.save(any())).thenThrow(new DataAccessException("Fallo BD") {});`
2. Invocar `crearPrestamo()`.
3. Validar el flujo de datos: `verify(prestamoRepository, times(1)).save(any());`
**Resultados Esperados:** El flujo de datos demostrará que la entidad préstamo muta su estado y se envía al mock del repositorio (`prestamoRepository.save()` se ejecuta). Sin embargo, cuando `libroRepository.save()` lanza la excepción mockeada, esta interrumpe la función sin ejecutar un rollback sobre la primera acción. Queda expuesto que la BD quedaría inconsistente (hallazgo WT-04 por falta de `@Transactional`).
**Criterios de Aceptación:** La prueba de flujo verifica con Mockito que se llamó al primer `.save()` pero el segundo falló. JaCoCo reporta cobertura de instrucciones completada hasta la línea exacta de la excepción.
**Trazabilidad:** `PrestamoService.crearPrestamo()` (líneas 58 y 61). Hallazgo WT-04.

---

### ID del Caso: CP-017
**Nivel y Enfoque:** Unitario / Caja Blanca
**Combinación:** Tolerancia a Fallos + Cobertura de Instrucciones (Statement Coverage)
**Objetivo:** DESTRUCTIVO. Comprobar cómo un bloque `try/catch` genérico devora y oculta la causa real de un error en el acceso a datos.
**Precondiciones:** Clase `LibroService` instanciada. Dependencias inyectadas con Mockito.
**Datos de Entrada:** ID de un libro existente en el mock.
**Pasos de Ejecución:**
1. Configurar Mockito: `when(libroRepository.findById(any())).thenThrow(new RuntimeException("Timeout de Conexión en Base de Datos"));`
2. Ejecutar el método objetivo de `LibroService` que contiene el `catch (Exception e)`.
3. Capturar la respuesta retornada por el servicio.
**Resultados Esperados:** La cobertura de instrucciones mostrará que el hilo de ejecución ingresa al bloque `catch (Exception e)`. Sin embargo, tal como se documentó en la segunda parte del hallazgo WT-01, la excepción real (`RuntimeException` con mensaje de "Timeout") será enmascarada y sustituida por el manejo genérico del catch, perdiéndose el rastro original del error y obstaculizando el debugging.
**Criterios de Aceptación:** El test de JUnit aserta que el mensaje de error o excepción final reportada por el servicio NO contiene la causa raíz inyectada por Mockito. JaCoCo evidencia 100% de Statement Coverage en las líneas del `catch` genérico (líneas 48-52).
**Trazabilidad:** `LibroService` (líneas 48-52). Hallazgo WT-01 (segunda parte).
