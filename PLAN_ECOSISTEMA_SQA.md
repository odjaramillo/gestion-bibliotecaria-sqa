# Plan de Implementación: Ecosistema SQA en GitHub

**Proyecto:** Sistema de Gestión Bibliotecaria — Equipo 58-1  
**Rol responsable:** Líder Tecnológico (Fase 1) / DevOps (Fase 2)  
**Fecha:** 2026-06-22  
**Referencia normativa:** IEEE 730, ISO/IEC 12207, ISO/IEC 25010, ISO/IEC/IEEE 29148, ISO/IEC/IEEE 42010

---

## 1. Estructura de archivos a crear

```
.
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── hallazgo-inspeccion.md       ← Fase 1: técnicas estáticas
│   │   ├── defecto-prueba.md            ← Fase 2: técnicas dinámicas
│   │   └── item-auditoria.md            ← Ambas fases: auditoría formal
│   ├── workflows/
│   │   ├── sync-labels.yml              ← Sincroniza labels.yml → GitHub
│   │   ├── pr-project.yml               ← Auto-add board + auto-label + sync estado
│   │   ├── ci-static.yml                ← Análisis estático (Checkstyle + SpotBugs + PMD + SonarCloud)
│   │   └── ci-tests.yml                 ← Pruebas dinámicas + JaCoCo (Fase 2)
│   ├── labels.yml                       ← Taxonomía canónica de etiquetas
│   └── PULL_REQUEST_TEMPLATE.md         ← Template PR como evidencia de revisión por pares
├── sonar-project.properties             ← Configuración SonarCloud
└── pom.xml                              ← Agregar JaCoCo + H2 + plugins de análisis (ver Sección 6)
```

---

## 2. Taxonomía de etiquetas — `.github/labels.yml`

Este archivo es la **fuente única de verdad** para todas las etiquetas del repositorio.  
Sincronizar con: `gh label sync -f .github/labels.yml`

```yaml
# ─────────────────────────────────────────────────────────────
# tipo:*  — naturaleza del ítem registrado
# ─────────────────────────────────────────────────────────────
- name: tipo:hallazgo
  color: 'e4e669'
  description: 'Hallazgo de técnica estática (inspección, walkthrough)'

- name: tipo:defecto
  color: 'd93f0b'
  description: 'Defecto encontrado mediante técnica dinámica (prueba)'

- name: tipo:no-conformidad
  color: 'b60205'
  description: 'No conformidad identificada en auditoría formal'

- name: tipo:tarea
  color: '0075ca'
  description: 'Tarea interna del proceso SQA (planificación, coordinación)'

- name: tipo:walkthrough
  color: 'cfd3d7'
  description: 'Ítem derivado de una sesión de walkthrough formal'

# ─────────────────────────────────────────────────────────────
# area:*  — artefacto o capa del sistema afectada
# ─────────────────────────────────────────────────────────────
- name: area:requisitos
  color: '0e8a86'
  description: 'ERS — Especificación de Requisitos de Software'

- name: area:arquitectura
  color: '0e8a86'
  description: 'DAS — Documento de Arquitectura de Software'

- name: area:codigo
  color: '0e8a86'
  description: 'Código fuente (backend Java / frontend Vue)'

- name: area:pruebas
  color: '0e8a86'
  description: 'Plan de pruebas, casos de prueba, resultados'

- name: area:proceso
  color: '0e8a86'
  description: 'Proceso SQA, PACS, métricas, gestión del equipo'

# ─────────────────────────────────────────────────────────────
# severidad:*  — impacto del hallazgo o defecto
# ─────────────────────────────────────────────────────────────
- name: severidad:critica
  color: 'b60205'
  description: 'Crítica — compromete la integridad del sistema o proceso'

- name: severidad:mayor
  color: 'd93f0b'
  description: 'Mayor — afecta funcionalidad o calidad de manera significativa'

- name: severidad:menor
  color: 'fbca04'
  description: 'Menor — afecta calidad de forma parcial, con solución alternativa'

- name: severidad:observacion
  color: 'c2e0c6'
  description: 'Observación — mejora recomendada sin impacto directo'

# ─────────────────────────────────────────────────────────────
# estado:*  — ciclo de vida del ítem
# ─────────────────────────────────────────────────────────────
- name: estado:abierto
  color: 'fef2c0'
  description: 'Registrado, pendiente de análisis'

- name: estado:en-analisis
  color: 'fbca04'
  description: 'En revisión o análisis por el equipo'

- name: estado:confirmado
  color: 'e4e669'
  description: 'Confirmado como hallazgo o defecto válido'

- name: estado:cerrado
  color: '0e8a86'
  description: 'Resuelto, documentado y aceptado'

- name: estado:falso-positivo
  color: 'cfd3d7'
  description: 'Descartado tras análisis — no es un defecto real'

# ─────────────────────────────────────────────────────────────
# rol:*  — responsable o quien registró el ítem
# ─────────────────────────────────────────────────────────────
- name: rol:lider-gral
  color: '5319e7'
  description: 'Líder General — coordinación y plan de aseguramiento'

- name: rol:lider-tec
  color: '5319e7'
  description: 'Líder Tecnológico — ecosistema tecnológico e integración'

- name: rol:tester
  color: '5319e7'
  description: 'Analista de Pruebas / Tester — diseño y ejecución de pruebas'

- name: rol:metricas
  color: '5319e7'
  description: 'Líder de Métricas — KPIs, dashboards y control estadístico'

- name: rol:escriba
  color: '5319e7'
  description: 'Escriba — documentación, auditoría y trazabilidad documental'

# ─────────────────────────────────────────────────────────────
# fase:*  — fase del proyecto en que se originó el ítem
# ─────────────────────────────────────────────────────────────
- name: fase:fase-1
  color: '1d76db'
  description: 'Fase 1 — Técnicas estáticas (inspección, walkthrough, auditoría)'

- name: fase:fase-2
  color: '0052cc'
  description: 'Fase 2 — Técnicas dinámicas (pruebas unitarias, integración, sistema, aceptación)'

# ─────────────────────────────────────────────────────────────
# iso:*  — característica ISO/IEC 25010 afectada
#          Elegir 1-2 características como foco del equipo.
#          Tener todas disponibles facilita el filtrado al Líder de Métricas.
# ─────────────────────────────────────────────────────────────
- name: iso:funcionalidad
  color: 'bfd4f2'
  description: 'ISO 25010 — Adecuación funcional'

- name: iso:confiabilidad
  color: 'bfd4f2'
  description: 'ISO 25010 — Fiabilidad / Confiabilidad'

- name: iso:usabilidad
  color: 'bfd4f2'
  description: 'ISO 25010 — Usabilidad'

- name: iso:eficiencia
  color: 'bfd4f2'
  description: 'ISO 25010 — Eficiencia de desempeño'

- name: iso:mantenibilidad
  color: 'bfd4f2'
  description: 'ISO 25010 — Mantenibilidad'

- name: iso:seguridad
  color: 'bfd4f2'
  description: 'ISO 25010 — Seguridad'

- name: iso:compatibilidad
  color: 'bfd4f2'
  description: 'ISO 25010 — Compatibilidad'

- name: iso:portabilidad
  color: 'bfd4f2'
  description: 'ISO 25010 — Portabilidad'
```

