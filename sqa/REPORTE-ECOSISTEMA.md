# Reporte de Migración del Ecosistema SQA — Equipo 58-1

**Proyecto:** Sistema de Gestión Bibliotecaria
**Migración:** Jira/Confluence → ecosistema GitHub-native
**Fecha del reporte:** 2026-06-23
**Estándares de referencia:** IEEE 730, ISO/IEC 12207, ISO/IEC 25010, ISO/IEC/IEEE 29148, ISO/IEC/IEEE 42010

> Documentos relacionados: [`PLAN_ECOSISTEMA_SQA.md`](../PLAN_ECOSISTEMA_SQA.md) (diseño),
> [`ECOSISTEMA-ESTADO.md`](./ECOSISTEMA-ESTADO.md) (estado vivo),
> [`ECOSISTEMA-SETUP-CHECKLIST.md`](./ECOSISTEMA-SETUP-CHECKLIST.md) (activación manual).

---

## 1. Resumen ejecutivo

Se reemplazó el ecosistema basado en agentes de IA contra Jira/Confluence por uno
**nativo de GitHub**, alineado a estándares internacionales y centrado en trazabilidad,
automatización y métricas. El núcleo (gestión, CI, métricas de código) está **operativo y
verificado de punta a punta**. El trabajo restante es mayormente de **Fase 2** (ejecución de
pruebas dinámicas) y de documentación final, detallado en la sección 4.

---

## 2. Lo realizado y verificado

### 2.1 Limpieza (salida de Jira/Confluence)
- Eliminado el sistema de agentes: workflows `wf1–wf7`, paquete `scripts/`, suite `tests/`,
  `requirements.txt` y artefactos/evidencia obsoletos de Fase 1.
- Borrados 8 secrets huérfanos (Jira/Confluence/Gemini). Solo quedan `SONAR_TOKEN` y `PROJECT_TOKEN`.

### 2.2 Ecosistema de trazabilidad
- **34 etiquetas** canónicas sincronizadas (`tipo/area/severidad/estado/rol/fase/iso`).
- 3 plantillas de issue (hallazgo F1, defecto F2, auditoría) con trazabilidad ERS/DAS obligatoria.
- Plantilla de PR como **evidencia formal de revisión por pares** (IEEE 730).

### 2.3 Automatización (GitHub Actions)
- `sync-labels` — etiquetas como código (fuente única de verdad).
- `pr-project` — auto-add de PRs al tablero + auto-label + sincronización de estado.
- `ci-static` — Checkstyle + SpotBugs + PMD + SonarCloud. **Verde y probado.**
- `ci-tests` — JUnit + JaCoCo (listo, se activa en Fase 2).

### 2.4 Métricas de código (vivo)
- **SonarCloud** analizando por CI: bugs, vulnerabilidades, code smells, complejidad,
  cobertura, duplicación y deuda técnica.

### 2.5 Gestión (GitHub Projects v2 #4)
- Tablero público, linkeado al repo, con campos **Fase / Severidad / Rol** y Status SQA
  (**Backlog → En Ejecución → En Revisión → Cerrado**).
- Auto-add de issues y PRs activos; workflows nativos del tablero reconfigurados al flujo SQA.
- **Issues del repositorio activados** (estaban deshabilitados — era el bloqueante de fondo).
- Milestones `#1 Fase 1` y `#2 Fase 2` creados.

### 2.6 Acceso del docente
- Repositorio **público** → issues, PRs, Actions, tablero y commits visibles sin ser colaborador.

---

## 3. Pendiente del ecosistema (no bloqueante)

| Ítem | Responsable | Notas |
|---|---|---|
| Fechas de los milestones (`due_on`) | Equipo | El usuario las debe; se setean por `gh api`. |
| GitHub Pages (publicar markdown de `sqa/`) | Líder Tec | Trackeado en issue #3. |
| Dashboard de métricas de proceso | Líder de Métricas | Projects v2 → Insights + opcional Action de `calcular_kpi.py`. |
| Migrar `sonarcloud-github-action` → `sonarqube-scan-action` | Líder Tec | La actual está deprecada (sigue funcionando). |

---

## 4. Trabajo de FASE 2 — mapeado a la rúbrica de evaluación

> **Precondición técnica (enunciado):** el equipo de desarrollo debe **re-entregar el código
> con pruebas unitarias** sobre la(s) característica(s) de calidad elegida(s) —
> **fiabilidad/confiabilidad (ISO/IEC 25010)**. Sin esa entrega, `ci-tests` no tiene qué ejecutar.

