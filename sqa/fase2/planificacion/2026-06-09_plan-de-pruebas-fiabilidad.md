# UNIVERSIDAD CATÓLICA ANDRÉS BELLO

```
Facultad de Ingeniería — Escuela de Ingeniería Informática
Aseguramiento de la Calidad del Software — Prof. Ernesto Suárez — NRC: 25790
```

# PLAN DE PRUEBAS — FIABILIDAD (ISO/IEC 25010:2023)

**Proyecto evaluado: Sistema de Gestión Bibliotecaria — Equipo 58-1**

| Campo | Valor |
|---|---|
| Identificador | PP-FIAB-001 |
| Versión | 1.0 |
| Fecha | 2026-06-09 |
| Equipo SQA | Equipo T 11 — Proyecto 16 (Turno Tarde) |
| Estándar de referencia | ISO/IEC/IEEE 29119-3:2021 |
| Estrategia de referencia | EST-FIAB-001 (2026-06-09_estrategia-de-pruebas-fiabilidad.md) |

| Rol | Nombre | Responsabilidad |
|---|---|---|
| Líder General | Alberto Rodriguez | Aprobación del plan, coordinación con Equipo 58-1, control de quality gates |
| Analista de Pruebas / Tester | Oscar Jaramillo | Diseño de casos de prueba, especificación de precondiciones y datos |
| Escriba | Samuel Artiles | Registro de incidencias, trazabilidad hallazgos → casos → resultados |
| Líder de Métricas | Edwin Li | Cálculo de M-01..M-07, reporte de resultados por sprint |
| DevOp | Daniel Cohen | Configuración de rama `simulacion-desarrollo`, workflows GitHub Actions, JaCoCo |
| Autor del SUT | Br. Carlos Méndez (Equipo 58-1) | Implementación del código de prueba según especificaciones del Equipo 11 |

---

## Tabla de Contenido