---

## 3. Plantillas de issues

### 3.1 `.github/ISSUE_TEMPLATE/hallazgo-inspeccion.md`

```markdown
---
name: Hallazgo de Inspección / Walkthrough
about: Registrar un hallazgo encontrado mediante técnica estática (Fase 1)
title: '[HALLAZGO] '
labels:
  - 'tipo:hallazgo'
  - 'fase:fase-1'
  - 'estado:abierto'
assignees: []
---

<!--
Completar TODOS los campos marcados como OBLIGATORIO.
La trazabilidad hacia ERS o DAS es un requisito de la ISO/IEC 12207.
No cerrar este issue sin confirmar el campo "Referencia exacta".
-->

## Técnica aplicada

<!--
OBLIGATORIO. Marcar solo una.
-->

- [ ] Inspección formal
- [ ] Walkthrough
- [ ] Revisión técnica
- [ ] Auditoría de producto

---

## Documento / Artefacto revisado

<!--
OBLIGATORIO. Marcar el artefacto fuente del hallazgo.
-->

- [ ] ERS — Especificación de Requisitos de Software
- [ ] DAS — Documento de Arquitectura de Software
- [ ] Diagrama UML (clases, secuencia, despliegue)
- [ ] Código fuente

---

## Referencia exacta

<!--
OBLIGATORIO. Identificador preciso dentro del documento.
Ejemplos: "ERS-RF-012", "DAS Sección 3.2 — Capa de Servicio", "Página 8, párrafo 2"
Sin este campo no hay trazabilidad bidireccional (ISO 12207).
-->

**Identificador de requisito / componente:** <!-- ERS-XXX / DAS-XXX -->  
**Sección / página:** <!-- ej. Sección 4.1, página 12 -->  
**Versión del documento:** <!-- ej. ERS v1.2 -->

---

## Componente de arquitectura afectado

<!--
OPCIONAL si el hallazgo es en ERS. OBLIGATORIO si es en DAS o código.
Identificar la capa o componente según el DAS (ej. "Capa de Repositorio", "Controlador REST /prestamos").
-->

---

## Descripción del hallazgo

<!--
OBLIGATORIO. Describir con precisión qué está mal, incompleto o ambiguo.
-->

---

## Evidencia — cita literal

<!--
OBLIGATORIO. Transcribir el fragmento exacto del documento que sustenta el hallazgo.
Si es código, incluir el fragmento con su ruta de archivo y número de línea.
-->

```
<!-- Pegar aquí la cita literal o el fragmento de código -->
```

---

## Severidad

<!--
OBLIGATORIO. Marcar solo una. Actualizar la etiqueta del issue con el valor elegido.
-->

- [ ] `severidad:critica` — Compromete la integridad del sistema o proceso
- [ ] `severidad:mayor` — Afecta funcionalidad de manera significativa
- [ ] `severidad:menor` — Afecta calidad parcialmente, existe alternativa
- [ ] `severidad:observacion` — Mejora recomendada, sin impacto directo

---

## Característica ISO/IEC 25010 afectada

<!--
OBLIGATORIO. Marcar la característica principal. Actualizar la etiqueta iso:* del issue.
-->

- [ ] `iso:funcionalidad`
- [ ] `iso:confiabilidad`
- [ ] `iso:usabilidad`
- [ ] `iso:eficiencia`
- [ ] `iso:mantenibilidad`
- [ ] `iso:seguridad`
- [ ] `iso:compatibilidad`
- [ ] `iso:portabilidad`

---

## Propuesta de corrección

<!--
OBLIGATORIO. Indicar qué debería corregirse en el artefacto original.
Ser específico: qué sección, qué texto nuevo, qué criterio de aceptación.
-->

---

## Área

<!--
OBLIGATORIO. Actualizar la etiqueta area:* del issue.
-->

- [ ] `area:requisitos`
- [ ] `area:arquitectura`
- [ ] `area:codigo`
- [ ] `area:proceso`

---

## Rol que registra

<!--
OBLIGATORIO. Actualizar la etiqueta rol:* del issue.
-->

- [ ] `rol:lider-gral`
- [ ] `rol:lider-tec`
- [ ] `rol:tester`
- [ ] `rol:metricas`
- [ ] `rol:escriba`
```

---

### 3.2 `.github/ISSUE_TEMPLATE/defecto-prueba.md`

```markdown
---
name: Defecto de Prueba
about: Registrar un defecto encontrado mediante técnica dinámica (Fase 2)
title: '[DEFECTO] '
labels:
  - 'tipo:defecto'
  - 'fase:fase-2'
  - 'estado:abierto'
assignees: []
---

<!--
Completar TODOS los campos marcados como OBLIGATORIO.
El campo "Referencia ERS" es trazabilidad mandatoria según ISO 12207.
-->

## Nivel de prueba

<!--
OBLIGATORIO. Marcar solo uno.
-->

- [ ] Unitaria
- [ ] Integración
- [ ] Sistema
- [ ] Aceptación

---

## Enfoque de prueba

<!--
OBLIGATORIO. Marcar solo uno.
-->

- [ ] Caja blanca (basada en estructura interna)
- [ ] Caja negra (basada en especificación de requisitos)
- [ ] Caja gris (combinación de ambas)

---

## Identificador del caso de prueba

<!--
OBLIGATORIO. ID asignado en el Plan de Pruebas.
Ejemplo: CP-001, TC-AUTH-03
-->

**ID caso de prueba:** <!-- CP-XXX -->

---

## Componente / Clase afectada

<!--
OBLIGATORIO. Clase Java, endpoint REST o componente Vue donde se manifiesta el defecto.
Ejemplo: "LibroService.java — método buscarPorIsbn()", "GET /api/libros/isbn/{isbn}"
-->

**Archivo / clase:** <!-- ruta relativa -->  
**Método / endpoint:** <!-- nombre exacto -->  
**Línea aproximada:** <!-- número de línea si aplica -->

---

## Referencia ERS

<!--
OBLIGATORIO. Trazabilidad hacia el requisito que la prueba verifica.
Sin este campo la trazabilidad bidireccional exigida por ISO 12207 está incompleta.
-->

**Identificador ERS:** <!-- ERS-RF-XXX -->  
**Descripción del requisito:** <!-- Breve paráfrasis del requisito -->

---

## Pasos para reproducir

<!--
OBLIGATORIO. Secuencia numerada, precisa y reproducible.
-->

1. 
2. 
3. 

---

## Comportamiento esperado

<!--
OBLIGATORIO. Qué debería ocurrir según ERS o el plan de pruebas.
-->

---

## Comportamiento actual (defecto)

<!--
OBLIGATORIO. Qué ocurrió realmente. Incluir stacktrace, respuesta HTTP o salida de consola.
-->

```
<!-- Pegar aquí la salida, error o log -->
```

---

## Severidad

<!--
OBLIGATORIO. Marcar solo una. Actualizar etiqueta severidad:* del issue.
-->

- [ ] `severidad:critica`
- [ ] `severidad:mayor`
- [ ] `severidad:menor`
- [ ] `severidad:observacion`

---

## Característica ISO/IEC 25010 afectada

<!--
OBLIGATORIO. Marcar la característica que este defecto viola.
-->

- [ ] `iso:funcionalidad`
- [ ] `iso:confiabilidad`
- [ ] `iso:usabilidad`
- [ ] `iso:eficiencia`
- [ ] `iso:mantenibilidad`
- [ ] `iso:seguridad`
- [ ] `iso:compatibilidad`
- [ ] `iso:portabilidad`

---

## Evidencia adjunta

<!--
Adjuntar capturas de pantalla, logs de ejecución, o reporte JUnit/Surefire.
Si el pipeline de CI detectó este defecto, enlazar el run de GitHub Actions.
-->

**Run de CI (si aplica):** <!-- URL del workflow run -->

---

## Rol que registra

- [ ] `rol:lider-gral`
- [ ] `rol:lider-tec`
- [ ] `rol:tester`
- [ ] `rol:metricas`
- [ ] `rol:escriba`
```

