# Estado del Ecosistema SQA — Equipo 58-1

Estado vivo de la migración Jira/Confluence → GitHub-native. Complementa
[`PLAN_ECOSISTEMA_SQA.md`](../PLAN_ECOSISTEMA_SQA.md) (diseño) y
[`ECOSISTEMA-SETUP-CHECKLIST.md`](./ECOSISTEMA-SETUP-CHECKLIST.md) (activación manual).

Última actualización: 2026-07-12 (sincronización de estado declarado, issue #33).

---

## ✅ Operativo y verificado

| Pieza | Detalle |
|---|---|
| Taxonomía de etiquetas | 34 labels sincronizadas (`tipo/area/severidad/estado/rol/fase/iso`) |
| Issue/PR templates | Hallazgo (F1), Defecto (F2), Auditoría, PR como evidencia peer-review |
| `sync-labels` | Workflow con `crazy-max/ghaction-github-labeler` (el `gh label sync` del plan no existía) |
| `ci-static` + SonarCloud | **Verde, probado**. Análisis por CI activo (Automatic Analysis desactivado) |
| Métricas de **código** | Dashboard vivo en SonarCloud (bugs, cobertura, complejidad, smells, deuda) |
| Tablero | [Projects v2 #4](https://github.com/users/odjaramillo/projects/4), público, campos Fase/Severidad/Rol/Status |
| Acceso docente | Repo público → ve issues, PRs, Actions, board sin ser colaborador |
| `ci-tests` (JUnit + JaCoCo) | **En ejecución**. Suite dinámica implementada: 5 clases unitarias, 4 de integración y 3 de sistema. Gate sobre el grupo `regresion`; el grupo `defecto-conocido` corre de modo informativo (ver `PACS.md` §5.1) |
| Métricas de **proceso** | [Dashboard en GitHub Pages](https://odjaramillo.github.io/gestion-bibliotecaria-sqa/), desplegado por `pages-dashboard.yml` en cada push a `main` (issue #27, PR #28) |

## ⏳ Listo pero inactivo

| Pieza | Espera |
|---|---|
| Auto-add de PRs al tablero | Decisión: `PROJECT_TOKEN` (PAT) **o** Auto-add nativo de Projects v2 (sin token) |

---

## 🕳️ Huecos en seguimiento (conscientes, no olvidados)

1. ✅ **CERRADO (2026-07-12) — Métricas de proceso sin dashboard automatizado.**
   `sqa/metricas/calcular_kpi.py` ya no se queda en un JSON local: el workflow `pages-dashboard.yml`
   lo ejecuta y publica el dashboard de métricas de proceso en
   https://odjaramillo.github.io/gestion-bibliotecaria-sqa/, con despliegue automático en cada push
   a `main` (issue #27, PR #28) más cron semanal y ejecución manual. La cobertura mostrada proviene
   de JaCoCo sobre el grupo de pruebas `regresion`.

2. ✅ **CERRADO parcialmente (2026-07-12) — Publicación de documentos (sustituto de Confluence).**
   - **Decisión tomada (vigente):** los entregables (PACS, informes de revisión, checklists) viven como
     **markdown en `sqa/`**, versionados y revisados por PR. **NO se usa GitHub Wiki** porque
     vive en un repo aparte, no pasa por PR y rompe la cadena de evidencia (peer-review IEEE 730
     + trazabilidad) que sostiene todo el ecosistema.
   - **GitHub Pages: operativo** desde el issue #7 / PR #12; hoy sirve el dashboard de métricas.
   - **Pendiente acotado:** renderizar además los **documentos** SQA (`sqa/*.md`) sobre ese mismo
     sitio — trabajo cubierto por el issue #3, no por este hueco.

3. **Entregables de documentación** (los hace el equipo, no el ecosistema):
   - ✅ **PACS consolidado F1+F2** — `sqa/PACS.md` v1.1 vigente (emisión inicial v1.0, issue #6, rama `docs/pacs-formal-consolidado-f1-f2`; sincronización de estado declarado en v1.1, issue #33). Cierra este hueco como contenedor formal.
   - Infograma del Ecosistema Tecnológico (apéndice del PACS) — pendiente.
   - Reflexión crítica sobre el ecosistema (apéndice del PACS) — pendiente.

4. **Milestones de Fase 1 / Fase 2** — crear vía `gh api .../milestones`
   (recordatorio: `gh milestone` no existe). Ver checklist §3.

---

## 🧭 Decisiones de arquitectura registradas

- **GitHub-native sobre Jira/Confluence:** el enunciado lo permite (lista GitHub Issues/Actions/
  SonarQube como sugeridas); mejora la cobertura de la rúbrica de ecosistema automatizado.
- **Documentos en repo, no Wiki:** prioriza trazabilidad y revisión por pares.
- **GitHub Pages para presentación:** capa de render, no de fuente de verdad.
- **Métricas en dos capas:** código → SonarCloud; proceso → `calcular_kpi.py` publicado como dashboard en GitHub Pages (`pages-dashboard.yml`), complementado por Projects Insights.
- **Guards `if: TOKEN != ''`:** los pasos que dependen de secrets externos (SonarCloud, Projects)
  se saltean limpiamente si el secret no está, en vez de teñir el CI de rojo.