- [1. Contexto e Identificación](#1-contexto-e-identificación)
- [2. Ítems de Prueba](#2-ítems-de-prueba)
- [3. Características a Probar y No Probar](#3-características-a-probar-y-no-probar)
- [4. Criterios de Entrada, Salida y Suspensión](#4-criterios-de-entrada-salida-y-suspensión)
- [5. Ambiente de Pruebas](#5-ambiente-de-pruebas)
- [6. Roles y Responsabilidades](#6-roles-y-responsabilidades)
- [7. Cronograma — Sprints Simulados](#7-cronograma--sprints-simulados)
- [8. Estrategia de Integración Incremental](#8-estrategia-de-integración-incremental)
- [9. Matriz de Trazabilidad](#9-matriz-de-trazabilidad)
- [10. Gestión de Incidencias](#10-gestión-de-incidencias)
- [11. Riesgos y Contingencias](#11-riesgos-y-contingencias)

---

## 1. Contexto e Identificación

Este Plan de Pruebas cubre la evaluación dinámica de la característica **Reliability** (ISO/IEC 25010:2023) del Sistema de Gestión Bibliotecaria, específicamente las sub-características **Tolerancia a Fallos** y **Capacidad de Recuperación**. Se enmarca en la Fase 2 del proceso SQA del Equipo 11 y está subordinado a la Estrategia de Pruebas EST-FIAB-001.

La **base de prueba** son los seis hallazgos documentados en el Walkthrough Técnico del 2026-06-02 (WT-01..WT-06), que confirmaron de forma concluyente la ausencia estructural de mecanismos de resiliencia en el SUT. Los casos de prueba de este plan no buscan descubrir nuevos defectos: buscan **operacionalizar** los hallazgos conocidos en aserciones ejecutables.

**Restricción crítica del enunciado:** El código de producción (`src/main/java`, `biblioteca-frontend/src`) está congelado. El Equipo 11 **especifica** los casos; Br. Carlos Méndez (Equipo 58-1) **implementa** el código de test. Los defectos no se corrigen; se reportan como incidencias y se cubren por la suite `defecto-conocido`.

---

## 2. Ítems de Prueba

| ID Ítem | Módulo / Artefacto | Ubicación en el repositorio | Hallazgos asociados |
|---|---|---|---|
| IT-01 | `PrestamoService.java` | `src/main/java/com/biblioteca/service/PrestamoService.java` | WT-01, WT-04 |
| IT-02 | `LibroService.java` | `src/main/java/com/biblioteca/service/LibroService.java` | WT-01 |
| IT-03 | `UsuarioService.java` | `src/main/java/com/biblioteca/service/UsuarioService.java` | WT-04 (import incorrecto) |
| IT-04 | `Controller.java` | `src/main/java/com/biblioteca/controller/Controller.java` | WT-02, WT-04 |
| IT-05 | `PantallaLibro.vue` | `biblioteca-frontend/src/components/PantallaLibro.vue` | WT-03 |
| IT-06 | `SolicitudVerificacionPago.vue` | `biblioteca-frontend/src/components/SolicitudVerificacionPago.vue` | WT-03, WT-06 |
| IT-07 | `VerificarPago.vue` | `biblioteca-frontend/src/components/VerificarPago.vue` | WT-03, WT-06 |
| IT-08 | `application.properties` | `src/main/resources/application.properties` | WT-05 |
| IT-09 | `main.js` | `biblioteca-frontend/src/main.js` | WT-02, WT-06 |

---

## 3. Características a Probar y No Probar

### 3.1 Características en alcance (a probar)

| Sub-característica | Comportamientos específicos a verificar |
|---|---|
| **Tolerancia a Fallos** | Captura de `DateTimeParseException` en `PrestamoService:47`; comportamiento ante catch genérico en `LibroService:48-52`; respuesta HTTP ante excepción no controlada (ausencia de `@RestControllerAdvice`); manejo de rechazo en las 9 funciones async del frontend |
| **Capacidad de Recuperación** | Atomicidad de `crearPrestamo`, `devolverPrestamo`, `renovarPrestamo` ante fallo parcial; atomicidad de `Controller.eliminarResena`; presencia de configuración HikariCP en `application.properties`; comportamiento del frontend ante respuestas 5xx |

### 3.2 Características fuera del alcance (no se prueba en este plan)

| Característica | Razón de exclusión |
|---|---|
| **Seguridad** (Confidencialidad, Integridad, Responsabilidad) | Cubierta en Fase 1 mediante auditoría estática y checklist COD-FIAB-01..COD-FIAB-11 |
| **Mantenibilidad** | Cubierta por checklist COD-01..COD-06 y análisis SonarQube/JaCoCo de mantenibilidad |
| **Adecuación Funcional** | Tratada en suites E2E separadas (Playwright, RestAssured) |
| **Eficiencia de Desempeño** | Fuera del alcance del PAC actual; planificada para iteraciones futuras |

---

## 4. Criterios de Entrada, Salida y Suspensión

### 4.1 Criterios de entrada (por sprint)

- La rama `simulacion-desarrollo` existe y contiene el código del sprint anterior integrado y compilando.
- El workflow de CI (`ci-fiabilidad.yml`) ejecuta `mvn verify` sin errores de compilación.
- Los módulos del sprint actual han sido re-comprometidos en la rama según la estrategia incremental (§8).
- Los casos de prueba del sprint han sido implementados por Br. Carlos Méndez conforme a las especificaciones.

### 4.2 Criterios de salida

| Nivel | Criterio de salida |
|---|---|
| Sprint individual | 100 % de casos `regresion` del sprint pasando; todos los casos `defecto-conocido` ejecutados (pueden fallar); cobertura JaCoCo ≥ 40 % en los módulos del sprint |
| Plan completo (post Sprint 5) | M-02 CRC = 100 % (todos los módulos en alcance con al menos 1 caso); M-04 JaCoCo ≥ 60 % global; M-07 tasa de error JMeter < 5 %; todas las incidencias INC-WT-01..INC-WT-06 creadas en Jira con estado "Pendiente de Revisión" |

### 4.3 Criterios de suspensión

- Error de compilación del proyecto de pruebas que impida ejecutar cualquier suite.
- Fallo en la configuración del perfil `test` de H2 que impida levantar el contexto Spring en pruebas de integración.
- Indisponibilidad de la rama `simulacion-desarrollo` después de 48 h del inicio del sprint.

### 4.4 Criterios de reanudación

- El bloqueo técnico es resuelto por Br. Carlos Méndez o el DevOp del Equipo 11.
- El sprint bloqueado se reinicia desde cero (re-commit del código del sprint en la rama).

---

## 5. Ambiente de Pruebas

| Ambiente | Propósito | Configuración |
|---|---|---|
| **Unitario / Integración** | Sprints 0–4; pruebas JUnit 5 | H2 in-memory, perfil `test` (`application-test.properties`); sin MySQL real; JaCoCo agent activado vía Maven Surefire |
| **Sistema** | Sprint 5; pruebas de carga JMeter | MySQL 8.0 real (Docker Compose); backend desplegado localmente en puerto 8080; perfil `system` |
| **CI (GitHub Actions)** | Validación por push en `simulacion-desarrollo` | `ubuntu-latest`; Java 21 (temurin); `mvn verify -Dgroups=regresion,defecto-conocido` |

### 5.1 Configuración del perfil de test (H2)

```properties
# src/test/resources/application-test.properties
spring.datasource.url=jdbc:h2:mem:testdb;DB_CLOSE_DELAY=-1;MODE=MySQL
spring.datasource.driver-class-name=org.h2.Driver
spring.datasource.username=sa
spring.datasource.password=
spring.jpa.hibernate.ddl-auto=create-drop
spring.jpa.database-platform=org.hibernate.dialect.H2Dialect
```

### 5.2 Dependencias de prueba requeridas en pom.xml (Sprint 0)

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-test</artifactId>
  <scope>test</scope>
</dependency>
<dependency>
  <groupId>com.h2database</groupId>
  <artifactId>h2</artifactId>
  <scope>test</scope>
</dependency>
<!-- JaCoCo plugin en <build><plugins> -->
```

---

## 6. Roles y Responsabilidades

| Rol | Nombre | Actividades de prueba |
|---|---|---|
| Líder General | Alberto Rodriguez | Aprueba el plan y la estrategia; coordina entrega de especificaciones a Br. Méndez; valida que los criterios de salida se cumplan antes de cerrar cada sprint |
| Analista de Pruebas / Tester | Oscar Jaramillo | Redacta especificaciones de casos TC-FIAB-001..TC-FIAB-022; define datos de prueba; verifica que las implementaciones sean fieles a las especificaciones |
| Escriba | Samuel Artiles | Crea incidencias INC-WT-01..INC-WT-06 en Jira; actualiza trazabilidad; documenta resultados de ejecución por sprint |
| Líder de Métricas | Edwin Li | Calcula M-01..M-07 al cierre de cada sprint; actualiza el dashboard de métricas en Confluence |
| DevOp | Daniel Cohen | Crea y mantiene la rama `simulacion-desarrollo`; configura `ci-fiabilidad.yml`; verifica que JaCoCo genere reportes en cada ejecución |
| Autor del SUT (implementador) | Br. Carlos Méndez (Equipo 58-1) | Implementa el código de test (`@Test`) siguiendo exactamente las especificaciones del Equipo 11; configura `pom.xml` con H2, JaCoCo y Surefire; realiza los commits incrementales en `simulacion-desarrollo` según la estrategia de sprints |

---

## 7. Cronograma — Sprints Simulados

La integración se simula en la rama `simulacion-desarrollo` mediante re-commits incrementales del código fuente del SUT en orden de dependencia. Cada sprint incorpora módulos adicionales y las pruebas correspondientes.

| Sprint | Alcance del código re-comprometido | Pruebas incorporadas | Criterio de salida del sprint |
|---|---|---|---|
| **Sprint 0** | Skeleton del proyecto: `pom.xml` con dependencias H2/JaCoCo/Surefire; `application-test.properties`; `BibliotecaApplicationTests.java` (contextLoads); workflow `ci-fiabilidad.yml` | TC-FIAB-001 (contextLoads pasa); JaCoCo genera reporte vacío | CI verde; JaCoCo plugin activo |
| **Sprint 1** | `UsuarioService.java`, `UsuarioRepository.java`, entidad `Usuario`, `SecurityConfig.java` | TC-FIAB-002..TC-FIAB-004 (UsuarioService; import @Transactional incorrecto documentado como defecto-conocido) | Casos `regresion` de Usuario pasan; INC-WT-04b creada |
| **Sprint 2** | `LibroService.java`, `LibroRepository.java`, entidad `Libro` | TC-FIAB-005..TC-FIAB-007 (LibroService; catch genérico documentado; LONGBLOB load test) | Casos `regresion` de Libro pasan; INC-WT-01b creada |
| **Sprint 3** | `PrestamoService.java`, `PrestamoRepository.java`, entidad `Prestamo`; `Controller.java` (endpoints de préstamo) | TC-FIAB-008..TC-FIAB-015 (núcleo fiabilidad: DateTimeParseException, fallo transaccional, atomicidad crearPrestamo/devolver/renovar, @RestControllerAdvice ausente) | Casos `regresion` pasan; INC-WT-01, INC-WT-02, INC-WT-04 creadas; cobertura ≥ 50 % en PrestamoService |
| **Sprint 4** | `AmonestacionService`, reseñas y comentarios en `Controller.java`; componentes Vue críticos | TC-FIAB-016..TC-FIAB-019 (eliminarResena sin @Transactional; funciones async sin catch; HikariCP ausente) | Casos `regresion` pasan; INC-WT-03, INC-WT-04c, INC-WT-05 creadas |
| **Sprint 5** | Sistema completo integrado con MySQL real; plan JMeter ejecutado | TC-FIAB-020..TC-FIAB-022 (carga sostenida, fallback frontend, aceptación vs. ERS) | M-07 tasa de error < 5 %; INC-WT-06 creada; todas las incidencias en Jira |

---

## 8. Estrategia de Integración Incremental

La estrategia es **incremental ascendente** (bottom-up): se integran primero las capas de menor nivel (repositorios, entidades, servicios) y se asciende hasta el controlador y el frontend.

```
[Repositorios + Entidades]
        ↓  (Sprint 1–2: stubs de dependencias de nivel superior)
[Servicios (Usuario, Libro)]
        ↓  (Sprint 3: drivers de Controller, stubs de servicios no integrados aún)
[PrestamoService + Controller (endpoints préstamo)]
        ↓  (Sprint 4: integración completa backend)
[AmonestacionService + reseñas + Controller completo]
        ↓  (Sprint 5: sistema completo + frontend + MySQL)
[Sistema integrado — pruebas de sistema y aceptación]
```

### 8.1 Stubs y Drivers utilizados

| Sprint | Componente bajo prueba | Stub utilizado | Driver utilizado |
|---|---|---|---|
| Sprint 1 | `UsuarioService` | `@MockBean PrestamoRepository` (no existe aún) | JUnit 5 test class (llama directamente al service) |
| Sprint 2 | `LibroService` | `@MockBean PrestamoRepository`, `@MockBean UsuarioRepository` | JUnit 5 test class |
| Sprint 3 | `PrestamoService`, `Controller` (préstamo) | `@MockBean LibroRepository` (para simular fallo en segundo save) | `MockMvc` como driver de Controller; `@MockBean PrestamoService` en test de Controller |
| Sprint 4 | `Controller` (eliminarResena) | `@MockBean ResenaRepository`, `@MockBean ComentarioRepository` | `MockMvc` |
| Sprint 5 | Sistema completo | Ninguno (integración real) | JMeter como driver de carga |

### 8.2 Configuración del workflow CI

```yaml
# .github/workflows/ci-fiabilidad.yml (rama simulacion-desarrollo)
name: CI Fiabilidad — Simulacion Desarrollo
on:
  push:
    branches: [simulacion-desarrollo]
jobs:
  test-fiabilidad:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { java-version: '21', distribution: 'temurin' }
      - name: Run regresion suite (gate)
        run: mvn verify -Dgroups=regresion --no-transfer-progress
      - name: Run defecto-conocido suite (informativo)
        run: mvn verify -Dgroups=defecto-conocido -DfailIfNoTests=false --no-transfer-progress
        continue-on-error: true
      - name: Upload JaCoCo report
        uses: actions/upload-artifact@v4
        with:
          name: jacoco-report
          path: target/site/jacoco/
```

---

## 9. Matriz de Trazabilidad

La siguiente tabla mapea cada hallazgo del walkthrough a su sub-característica, nivel de prueba, técnica, casos de prueba planificados y métrica asociada.

| Hallazgo | Sub-car. (ISO 25010) | Nivel | Caja | ID Casos de Prueba | Descripción del caso | Suite | Métrica |
|---|---|---|---|---|---|---|---|
| WT-01 | Tolerancia a Fallos | Unitario | Blanca | TC-FIAB-008 | `PrestamoService`: fecha con formato inválido `dd-MM-yyyy` lanza `DateTimeParseException` sin captura → excepción se propaga | defecto-conocido | M-01, M-05 |
| WT-01 | Tolerancia a Fallos | Unitario | Blanca | TC-FIAB-009 | `PrestamoService`: fecha nula lanza `NullPointerException` sin captura | defecto-conocido | M-01 |
| WT-01 | Tolerancia a Fallos | Unitario | Blanca | TC-FIAB-010 | `LibroService`: excepción de JPA absorbida por catch genérico sin log → servicio retorna estado incorrecto | defecto-conocido | M-01 |
| WT-01 | Tolerancia a Fallos | Unitario | Blanca | TC-FIAB-005 | `LibroService`: operación exitosa con datos válidos retorna resultado correcto | regresion | M-05 |
| WT-02 | Tolerancia a Fallos | Integración | Gris | TC-FIAB-011 | `POST /api/prestamos` con fecha inválida devuelve HTTP 500 con stacktrace expuesto (ausencia de `@RestControllerAdvice`) | defecto-conocido | M-01, M-05 |
| WT-02 | Tolerancia a Fallos | Integración | Gris | TC-FIAB-012 | `POST /api/prestamos` con datos válidos devuelve HTTP 200 y cuerpo JSON correcto | regresion | M-05 |
| WT-03 | Tolerancia a Fallos | Sistema | Negra | TC-FIAB-016 | Simular fallo de red en `PantallaLibro.vue`: `agregarResena` genera `unhandled promise rejection` visible en consola | defecto-conocido | M-01 |
| WT-03 | Tolerancia a Fallos | Sistema | Negra | TC-FIAB-017 | Simular fallo de red en `SolicitudVerificacionPago.vue`: `pagarAmonestacion` con `try/finally` sin `catch` no muestra retroalimentación al usuario | defecto-conocido | M-01 |
| WT-04 | Capacidad de Recuperación | Integración | Gris | TC-FIAB-013 | `PrestamoService.crearPrestamo`: fallo forzado tras primer `save()` → sin `@Transactional`, entidad parcial persiste en H2 | defecto-conocido | M-01, M-06 |
| WT-04 | Capacidad de Recuperación | Integración | Gris | TC-FIAB-014 | `PrestamoService.devolverPrestamo`: fallo forzado tras actualización de Prestamo → Libro no restaura stock | defecto-conocido | M-01, M-06 |
| WT-04 | Capacidad de Recuperación | Integración | Gris | TC-FIAB-015 | `Controller.eliminarResena`: fallo tras primer borrado → comentarios huérfanos persisten | defecto-conocido | M-01 |
| WT-04 | Capacidad de Recuperación | Unitario | Blanca | TC-FIAB-002 | `UsuarioService`: anotación `@Transactional` presente pero es `jakarta.transaction.Transactional` (import incorrecto, no Spring) | defecto-conocido | M-01 |
| WT-04 | Capacidad de Recuperación | Integración | Gris | TC-FIAB-003 | `UsuarioService.eliminarUsuario` con `@Transactional` Spring: fallo forzado → rollback completo, usuario no eliminado | regresion | M-05, M-06 |
| WT-05 | Capacidad de Recuperación | Integración | Gris | TC-FIAB-018 | `application.properties` no contiene ninguna clave `spring.datasource.hikari.*` → `HikariConfig` usa defaults inseguros | defecto-conocido | M-01 |
| WT-05 | Capacidad de Recuperación | Sistema | Negra | TC-FIAB-020 | Carga sostenida 50 usuarios/3 min sobre `POST /api/prestamos`: tasa de error y p95 dentro de umbral | regresion | M-07 |
| WT-06 | Capacidad de Recuperación | Sistema | Negra | TC-FIAB-019 | Frontend recibe HTTP 503: componentes Vue muestran mensaje genérico sin pantalla de fallback específica | defecto-conocido | M-01 |
| WT-06 | Capacidad de Recuperación | Sistema | Negra | TC-FIAB-021 | `main.js` no configura `app.config.errorHandler`: errores Vue no capturados globalmente | defecto-conocido | M-01 |
| — (LONGBLOB/carga) | Capacidad de Recuperación | Sistema | Negra | TC-FIAB-022 | `GET /api/libros` carga todos los BLOBs de portadas: medir impacto en p99 bajo carga concurrente | regresion | M-07 |
| — (smoke) | Tolerancia a Fallos | Integración | Gris | TC-FIAB-001 | Context loads: Spring Boot levanta sin errores con perfil H2 | regresion | M-02 |
| — (Libro válido) | Tolerancia a Fallos | Unitario | Blanca | TC-FIAB-006 | `LibroService`: búsqueda por ISBN inexistente retorna `Optional.empty()` sin excepción | regresion | M-05 |
| — (Libro BLOB) | Capacidad de Recuperación | Unitario | Blanca | TC-FIAB-007 | `LibroService`: portada null se trata sin `NullPointerException` | regresion | M-05 |
| — (PrestamoService válido) | Tolerancia a Fallos | Unitario | Blanca | TC-FIAB-004 | `PrestamoService`: fecha ISO 8601 válida procesada correctamente sin excepción | regresion | M-05 |

**Total de casos planificados:** 22 (TC-FIAB-001 a TC-FIAB-022)
- Suite `regresion`: 9 casos (TC-FIAB-001, -003, -004, -005, -006, -007, -012, -020, -022)
- Suite `defecto-conocido`: 13 casos (TC-FIAB-002, -008..011, -013..019, -021)

---

## 10. Gestión de Incidencias

Cada caso de la suite `defecto-conocido` está vinculado a una incidencia en Jira. La incidencia documenta el hallazgo WT de origen, el comportamiento observado y el comportamiento esperado según la ERS.

| ID Incidencia | Hallazgo origen | Severidad | Título de la incidencia | Casos de prueba vinculados |
|---|---|---|---|---|
| INC-WT-01 | WT-01 | Alta | `PrestamoService`: `LocalDate.parse` sin try/catch propaga `DateTimeParseException` | TC-FIAB-008, TC-FIAB-009 |
| INC-WT-01b | WT-01 | Media | `LibroService`: catch genérico oculta causa de excepción JPA | TC-FIAB-010 |
| INC-WT-02 | WT-02 | Alta | Ausencia de `@RestControllerAdvice`: HTTP 500 expone stacktrace al cliente | TC-FIAB-011 |
| INC-WT-03 | WT-03 | Media | 9 funciones async del frontend sin manejo de rechazos (`catch` ausente) | TC-FIAB-016, TC-FIAB-017 |
| INC-WT-04 | WT-04 | Alta | `PrestamoService`: mutaciones múltiples sin `@Transactional` → estados inconsistentes | TC-FIAB-013, TC-FIAB-014 |
| INC-WT-04b | WT-04 | Alta | `UsuarioService`: import `jakarta.transaction.Transactional` en lugar de Spring | TC-FIAB-002 |
| INC-WT-04c | WT-04 | Alta | `Controller.eliminarResena`: borrados encadenados sin transacción | TC-FIAB-015 |
| INC-WT-05 | WT-05 | Baja | `application.properties`: sin configuración HikariCP → conexiones muertas no recuperadas | TC-FIAB-018 |
| INC-WT-06 | WT-06 | Media | Frontend sin interceptor axios ni pantalla de fallback para respuestas 5xx | TC-FIAB-019, TC-FIAB-021 |

### 10.1 Convención de Javadoc para casos `defecto-conocido`

```java
/**
 * [Una línea describiendo el comportamiento que se observa]
 *
 * <p>Comportamiento esperado (ERS §NFR-FIAB-*): [descripción breve]</p>
 * <p>Comportamiento actual (defecto): [descripción breve]</p>
 *
 * @see INC-WT-XX  (ID de incidencia en Jira)
 */
@Test
@Tag("defecto-conocido")
void nombreDelTest() { ... }
```

---

## 11. Riesgos y Contingencias

| ID | Riesgo | Probabilidad | Impacto | Contingencia |
|---|---|---|---|---|
| RIE-01 | **Precondición técnica del enunciado**: Br. Carlos Méndez (Equipo 58-1) no entrega el código de pruebas en el plazo del sprint | Media | Alto | El Equipo 11 escala al profesor Ernesto Suárez. El sprint se suspende (§4.3) hasta recibir la implementación. La falta de entrega se documenta como riesgo materializado en el informe de métricas. |
| RIE-02 | **Incompatibilidad H2/MySQL**: queries JPA con sintaxis MySQL-específica fallan en H2 in-memory | Media | Alto | Usar `MODE=MySQL` en la URL H2. Si persiste, aislar los tests afectados con `@Disabled("H2 incompatibility")` y moverlos al perfil de sistema (Sprint 5). |
| RIE-03 | **Cobertura JaCoCo insuficiente**: los módulos tienen lógica condicional compleja difícil de cubrir sin corregir el código | Media | Medio | Reducir meta a ≥ 40 % para Sprint 3; alcanzar ≥ 60 % al final del Sprint 5 con casos adicionales de integración. |
| RIE-04 | **Riesgo de cronograma**: los 6 sprints simulados deben completarse antes de la fecha de entrega de la Fase 2 | Alta | Alto | Sprint 0 y Sprint 1 se ejecutan en paralelo la primera semana. Sprint 5 (sistema/aceptación) puede ejecutarse con un subconjunto de casos si el tiempo no permite el plan JMeter completo. |
| RIE-05 | **LONGBLOB en `GET /api/libros`**: bajo carga de 50 usuarios, la carga de todos los BLOBs puede saturar la memoria del servidor de prueba | Baja | Medio | Limitar el plan JMeter a 20 usuarios para TC-FIAB-022 si el servidor de prueba tiene menos de 4 GB de RAM disponible. Documentar la limitación en el informe de sistema. |
| RIE-06 | **Ausencia de pruebas frontend ejecutables en CI**: los tests Vue (jest/vitest) requieren configuración adicional no presente en el proyecto | Alta | Medio | TC-FIAB-016, TC-FIAB-017 y TC-FIAB-021 se ejecutan como pruebas manuales con Playwright en Sprint 5. Se documentan los pasos de reproducción en la especificación de caso. |

---

*Documento generado el 9 de junio de 2026 por el Equipo SQA 11 como parte de la Fase 2 del proceso de aseguramiento bajo ISO/IEC/IEEE 29119-3 y la característica Reliability de ISO/IEC 25010:2023.*
