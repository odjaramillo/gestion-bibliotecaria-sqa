# Roadmap de Mejoras Pre-Producción — SQA Workflows

**Estado:** WF1-WF4 implementados en `dry_run`. M1, M2, M3, M4 completados. M5, M6, M7 pendientes.
**Rama tracker:** `feature/sdd-workflows`
**Branch actual:** `feature/sdd-workflows-slice-4-wf4`
**Tests:** 99/99 pasando

---

## Contexto para Retomar (Lectura obligatoria en nuevo chat)

Este proyecto tiene:
- 4 workflows (WF1-WF4) implementados en Python + GitHub Actions
- Módulo de análisis visual de diagramas integrado en WF2 (`scripts/sqa_core/image_analysis.py`)
- 5 checklists JSON con 75 ítems de auditoría (71 textual + 4 visual)
- Imágenes de diagramas extraídas automáticamente de PDFs y auditadas por Gemini multimodal
- Jira idempotente: `upsert_issue()` con `external_id` evita duplicados
- Prompts few-shot para Gemini en WF1, WF2 e image_analysis (reduce falsos positivos)
- Modelo Gemini estandarizado: `gemini-3.1-flash-lite-preview`

**Regla de oro:** El código fuente del Equipo 58-1 (`src/`, `biblioteca-frontend/src/`) es INMUTABLE.

---

## Mejoras Requeridas Antes de Producción

### M1: Integrar Análisis Visual en WF2
**Prioridad:** CRÍTICA
**Por qué:** Los diagramas C4 y UML del DAS no están siendo auditados. Puede haber defectos visuales graves (componentes faltantes, flechas incorrectas, inconsistencias diagrama→código).

**Qué hay que hacer:**
1. Extender `scripts/wf2_inspeccion_arquitectura.py` para:
   - Detectar imágenes extraídas de PDFs en `tmp_pdf_images/` o `sqa/extracted_images/`
   - Clasificar cada imagen por tipo de diagrama (C4 Context/Container/Component, UML)
   - Llamar a `ImageAnalyzer` para cada imagen
   - Agregar hallazgos visuales al `wf2_summary.json`
2. Agregar tests para la integración visual en WF2
3. Actualizar `.github/workflows/wf2_inspeccion_arquitectura.yml` para extraer imágenes de PDFs en CI (usar PyMuPDF o pdf2image)

**Archivos a tocar:**
- `scripts/wf2_inspeccion_arquitectura.py`
- `tests/scripts/test_wf2_inspeccion_arquitectura.py`
- `.github/workflows/wf2_inspeccion_arquitectura.yml`
- `scripts/sqa_core/pdf_text.py` (posiblemente agregar extracción de imágenes)

---

### M2: Idempotencia en Jira/Confluence
**Prioridad:** ALTA
**Por qué:** Si ejecutás WF1/WF2 dos veces, se duplican tickets. En producción esto es un desastre.

**Qué hay que hacer:**
1. En `scripts/sqa_core/clients.py` (JiraClient):
   - Antes de crear un issue, buscar si ya existe uno con el mismo `summary` o una etiqueta personalizada (ej. `checklist-id: ERS-02`)
   - Si existe, actualizarlo en lugar de crear uno nuevo
2. En ConfluenceClient:
   - Usar el título de la página como clave única
   - Si la página ya existe, actualizar su contenido
3. Agregar campo `external_id` a los issues de Jira que sea determinista: `SQA-{artifact}-{checklist_id}`

**Archivos a tocar:**
- `scripts/sqa_core/clients.py`
- `scripts/wf1_auditoria_requisitos.py`
- `scripts/wf2_inspeccion_arquitectura.py`
- Tests correspondientes

---

### M3: Extracción Automática de Imágenes de PDFs
**Prioridad:** ALTA (bloquea M1)
**Por qué:** Ahora las imágenes están en `tmp_pdf_images/` (extraídas manualmente). En CI no hay imágenes.

**Qué hay que hacer:**
1. Crear función `extract_images_from_pdf(pdf_path, output_dir)` en `scripts/sqa_core/pdf_text.py`
2. Usar `PyMuPDF` (fitz) para iterar páginas y extraer imágenes incrustadas
3. Guardar imágenes en `sqa/extracted_images/{pdf_name}_page{N}_img{M}.png`
4. Agregar tests

