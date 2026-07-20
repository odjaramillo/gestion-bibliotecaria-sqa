# Plan de Aseguramiento de la Calidad del Software (PACS)

## Histórico de Revisiones
| Fecha | Versión | Descripción | Autor(es) |
|---|---|---|---|
| 2026-07-07 | 1.0 | Emisión inicial del PACS consolidado F1+F2 | Oscar Jaramillo |
| 2026-07-12 | 1.1 | Actualización de pruebas dinámicas (Unitarias, Integración, Sistema) | Oscar Jaramillo |
| 2026-07-19 | 2.0 | Reestructuración del PACS según Plantilla v4.0 exigida | Equipo 11 |

## 1. Objetivos de Calidad
El nivel de calidad deseado se centra en garantizar que el Sistema de Gestión Bibliotecaria (SUT) integre de manera intrínseca la característica de **Fiabilidad** (según ISO/IEC 25010). Para lograrlo, los objetivos SMART definidos se concentran en las siguientes sub-características:
- **Tolerancia a Fallos**: Garantizar que el sistema controle excepciones específicas en backend (evitando stacktraces expuestos) y maneje correctamente los rechazos de promesas asíncronas en el frontend.
- **Capacidad de Recuperación**: Asegurar la atomicidad transaccional ante fallos parciales (mediante `@Transactional`), el establecimiento de una degradación elegante en la UI y la resiliencia en el pool de conexiones de base de datos.

## 2. Gestión

### 2.1 Organización
El equipo SQA (Equipo 11) está conformado por los siguientes 5 integrantes, quienes garantizan la independencia de las auditorías:
- **Líder General (Alberto Rodriguez)**: Coordina el proceso completo, elabora el PAC, aprueba entregables y dirige la inspección y el walkthrough.
- **Líder Tecnológico / DevOp (Daniel Cohen / Oscar Jaramillo)**: Diseña e implementa el ecosistema tecnológico automatizado en GitHub Actions simulando la integración continua.
- **Líder Funcional (Daniel Cohen)**: Brinda soporte en la verificación de dominio, trazabilidad de requisitos y comportamiento del negocio.
- **Líder de Métricas (Edwin Li)**: Define, calcula y reporta las métricas a lo largo de los sprints (M-01 a M-06).
- **Escriba (Samuel Artiles)**: Documenta hallazgos, levanta actas y diseña/reporta las auditorías estáticas.
- *Rol Complementario*: **Analista de Pruebas / Tester (Oscar Jaramillo)**: Diseña el Plan de Pruebas, Especificación de Casos y ejecuta las pruebas dinámicas.

**En las pruebas de aceptación participará la Profesora de la materia.**

### 2.2 Tareas y Responsabilidades
Las actividades de SQA dentro del equipo se guían por los siguientes principios:
- **Validación** *(Hacer el sistema correcto)*: Comprobar que el software satisfaga las necesidades reales del usuario y el negocio.
- **Verificación** *(Hacer el sistema correctamente)*: Asegurar que el software cumple con las especificaciones técnicas, arquitectónicas y estándares de calidad definidos.

Para la Segunda Entrega, se planificaron y asignaron las siguientes actividades centrales:
- **Pruebas Estáticas a Código**: Walkthrough Técnico guiado por el autor sobre los 6 módulos críticos y Auditoría estática asistida con IA. 
  *Responsables: Líder General, Escriba, y el resto del equipo SQA como revisores.*
- **Pruebas Dinámicas en 4 Niveles**: 
  - Pruebas Unitarias (Caja Blanca) a nivel de lógica de métodos.
  - Pruebas de Integración (Caja Gris) a nivel de interacción de componentes y BD.
  - Pruebas de Sistema (Caja Negra) a nivel de API REST.
  - Pruebas de Aceptación (Caja Negra) end-to-end simulando la navegación.
  *Responsables: Analista de Pruebas (Tester) y Líder Tecnológico.*

## 3. Documentación
Los artefactos sometidos a revisión y base fundamental del aseguramiento de la calidad en esta iteración son:
1. **Especificación de Requerimientos de Software (ERS)**
2. **Documento de la Arquitectura del Software (DAS)**
3. **Código** (Repositorio fuente del Sistema de Gestión Bibliotecaria: Java/Spring Boot + Vue.js)

## 4. Estándares y guías
Los estándares y prácticas normativas que rigen el proyecto son:
- **IEEE 730-2014**: Planificación, control y ejecución del Aseguramiento de la Calidad del Software.
- **ISO/IEC 25010:2023**: Modelo de calidad de producto, base para la característica de Fiabilidad.
- **ISO/IEC 25023:2016**: Medición de características de calidad y definición de métricas cuantitativas.
- **ISO/IEC/IEEE 29119-2/3/4**: Referencia para procesos de prueba, documentación de planes de prueba, especificación de casos y ejecución de la técnica de walkthrough.
- **ISO/IEC/IEEE 15289:2019**: Guía para la estructura y contenido de los reportes y registros técnicos.

