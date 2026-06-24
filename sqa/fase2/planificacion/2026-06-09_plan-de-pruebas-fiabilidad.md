# UNIVERSIDAD CATÓLICA ANDRÉS BELLO

```
Facultad de Ingeniería — Escuela de Ingeniería Informática
Aseguramiento de la Calidad del Software — Prof. Ernesto Suárez — NRC: 25790
```

# PLAN DE PRUEBAS — FIABILIDAD (ISO/IEC 25010:2023)
## (Test Plan — ISO/IEC/IEEE 29119-3:2021, §7.2 / A.2.4)

**Proyecto evaluado: Sistema de Gestión Bibliotecaria — Equipo 58-1**

| Campo | Valor |
|---|---|
| Identificador | PP-FIAB-001 |
| Versión | 2.0 |
| Estado | Revisado |
| Fecha | 2026-06-24 |
| Organización emisora | Equipo SQA T 11 — Proyecto 16 (Turno Tarde) |
| Autoridad de aprobación | Líder General (Alberto Rodriguez) — revisa y aprueba antes de la entrega al Equipo 58-1 |
| Estándar de referencia | ISO/IEC/IEEE 29119-3:2021 (Test Plan, §7.2 / A.2.4) |
| Estrategia de referencia | EST-FIAB-001 |
| Especificación de casos | TCS-FIAB-001 |
| Sub-características | Madurez · Tolerancia a Fallos |

### Historial de cambios
| Versión | Fecha | Descripción del cambio | Razón | Autor |
|---|---|---|---|---|
| 1.0 | 2026-06-09 | Versión inicial (Tolerancia a Fallos · Capacidad de Recuperación; 22 casos; ecosistema Jira/Confluence). | Planificación inicial Fase 2 | Equipo 11 |
| 2.0 | 2026-06-24 | Segunda sub-característica realineada a **Madurez** (`objetivos.txt`); casos de recuperación/carga retirados; WT-04 reinterpretado como defecto de Madurez; incidencias a **GitHub Issues**, métricas a **GitHub Projects (Insights)**; estructura reorganizada a la plantilla de Test Plan de 29119-3. | Realineación + migración GitHub-native + conformidad 29119-3 | Equipo 11 |

---

## Tabla de Contenido

