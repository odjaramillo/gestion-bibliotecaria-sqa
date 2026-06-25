# IEEE Std 730-2014 — Referencia estructural para el PACS

> **Aviso importante:** Este archivo NO contiene el texto del estándar IEEE 730-2014.
> Es solo una referencia estructural (citas + índice + mapeo a nuestras secciones) para
> trazabilidad del PACS formal consolidado del Equipo 58-1.
>
> El texto completo del estándar (8857 líneas) se mantiene como referencia local fuera
> del repositorio y NO se commitea por motivos de licencia/copyright. El equipo de SQA
> puede consultarlo en su copia personal cuando lo requiera.
>
> **Copia local de referencia:** `sqa/referencias/IEEE 730/730.md` (no trackeada en git).
> **Citación estándar:**
> IEEE Std 730™-2014 (Revision of IEEE Std 730-2002), *IEEE Standard for Software Quality
> Assurance Processes*. IEEE Computer Society / Software & Systems Engineering Standards
> Committee. Approved 27 March 2014. Published 13 June 2014. ISBN 978-0-7381-9168-3.

---

## 1. Por qué este estándar es nuestro ancla estructural

El enunciado de **Fase 1** establece: *"El PACS debe estar alineado con estándares
internacionales como… IEEE 730"*. El enunciado de **Fase 2** lo ratifica.

Conforme a IEEE 730-2014 §1.5.2: *"Conformance to this standard is achieved by
demonstrating that the requirements of Clause 5, indicated by the use of 'shall', are
satisfied."* → La conformidad con IEEE 730 exige cumplir **Clause 5** (SQA process).
**Annex C** (informativo) provee la guía para crear el SQAP que Clause 5 requiere.

## 2. Índice del estándar (resumen de cláusulas y anexos)

| Sección | Título | Tipo | Relevante para nosotros |
|---|---|---|---|
| 1 | Overview (scope, purpose, conformance) | Normativo | Bajo |
| 2 | Normative references | Normativo | Bajo (referencia) |
| 3 | Definitions, acronyms, abbreviations | Normativo | Medio (glosario) |
| 4 | Key concepts of SQA | Normativo | Bajo (contexto) |
| **5** | **SQA process** | **Normativo (shall)** | **CRÍTICO — el SQAP debe cumplir esto** |
| A | Mapping a ISO/IEC/IEEE 12207:2008 | Informativo | Medio |
| B | Mapping IEEE 730-2002 ↔ 2014 | Informativo | Bajo |
| **C** | **Guidance for creating SQA Plans** | **Informativo** | **CRÍTICO — guía práctica del SQAP** |
| D | Mapping a ISO/IEC 15504 (SPICE) | Informativo | Bajo |
| E | Industry-specific guidance | Informativo | N/A |
| F | Agile | Informativo | Bajo |
| G | ISO/IEC 29110 (VSE) | Informativo | N/A |
| H | Tool validation | Informativo | Bajo |
| I | Risk assessment / software integrity levels | Informativo | Medio |
| J | Corrective/preventive action | Informativo | Medio |
| K | Cross-reference | Informativo | Bajo |
| L | Bibliography | Informativo | Bajo |

## 3. Clause 5 (SQAP Outline) — la estructura mandatoria

Conforme a Figure 5 de IEEE 730-2014, todo SQAP/PACS conforme debe tener estas
secciones en este orden:

1. **Purpose and scope**
2. **Definitions and acronyms**
3. **Reference documents**
4. **SQA plan overview**
   - 4.1 Organization and independence
   - 4.2 Software product risk
   - 4.3 Tools
   - 4.4 Standards, practices, and conventions
   - 4.5 Effort, resources, and schedule
5. **Activities, outcomes, and tasks**
   - 5.1 Product assurance
   - 5.2 Process assurance
6. **Additional considerations**
   - 6.1 Contract review
   - 6.2 Quality measurement
   - 6.3 Waivers and deviations
   - 6.4 Task repetition
   - 6.5 Risk to performing SQA
   - 6.6 Communications strategy
   - 6.7 Non-conformance process
7. **SQA records**
   - 7.1 Analyze, identify, collect, file, maintain and dispose
   - 7.2 Availability of records

## 4. Mapeo tentativo PACS del Equipo 58-1 → IEEE 730

(Este mapeo se ajustará en el ciclo sdd-new del PACS formal consolidado. Se publica
acá como punto de partida para que cualquier reviewer pueda verificar conformidad.)

| Sección IEEE 730 | Sección propuesta para nuestro PACS | Estado |
|---|---|---|
| 1. Purpose and scope | §1 Propósito y alcance | Pendiente |
| 2. Definitions and acronyms | §2 Definiciones y acrónimos (referenciar `sqa/referencias/objetivos.txt` y glosario SQA) | Pendiente |
| 3. Reference documents | §3 Documentos de referencia (ERS, DAS, IEEE 730, ISO/IEC 25010, 29119-3, 12207, 42010) | Pendiente |
| 4.1 Organization and independence | §4.1 Organización del equipo y roles (mapeo a etiquetas `rol:*` ya operativas) | Pendiente |
| 4.2 Software product risk | §4.2 Riesgos (riesgos de producto + riesgos del SQA) | Pendiente |
| 4.3 Tools | §4.3 Herramientas (declaradas, mapeo al ecosistema GitHub-native) | Pendiente |
| 4.4 Standards, practices, conventions | §4.4 Estándares y prácticas | Pendiente |
| 4.5 Effort, resources, schedule | §4.5 Esfuerzo, recursos y cronograma | Pendiente |
| 5.1 Product assurance | §5.1 Aseguramiento de producto (técnicas estáticas + dinámicas) | Pendiente |
| 5.2 Process assurance | §5.2 Aseguramiento de proceso (peer-review IEEE 730, métricas, PACS checks) | Pendiente |
| 6.1–6.7 Additional considerations | §6 Consideraciones adicionales (contrato con Equipo 58-1, waivers, no-conformidades) | Pendiente |
| 7.1–7.2 SQA records | §7 Registros SQA (repositorio, issues, PRs, actions runs) | Pendiente |

---

*Esta referencia es parte del trabajo de consolidación del ecosistema SQA. Cualquier
modificación al mapeo se hace dentro del ciclo sdd-new del issue #6 (PACS formal
consolidado F1+F2).*