---

### 3.3 `.github/ISSUE_TEMPLATE/item-auditoria.md`

```markdown
---
name: Ítem de Auditoría
about: Registrar una no conformidad o hallazgo de auditoría formal (IEEE 730)
title: '[AUDITORÍA] '
labels:
  - 'tipo:no-conformidad'
  - 'estado:abierto'
assignees: []
---

<!--
Completar TODOS los campos marcados como OBLIGATORIO.
Este template soporta auditorías de proceso y de producto.
Referencia: IEEE 730 — Software Quality Assurance Plans.
-->

## Tipo de auditoría

<!--
OBLIGATORIO. Marcar solo uno.
-->

- [ ] Auditoría de producto (evalúa artefactos: ERS, DAS, código)
- [ ] Auditoría de proceso (evalúa el seguimiento del PACS)

---

## Fase

- [ ] `fase:fase-1`
- [ ] `fase:fase-2`

---

## Estándar de referencia

<!--
OBLIGATORIO. Indicar el estándar cuyo criterio fue evaluado.
-->

- [ ] IEEE 730 — Plan de Aseguramiento de la Calidad del Software
- [ ] ISO/IEC 12207 — Procesos del ciclo de vida del software
- [ ] ISO/IEC/IEEE 29148 — Requisitos de sistemas y software
- [ ] ISO/IEC 25010 — Modelo de calidad del producto software
- [ ] ISO/IEC/IEEE 42010 — Descripción de arquitectura
- [ ] Otro: <!-- especificar -->

---

## Criterio auditado

<!--
OBLIGATORIO. Qué criterio, cláusula o sección del estándar se evaluó.
Ejemplo: "IEEE 730 §4.3 — El PACS debe identificar métricas de calidad aplicables"
-->

**Cláusula / sección:** <!-- ej. IEEE 730 §4.3 -->  
**Descripción del criterio:** <!-- paráfrasis del criterio -->

---

## Evidencia encontrada

<!--
OBLIGATORIO. Qué se observó durante la auditoría. Cita o descripción objetiva.
-->

---

## No conformidad identificada

<!--
OBLIGATORIO si existe no conformidad. Si es conforme, indicar "CONFORME" y cerrar issue.
Describir con precisión la brecha entre lo observado y lo exigido por el estándar.
-->

---

## Área afectada

- [ ] `area:requisitos`
- [ ] `area:arquitectura`
- [ ] `area:codigo`
- [ ] `area:pruebas`
- [ ] `area:proceso`

---

## Severidad

- [ ] `severidad:critica`
- [ ] `severidad:mayor`
- [ ] `severidad:menor`
- [ ] `severidad:observacion`

---

## Recomendación

<!--
OBLIGATORIO. Acción correctiva específica que elimina la no conformidad.
Indicar responsable sugerido y plazo estimado.
-->

**Acción:** <!-- qué debe hacerse -->  
**Responsable sugerido:** <!-- rol -->  
**Plazo:** <!-- ej. antes de la entrega Fase 1 -->

---

## Rol auditor

- [ ] `rol:lider-gral`
- [ ] `rol:lider-tec`
- [ ] `rol:tester`
- [ ] `rol:metricas`
- [ ] `rol:escriba`
```

---

## 4. Plantilla de pull request — `.github/PULL_REQUEST_TEMPLATE.md`

```markdown
<!--
Template de PR para el repositorio SQA — Equipo 58-1.

Este PR actúa como EVIDENCIA FORMAL DE REVISIÓN POR PARES (Peer Review / Walkthrough)
conforme a IEEE 730. Completar todos los campos antes de solicitar revisión.

REGLA DE CIERRE: usar siempre la keyword en INGLÉS.
  Closes #N  /  Fixes #N  /  Resolves #N
GitHub solo auto-cierra issues con keywords en inglés.
Si no cierra un issue usar: [sin-issue]
-->

## Descripción del artefacto entregado

<!--
OBLIGATORIO. 1-3 oraciones: qué artefacto se entrega, quién lo elaboró, qué cubre.
-->

---

## Issues cerrados

<!--
OBLIGATORIO. Un issue por línea. Keyword en INGLÉS.
Si no aplica: [sin-issue]
-->

- Closes #

---

## Tipo de entrega

<!--
OBLIGATORIO. Marcar solo uno. Esto activa el auto-labeling del workflow.
-->

- [ ] `informe-inspeccion`
- [ ] `plan-pruebas`
- [ ] `lista-chequeo`
- [ ] `pacs`
- [ ] `informe-auditoria`
- [ ] `evidencia-pruebas`
- [ ] `metricas-dashboard`
- [ ] `otro`

---

## Fase

<!--
OBLIGATORIO. Marcar la fase correspondiente.
-->

- [ ] `fase:fase-1`
- [ ] `fase:fase-2`

---

## Rol responsable del artefacto

<!--
OBLIGATORIO. Quien elaboró el artefacto entregado.
-->

- [ ] `rol:lider-gral`
- [ ] `rol:lider-tec`
- [ ] `rol:tester`
- [ ] `rol:metricas`
- [ ] `rol:escriba`

---

## Checklist de revisión por pares (IEEE 730 — Peer Review)

<!--
OBLIGATORIO. A ser completado por el REVISOR, no por el autor.
Esta sección es la evidencia formal de que el artefacto fue revisado antes de integrarse.
-->

- [ ] El contenido del artefacto está completo según el PACS
- [ ] La trazabilidad hacia ERS / DAS está documentada (ISO 12207)
- [ ] El estándar de referencia fue aplicado correctamente
- [ ] Los hallazgos o defectos están debidamente documentados con issues vinculados
- [ ] Las métricas relevantes están incluidas o referenciadas
- [ ] El documento sigue la estructura de nomenclatura y versión acordada
- [ ] No hay inconsistencias con artefactos previos de la misma fase

---

## Evidencias adjuntas

<!--
OPCIONAL. Adjuntar o enlazar: capturas, reportes de ejecución, runs de CI.
-->

---

## Observaciones del revisor

<!--
OPCIONAL. Comentarios adicionales del par revisor que no generan un issue nuevo.
-->
```

