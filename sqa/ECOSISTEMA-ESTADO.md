# Estado del Ecosistema SQA — Equipo 58-1

Estado vivo de la migración Jira/Confluence → GitHub-native. Complementa
[`PLAN_ECOSISTEMA_SQA.md`](../PLAN_ECOSISTEMA_SQA.md) (diseño) y
[`ECOSISTEMA-SETUP-CHECKLIST.md`](./ECOSISTEMA-SETUP-CHECKLIST.md) (activación manual).

Última actualización: 2026-06-23.

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

## ⏳ Listo pero inactivo

| Pieza | Espera |
|---|---|
| `ci-tests` (JUnit + JaCoCo) | Que el equipo dev entregue el código con pruebas unitarias (Fase 2) |
| Auto-add de PRs al tablero | Decisión: `PROJECT_TOKEN` (PAT) **o** Auto-add nativo de Projects v2 (sin token) |

---

## 🕳️ Huecos abiertos (consciente, no olvidado)

1. **Métricas de proceso sin dashboard automatizado.**
   `sqa/metricas/calcular_kpi.py` calcula KPIs GQM/PSM (hallazgos por severidad/fase/ISO,
   tasa de resolución) pero hoy solo genera un JSON local.
   - **Plan:** usar **Projects v2 → Insights** (gráficos nativos por estado/severidad/fase, sin código)
     como dashboard de proceso; opcionalmente una Action programada que corra `calcular_kpi.py`
     y commitee un `reporte_kpi.md` versionado.

2. **Publicación de documentos (sustituto de Confluence).**
   - **Decisión tomada:** los entregables (PACS, informes de revisión, checklists) viven como
     **markdown en `sqa/`**, versionados y revisados por PR. **NO se usa GitHub Wiki** porque
     vive en un repo aparte, no pasa por PR y rompe la cadena de evidencia (peer-review IEEE 730
     + trazabilidad) que sostiene todo el ecosistema.
   - **Pendiente:** configurar **GitHub Pages** para renderizar ese mismo markdown como sitio
     presentable para el docente (sin perder la trazabilidad del repo).

3. **Entregables de documentación** (los hace el equipo, no el ecosistema):
   - ✅ **PACS consolidado F1+F2** — `sqa/PACS.md` v1.0 emitido, ver PR de la rama `docs/pacs-formal-consolidado-f1-f2` (issue #6). Cierra este hueco como contenedor formal.
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
- **Métricas en dos capas:** código → SonarCloud; proceso → Projects Insights (+ `calcular_kpi.py`).
- **Guards `if: TOKEN != ''`:** los pasos que dependen de secrets externos (SonarCloud, Projects)
  se saltean limpiamente si el secret no está, en vez de teñir el CI de rojo.