La rúbrica de Fase 2 son **6 criterios × 5 pts = 30**. Abajo, qué aporta ya el ecosistema (✅) y
qué debe **producir el equipo** (⬜) para cada criterio.

### a) Documentación de aseguramiento (5 pts)
*Evalúa: completitud, coherencia metodológica, estándares y trazabilidad.*
- ✅ Plantillas que fuerzan trazabilidad ERS↔hallazgo↔defecto↔prueba (ISO 12207).
- ✅ PR como evidencia de revisión por pares (IEEE 730).
- ✅ **PACS consolidado** que integre Fase 1 (con correcciones para reconsideración de nota) — `sqa/PACS.md` v1.0, ver PR de la rama `docs/pacs-formal-consolidado-f1-f2` (issue #6).
- ⬜ **Plan de Calidad, Estrategia de Pruebas y Plan de Pruebas** (ya iniciados en `sqa/fase2/planificacion/`).
- ⬜ **Informe de revisión de requisitos** (de la primera entrega) incorporado como anexo.
- ⬜ **Informe de Resultados de Pruebas** (lo redacta el Analista de Pruebas).

### b) Pruebas unitarias (5 pts)
*Evalúa: cobertura, evidencia, análisis y métricas.*
- ✅ `ci-tests` ejecuta `mvn test` + **JaCoCo** y sube cobertura a SonarCloud.
- ✅ Reporte JUnit publicado como check en cada run.
- ⬜ **Escribir las pruebas unitarias** (JUnit) sobre las clases de fiabilidad — enfoque **caja blanca**
  (cobertura de decisiones/ramas en métodos críticos).
- ⬜ **Análisis de cobertura** por clase y su interpretación (no solo el %).
- ⬜ Registrar defectos encontrados como issues (`tipo:defecto`, plantilla lista).

### c) Pruebas de integración (5 pts)
*Evalúa: ejecución, evidencia, métricas y reflexión sobre integración.*
- ✅ `ci-tests` ya levanta un servicio **MySQL 8** para pruebas con BD real.
- ⬜ **Pruebas de integración** (`@SpringBootTest`) sobre la interacción Controller↔Service↔Repository
  y endpoints REST — enfoque **caja gris**.
- ⬜ Evidencia de ejecución + **reflexión sobre la integración** entre componentes.

### d) Pruebas de sistema y aceptación (5 pts)
*Evalúa: validación de requisitos, feedback y análisis de aceptación.*
- ⬜ **Pruebas de sistema** end-to-end del flujo completo — enfoque **caja negra** (basado en ERS).
  Herramientas sugeridas: Postman/Selenium.
- ⬜ **Criterios de aceptación** explícitos por requisito + validación contra la ERS.
- ⬜ Feedback documentado y **análisis de aceptación** (¿se cumplieron los criterios?).

### e) Ecosistema tecnológico (5 pts)
*Evalúa: automatización, dashboards, trazabilidad y reflexión crítica.*
- ✅ Automatización (Actions), trazabilidad (labels/issues/PR), dashboard de código (SonarCloud).
- ⬜ **Dashboard de métricas de proceso** (Projects Insights).
- ⬜ **Infograma del ecosistema** (apéndice del PACS) — esquema de integración entre herramientas.
- ⬜ **Reflexión crítica**: ventajas, limitaciones, oportunidades de mejora, y qué herramientas de IA
  apoyan el proceso y cómo (apéndice del PACS).

### f) Organización del equipo y roles (5 pts)
*Evalúa: liderazgo, sinergia y reflexión sobre el desempeño.*
- ✅ Roles trazables por etiqueta `rol:*`, autoría de commits, PRs e issues por integrante.
- ⬜ **Evidencia de actividad por rol**: cada integrante con issues/PRs/commits a su nombre.
- ⬜ **Reflexión sobre el desempeño** del equipo y la sinergia entre roles.

---

## 5. Conclusión

La migración de Jira/Confluence a GitHub-native está **cumplida**: el ecosistema soporta,
automatiza y documenta el proceso SQA conforme a los estándares exigidos, y el docente lo observa
en tiempo real sobre un repositorio público. Lo que resta para Fase 2 es **ejecución de pruebas
dinámicas y documentación final** — todo apoyado sobre la infraestructura ya operativa, sin
necesidad de cambios adicionales de plataforma.