---

## 5. Workflows de GitHub Actions

### 5.1 `.github/workflows/sync-labels.yml`

```yaml
name: Sync Labels

on:
  push:
    branches: [main, develop]
    paths:
      - '.github/labels.yml'
  workflow_dispatch:

permissions:
  contents: read

jobs:
  sync:
    name: Sync labels to GitHub
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Sync labels
        run: gh label sync -f .github/labels.yml
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

### 5.2 `.github/workflows/pr-project.yml`

```yaml
name: PR — Project Board + Auto-label + Sync Estado

# Cablea tres comportamientos automáticos sobre cada PR:
#   1. auto-add-to-project  — agrega el PR al tablero GitHub Projects v2.
#   2. auto-label-from-body — aplica etiquetas según checkboxes del PR body.
#   3. sync-estado          — mueve el PR a estado:en-analisis al abrir
#                             y a estado:cerrado al mergear.

on:
  pull_request:
    types:
      - opened
      - edited
      - synchronize
      - reopened
      - ready_for_review
      - converted_to_draft
      - closed

permissions:
  contents: read
  issues: write
  pull-requests: write

jobs:
  # ───────────────────────────────────────────────────────────
  # Job 1: Agregar al tablero Projects v2
  # ───────────────────────────────────────────────────────────
  auto-add-to-project:
    name: Agregar PR al tablero SQA
    runs-on: ubuntu-latest
    if: >
      github.event_name == 'pull_request' &&
      (github.event.action == 'opened' || github.event.action == 'reopened')
    steps:
      - name: Add to project
        uses: actions/add-to-project@v2.0.0
        with:
          # REEMPLAZAR con la URL real del Projects v2 del equipo
          # Ejemplo: https://github.com/users/USUARIO/projects/N
          project-url: https://github.com/users/REEMPLAZAR_USUARIO/projects/REEMPLAZAR_N
          github-token: ${{ secrets.PROJECT_TOKEN }}

  # ───────────────────────────────────────────────────────────
  # Job 2: Auto-label desde checkboxes del PR body
  # ───────────────────────────────────────────────────────────
  auto-label-from-body:
    name: Aplicar etiquetas desde PR body
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    steps:
      - name: Apply labels from checkboxes
        uses: actions/github-script@v7
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          script: |
            const pr = context.payload.pull_request;
            const body = (pr && pr.body) || '';

            // Mapa: texto del checkbox en el PR template → nombre real de la etiqueta
            const LABELS = {
              // Tipo de entrega
              'informe-inspeccion': 'tipo:hallazgo',
              'plan-pruebas':       'tipo:tarea',
              'lista-chequeo':      'tipo:tarea',
              'pacs':               'tipo:tarea',
              'informe-auditoria':  'tipo:no-conformidad',
              'evidencia-pruebas':  'tipo:defecto',
              'metricas-dashboard': 'tipo:tarea',
              // Fase
              'fase:fase-1': 'fase:fase-1',
              'fase:fase-2': 'fase:fase-2',
              // Rol
              'rol:lider-gral':   'rol:lider-gral',
              'rol:lider-tec':    'rol:lider-tec',
              'rol:tester':       'rol:tester',
              'rol:metricas':     'rol:metricas',
              'rol:escriba':      'rol:escriba',
            };

            const CHECKBOX_RE = /^[\s]*-\s*\[([ xX])\]\s*`?([a-zA-Z0-9_:/-]+)`?/gm;
            const labels = new Set();
            let m;
            while ((m = CHECKBOX_RE.exec(body)) !== null) {
              if (m[1].toLowerCase() !== 'x') continue;
              const key = m[2];
              if (Object.prototype.hasOwnProperty.call(LABELS, key) && LABELS[key]) {
                labels.add(LABELS[key]);
              }
            }

            if (labels.size === 0) {
              core.info('No se encontraron checkboxes marcados con etiquetas reconocidas.');
              return;
            }

            // Verificar que las etiquetas existen en el repo antes de aplicarlas
            let existing = new Set();
            try {
              const all = await github.paginate(
                github.rest.issues.listLabelsForRepo,
                { owner: context.repo.owner, repo: context.repo.repo, per_page: 100 }
              );
              existing = new Set(all.map(l => l.name));
            } catch (e) {
              core.warning(`No se pudo obtener la lista de etiquetas: ${e.message}`);
            }

            const toApply = Array.from(labels).filter(name => {
              if (existing.has(name)) return true;
              core.warning(`Etiqueta "${name}" no existe en el repo. Ejecutar sync-labels primero.`);
              return false;
            });

            for (const label of toApply) {
              try {
                await github.rest.issues.addLabels({
                  owner: context.repo.owner,
                  repo: context.repo.repo,
                  issue_number: pr.number,
                  labels: [label],
                });
                core.info(`✓ ${label}`);
              } catch (e) {
                if (e.status !== 404) throw e;
              }
            }

  # ───────────────────────────────────────────────────────────
  # Job 3: Sincronizar etiqueta de estado del PR
  # ───────────────────────────────────────────────────────────
  sync-estado:
    name: Sincronizar estado del PR
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    steps:
      - name: Sync estado label
        uses: actions/github-script@v7
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          script: |
            const STATUS_LABELS = ['estado:abierto', 'estado:en-analisis', 'estado:confirmado', 'estado:cerrado'];
            const CLOSING_REGEX = /\b(closes|fixes|resolves)\s+#(\d+)\b/gi;

            const pr = context.payload.pull_request;
            const action = context.payload.action;
            const body = (pr && pr.body) || '';
            const prNumber = pr.number;
            const isDraft = !!pr.draft;

            const labelCache = new Map();
            async function labelExists(name) {
              if (labelCache.has(name)) return labelCache.get(name);
              try {
                await github.rest.issues.getLabel({
                  owner: context.repo.owner, repo: context.repo.repo, name
                });
                labelCache.set(name, true);
                return true;
              } catch (e) {
                if (e.status === 404) { labelCache.set(name, false); return false; }
                throw e;
              }
            }

            async function setStatusLabel(issueNumber, newLabel) {
              const { data: issue } = await github.rest.issues.get({
                owner: context.repo.owner, repo: context.repo.repo, issue_number: issueNumber
              });
              const toRemove = (issue.labels || [])
                .map(l => (typeof l === 'string' ? l : l.name))
                .filter(n => n && n.startsWith('estado:'));
              for (const old of toRemove) {
                if (old !== newLabel) {
                  try {
                    await github.rest.issues.removeLabel({
                      owner: context.repo.owner, repo: context.repo.repo,
                      issue_number: issueNumber, name: old
                    });
                  } catch (e) { if (e.status !== 404) throw e; }
                }
              }
              if (newLabel) {
                if (!await labelExists(newLabel)) {
                  core.warning(`Etiqueta "${newLabel}" no existe. Ejecutar sync-labels.`);
                  return;
                }
                await github.rest.issues.addLabels({
                  owner: context.repo.owner, repo: context.repo.repo,
                  issue_number: issueNumber, labels: [newLabel]
                });
              }
            }

            function parseClosing(body) {
              const refs = []; const seen = new Set();
              CLOSING_REGEX.lastIndex = 0;
              let m;
              while ((m = CLOSING_REGEX.exec(body)) !== null) {
                const ref = `#${m[2]}`;
                if (!seen.has(ref)) { seen.add(ref); refs.push(parseInt(m[2], 10)); }
              }
              return refs;
            }

            if (['opened', 'reopened', 'ready_for_review', 'edited', 'synchronize'].includes(action)) {
              if (isDraft) {
                await setStatusLabel(prNumber, null);
                return;
              }
              await setStatusLabel(prNumber, 'estado:en-analisis');
              for (const issueNum of parseClosing(body)) {
                try { await setStatusLabel(issueNum, 'estado:en-analisis'); }
                catch (e) { if (e.status !== 404) throw e; }
              }
              return;
            }

            if (action === 'converted_to_draft') {
              await setStatusLabel(prNumber, null);
              return;
            }

            if (action === 'closed') {
              await setStatusLabel(prNumber, 'estado:cerrado');
              return;
            }

            core.info(`Sin acción para el evento "${action}".`);