## 5. Métricas

| N | Definición | Objetivo | Procedimiento | Responsables |
|---|---|---|---|---|
| M-01 | **Cobertura de decisión/rama** | Evaluar la corrección de la lógica de negocio crítica (Meta: ≥ 70%). | Cálculo automático mediante JaCoCo y CI midiendo ramas ejercitadas / ramas totales en tests unitarios. | Líder de Métricas, Líder Tecnológico |
| M-02 | **Densidad de defectos** | Cuantificar la ausencia de defectos estructurales en la Fiabilidad. | Conteo de defectos detectados por pruebas estáticas/dinámicas dividido por los módulos revisados (o KLOC). | Líder de Métricas, Escriba |
| M-03 | **Tasa de pruebas que pasan** | Asegurar la madurez de la suite antes de integrar al SUT. | Evaluar de manera automatizada: (Pruebas exitosas / Pruebas ejecutadas) * 100 en GitHub Actions. | Líder Tecnológico, Analista de Pruebas |
| M-04 | **Entradas inválidas controladas** | Evaluar la tolerancia a fallos ante inyecciones malformadas (Meta: ≥ 80%). | Enfoque de Caja Negra/Gris: Casos inválidos manejados sin excepción no controlada / casos inválidos probados. | Analista de Pruebas |
| M-05 | **Operaciones con guarda de estado** | Prevenir estados inconsistentes y pérdida de atomicidad (Meta: ≥ 80%). | Revisión de caja blanca: Operaciones críticas con validación de precondición (ej. `@Transactional`) / operaciones totales. | Analista de Pruebas, Escriba |

## 6. Cronograma de SQA
- **Sprints 0 y 1**: Configuración del ecosistema tecnológico (GitHub Actions, SonarCloud) y del esqueleto de pruebas (H2, JaCoCo, JUnit).
- **Sprint 2**: Ejecución de las Pruebas Estáticas (Auditoría IA y Sesión de Walkthrough Técnico con los autores).
- **Sprint 3**: Definición del Plan de Pruebas y Especificación exhaustiva de Casos de Prueba Dinámicos (Unitarias e Integración).
- **Sprint 4**: Desarrollo y automatización de las Pruebas de Sistema (Caja Negra) y Pruebas E2E de Aceptación (Playwright).
- **Cierre**: Consolidación de métricas (DDF, CRC, FTR), reporte de resultados en el dashboard y generación del documento final.

## 7. Pruebas
**Plan de Pruebas (PP):**
El plan abarcará una validación rigurosa de la Fiabilidad en los siguientes niveles, incorporando enfoques complementarios:
- **Nivel Unitario (Enfoque de Caja Blanca)**: Verificación directa de la lógica de los servicios (`PrestamoService`, `UsuarioService`), controlando los límites, excepciones y ramas algorítmicas haciendo uso de JUnit 5 y mocks (Mockito).
- **Nivel de Integración (Enfoque de Caja Gris)**: Análisis del comportamiento integrado entre las capas de servicio y la persistencia en base de datos H2 para detectar huérfanos o fallos transaccionales.
- **Nivel de Sistema y Aceptación (Enfoque de Caja Negra)**: Validación de los endpoints API a través de MockMvc, analizando las respuestas HTTP, el manejo de serialización y la seguridad (gating). Asimismo, pruebas de aceptación E2E del frontend Vue conectadas al backend simulando flujos completos.

## 8. Resolución de Problemas
El procedimiento institucional del Equipo 11 para la gestión de defectos es:
1. **Reporte**: Todo hallazgo o vulnerabilidad detectada se documenta como un *Issue* en GitHub bajo la etiqueta `tipo:defecto` o `tipo:hallazgo`.
2. **Clasificación**: Se asigna severidad (Alta/Media/Baja) y rol correspondiente, moviéndose a la columna "Abierto" en el tablero Kanban (GitHub Projects v2).
3. **Tratamiento**: Si el hallazgo afecta al ecosistema SQA, se resuelve mediante un *Pull Request* que requiere un Peer-Review normado antes de integrarse. Si el defecto pertenece al SUT, la incidencia documentada y categorizada es escalada al Equipo 58-1 para su remediación externa.
4. **Cierre**: El Líder General o el responsable del Issue valida la corrección o finalización del informe, pasando el ticket al estado "Cerrado".

## 9. Registros de Calidad