**Archivos a tocar:**
- `scripts/sqa_core/pdf_text.py`
- `tests/scripts/test_sqa_core_pdf_text.py`
- `requirements.txt` (asegurar que PyMuPDF esté)

---

### M4: Mejorar Prompts de Gemini con Few-Shot
**Prioridad:** MEDIA
**Por qué:** Los prompts actuales pueden generar falsos positivos. Ejemplos concretos de "buen" vs "mal" hallazgo mejoran la precisión.

**Qué hay que hacer:**
1. En `scripts/sqa_core/image_analysis.py`, agregar ejemplos de few-shot a los prompts
2. En `scripts/wf1_auditoria_requisitos.py`, agregar ejemplos de hallazgos reales vs. falsos positivos
3. Documentar la tasa de precisión (cuántos hallazgos de la IA son reales después de validación humana)

**Archivos a tocar:**
- `scripts/sqa_core/image_analysis.py`
- `scripts/wf1_auditoria_requisitos.py`
- `scripts/wf2_inspeccion_arquitectura.py`

---

### M5: Cobertura de Auditoría
**Prioridad:** MEDIA
**Por qué:** No sabemos qué % de cada artefacto está siendo auditado.

**Qué hay que hacer:**
1. En `scripts/wf4_orquestador.py`, agregar métrica de cobertura:
   - Páginas auditadas / páginas totales del PDF
   - Ítems verificados / ítems totales de la checklist
   - Imágenes auditadas / imágenes totales
2. Incluir en el reporte Markdown: *"Cobertura de auditoría: X% del artefacto fue verificado"*

**Archivos a tocar:**
- `scripts/wf4_orquestador.py`
- `scripts/sqa_core/reporting.py`

---

### M6: Cleanup y Remover POC Obsoleto
**Prioridad:** BAJA
**Por qué:** `scripts/agente_sqa.py` es un POC que ya no se usa. WF1 lo reemplaza formalmente.

**Qué hay que hacer:**
1. Mover `scripts/agente_sqa.py` a `scripts/legacy/` o eliminarlo
2. Actualizar `.github/workflows/auditoria_sqa.yml` para que use WF1 en lugar del agente legacy
3. O simplemente eliminar el workflow legacy

**Archivos a tocar:**
- `scripts/agente_sqa.py`
- `.github/workflows/auditoria_sqa.yml`

---

### M7: Generación Semi-Automatizada del PAC
**Prioridad:** MEDIA (post-producción)
**Por qué:** El PAC se escribe manualmente siguiendo IEEE 730-2014. Es repetitivo, propenso a olvidar secciones, y las herramientas/métricas dependen del stack del SUT. Semi-automatizarlo reduce errores y acelera el inicio de nuevos proyectos SQA.

**Qué hay que hacer:**
1. Crear `scripts/wf_pac_generator.py` que:
   - Tome como input: stack del SUT, artefactos a auditar, estándar deseado (IEEE 730)
   - Genere la estructura base del PAC con todas las secciones obligatorias
   - Sugiera métricas estándar (Densidad de Defectos, Cobertura, Deuda Técnica) con fórmulas y fuentes de datos
   - Sugiera herramientas según el stack (ej: Java+Spring → SonarQube, JaCoCo, RestAssured)
   - Genere checklists base a partir de estándares ISO/IEEE
2. Crear `scripts/wf_pac_auditor.py` que valide un PAC existente:
   - Verifique que todas las secciones IEEE 730 estén presentes
   - Valide que cada métrica tenga fórmula + responsable
   - Verifique que herramientas declaradas estén en requirements.txt
   - Genere un reporte de madurez del PAC
3. Integrar como WF_PAC en el ecosistema SQA

**Qué NO se puede automatizar (requiere humano):**
- Objetivos de calidad (prioridades de negocio)
- Roles y responsabilidades del equipo
- Aceptación de riesgos
- Umbral de calidad (% de cobertura aceptable)

**Archivos a tocar:**
- `scripts/wf_pac_generator.py` (nuevo)
- `scripts/wf_pac_auditor.py` (nuevo)
- `sqa/PACS-Fase2-Herramientas.md` (actualizar como output del generador)
- `tests/scripts/test_wf_pac_generator.py` (nuevo)
- `tests/scripts/test_wf_pac_auditor.py` (nuevo)

**Nota:** M7 es una mejora de metodología, no bloquea producción. Se puede trabajar después de activar DRY_RUN=false.

