# Sistema de Checklists de Inspección Estática — SQA Equipo 11
## Basado en Evidencia Real de Artefactos del Equipo 58-1

**Versión:** 1.0
**Fecha:** 2026-05-06
**Equipo:** SQA 11 (Auditoría del Sistema de Gestión Bibliotecaria del Equipo 58-1)
**Principio rector:** Cada ítem de checklist debe ser verificable contra el contenido REAL del artefacto. No se audita con estándares que el artefacto no declara seguir.

**¿Qué es esto?**
Este documento define las 5 checklists que el Equipo 11 utilizará para auditar los artefactos del Equipo 58-1. Cada checklist está basada en **evidencia real** (páginas específicas de PDFs, líneas de código) y en **estándares internacionales** aplicables.

**Checklists incluidas:**
1. BRIEF (8 ítems) — Prácticas de Ingeniería de Requisitos
2. ERS (13 ítems) — ISO/IEC/IEEE 29148:2018
3. DAS (19 ítems + 4 ítems de auditoría visual) — ISO/IEC/IEEE 42010:2022 + C4
4. Código (16 ítems) — ISO/IEC 25010
5. PAC (15 ítems) — IEEE 730-2014

**Total: 75 ítems de verificación**

---

## 📋 ÍNDICE DE CHECKLISTS