### 9.1 Métricas
| Fecha | Métrica | Resultado | Observaciones |
|---|---|---|---|
| 2026-06-02 | M-01 (DDF) Densidad de Defectos | 1.0 def/módulo | Rango Bueno. 6 hallazgos detectados en 6 módulos críticos evaluados durante el Walkthrough. |
| 2026-06-02 | Cobertura de Revisión de Código (CRC) | 100% | Meta Alcanzada. Se auditaron satisfactoriamente los 6 módulos propuestos. |
| 2026-06-02 | First Time Right (FTR) de Fiabilidad | 0% | Rango Malo. Falla estructural generalizada; ningún módulo revisado estuvo libre de defectos de diseño de fiabilidad. |

### 9.2 Revisiones
| Fecha | Participantes | Artefacto | Observaciones | Acuerdos |
|---|---|---|---|---|
| 2026-07-12 | Oscar Jaramillo, Alberto Rodriguez | PAC, Tooling de Pruebas Dinámicas | Se discutió el desvío de uso de Postman para el nivel de sistema. | Se aprueba usar MockMvc en el CI en lugar de RestAssured/Postman. Desvío documentado. |
| 2026-07-13 | Equipo 11 | Dashboard SQA y Generación de Docs | El sitio publicado necesitaba un renderizador Markdown en Python. | Se aprueba la inserción de dependencia de runtime `markdown` controlada; registrado como dispensa formal. |

### 9.3 Walkthrough
| Fecha | Participantes | Artefacto | Observaciones | Acuerdos |
|---|---|---|---|---|
| 2026-06-02 | Autores (Eq. 58-1), Moderador (A. Rodriguez), Escriba (S. Artiles), Revisores (E. Li, D. Cohen, O. Jaramillo) | Código Fuente Backend y Frontend (6 Módulos críticos) | Se evidenció una falla estructural en Tolerancia a Fallos (catch genéricos, ausencia de `@ControllerAdvice`, frontend sin manejo asíncrono) y en Capacidad de Recuperación (carencia de `@Transactional` en flujos de negocio y HikariCP sin configuración). | Documentar los 6 hallazgos mayores (WT-01 a WT-06) en los Issues y escalar el informe con veredicto FAIL al Equipo 58-1. No se efectuarán correcciones de código por parte de SQA (Código congelado). |

### 9.4 Análisis de los RNF
| N | Especificación del RNF | Diagrama que especifica su diseño | Elementos que especifican su diseño | Descripción-Observaciones |
|---|---|---|---|---|
| 1 | El sistema debe interceptar errores lógicos sin exponer stacktraces en las respuestas HTTP (Tolerancia a fallos). | Diagrama de Arquitectura de API REST | `@RestControllerAdvice`, Excepciones Propias | Actualmente no implementado en el SUT. Verificado en revisión estática (WT-02) y probado con JSON malformados en dinámicas. |
| 2 | El sistema debe mantener consistencia de la base de datos si ocurre un error a la mitad de una transacción de préstamo (Capacidad de Recuperación). | Diagrama de Clases / Diagrama de Secuencia | Capa Service, anotaciones `@Transactional` | Parcialmente ausente. Registrado en WT-04. Evidenciado mediante pruebas dinámicas de caja gris que generan "huérfanos". |

### 9.5 Informes de Pruebas
**Informe 1: Pruebas Estáticas (Auditoría y Walkthrough Técnico)**
Durante la auditoría asistida y el walkthrough guiado por el equipo desarrollador se examinaron 6 módulos centrales del sistema enfocados en Fiabilidad. La revisión concluyó que la tolerancia a fallos y la capacidad de recuperación no fueron tomadas en cuenta a nivel de diseño arquitectónico. El sistema es vulnerable a excepciones no controladas por entradas incorrectas y permite mutaciones de persistencia fragmentadas. Esto resultó en una métrica *First Time Right* del 0% y una *Densidad de Defectos* de 1.0 por módulo, diagnosticando una deuda técnica temprana que fue notificada inmediatamente.

**Informe 2: Pruebas Dinámicas y Automatización**
Se diseñó y ejecutó una suite robusta de pruebas dividida en ambientes de "regresión" y "defecto-conocido". Al ser ejecutadas en los niveles Unitario, Integración y Sistema (Caja Blanca, Gris y Negra), las pruebas reconfirmaron los hallazgos estáticos con evidencia empírica: el sistema devuelve errores HTTP 500 frente a fallas transaccionales y de red, sin proteger el estado del inventario. Adicionalmente, el pipeline CI implementado en GitHub Actions superó con éxito las barreras automáticas midiendo coberturas de JaCoCo, consolidando el aseguramiento total de la característica.