```

---

### 5.3 `.github/workflows/ci-static.yml`

```yaml
name: CI — Análisis Estático

# Ejecuta análisis estático sobre el backend Java.
# No modifica el código fuente — solo audita y reporta.
# SonarCloud requiere que el secret SONAR_TOKEN esté configurado
# en Settings → Secrets → Actions del repositorio.

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
  workflow_dispatch:

permissions:
  contents: read
  pull-requests: write

jobs:
  static-analysis:
    name: Checkstyle + SpotBugs + PMD + SonarCloud
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0   # SonarCloud necesita historial completo

      - name: Setup Java 21
        uses: actions/setup-java@v4
        with:
          java-version: '21'
          distribution: 'temurin'

      - name: Cache Maven
        uses: actions/cache@v4
        with:
          path: ~/.m2/repository
          key: ${{ runner.os }}-maven-${{ hashFiles('**/pom.xml') }}
          restore-keys: ${{ runner.os }}-maven-

      - name: Compilar sin ejecutar tests
        run: ./mvnw compile -DskipTests --no-transfer-progress

      - name: Checkstyle
        run: ./mvnw checkstyle:check --no-transfer-progress
        continue-on-error: true   # Reportar pero no bloquear el pipeline en Fase 1

      - name: SpotBugs
        run: ./mvnw spotbugs:check --no-transfer-progress
        continue-on-error: true

      - name: PMD
        run: ./mvnw pmd:check --no-transfer-progress
        continue-on-error: true

      - name: Publicar reportes de análisis estático como artefacto
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: static-analysis-reports
          path: |
            target/checkstyle-result.xml
            target/spotbugsXml.xml
            target/pmd.xml
          retention-days: 30

      - name: SonarCloud Scan
        uses: SonarSource/sonarcloud-github-action@master
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
        with:
          args: >
            -Dsonar.projectKey=REEMPLAZAR_ORG_REEMPLAZAR_REPO
            -Dsonar.organization=REEMPLAZAR_ORG
            -Dsonar.java.binaries=target/classes
            -Dsonar.sources=src/main/java
            -Dsonar.exclusions=**/test/**
```

---

### 5.4 `.github/workflows/ci-tests.yml`

```yaml
name: CI — Pruebas Dinámicas (Fase 2)

# Se activa cuando el equipo de desarrollo entrega el código con pruebas unitarias.
# Requiere MySQL 8. Genera reporte JaCoCo y lo envía a SonarCloud.

on:
  push:
    branches: [main, develop]
    paths:
      - 'src/test/**'
      - 'src/main/**'
  workflow_dispatch:

permissions:
  contents: read
  pull-requests: write
  checks: write

jobs:
  tests:
    name: mvn test + JaCoCo + SonarCloud
    runs-on: ubuntu-latest

    services:
      mysql:
        image: mysql:8.0
        env:
          MYSQL_DATABASE: biblioteca_db_test
          MYSQL_ROOT_PASSWORD: sqa_ci_root_2026
          MYSQL_USER: biblioteca
          MYSQL_PASSWORD: sqa_ci_pass_2026
        ports:
          - 3306:3306
        options: >-
          --health-cmd "mysqladmin ping -h localhost -u root --password=sqa_ci_root_2026"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 10

    env:
      SPRING_DATASOURCE_URL: jdbc:mysql://localhost:3306/biblioteca_db_test
      SPRING_DATASOURCE_USERNAME: biblioteca
      SPRING_DATASOURCE_PASSWORD: sqa_ci_pass_2026
      SPRING_JPA_HIBERNATE_DDL_AUTO: create-drop

    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Java 21
        uses: actions/setup-java@v4
        with:
          java-version: '21'
          distribution: 'temurin'

      - name: Cache Maven
        uses: actions/cache@v4
        with:
          path: ~/.m2/repository
          key: ${{ runner.os }}-maven-${{ hashFiles('**/pom.xml') }}
          restore-keys: ${{ runner.os }}-maven-

      - name: Ejecutar pruebas con cobertura JaCoCo
        run: ./mvnw test jacoco:report --no-transfer-progress

      - name: Publicar reporte JaCoCo como artefacto
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: jacoco-coverage-report
          path: target/site/jacoco/
          retention-days: 30

      - name: Publicar resultados de pruebas (JUnit XML)
        if: always()
        uses: mikepenz/action-junit-report@v4
        with:
          report_paths: 'target/surefire-reports/*.xml'
          check_name: 'Resultados de Pruebas JUnit'

      - name: SonarCloud Scan con cobertura
        uses: SonarSource/sonarcloud-github-action@master
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
        with:
          args: >
            -Dsonar.projectKey=REEMPLAZAR_ORG_REEMPLAZAR_REPO
            -Dsonar.organization=REEMPLAZAR_ORG
            -Dsonar.java.binaries=target/classes
            -Dsonar.sources=src/main/java
            -Dsonar.tests=src/test/java
            -Dsonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml
```

---

## 6. Cambios en `pom.xml`

Agregar los siguientes bloques dentro de las secciones correspondientes. **No reemplazar el contenido existente — agregar dentro de `<dependencies>` y `<build><plugins>`.**

### 6.1 Dependencias de prueba adicionales

```xml
<!-- Dentro de <dependencies> -->

<!-- H2 en memoria: permite pruebas unitarias sin MySQL real -->
<dependency>
    <groupId>com.h2database</groupId>
    <artifactId>h2</artifactId>
    <scope>test</scope>
</dependency>
```

### 6.2 Plugins de análisis y cobertura

```xml
<!-- Dentro de <build><plugins> -->

<!-- JaCoCo: reporte de cobertura de código -->
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <version>0.8.12</version>
    <executions>
        <execution>
            <id>prepare-agent</id>
            <goals><goal>prepare-agent</goal></goals>
        </execution>
        <execution>
            <id>report</id>
            <phase>test</phase>
            <goals><goal>report</goal></goals>
        </execution>
    </executions>
</plugin>

<!-- Checkstyle: estilo de código -->
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-checkstyle-plugin</artifactId>
    <version>3.3.1</version>
    <configuration>
        <!-- Usar Google Style o Sun Style. Google es más moderno. -->
        <configLocation>google_checks.xml</configLocation>
        <consoleOutput>true</consoleOutput>
        <failsOnError>false</failsOnError>
        <outputFile>${project.build.directory}/checkstyle-result.xml</outputFile>
    </configuration>
</plugin>

<!-- SpotBugs: detección de bugs potenciales en bytecode -->
<plugin>
    <groupId>com.github.spotbugs</groupId>
    <artifactId>spotbugs-maven-plugin</artifactId>
    <version>4.8.6.4</version>
    <configuration>
        <effort>Max</effort>
        <threshold>Low</threshold>
        <failOnError>false</failOnError>
        <xmlOutput>true</xmlOutput>
        <xmlOutputDirectory>${project.build.directory}</xmlOutputDirectory>
    </configuration>
</plugin>

<!-- PMD: análisis de código fuente -->
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-pmd-plugin</artifactId>
    <version>3.23.0</version>
    <configuration>
        <failOnViolation>false</failOnViolation>
        <printFailingErrors>true</printFailingErrors>
        <outputDirectory>${project.build.directory}</outputDirectory>
    </configuration>
</plugin>
```

### 6.3 Configuración para pruebas con H2 (sin MySQL)

Crear el archivo `src/test/resources/application-test.properties`:

```properties
# Perfil de test: usa H2 en lugar de MySQL
# Activar con @ActiveProfiles("test") en las clases de prueba unitaria

spring.datasource.url=jdbc:h2:mem:biblioteca_test;DB_CLOSE_DELAY=-1;MODE=MySQL
spring.datasource.driver-class-name=org.h2.Driver
spring.datasource.username=sa
spring.datasource.password=
spring.jpa.hibernate.ddl-auto=create-drop
spring.jpa.database-platform=org.hibernate.dialect.H2Dialect

# Desactivar Spring Security en pruebas unitarias si aplica
spring.autoconfigure.exclude=org.springframework.boot.autoconfigure.security.servlet.SecurityAutoConfiguration
```

---

## 7. Configuración de GitHub Projects v2

### 7.1 Crear el tablero (CLI)

```bash
# Autenticarse con gh (solo la primera vez)
gh auth login

# Crear el proyecto. Anotar el número N que devuelve.
gh project create --owner "@me" --title "SQA — Gestión Bibliotecaria Equipo 58-1"
```

Si el equipo trabaja bajo una organización, reemplazar `"@me"` por `"NOMBRE_ORG"`.

### 7.2 Crear milestones

```bash
# Desde la raíz del repositorio clonado
gh milestone create \
  --title "Fase 1 — Técnicas Estáticas" \
  --description "Inspección, walkthrough y auditoría sobre ERS y DAS" \
  --due-date "REEMPLAZAR_FECHA_ENTREGA_FASE1"

gh milestone create \
  --title "Fase 2 — Técnicas Dinámicas" \
  --description "Pruebas unitarias, integración, sistema y aceptación + CI automatizado" \
  --due-date "REEMPLAZAR_FECHA_ENTREGA_FASE2"
```

### 7.3 Columnas del tablero (configuración manual en UI)

Acceder a `github.com/users/USUARIO/projects/N` y crear los siguientes campos:

| Campo | Tipo | Opciones |
|---|---|---|
| **Status** | Single select | `Backlog`, `En Ejecución`, `En Revisión`, `Cerrado` |
| **Fase** | Single select | `Fase 1`, `Fase 2` |
| **Severidad** | Single select | `Crítica`, `Mayor`, `Menor`, `Observación` |
| **Rol** | Single select | `Líder General`, `Líder Tec`, `Tester`, `Métricas`, `Escriba` |

### 7.4 Vistas recomendadas

Crear las siguientes vistas desde la UI del Projects v2:

| Vista | Tipo | Agrupación | Filtro |
|---|---|---|---|
| **Kanban General** | Board | por `Status` | Sin filtro |
| **Por Fase** | Table | por `Fase` | Sin filtro |
| **Por Rol** | Table | por `Rol` | Sin filtro |
| **Hallazgos Fase 1** | Table | por `Severidad` | `fase:fase-1` |
| **Defectos Fase 2** | Table | por `Severidad` | `fase:fase-2` |

---

## 8. Configuración de SonarCloud

### 8.1 Pasos de configuración

1. Ir a [sonarcloud.io](https://sonarcloud.io) e iniciar sesión con GitHub.
2. Clic en **"+"** → **"Analyze new project"** → seleccionar el repositorio.
3. Elegir el plan gratuito (válido para repositorios públicos).
4. En la página del proyecto SonarCloud, ir a **"Administration" → "Analysis Method"** → seleccionar **"GitHub Actions"**.
5. Copiar el valor del `SONAR_TOKEN` que se genera.
6. En el repositorio GitHub: **Settings → Secrets and variables → Actions → New repository secret**.
   - Name: `SONAR_TOKEN`
   - Value: pegar el token copiado.
7. Anotar el **Project Key** y la **Organization Key** que muestra SonarCloud (los necesitarás en `sonar-project.properties`).

### 8.2 Archivo `sonar-project.properties`

Crear en la raíz del repositorio:

```properties
# Reemplazar con los valores obtenidos en SonarCloud → Administration → General Settings
sonar.projectKey=REEMPLAZAR_ORG_REEMPLAZAR_REPO
sonar.organization=REEMPLAZAR_ORG