---

## Orden Sugerido de Implementación

```
M3 (Extracción de imágenes) ─┬─> M1 (Análisis visual en WF2) ─┐
                              │                                │
M2 (Idempotencia) ────────────┼────────────────────────────────┼─> Producción
                              │                                │
M4 (Mejorar prompts) ─────────┘                                │
                                                               │
M5 (Cobertura) ────────────────────────────────────────────────┘

M6 (Cleanup) ───> Puede hacerse en cualquier momento

M7 (PAC semi-automatizado) ───> Post-producción / mejora de metodología
```

**Secuencia recomendada:**
1. ✅ M3 + M1 juntos (son dependientes) — COMPLETADOS
2. ✅ M2 (idempotencia — crítico para no romper Jira) — COMPLETADO
3. ✅ M4 (mejorar prompts) — COMPLETADO
4. M5 (cobertura de auditoría) — PENDIENTE: esperando definición del líder de métricas
5. M6 (limpieza legacy) — PENDIENTE
6. **Activar producción**
7. M7 (PAC semi-automatizado) — PENDIENTE: post-producción, mejora de metodología

---

## Comandos para Retomar en Nuevo Chat

Cuando abras un chat nuevo, copiá y pegá esto:

```
Retomemos el proyecto gestion-bibliotecaria-sqa.

ESTADO ACTUAL (2026-05-06):
- M1 (Análisis visual en WF2): ✅ COMPLETADO — 86 tests
- M2 (Idempotencia Jira): ✅ COMPLETADO — 32 tests
- M3 (Extracción de imágenes): ✅ COMPLETADO — integrado en M1
- M4 (Few-shot prompts): ✅ COMPLETADO — 99 tests
- M5 (Cobertura métricas): 🔲 PENDIENTE — esperando definición del líder de métricas
- M6 (Cleanup legacy): 🔲 PENDIENTE
- M7 (PAC semi-automatizado): 🔲 PENDIENTE — idea guardada, no iniciada

Total tests: 99/99 pasando
Rama: feature/sdd-workflows-slice-4-wf4
Documentos para el líder: actualizados y listos (INFORME-APROBACION, Checklists, PACS)

Quiero trabajar en: [M5, M6, M7, o activar producción]
```

El agente debería:
1. Buscar en Engram el estado de los slices completados (`sdd/mejoras-pre-produccion-*/archive-report`)
2. Verificar la rama actual (`feature/sdd-workflows-slice-4-wf4`)
3. Confirmar que hay 99 tests pasando (`python3 -m unittest discover -s tests/scripts -v`)
4. Implementar lo que pidas en el orden correcto

---

## Estado de los Secrets (para configurar antes de producción)

| Secret | Para qué workflow | Estado |
|---|---|---|
| `JIRA_SERVER` | Todos | Pendiente |
| `JIRA_EMAIL` | Todos | Pendiente |
| `JIRA_API_TOKEN` | Todos | Pendiente |
| `CONFLUENCE_URL` | Todos | Pendiente |
| `CONFLUENCE_USER` | Todos | Pendiente |
| `CONFLUENCE_TOKEN` | Todos | Pendiente |
| `GEMINI_API_KEY` | Todos | Pendiente |
| `SONARQUBE_URL` | WF2 | Pendiente |
| `SONARQUBE_TOKEN` | WF2 | Pendiente |
| `GITHUB_TOKEN` | WF3 | Ya disponible en Actions |

---

## Notas Técnicas para el Próximo Agent

- **Tests:** Usar `python3 -m unittest discover -s tests/scripts -v`
- **Branch:** Crear nueva rama desde `feature/sdd-workflows-slice-4-wf4`
- **Commits:** Work-unit commits (código + tests juntos)
- **Modelo Gemini:** `gemini-3.1-flash-lite-preview` (ya configurado en `sqa_core/clients.py`)
- **Dry run:** Mantener `DRY_RUN=true` hasta que TODAS las mejoras estén listas
- **Idioma:** Código y comentarios en español (convención del proyecto)

---

*Documento actualizado el 2026-05-06 por el Equipo SQA 11*
*Último commit: `d5181d4` — docs(sqa): reescribe documentos como primera presentacion al lider*
*Rama: `feature/sdd-workflows-slice-4-wf4`*
*Slices completados: M1, M2, M3, M4 | Pendientes: M5, M6, M7*