- [0. Introducción](#0-introducción)
- [1. Contexto de la Prueba](#1-contexto-de-la-prueba)
- [2. Comunicación de la Prueba](#2-comunicación-de-la-prueba)
- [3. Registro de Riesgos (Producto y Proyecto)](#3-registro-de-riesgos-producto-y-proyecto)
- [4. Estrategia de Prueba del Plan](#4-estrategia-de-prueba-del-plan)
- [5. Actividades, Estimaciones, Roles y Cronograma](#5-actividades-estimaciones-roles-y-cronograma)
- [6. Matriz de Trazabilidad](#6-matriz-de-trazabilidad)
- [7. Gestión de Incidencias](#7-gestión-de-incidencias)

> **Conformidad 29119-3 (A.2.4):** Context of testing (§1), Testing communication
> (§2), Risk register producto/proyecto (§3), Test strategy del plan —
> sub-procesos, entregables, técnicas, criterios de finalización, métricas,
> requisitos de datos y ambiente, retest/regresión, suspensión/reanudación,
> desviaciones — (§4), Testing activities and estimates + Staffing + Schedule (§5).

---

## 0. Introducción

### 0.1 Alcance
Cubre la evaluación dinámica de la característica **Reliability** (ISO/IEC 25010:2023), sub-características **Madurez** y **Tolerancia a Fallos**. Excluye Disponibilidad y Capacidad de Recuperación (no seleccionadas) y las correcciones de código (SUT congelado).

### 0.2 Referencias
- **Externas:** ISO/IEC/IEEE 29119-3:2021; ISO/IEC/IEEE 29119-2:2021; ISO/IEC 25010:2023; ISO/IEC 25023:2016.
- **Internas:** EST-FIAB-001 (Estrategia de proyecto); TCS-FIAB-001 (Especificación de casos); `referencias/objetivos.txt`; `2026-06-02_walkthrough-fiabilidad-sut-biblioteca.md` (base de prueba, WT-01..WT-04).

### 0.3 Convenciones de notación
`IT-##` ítem de prueba · `TC-FIAB-###` caso de prueba · `WT-##` / `INC-WT-##` hallazgo / incidencia (GitHub Issue) · `M-0#` métrica (ISO 25023) · `RIE-P##` riesgo de producto · `RIE-J##` riesgo de proyecto.

### 0.4 Glosario
- **Suite `regresion`:** casos que deben pasar en el código actual (gate de CI).
- **Suite `defecto-conocido`:** casos que documentan un defecto conocido; se ejecutan sin bloquear el pipeline.
- **SUT congelado:** el código de producción no se modifica; el Equipo 11 especifica y el Equipo 58-1 implementa los `@Test`.

---

## 1. Contexto de la Prueba

### 1.1 Proyecto / sub-proceso de prueba
Fase 2 del proceso SQA. Sub-procesos: unitario, integración, sistema y aceptación (detalle en §4 y en EST-FIAB-001).

### 1.2 Base de prueba
Hallazgos del Walkthrough Técnico del 2026-06-02 (WT-01..WT-04) y el marco de medición de `referencias/objetivos.txt`. Los casos **operacionalizan** los hallazgos en aserciones ejecutables (Tolerancia a Fallos) y **miden la corrección y ausencia de defectos** de la lógica crítica mediante cobertura de decisión (Madurez).

### 1.3 Ítems de prueba

| ID Ítem | Módulo / Artefacto | Ubicación en el repositorio | Hallazgos asociados |
|---|---|---|---|
| IT-01 | `PrestamoService.java` | `src/main/java/com/biblioteca/service/PrestamoService.java` | WT-01, WT-04 |
| IT-02 | `LibroService.java` | `src/main/java/com/biblioteca/service/LibroService.java` | WT-01 |
| IT-03 | `UsuarioService.java` | `src/main/java/com/biblioteca/service/UsuarioService.java` | WT-04 (import incorrecto) |
| IT-04 | `AmonestacionService.java` | `src/main/java/com/biblioteca/service/AmonestacionService.java` | Madurez (cobertura de decisión) |
| IT-05 | `Controller.java` | `src/main/java/com/biblioteca/controller/Controller.java` | WT-02, WT-04 |
| IT-06 | `PantallaLibro.vue` | `biblioteca-frontend/src/components/PantallaLibro.vue` | WT-03 |
| IT-07 | `SolicitudVerificacionPago.vue` | `biblioteca-frontend/src/components/SolicitudVerificacionPago.vue` | WT-03 |

### 1.4 Alcance de la prueba (a probar / no probar)

**En alcance:**

| Sub-característica | Comportamientos a verificar |
|---|---|
| **Madurez** | Cobertura de decisión de los métodos críticos (6 guardas de `crearPrestamo`, 3 ramas de `devolverPrestamo`, 4 de `renovarPrestamo`, 2 de `eliminarAmonestacion`); corrección en operación normal; defectos de consistencia de estado (mutaciones múltiples sin `@Transactional`, WT-04). |
| **Tolerancia a Fallos** | `DateTimeParseException` en `PrestamoService:47`; catch genérico en `LibroService`; respuesta HTTP ante excepción no controlada (sin `@RestControllerAdvice`); rechazo de promesas async en frontend. |

**Fuera de alcance:** Capacidad de Recuperación y Disponibilidad (sub-características no seleccionadas; los hallazgos de atomicidad se reinterpretan como defectos de Madurez); Seguridad (Fase 1); Mantenibilidad (checklist COD-01..06); Adecuación Funcional (E2E separadas); Eficiencia de Desempeño.

### 1.5 Supuestos y restricciones
- **Restricción del enunciado:** código de producción **congelado**. El Equipo 11 especifica; el Equipo 58-1 implementa los `@Test`. Los defectos se reportan (GitHub Issues), no se corrigen.
- **Supuesto:** el Equipo 58-1 re-entrega el código con pruebas unitarias sobre la característica (precondición técnica).

### 1.6 Stakeholders
| Stakeholder | Interés en la prueba |
|---|---|
| Profesor Ernesto Suárez (evaluador) | Verifica el proceso SQA y los resultados conforme a la rúbrica |
| Equipo 11 (SQA) | Diseña, ejecuta y reporta la prueba |
| Equipo 58-1 (autores del SUT) | Implementa los `@Test`; recibe los reportes de defectos |

---

## 2. Comunicación de la Prueba

| Canal | Propósito | Frecuencia |
|---|---|---|
| GitHub Issues | Reporte y seguimiento de defectos (plantilla "Defecto F2") | Continuo |
| GitHub Projects (tablero #4) | Estado de casos/incidencias (Backlog → En Ejecución → En Revisión → Cerrado) | Continuo |
| Pull Requests | Evidencia de revisión por pares (IEEE 730) sobre los artefactos de prueba | Por entrega |
| Reunión de cierre de sprint | Revisión de criterios de salida y métricas con el Líder General | Por sprint |
| Coordinación Equipo 11 ↔ Equipo 58-1 | Entrega de especificaciones e implementación de `@Test` | Por sprint |

---

## 3. Registro de Riesgos (Producto y Proyecto)

### 3.1 Riesgos de producto (en el SUT)
| ID | Riesgo en el producto | Probabilidad | Impacto | Mitigación / Caso asociado |
|---|---|---|---|---|
| RIE-P01 | `LocalDate.parse` sin guarda → excepción no controlada ante fecha inválida | Alta | Alto | Cubierto por TC-FIAB-008 (defecto-conocido), INC-WT-01 |
| RIE-P02 | Mutaciones múltiples sin `@Transactional` → estado inconsistente | Alta | Alto | Cubierto por TC-FIAB-022, INC-WT-04 |
| RIE-P03 | Ausencia de `@RestControllerAdvice` → HTTP 500 con stacktrace expuesto | Media | Medio | Cubierto por TC-FIAB-011, INC-WT-02 |
| RIE-P04 | Pago de amonestación sin validación de entrada | Media | Medio | Cubierto por TC-FIAB-025 |

### 3.2 Riesgos de proyecto (en el proceso de prueba)
| ID | Riesgo del proyecto | Probabilidad | Impacto | Contingencia |
|---|---|---|---|---|
| RIE-J01 | El Equipo 58-1 no entrega el código de pruebas en el plazo del sprint (precondición técnica) | Media | Alto | Escalar al profesor Ernesto Suárez; suspender el sprint (§4.5) hasta recibir la implementación; documentar el riesgo materializado. |
| RIE-J02 | Incompatibilidad H2/MySQL: queries MySQL-específicas fallan en H2 | Media | Alto | Usar `MODE=MySQL`; aislar tests afectados con `@Disabled` y moverlos al perfil de sistema. |
| RIE-J03 | Cobertura de decisión insuficiente por lógica condicional compleja | Media | Medio | Meta ≥ 50% para Sprint 3; ≥ 70% al final del Sprint 4 con casos de integración. |
| RIE-J04 | Cronograma: 5 sprints simulados antes de la entrega | Alta | Alto | Sprint 0 y 1 en paralelo la primera semana; Sprint 4 con subconjunto de casos de sistema si falta tiempo. |
| RIE-J05 | Pruebas frontend (Vue) no ejecutables en CI sin configuración adicional | Alta | Medio | TC-FIAB-017 como prueba manual con Playwright; documentar pasos de reproducción. |

---

## 4. Estrategia de Prueba del Plan

> Adapta la Estrategia de proyecto EST-FIAB-001 a este plan (29119-3 §A.2.4.d).

### 4.1 Sub-procesos de prueba
Unitario (caja blanca, JUnit 5 + Mockito + JaCoCo) · Integración (caja gris, `@SpringBootTest` + H2) · Sistema (caja negra, cliente HTTP) · Aceptación (caja negra, revisión contra ERS). Detalle en EST-FIAB-001 §4.

### 4.2 Entregables de prueba
- Especificación de casos de prueba (TCS-FIAB-001).
- Código de test `@Test` en rama `simulacion-desarrollo` (implementa el Equipo 58-1).
- Reportes JUnit/Surefire y de cobertura JaCoCo (branch) por ejecución de CI.
- Incidencias (GitHub Issues) INC-WT-01..04.
- Informe de Resultados de Pruebas (cierre de Fase 2).

### 4.3 Técnicas de diseño (29119-4)
Partición de equivalencia, análisis de valores límite, transición de estados, pruebas basadas en escenarios, pruebas de sintaxis y tablas de decisión. Asignación por caso en TCS-FIAB-001 §3.

### 4.4 Criterios de finalización y métricas
| Métrica (ISO 25023 / `objetivos.txt`) | Umbral [PROP] |
|---|---|
| M-02 Cobertura de decisión en métodos críticos | ≥ 70% |
| M-03 Tasa de pruebas `regresion` que pasan | 100% |
| M-05 Entradas inválidas controladas | ≥ 80% |
| Incidencias INC-WT-01..04 creadas como GitHub Issues | 100% |

### 4.5 Criterios de entrada, salida, suspensión y reanudación

**Entrada (por sprint):** rama `simulacion-desarrollo` con el código del sprint anterior integrado y compilando; CI (`ci-fiabilidad.yml`) ejecuta `mvn verify` sin errores; casos del sprint implementados por el Equipo 58-1.

**Salida (por sprint):** 100% de casos `regresion` del sprint pasando; casos `defecto-conocido` ejecutados; cobertura de decisión (M-02) ≥ 50% en los métodos críticos del sprint.

**Salida (plan completo, post Sprint 4):** M-02 ≥ 70%; M-03 = 100%; M-05 ≥ 80%; INC-WT-01..04 creadas.

**Suspensión:** error de compilación del proyecto de pruebas; fallo del perfil `test` de H2; indisponibilidad de la rama tras 48 h.

**Reanudación:** bloqueo resuelto por el Equipo 58-1 o el DevOp; el sprint se reinicia desde el re-commit del código.

### 4.6 Retest y pruebas de regresión
La suite `regresion` constituye el gate de CI y se re-ejecuta en cada push a `simulacion-desarrollo`. La suite `defecto-conocido` se ejecuta de forma informativa (no bloquea).

### 4.7 Requisitos de datos de prueba
IDs de libros válidos; ISBN de 13 dígitos; fechas ISO 8601 válidas e inválidas (`"24-06-2026"`, `"99/99/9999"`, `null`); archivos binarios de 0.9/1.0/1.1 MB; combinaciones de `metodoPago`/`comprobantePago`. Detalle por caso en TCS-FIAB-001.

### 4.8 Requisitos de ambiente de prueba
| Ambiente | Propósito | Configuración |
|---|---|---|
| Unitario / Integración | Sprints 0–4; JUnit 5 | H2 in-memory, perfil `test` (`application-test.properties`); JaCoCo vía Surefire |
| Sistema | Sprint 4; caja negra de endpoints | MySQL 8.0 (Docker Compose); backend en puerto 8080; cliente HTTP Postman/RestAssured |
| CI (GitHub Actions) | Validación por push en `simulacion-desarrollo` | `ubuntu-latest`; Java 21 (temurin); `mvn verify -Dgroups=regresion,defecto-conocido` |

```properties
# src/test/resources/application-test.properties
spring.datasource.url=jdbc:h2:mem:testdb;DB_CLOSE_DELAY=-1;MODE=MySQL
spring.jpa.hibernate.ddl-auto=create-drop
spring.jpa.database-platform=org.hibernate.dialect.H2Dialect
```

### 4.9 Desviaciones respecto de la Estrategia de proyecto
- El nivel de **sistema** usa cliente HTTP (Postman/RestAssured) en lugar de pruebas de carga JMeter (estas medían Capacidad de Recuperación, fuera de alcance en v2.0).
- Las métricas IEEE 1061 de la v1.0 se remapearon a ISO/IEC 25023 (ver TCS-FIAB-001 §6.1).

---

## 5. Actividades, Estimaciones, Roles y Cronograma

### 5.1 Roles, actividades y responsabilidades (Staffing)
| Rol | Nombre | Actividades de prueba |
|---|---|---|
| Líder General | Alberto Rodriguez | Aprueba plan y estrategia; coordina entrega de especificaciones al equipo autor del SUT; valida criterios de salida por sprint |
| Analista de Pruebas / Tester | Oscar Jaramillo | Redacta especificaciones TC-FIAB-*; define datos de prueba; verifica fidelidad de las implementaciones |
| Escriba | Samuel Artiles | Crea incidencias INC-WT-* como GitHub Issues; mantiene trazabilidad; documenta resultados |
| Líder de Métricas | Edwin Li | Calcula M-01..M-06 por sprint; actualiza el dashboard en GitHub Projects (Insights) |
| DevOp | Daniel Cohen | Mantiene la rama `simulacion-desarrollo`; configura `ci-fiabilidad.yml`; verifica reportes JaCoCo de rama |
| Autor del SUT | Equipo 58-1 (autores del software) | Implementa los `@Test` según especificaciones; configura `pom.xml` (H2, JaCoCo, Surefire); commits incrementales |

> **Necesidades de contratación / formación:** no aplica (equipo académico fijo de cinco roles).

### 5.2 Cronograma — Sprints simulados (actividades y estimaciones)

| Sprint | Código re-comprometido | Pruebas incorporadas | Criterio de salida |
|---|---|---|---|
| **Sprint 0** | Skeleton: `pom.xml` (H2/JaCoCo/Surefire), `application-test.properties`, `GestionBibliotecariaApplicationTests`, `ci-fiabilidad.yml` | TC-FIAB-001 | CI verde; JaCoCo con regla de branch |
| **Sprint 1** | `UsuarioService`, `UsuarioRepository`, `Usuario`, `SecurityConfig` | TC-FIAB-002..004 | `regresion` de Usuario pasa; INC-WT-04b |
| **Sprint 2** | `LibroService`, `LibroRepository`, `Libro` | TC-FIAB-005..007 | `regresion` de Libro pasa; INC-WT-01b |
| **Sprint 3** | `PrestamoService`, `PrestamoRepository`, `Prestamo`; `Controller` (préstamo) | TC-FIAB-008..022 (núcleo: cobertura de decisión, parse, no-atomicidad, advice ausente) | `regresion` pasa; INC-WT-01/02/04; M-02 ≥ 50% en PrestamoService |
| **Sprint 4** | `AmonestacionService`, reseñas en `Controller`; componentes Vue; sistema desplegable | TC-FIAB-025 + sistema caja negra | `regresion` pasa; INC-WT-03/04c; M-02 ≥ 70% global |

### 5.3 Configuración del workflow CI

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
        with: { name: jacoco-report, path: target/site/jacoco/ }
```

### 5.4 Estrategia de integración incremental
**Incremental ascendente (bottom-up):** repositorios/entidades → servicios (Usuario, Libro) → `PrestamoService` + `Controller` → `AmonestacionService` + reseñas + sistema. Stubs con `@MockBean`; drivers con clases de test JUnit 5 y `MockMvc`.

---

## 6. Matriz de Trazabilidad

| Hallazgo / Objetivo | Sub-car. | Nivel | Caja | Casos | Suite | Métrica |
|---|---|---|---|---|---|---|
| WT-01 | Tolerancia | Unitario | Blanca | TC-FIAB-008, 009 | defecto-conocido | M-05 |
| WT-01 | Madurez | Unitario | Blanca | TC-FIAB-005 | regresion | M-02, M-03 |
| WT-02 | Tolerancia | Integración | Gris | TC-FIAB-011 | defecto-conocido | M-05 |
| WT-02 | Madurez | Integración | Gris | TC-FIAB-012, 025 | regresion / defecto | M-01, M-03, M-06 |
| WT-03 | Tolerancia | Sistema | Negra | TC-FIAB-016, 017 | defecto-conocido | M-05 |
| WT-04 | Madurez | Integración | Gris | TC-FIAB-013, 014, 015, 022 | defecto-conocido | M-01, M-06 |
| WT-04 | Madurez | Unitario | Blanca | TC-FIAB-002 | defecto-conocido | M-01 |
| WT-04 | Madurez | Integración | Gris | TC-FIAB-003 | regresion | M-03, M-06 |
| Cobertura Madurez | Madurez | Unitario | Blanca | TC-FIAB-004, 006, 007, 018, 019, 020 | regresion | M-02 |
| Smoke | Madurez | Integración | Gris | TC-FIAB-001 | regresion | M-03 |
| Multipart límite | Tolerancia | Sistema | Negra | TC-FIAB-021 | defecto-conocido | M-05 |

**Especificación detallada de cada caso:** TCS-FIAB-001 (con ítems de cobertura TCI y datos de entrada por rama).

---

## 7. Gestión de Incidencias

Cada caso `defecto-conocido` se vincula a una incidencia en **GitHub Issues** (plantilla "Defecto F2"), con etiquetas `tipo:defecto`, `severidad:*`, `fase:fase-2`.

| ID Incidencia | Hallazgo | Severidad | Título | Casos vinculados |
|---|---|---|---|---|
| INC-WT-01 | WT-01 | Alta | `PrestamoService`: `LocalDate.parse` sin try/catch propaga `DateTimeParseException` | TC-FIAB-008, 009 |
| INC-WT-01b | WT-01 | Media | `LibroService`: catch genérico oculta causa de excepción JPA | TC-FIAB-010 |
| INC-WT-02 | WT-02 | Alta | Ausencia de `@RestControllerAdvice`: HTTP 500 expone stacktrace | TC-FIAB-011 |
| INC-WT-03 | WT-03 | Media | Funciones async del frontend sin manejo de rechazos | TC-FIAB-016, 017 |
| INC-WT-04 | WT-04 | Alta | `PrestamoService`: mutaciones múltiples sin `@Transactional` → estado inconsistente | TC-FIAB-013, 014, 022 |
| INC-WT-04b | WT-04 | Alta | `UsuarioService`: import `jakarta.transaction.Transactional` en lugar de Spring | TC-FIAB-002 |
| INC-WT-04c | WT-04 | Alta | `Controller.eliminarResena`: borrados encadenados sin transacción | TC-FIAB-015 |

### 7.1 Convención de Javadoc para casos `defecto-conocido`
```java
/**
 * [Comportamiento observado]
 * <p>Esperado (ERS §NFR-FIAB-*): [...]</p>
 * <p>Actual (defecto): [...]</p>
 * @see INC-WT-XX  (número de GitHub Issue)
 */
@Test
@Tag("defecto-conocido")
void nombreDelTest() { ... }
```

---

*Plan de Pruebas conforme a ISO/IEC/IEEE 29119-3:2021 (§7.2 / A.2.4), característica Reliability (Madurez · Tolerancia a Fallos) de ISO/IEC 25010:2023. Equipo SQA 11 — revisado el 24 de junio de 2026.*