sonar.projectName=SQA - Gestion Bibliotecaria Equipo 58-1
sonar.projectVersion=1.0

# Rutas del código fuente
sonar.sources=src/main/java
sonar.tests=src/test/java
sonar.java.binaries=target/classes

# Reporte de cobertura JaCoCo (disponible tras ejecutar mvn test jacoco:report)
sonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml

# Exclusiones
sonar.exclusions=**/dto/**,**/config/**,**/*Application.java

# Encoding
sonar.sourceEncoding=UTF-8
```

### 8.3 Métricas a rastrear en SonarCloud

| Métrica | Descripción | Relevancia SQA |
|---|---|---|
| **Bugs** | Errores detectados en el código | Defectos Fase 2 |
| **Vulnerabilities** | Problemas de seguridad | ISO 25010 — Seguridad |
| **Code Smells** | Malas prácticas de mantenibilidad | ISO 25010 — Mantenibilidad |
| **Cyclomatic Complexity** | Complejidad de los métodos | Esfuerzo de prueba (GQM) |
| **Coverage** | % de líneas cubiertas por pruebas | KPI Fase 2 |
| **Duplication** | % de código duplicado | Mantenibilidad |
| **Technical Debt** | Tiempo estimado de corrección | Métricas PSM |

---

## 9. Extracción de métricas para el Líder de Métricas

### 9.1 Exportar issues como CSV con `gh` CLI

```bash
# Exportar todos los issues con sus labels, estado y fecha de creación
gh issue list \
  --repo REEMPLAZAR_USUARIO/REEMPLAZAR_REPO \
  --state all \
  --limit 500 \
  --json number,title,state,labels,createdAt,closedAt,assignees \
  > sqa/metricas/issues_export.json

# Convertir a CSV con Python
python3 -c "
import json, csv, sys

with open('sqa/metricas/issues_export.json') as f:
    issues = json.load(f)