1. [Checklist BRIEF](#1-checklist-brief)
2. [Checklist ERS](#2-checklist-ers)
3. [Checklist DAS](#3-checklist-das)
4. [Checklist Código](#4-checklist-código)
5. [Checklist PAC](#5-checklist-pac)
6. [Diseño del WF4 — Inyección de Checklists](#6-diseño-del-wf4--inyección-de-checklists)

---

## 1. CHECKLIST BRIEF

**Artefacto:** BRIEF EQUIPO 58 1 - v1.1.pdf  
**Estándar aplicable:** Ninguno formal declarado. Se audita como documento de entrada previo a ERS (prácticas de ingeniería de requisitos).  
**Enfoque:** Verificar que el BRIEF sea suficiente para derivar un ERS completo.

| ID | Ítem | Verificación | Resultado | Evidencia / Referencia |
|---|---|---|---|---|
| BRIEF-01 | ¿El documento tiene identificación clara (nombre del sistema, versión, fecha, autores)? | [ ] Cumple [ ] No Cumple | | Portada v1.1, fecha 01/05/25 |
| BRIEF-02 | ¿El propósito del documento está definido? | [ ] Cumple [ ] No Cumple | | "El propósito de este documento es recolectar, analizar y definir las necesidades a un alto nivel" — Pág. 3 |
| BRIEF-03 | ¿Identifica stakeholders clave con sus roles? | [ ] Cumple [ ] No Cumple | | Tabla Meta/Personas/Impacto/Entregable — Pág. 4 |
| BRIEF-04 | ¿El backlog está poblado con entregables concretos? | [ ] Cumple [ ] No Cumple | | **DEFECTO:** Sección "2. Backlog" está VACÍA — Pág. 5 |
| BRIEF-05 | ¿Las restricciones están clasificadas (negocio vs técnico)? | [ ] Cumple [ ] No Cumple | | **DEFECTO:** Mezcla "gestiona catálogo físico" (negocio) con "solo disponible en español y por navegador" (técnico) — Pág. 5 |
| BRIEF-06 | ¿Los rangos de calidad son medibles/quantificables? | [ ] Cumple [ ] No Cumple | | **DEFECTO:** "Diseño atractivo y sencillo de usar" (subjetivo), "Seguridad básica" (sin métrica) — Pág. 5 |
| BRIEF-07 | ¿El plan de trabajo está incluido o referenciado con acceso? | [ ] Cumple [ ] No Cumple | | **DEFECTO:** "Plan de trabajo creado en JIRA" sin link ni evidencia — Pág. 5 |
| BRIEF-08 | ¿El histórico de revisiones documenta cambios significativos? | [ ] Cumple [ ] No Cumple | | v1.0 → v1.1: añadida amonestaciones, modificadas restricciones — Pág. 2 |

**Estándares NO aplicables (y por qué):**
- ❌ INVEST: El BRIEF no contiene historias de usuario.
- ❌ ISO/IEC/IEEE 29148: El BRIEF no es una Especificación de Requisitos formal.
- ❌ Modelo C4: El BRIEF no describe arquitectura.

---

## 2. CHECKLIST ERS

**Artefacto:** ERS Equipo 58 1 v.1.2.pdf  
**Estándar aplicable:** ISO/IEC/IEEE 29148:2018 (Estructura, consistencia, trazabilidad) + ISO/IEC 25010 (Requisitos suplementarios)  
**Formato real del artefacto:** Canvas/3C propio (1 Historia, 2 Conversación, 3 Criterios de Aceptación)  
**NOTA CRÍTICA:** El ERS NO declara usar INVEST. Auditar INVEST es INAPROPRIADO.

### 2.1 Control de Documento

| ID | Ítem | Verificación | Resultado | Evidencia |
|---|---|---|---|---|
| ERS-01 | ¿El documento tiene control de versiones con histórico? | [ ] Cumple [ ] No Cumple | | Histórico v1.0→v1.1→v1.2 — Pág. 2 |
| ERS-02 | ¿La versión en portada coincide con la del histórico? | [ ] Cumple [ ] No Cumple | | **DEFECTO:** Portada dice "Versión: 1.1", archivo y histórico dicen 1.2 — Pág. 1 vs Pág. 2 |
| ERS-03 | ¿Cada historia tiene identificación única? | [ ] Cumple [ ] No Cumple | | HU1 a HU5 numeradas — Págs. 4-8 |

### 2.2 Estructura de Historias de Usuario (Canvas/3C)

| ID | Ítem | Verificación | Resultado | Evidencia |
|---|---|---|---|---|
| ERS-04 | ¿Cada historia tiene formato estructurado (Historia + Conversación + Criterios)? | [ ] Cumple [ ] No Cumple | | 5 historias con formato 3C — Págs. 4-8 |
| ERS-05 | ¿La historia declara el actor (quién), la acción (qué) y el beneficio (por qué)? | [ ] Cumple [ ] No Cumple | | "Como [rol] quiero [acción] para [beneficio]" — Todas las HUs |
| ERS-06 | ¿La conversación incluye escenarios de uso claros? | [ ] Cumple [ ] No Cumple | | Todas las HUs incluyen escenario — Págs. 4-8 |
| ERS-07 | ¿Las reglas de negocio son coherentes con los criterios de aceptación? | [ ] Cumple [ ] No Cumple | | **DEFECTO:** HU5 — Regla dice "una amonestación a la vez", criterio dice "una o varias" — Pág. 8 |
| ERS-08 | ¿Los criterios de aceptación son exhaustivos (camino feliz + errores)? | [ ] Cumple [ ] No Cumple | | HU1-HU4: ✅. HU5: solo camino feliz. |
| ERS-09 | ¿No hay redundancia exacta entre criterios de aceptación? | [ ] Cumple [ ] No Cumple | | **DEFECTO:** HU3 — "La contraseña se guarda de forma segura (hasheada)" repetido dos veces — Pág. 6 |
| ERS-10 | ¿Las dependencias están identificadas? | [ ] Cumple [ ] No Cumple | | "Dependencias: Acceso a base de datos" — HU1, HU2, HU4 |

### 2.3 Requisitos Suplementarios (ISO/IEC 25010)

| ID | Ítem | Verificación | Resultado | Evidencia |
|---|---|---|---|---|
| ERS-11 | ¿Los requisitos suplementarios cubren todos los atributos de calidad definidos en el PAC? | [ ] Cumple [ ] No Cumple | | **DEFECTO:** Solo 4 de 12+ sub-características: Operabilidad, Ausencia de fallos, Integridad, Capacidad para ser modificado — Pág. 9 |
| ERS-12 | ¿Cada requisito suplementario es medible/verificable? | [ ] Cumple [ ] No Cumple | | **DEFECTO:** "sin errores internos, bloqueos inesperados o corrupción de datos" (no medible) — Pág. 9 |
| ERS-13 | ¿Existe matriz de trazabilidad historias ↔ requisitos suplementarios? | [ ] Cumple [ ] No Cumple | | **DEFECTO:** No existe — Documento completo |

**Estándares NO aplicables (y por qué):**
- ❌ **INVEST:** El ERS NO declara INVEST. Usa Canvas/3C propio. Auditar INVEST sería como auditar un edificio con normas de aviones.
- ❌ **Casos de uso UML:** No se utilizan en el artefacto.
- ❌ **BDD/Gherkin:** No se utilizan en el artefacto.

---

## 3. CHECKLIST DAS

**Artefacto:** DAS Equipo 58-1 v1.5.pdf  
**Estándar aplicable:** ISO/IEC/IEEE 42010:2022 + Modelo C4 (implícito en diagramas)  
**Arquitectura real:** Patrón de Capas + Cliente-Servidor (DECLARADO explícitamente)  
**NOTA CRÍTICA:** El DAS NO usa DDD ni Bounded Contexts. Auditar DDD es INAPROPRIADO.

### 3.1 Control de Documento

| ID | Ítem | Verificación | Resultado | Evidencia |
|---|---|---|---|---|
| DAS-01 | ¿El documento tiene control de versiones con histórico detallado? | [ ] Cumple [ ] No Cumple | | 6 versiones (1.0 a 1.5) con descripciones — Pág. 2 |
| DAS-02 | ¿Las fechas del histórico son coherentes cronológicamente? | [ ] Cumple [ ] No Cumple | | **DEFECTO:** v1.5 dice "17/05/25" (mayo) pero debería ser junio — Pág. 2 |
| DAS-03 | ¿La versión actual coincide con el nombre del archivo? | [ ] Cumple [ ] No Cumple | | Archivo "v1.5", documento dice "Versión: 1.5" — Pág. 1 |

### 3.2 Decisiones Arquitectónicas

| ID | Ítem | Verificación | Resultado | Evidencia |
|---|---|---|---|---|
| DAS-04 | ¿Cada decisión tiene ID, fecha, descripción, justificación? | [ ] Cumple [ ] No Cumple | | 6 decisiones con tabla completa — Pág. 5 |
| DAS-05 | ¿Las fechas de decisiones son anteriores o iguales a la fecha del documento? | [ ] Cumple [ ] No Cumple | | **DEFECTO:** ID-5 (21/06/25) e ID-6 (26/06/25) son POSTERIORES a la fecha del documento (17/06/25) — Pág. 5 |
| DAS-06 | ¿Las decisiones usan terminología arquitectónica correcta? | [ ] Cumple [ ] No Cumple | | **DEFECTO:** ID-4 dice "alto cohesivo" para un SPA — la cohesión mide relación entre responsabilidades de un módulo, no si es una sola página — Pág. 5 |

### 3.3 Diagramas y Vistas (Modelo C4)

| ID | Ítem | Verificación | Resultado | Evidencia |
|---|---|---|---|---|
| DAS-07 | ¿Existe Diagrama de Contexto (Nivel 1 C4)? | [ ] Cumple [ ] No Cumple | | ✅ En PDF separado: "Equipo 58-1_ Diagrama de contexto..." |
| DAS-08 | ¿Existe Diagrama de Contenedores (Nivel 2 C4)? | [ ] Cumple [ ] No Cumple | | ✅ En PDF separado |
| DAS-09 | ¿Existe Diagrama de Componentes (Nivel 3 C4)? | [ ] Cumple [ ] No Cumple | | ✅ En PDF separado (aunque es discutible si es C4 puro) |
| DAS-10 | ¿Los diagramas C4 están embebidos en el DAS o referenciados con acceso? | [ ] Cumple [ ] No Cumple | | **DEFECTO:** Placeholders vacíos en DAS (Págs. 8-11), reales en PDF separado |
| DAS-11 | ¿Existe Diagrama de Clases UML? | [ ] Cumple [ ] No Cumple | | ✅ Referenciado con link — Pág. 13 |
| DAS-12 | ¿Existe vista de despliegue/procesos? | [ ] Cumple [ ] No Cumple | | **DEFECTO:** No existe — Documento completo |

### 3.4 Trazabilidad y Consistencia

| ID | Ítem | Verificación | Resultado | Evidencia |
|---|---|---|---|---|
| DAS-13 | ¿La lista de archivos por componente es completa vs el código real? | [ ] Cumple [ ] No Cumple | | **DEFECTO:** Faltan componentes Vue reales: EliminarLibroPantallaBusqueda.vue, ModificarLibroPantallaBusqueda.vue, etc. — Pág. 14 |
| DAS-14 | ¿La arquitectura declarada (Capas) se refleja en la estructura de paquetes del código? | [ ] Cumple [ ] No Cumple | | ✅ model, controller, service, repository, config, security, dto — Pág. 14 |
| DAS-15 | ¿Cada componente del DAS se vincula con al menos una historia del ERS? | [ ] Cumple [ ] No Cumple | | ✅ Interfaces de Usuario listan HUs asociadas — Págs. 15-24 |

### 3.5 Validación de Atributos de Calidad

| ID | Ítem | Verificación | Resultado | Evidencia |
|---|---|---|---|---|
| DAS-16 | ¿La arquitectura justifica cómo soporta Mantenibilidad (separación de responsabilidades)? | [ ] Cumple [ ] No Cumple | | ✅ Decisiones ID-2 e ID-3: Controller/Service/Repository separados — Pág. 5 |
| DAS-17 | ¿La arquitectura justifica cómo soporta Seguridad (autenticación/autorización)? | [ ] Cumple [ ] No Cumple | | ✅ Decisiones ID-5 y ID-6: SecurityConfig + encriptación — Pág. 5 |
| DAS-18 | ¿La arquitectura justifica cómo soporta Fiabilidad (tolerancia a fallos)? | [ ] Cumple [ ] No Cumple | | **DEFECTO:** No hay mecanismos de redundancia, respaldo, o circuit breaker documentados |
| DAS-19 | ¿Se identifican cuellos de botella o riesgos técnicos? | [ ] Cumple [ ] No Cumple | | **DEFECTO:** No se identifican riesgos técnicos explícitamente |

### 3.6 Auditoría Visual de Diagramas (Nuevo en v1.1)

**Herramienta:** WF2 con análisis visual Gemini multimodal (`scripts/sqa_core/image_analysis.py`)
**Trigger:** Automático al detectar PDF con diagramas C4/UML

| ID | Ítem | Verificación | Resultado | Evidencia |
|---|---|---|---|---|
| DAS-VIS-01 | ¿El Diagrama de Contexto incluye todos los actores externos mencionados en el ERS? | [ ] Cumple [ ] No Cumple | | Análisis visual por IA |
| DAS-VIS-02 | ¿Las relaciones entre componentes tienen dirección y protocolo indicados? | [ ] Cumple [ ] No Cumple | | Análisis visual por IA |
| DAS-VIS-03 | ¿Los contenedores del Nivel 2 corresponden a los componentes declarados en el DAS? | [ ] Cumple [ ] No Cumple | | Análisis visual + trazabilidad textual |
| DAS-VIS-04 | ¿La notación C4 es correcta (cajas, personas, líneas etiquetadas)? | [ ] Cumple [ ] No Cumple | | Análisis visual por IA |

**Nota técnica:** Los diagramas se extraen automáticamente de los PDFs del DAS, se clasifican por tipo (Contexto/Contenedor/Componente/UML), y se analizan con Gemini multimodal usando prompts few-shot para reducir falsos positivos. Los hallazgos visuales se mergean con los hallazgos textuales en el reporte consolidado de WF2.

**Estándares NO aplicables (y por qué):**
- ❌ **DDD / Bounded Contexts:** El DAS NO usa DDD. Usa Patrón de Capas.
- ❌ **Arquitectura Hexagonal / Clean:** No se declara ni se usa.
- ❌ **Microservicios:** Es una aplicación monolítica SPA + API.
- ❌ **Event Sourcing / CQRS:** No se utiliza.

---

## 4. CHECKLIST CÓDIGO

**Artefacto:** Código fuente del Equipo 58-1 (Java 21 + Spring Boot 3.4.5 / Vue 3.2.13)  
**Estándar aplicable:** ISO/IEC 25010 (Mantenibilidad, Seguridad) + Convenciones Spring/Vue  
**NOTA CRÍTICA:** Esta es inspección ESTÁTICA (análisis de código sin ejecutar). Atributos dinámicos (rendimiento, carga, E2E) NO se verifican aquí.

### 4.1 Mantenibilidad — Análisis Estático

| ID | Ítem | Verificación | Resultado | Evidencia |
|---|---|---|---|---|
| COD-01 | ¿El backend sigue el patrón de capas declarado en el DAS? | [ ] Cumple [ ] No Cumple | | **PARCIAL:** Estructura de paquetes correcta, pero Controller.java maneja 6 dominios en un solo archivo (458 líneas) — viola SRP |
| COD-02 | ¿La inyección de dependencias usa constructor (recomendación Spring)? | [ ] Cumple [ ] No Cumple | | **DEFECTO:** Usa @Autowired por campo en lugar de constructor |
| COD-03 | ¿Las clases de servicio tienen una única responsabilidad? | [ ] Cumple [ ] No Cumple | | **PARCIAL:** Cada servicio maneja un dominio, pero Controller monolítico rompe la separación |
| COD-04 | ¿Los DTOs se usan para controlar exposición de datos? | [ ] Cumple [ ] No Cumple | | ✅ Solo 3 DTOs: ComentarioResenaRequest, PrestamoRequest, ResenaRequest |
| COD-05 | ¿El código tiene convenciones de nomenclatura consistentes? | [ ] Cumple [ ] No Cumple | | **DEFECTO:** Clase principal duplicada `__1.spring_boot.GestionBibliotecariaApplication` |
| COD-06 | ¿El pom.xml está limpio (sin dependencias duplicadas)? | [ ] Cumple [ ] No Cumple | | **DEFECTO:** `spring-boot-starter-data-jpa` aparece DOS veces (líneas 43 y 65) |

### 4.2 Seguridad — Análisis Estático

| ID | Ítem | Verificación | Resultado | Evidencia |
|---|---|---|---|---|
| COD-07 | ¿Las contraseñas se hashean antes de persistir? | [ ] Cumple [ ] No Cumple | | ✅ `UsuarioService` usa `passwordEncoder.encode()` |
| COD-08 | ¿El backend valida la complejidad de contraseña antes de hashear? | [ ] Cumple [ ] No Cumple | | **DEFECTO:** ERS exige 8 caracteres + mayúscula + número + símbolo. Backend NO valida esto. |
| COD-09 | ¿El frontend valida la complejidad de contraseña antes de enviar? | [ ] Cumple [ ] No Cumple | | **DEFECTO:** `RegistroUsuario.vue` línea 104 tiene la validación COMENTADA: `// if (password.length < 8)...` |
| COD-10 | ¿Las credenciales de base de datos están externalizadas? | [ ] Cumple [ ] No Cumple | | **DEFECTO:** `application.properties` tiene `password=admin` hardcodeado |
| COD-11 | ¿SecurityConfig protege endpoints sensibles por rol? | [ ] Cumple [ ] No Cumple | | **PARCIAL:** DELETE /api/libros protegido, pero POST /api/libros depende de lógica de negocio, no de seguridad |
| COD-12 | ¿Hay manejo global de excepciones (@ControllerAdvice)? | [ ] Cumple [ ] No Cumple | | **DEFECTO:** No existe — riesgo de exponer stack traces |

### 4.3 Fiabilidad — Análisis Estático

| ID | Ítem | Verificación | Resultado | Evidencia |
|---|---|---|---|---|
| COD-13 | ¿El código captura excepciones en operaciones críticas (acceso a DB, parsing)? | [ ] Cumple [ ] No Cumple | | **DEFECTO:** `PrestamoService` hace `LocalDate.parse(fechaPrestamoStr)` sin try-catch |
| COD-14 | ¿Hay mecanismos de recuperación o fallback documentados en código? | [ ] Cumple [ ] No Cumple | | **DEFECTO:** No hay retry, circuit breaker, ni fallback |

### 4.4 Trazabilidad

| ID | Ítem | Verificación | Resultado | Evidencia |
|---|---|---|---|---|
| COD-15 | ¿Cada endpoint REST corresponde a una funcionalidad del ERS? | [ ] Cumple [ ] No Cumple | | **PARCIAL:** Algunos endpoints no tienen HU directa (ej. edición de perfil) |
| COD-16 | ¿Cada componente Vue se vincula con una historia del ERS? | [ ] Cumple [ ] No Cumple | | **PARCIAL:** DAS lista asociaciones, pero algunos componentes como InicioSesion.vue no tienen HU asignada |

**Atributos NO verificables por análisis ESTÁTICO (requieren pruebas DINÁMICAS):**
- ⚠️ **Rendimiento / Eficiencia:** Requiere pruebas de carga (k6, JMeter).
- ⚠️ **Cobertura de código:** Requiere ejecución de tests + JaCoCo.
- ⚠️ **Pruebas E2E / UI:** Requiere Playwright/Selenium ejecutando el navegador.
- ⚠️ **Tolerancia a fallos en runtime:** Requiere Chaos Monkey o simulación de fallos.

---

## 5. CHECKLIST PAC

**Artefacto:** Plan de Aseguramiento de la Calidad (en desarrollo por el Equipo 11)  
**Estándar aplicable:** IEEE 730-2014 (Plan de Aseguramiento de la Calidad de Software)  
**NOTA:** Esta checklist valida que el PAC del Equipo 11 cumpla con IEEE 730.

### 5.1 Objetivos de Calidad (ISO/IEC 25010)

| ID | Ítem | Verificación | Resultado | Referencia PAC |
|---|---|---|---|---|
| PAC-01 | ¿Se definen explícitamente los atributos de calidad a evaluar? | [ ] Cumple [ ] No Cumple | | Sección "Objetivos de Calidad" |
| PAC-02 | ¿Cada atributo tiene sub-características medibles? | [ ] Cumple [ ] No Cumple | | Ej: Mantenibilidad → Capacidad para ser probado, Reusabilidad, Analizabilidad |
| PAC-03 | ¿Los objetivos de calidad del producto están diferenciados de los del proceso? | [ ] Cumple [ ] No Cumple | | ISO 25010 vs IEEE 730 / ISO 12207 |

### 5.2 Gestión y Organización

| ID | Ítem | Verificación | Resultado | Referencia |
|---|---|---|---|---|
| PAC-04 | ¿Están definidos los roles y responsabilidades del equipo SQA? | [ ] Cumple [ ] No Cumple | | Alberto (Responsable), Oscar (Tecnología), Daniel (Funcional), Edwin (Métricas), Samuel (Escriba) |
| PAC-05 | ¿Se describe la estrategia de validación (¿construimos el sistema correcto?)? | [ ] Cumple [ ] No Cumple | | Validación vs Verificación |
| PAC-06 | ¿Se describe la estrategia de verificación (¿construimos correctamente?)? | [ ] Cumple [ ] No Cumple | | Pruebas estáticas + dinámicas |

### 5.3 Documentación, Estándares y Guías

| ID | Ítem | Verificación | Resultado | Referencia |
|---|---|---|---|---|
| PAC-07 | ¿El PAC lista los artefactos a auditar (ERS, DAS, Código)? | [ ] Cumple [ ] No Cumple | | Inventario documental |
| PAC-08 | ¿Se especifica qué estándar se aplica a cada artefacto? | [ ] Cumple [ ] No Cumple | | Ej: 29148 para ERS, 42010 para DAS, 25010 para Código |
| PAC-09 | ¿Se declaran las herramientas tecnológicas para cada fase? | [ ] Cumple [ ] No Cumple | | Ver `sqa/PACS-Fase2-Herramientas.md` |

### 5.4 Métricas y Control Estadístico

| ID | Ítem | Verificación | Resultado | Referencia |
|---|---|---|---|---|
| PAC-10 | ¿Cada métrica tiene nombre, definición, objetivo, fórmula y responsable? | [ ] Cumple [ ] No Cumple | | Densidad de Defectos = Defectos / Tamaño (KLOC) |
| PAC-11 | ¿Se incluye Cobertura de Revisiones? | [ ] Cumple [ ] No Cumple | | Fórmula: (Artefactos revisados / Artefactos planificados) × 100 |
| PAC-12 | ¿Se incluye Densidad de Defectos con unidad de medida? | [ ] Cumple [ ] No Cumple | | **CORREGIDO:** Debe especificar "Defectos por KLOC" o "Defectos por Punto de Función" |

### 5.5 Ejecución y Cronograma

| ID | Ítem | Verificación | Resultado | Referencia |
|---|---|---|---|---|
| PAC-13 | ¿Existe un vínculo al Plan de Pruebas (PP)? | [ ] Cumple [ ] No Cumple | | Fase 2: Pruebas Dinámicas |
| PAC-14 | ¿El cronograma mapea actividades por iteración? | [ ] Cumple [ ] No Cumple | | Iteraciones del proyecto |
| PAC-15 | ¿Se define el proceso de gestión de defectos (tickets en Jira)? | [ ] Cumple [ ] No Cumple | | Workflow de resolución |

---

## 6. DISEÑO DEL WF4 — INYECCIÓN DE CHECKLISTS

### 6.1 Trigger del WF4

```
Evento: Nuevo commit en /documentacion/ o cambio en código fuente
↓
Detección de tipo de artefacto modificado
↓
Selección de checklist correspondiente
↓
Inyección en Jira + Confluence
↓
Bloqueo de fases posteriores hasta aprobación
```

### 6.2 Mapeo Artefacto → Checklist → Estándar

| Artefacto Detectado | Checklist Aplicada | Estándar Rector | Rol Responsable |
|---|---|---|---|
| `BRIEF*.pdf` | Checklist BRIEF | Prácticas de IR | Líder Funcional |
| `ERS*.pdf` | Checklist ERS | ISO/IEC/IEEE 29148 | Líder Funcional |
| `DAS*.pdf` | Checklist DAS | ISO/IEC/IEEE 42010 + C4 | Líder Tecnológico |
| `*.java`, `*.vue` | Checklist Código | ISO/IEC 25010 | Líder Tecnológico |
| `PAC*.md/pdf` | Checklist PAC | IEEE 730 | Líder General |

### 6.3 Payload JSON para Jira

```json
{
  "project": "SQA11",
  "issuetype": "Inspección",
  "summary": "Inspección Estática: ERS Equipo 58-1 v1.2",
  "description": "Checklist de inspección estática según ISO/IEC/IEEE 29148",
  "artifact": "ERS Equipo 58 1 v.1.2.pdf",
  "standard": "ISO/IEC/IEEE 29148:2018",
  "checklist_version": "1.0",
  "subtasks": [
    {
      "id": "ERS-01",
      "summary": "Control de versiones consistente",
      "description": "¿La versión en portada coincide con el histórico?",
      "acceptance_criteria": "Portada v1.2 = Histórico v1.2"
    },
    {
      "id": "ERS-07",
      "summary": "Coherencia reglas vs criterios HU5",
      "description": "Regla: una amonestación a la vez. Criterio: una o varias.",
      "acceptance_criteria": "Sin contradicciones internas"
    }
  ]
}
```

### 6.4 Quality Gate

El artefacto NO puede pasar a Workflow 1 (Auditoría con IA) ni Workflow 2 (Análisis estático de código) hasta que:
1. TODAS las subtareas del checklist estén en estado DONE, O
2. Los defectos encontrados estén documentados como Bugs Documentales en Jira con su ID de checklist.

### 6.5 Plantilla de Reporte en Confluence

```markdown
# Acta de Inspección: [Nombre del Artefacto]
**Fecha:** [Auto]
**Inspector:** [Rol]
**Estándar:** [ISO/EEE]
**Versión Checklist:** 1.0

## Resultados
| ID | Ítem | Resultado | Observación |
|---|---|---|---|
| [ID] | [Descripción] | Cumple / No Cumple | [Evidencia] |

## Métricas
- Cobertura de Revisión: [X/Y] = Z%
- Densidad de Defectos: [N defectos / tamaño]

## Defectos Documentados
- [Link a Jira BUG-XXX]
```

---

## 📊 RESUMEN DE DEFECTOS ENCONTRADOS

| ID | Artefacto | Defecto | Severidad | Checklist ID |
|---|---|---|---|---|
| D-001 | BRIEF | Backlog vacío | Alta | BRIEF-04 |
| D-002 | BRIEF | Rangos de calidad no medibles | Media | BRIEF-06 |
| D-003 | ERS | Inconsistencia de versión (1.1 vs 1.2) | Media | ERS-02 |
| D-004 | ERS | HU5 contradicción interna | **Crítica** | ERS-07 |
| D-005 | ERS | HU3 redundancia exacta | Baja | ERS-09 |
| D-006 | ERS | Requisitos suplementarios incompletos | Alta | ERS-11 |
| D-007 | DAS | Fechas futuras imposibles (ID-5, ID-6) | **Crítica** | DAS-05 |
| D-008 | DAS | Error conceptual "alto cohesivo" en ID-4 | Media | DAS-06 |
| D-009 | DAS | Lista de archivos incompleta | Media | DAS-13 |
| D-010 | DAS | Falta vista de despliegue | Media | DAS-12 |
| D-011 | CÓDIGO | Controller monolítico (458 líneas) | Alta | COD-01 |
| D-012 | CÓDIGO | Validación contraseña comentada en frontend | **Crítica** | COD-09 |
| D-013 | CÓDIGO | Backend no valida complejidad de contraseña | **Crítica** | COD-08 |
| D-014 | CÓDIGO | Credenciales hardcodeadas | **Crítica** | COD-10 |
| D-015 | CÓDIGO | Sin @ControllerAdvice | Alta | COD-12 |
| D-016 | CÓDIGO | Dependencias duplicadas en pom.xml | Baja | COD-06 |
| D-017 | CÓDIGO | Parsing de fecha sin manejo de excepciones | Media | COD-13 |

---

**Fin del Documento de Checklists**