with open('sqa/metricas/issues_export.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['numero','titulo','estado','labels','creado','cerrado','asignados'])
    for i in issues:
        writer.writerow([
            i['number'],
            i['title'],
            i['state'],
            '|'.join(l['name'] for l in i.get('labels', [])),
            i.get('createdAt', ''),
            i.get('closedAt', ''),
            '|'.join(a['login'] for a in i.get('assignees', []))
        ])
print('CSV generado: sqa/metricas/issues_export.csv')
"
```

### 9.2 Métricas GQM/PSM a calcular

| Métrica | Cálculo | Fuente |
|---|---|---|
| **Densidad de defectos por área** | issues `tipo:defecto` agrupados por `area:*` / total issues | issues_export.csv |
| **Tasa de resolución** | issues `estado:cerrado` / issues totales × 100 | issues_export.csv |
| **Distribución por severidad** | count por `severidad:*` | issues_export.csv |
| **Hallazgos por fase** | count `fase:fase-1` vs `fase:fase-2` | issues_export.csv |
| **Hallazgos por característica ISO 25010** | count por `iso:*` | issues_export.csv |
| **Tiempo medio de resolución** | avg(closedAt - createdAt) para issues cerrados | issues_export.csv |
| **Complejidad ciclomática promedio** | Obtenida de SonarCloud API | SonarCloud |
| **Cobertura de pruebas** | % lines covered — JaCoCo / SonarCloud | ci-tests run |

### 9.3 Script de métricas local

El Líder de Métricas puede crear `sqa/metricas/calcular_kpi.py` para procesar el export:

```python
import json
from collections import Counter
from pathlib import Path

def generar_reporte_metricas(issues_path: str = "sqa/metricas/issues_export.json") -> dict:
    data = json.loads(Path(issues_path).read_text())
    all_labels = [l["name"] for i in data for l in i.get("labels", [])]
    total = len(data)
    cerrados = sum(1 for i in data if i["state"] == "CLOSED")

    metricas = {
        "total_issues": total,
        "cerrados": cerrados,
        "tasa_resolucion_pct": round(cerrados / total * 100, 1) if total else 0,
        "por_tipo":      Counter(l for l in all_labels if l.startswith("tipo:")),
        "por_area":      Counter(l for l in all_labels if l.startswith("area:")),
        "por_severidad": Counter(l for l in all_labels if l.startswith("severidad:")),
        "por_fase":      Counter(l for l in all_labels if l.startswith("fase:")),
        "por_iso":       Counter(l for l in all_labels if l.startswith("iso:")),
        "por_rol":       Counter(l for l in all_labels if l.startswith("rol:")),
    }

    output_path = Path("sqa/metricas/reporte_kpi.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(metricas, indent=2, ensure_ascii=False))
    print(f"Reporte KPI generado: {output_path}")
    return metricas

if __name__ == "__main__":
    generar_reporte_metricas()
```

Ejecutar localmente: `python sqa/metricas/calcular_kpi.py`

---

## 10. Orden de implementación

Seguir exactamente este orden. Cada paso tiene una condición de completado.

### Paso 1 — Crear taxonomía de etiquetas
```bash
mkdir -p .github
# Crear .github/labels.yml con el contenido de la Sección 2
# Luego sincronizar:
gh label sync -f .github/labels.yml
```
**Completado cuando:** `gh label list` muestra todas las etiquetas definidas.

---

### Paso 2 — Crear plantillas de issues
```bash
mkdir -p .github/ISSUE_TEMPLATE
# Crear los tres archivos de la Sección 3
```
**Completado cuando:** Al abrir un nuevo issue en GitHub, aparecen las tres opciones de template.

---

### Paso 3 — Crear plantilla de PR
```bash
# Crear .github/PULL_REQUEST_TEMPLATE.md con el contenido de la Sección 4
```
**Completado cuando:** Al abrir un nuevo PR, el body se pre-llena con el template.

---

### Paso 4 — Configurar GitHub Projects v2 y Milestones
```bash
gh project create --owner "@me" --title "SQA — Gestión Bibliotecaria Equipo 58-1"
gh milestone create --title "Fase 1 — Técnicas Estáticas" --due-date "FECHA"
gh milestone create --title "Fase 2 — Técnicas Dinámicas" --due-date "FECHA"
```
Luego, configurar campos y vistas en la UI (ver Sección 7.3 y 7.4).  
**Completado cuando:** El tablero tiene las 5 vistas y los 2 milestones.

---

### Paso 5 — Crear workflow sync-labels
```bash
mkdir -p .github/workflows
# Crear .github/workflows/sync-labels.yml con el contenido de la Sección 5.1
git add .github/workflows/sync-labels.yml
git commit -m "ci: add sync-labels workflow"
git push
```
**Completado cuando:** El workflow corre exitosamente en la pestaña Actions.

---

### Paso 6 — Crear workflow pr-project
```bash
# Crear .github/workflows/pr-project.yml con el contenido de la Sección 5.2
# IMPORTANTE: Reemplazar la project-url con la URL real del tablero
# Crear el secret PROJECT_TOKEN:
#   Settings → Secrets → Actions → New secret
#   Name: PROJECT_TOKEN
#   Value: Personal Access Token con scopes "repo" y "project"
git add .github/workflows/pr-project.yml
git commit -m "ci: add PR auto-project and auto-label workflow"
git push
```
**Completado cuando:** Al abrir un PR de prueba, se agrega al tablero y recibe etiquetas automáticamente.

---

### Paso 7 — Configurar SonarCloud
1. Registrarse en [sonarcloud.io](https://sonarcloud.io) con la cuenta de GitHub del equipo.
2. Importar el repositorio y copiar el `SONAR_TOKEN`.
3. Agregar el secret `SONAR_TOKEN` en Settings → Secrets → Actions.
4. Crear `sonar-project.properties` en la raíz con el contenido de la Sección 8.2. Reemplazar `REEMPLAZAR_ORG` y `REEMPLAZAR_REPO`.

```bash
git add sonar-project.properties
git commit -m "ci: add SonarCloud configuration"
git push
```
**Completado cuando:** El dashboard de SonarCloud muestra el proyecto importado.

---

### Paso 8 — Crear workflow ci-static
```bash
# Crear .github/workflows/ci-static.yml con el contenido de la Sección 5.3
# Reemplazar sonar.projectKey y sonar.organization con los valores reales
git add .github/workflows/ci-static.yml
git commit -m "ci: add static analysis pipeline (Checkstyle + SpotBugs + PMD + SonarCloud)"
git push
```
**Completado cuando:** El workflow corre, los reportes XML se publican como artefactos, y SonarCloud muestra el primer análisis.

---

### Paso 9 — Agregar JaCoCo y plugins a `pom.xml`
```bash
# Editar pom.xml con los bloques de la Sección 6
# Verificar localmente:
./mvnw compile checkstyle:check spotbugs:check pmd:check -DskipTests
./mvnw test jacoco:report  # (puede fallar si no hay tests — es esperado en Fase 1)
git add pom.xml src/test/resources/application-test.properties
git commit -m "build: add JaCoCo, Checkstyle, SpotBugs, PMD plugins + H2 test scope"
git push
```
**Completado cuando:** `./mvnw compile checkstyle:check` termina sin error de compilación.

---

### Paso 10 — Crear workflow ci-tests (en espera de Fase 2)
```bash
# Crear .github/workflows/ci-tests.yml con el contenido de la Sección 5.4
# Este workflow queda listo pero inactivo hasta que el equipo dev entregue pruebas
git add .github/workflows/ci-tests.yml
git commit -m "ci: add dynamic testing pipeline (mvn test + JaCoCo + SonarCloud) — ready for Fase 2"
git push
```
**Completado cuando:** El workflow existe en la pestaña Actions y puede ejecutarse manualmente (workflow_dispatch).

---

### Paso 11 — Dar acceso al docente
```bash
# Opción A: Repositorio público (recomendado — el docente puede ver todo sin ser colaborador)
gh repo edit --visibility public

# Opción B: Repositorio privado — agregar al docente como colaborador Read-only
gh api repos/REEMPLAZAR_USUARIO/REEMPLAZAR_REPO/collaborators/REEMPLAZAR_USERNAME_DOCENTE \
  --method PUT \
  --field permission=read
```
**Completado cuando:** El docente puede ver issues, PRs, workflows y el tablero Projects v2 sin autenticación adicional (si es público) o con su cuenta de GitHub (si es privado).

---

## 12. Acceso del docente

### Lo que el docente puede observar

| Artefacto | Dónde verlo | Qué evidencia |
|---|---|---|
| Tablero Kanban | `github.com/users/USUARIO/projects/N` | Estado del proceso SQA en tiempo real |
| Issues (hallazgos/defectos) | `github.com/REPO/issues` | Trazabilidad, roles, severidad, ISO 25010 |
| PR history | `github.com/REPO/pulls?state=all` | Revisiones por pares (IEEE 730) |
| Workflow runs (CI) | `github.com/REPO/actions` | Automatización, reportes, SonarCloud |
| SonarCloud dashboard | `sonarcloud.io/project/...` | Métricas de calidad del código |
| Artefactos de CI | Cada workflow run → Artifacts | Reportes JaCoCo, Checkstyle, SpotBugs, AI |
| Commits por autor | `github.com/REPO/graphs/contributors` | Participación de cada integrante |

### Enlace único a compartir con el docente

```
Repositorio:   https://github.com/REEMPLAZAR_USUARIO/gestion-bibliotecaria-sqa
Tablero SQA:   https://github.com/users/REEMPLAZAR_USUARIO/projects/N
SonarCloud:    https://sonarcloud.io/project/overview?id=REEMPLAZAR_PROJECTKEY
```

---

## Resumen del ecosistema completo

```
┌─────────────────────────────────────────────────────────────────┐
│                   ECOSISTEMA SQA — EQUIPO 58-1                  │
├────────────────────┬────────────────────────────────────────────┤
│ GESTIÓN            │ GitHub Projects v2 (tablero + vistas)      │
│                    │ Milestones: Fase 1 / Fase 2                │
│                    │ Issues: hallazgos, defectos, auditoría     │
├────────────────────┼────────────────────────────────────────────┤
│ TRAZABILIDAD       │ Labels taxonomy (tipo/area/severidad/       │
│                    │   estado/rol/fase/iso)                     │
│                    │ PR template = evidencia peer review (IEEE 730)│
│                    │ Campo ERS-XXX obligatorio en templates     │
├────────────────────┼────────────────────────────────────────────┤
│ AUTOMATIZACIÓN     │ sync-labels.yml → labels como código       │
│                    │ pr-project.yml → auto-add, auto-label,     │
│                    │   sync estado                              │
├────────────────────┼────────────────────────────────────────────┤
│ CI ESTÁTICO        │ Checkstyle + SpotBugs + PMD (Maven)        │
│ (Fase 1 y 2)       │ SonarCloud → dashboard métricas            │
│                    │ Artefactos XML publicados en Actions       │
├────────────────────┼────────────────────────────────────────────┤
│ CI DINÁMICO        │ mvn test + JaCoCo → cobertura              │
│ (Fase 2)           │ MySQL 8 service en CI                      │
│                    │ Reporte JUnit publicado en Actions         │
├────────────────────┼────────────────────────────────────────────┤
│ MÉTRICAS           │ gh issue list --json → CSV                 │
│                    │ calcular_kpi.py → KPIs GQM/PSM            │
│                    │ SonarCloud API → complejidad + cobertura   │
└────────────────────┴────────────────────────────────────────────┘
```
