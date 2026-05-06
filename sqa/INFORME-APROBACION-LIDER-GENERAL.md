# Informe de Avance SQA — Revisión para Aprobación del Líder General
**Para:** Alberto Rodríguez (Líder General, Equipo SQA 11)
**De:** Oscar Jaramillo (Líder de Tecnología, Equipo SQA 11)
**Fecha:** 2026-05-06
**Asunto:** Checklists v1.0 + Workflows 1-4 + Análisis Visual + Mejoras Pre-Producción — Pendiente de Aprobación

---

## 1. Resumen Ejecutivo

Se ha desarrollado la infraestructura completa del Sistema de Checklists de Inspección Estática y los 4 Workflows de automatización SQA en modo **dry_run**. Además, se han implementado **3 slices de mejoras pre-producción** que elevan la calidad y confiabilidad del sistema antes de activar producción.

**Estado:** ✅ Listo para revisión. **NO activado en producción** hasta aprobación del Líder General.

**Novedades desde el informe anterior (2026-05-05):**
- **M3+M1:** Extracción automática de imágenes de PDFs + Análisis visual integrado en WF2
- **M2:** Idempotencia en Jira (evita duplicación de tickets en re-runs)
- **M4:** Prompts few-shot para Gemini (reduce falsos positivos)
- **99 tests automatizados, todos pasando** (subió de 74)
- Modelo de IA estandarizado: `gemini-3.1-flash-lite-preview`

---

## 2. Alcance de lo Entregado

### 2.1 Checklists de Inspección Estática (5 documentos JSON)
Cada checklist está basada en **evidencia real** de los artefactos del Equipo 58-1.

| Checklist | Estándar | Artefacto Auditado | Ítems |
|---|---|---|---|
| BRIEF | Prácticas de IR | BRIEF EQUIPO 58 1 - v1.1.pdf | 8 |
| ERS | ISO/IEC/IEEE 29148 | ERS Equipo 58 1 v.1.2.pdf | 13 |
| DAS | ISO/IEC/IEEE 42010 + C4 | DAS Equipo 58-1 v1.5.pdf | 19 |
| Código | ISO/IEC 25010 (estático) | Código fuente Java/Vue | 16 |
| PAC | IEEE 730 | Plan de Aseguramiento de Calidad (Equipo 11) | 15 |

**Total:** 71 ítems de verificación binaria (Cumple / No Cumple / Parcial).

**Mejora v1.1 implementada:** La auditoría de diagramas (C4, UML) ya no se limita a texto extraído de PDFs. El módulo de análisis visual con Gemini multimodal está **integrado en WF2** y analiza automáticamente las imágenes extraídas de los documentos.

### 2.2 Workflows Implementados

| Workflow | Script | GitHub Action | Estado |
|---|---|---|---|
| **WF1** — Auditoría Estática de Requisitos | `scripts/wf1_auditoria_requisitos.py` | `.github/workflows/wf1_auditoria_requisitos.yml` | ✅ dry_run + idempotente |
| **WF2** — Inspección Arquitectónica y Código | `scripts/wf2_inspeccion_arquitectura.py` | `.github/workflows/wf2_inspeccion_arquitectura.yml` | ✅ dry_run + análisis visual |
| **WF3** — Generación del Plan de Pruebas | `scripts/wf3_generacion_pruebas.py` | `.github/workflows/wf3_generacion_pruebas.yml` | ✅ dry_run |
| **WF4** — Orquestador de Quality Gates | `scripts/wf4_orquestador.py` | `.github/workflows/wf4_orquestador.yml` | ✅ dry_run |

**Características comunes:**
- Todos usan `gemini-3.1-flash-lite-preview` para análisis con IA
- Todos usan el núcleo compartido `scripts/sqa_core/`
- Todos generan reportes Markdown locales (NO crean tickets reales aún)

### 2.3 Módulo de Análisis Visual (Integrado en WF2)
- **Script:** `scripts/sqa_core/image_analysis.py`
- **Capacidad:** Analiza imágenes de diagramas C4, UML y wireframes usando Gemini multimodal
- **Salida:** Hallazgos estructurados con severidad (Crítica/Alta/Media/Baja)
- **Estado:** ✅ Integrado en WF2. Extrae imágenes de PDFs automáticamente, clasifica por tipo de diagrama, y mergea hallazgos visuales con hallazgos de texto + SonarQube.
- **Tests:** 99 tests pasando (incluye tests de extracción, conversión PNG, integración visual y degradación graceful)

### 2.4 Mejoras Pre-Producción Implementadas

| Slice | Descripción | Estado | Tests |
|---|---|---|---|
| **M3+M1** | Extracción automática de imágenes de PDFs + Análisis visual en WF2 | ✅ Implementado | 86/86 |
| **M2** | Idempotencia en Jira (search-then-create/update con `external_id`) | ✅ Implementado | 32/32 |
| **M4** | Few-shot prompts para Gemini (reduce falsos positivos) | ✅ Implementado | 99/99 |

**Pendientes (post-aprobación):**
- **M5:** Métricas de cobertura de auditoría (esperando definición del líder de métricas)
- **M6:** Cleanup del POC legacy (`agente_sqa.py`)

---

## 3. Hallazgos Principales (Ejecución de Prueba)

| Artefacto | Cobertura de Revisión | Defectos Detectados | Severidad Crítica |
|---|---|---|---|
| BRIEF | 50.0% | 4 | 0 |
| ERS | 53.8% | 6 | 1 |
| DAS | 57.9% | 8 | 0 |
| **Código** | **12.5%** | **14** | **3** |

### Defectos Críticos Detectados

| ID | Artefacto | Defecto | Impacto |
|---|---|---|---|
| ERS-09 | ERS | HU3: Redundancia exacta en criterios de contraseña (repetido 2 veces) | Riesgo de implementación inconsistente |
| COD-08 | Código | Backend NO valida complejidad de contraseña (ERS exige 8 chars + mayúscula + número + símbolo) | **Brecha de seguridad** |
| COD-09 | Código | Frontend tiene validación de contraseña COMENTADA (RegistroUsuario.vue línea 104) | **Brecha de seguridad** |
| COD-10 | Código | Credenciales de DB hardcodeadas en application.properties (`password=admin`) | **Exposición de credenciales** |
| COD-12 | Código | Sin `@ControllerAdvice` — riesgo de exponer stack traces al usuario | **Fuga de información** |

---

## 4. Correcciones Aplicadas vs Checklists Originales de IA

| Error Original | Corrección Aplicada |
|---|---|
| ERS auditado con INVEST | ERS auditado con ISO/IEC/IEEE 29148 (el ERS real NO usa INVEST) |
| DAS auditado con DDD/Bounded Contexts | DAS auditado con Patrón de Capas + C4 (el DAS real NO usa DDD) |
| Cohesión/acoplamiento invertidos | Terminología corregida según definición formal |
| Análisis estático y dinámico mezclados | Separación explícita: estático (SonarQube) vs dinámico (Playwright, k6) |
| Ítems genéricos sin evidencia | Cada ítem cita página/sección exacta del artefacto real |

---

## 5. Estructura de Archivos en la Rama

```
feature/sdd-workflows-slice-4-wf4
├── .github/workflows/
│   ├── wf1_auditoria_requisitos.yml
│   ├── wf2_inspeccion_arquitectura.yml
│   ├── wf3_generacion_pruebas.yml
│   └── wf4_orquestador.yml
├── scripts/
│   ├── sqa_core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── clients.py          ← M2: upsert_issue con idempotencia
│   │   ├── pdf_text.py         ← M3: extract_images_from_pdf()
│   │   ├── reporting.py
│   │   └── image_analysis.py   ← M1+M4: análisis visual + few-shot
│   ├── wf1_auditoria_requisitos.py   ← M2+M4: idempotencia + few-shot
│   ├── wf2_inspeccion_arquitectura.py ← M1+M2+M4: visual + idempotencia + few-shot
│   ├── wf3_generacion_pruebas.py
│   ├── wf4_orquestador.py
│   └── agente_sqa.py              ← POC (obsoleto, será removido en M6)
├── tests/scripts/                  ← 99 tests
│   ├── test_sqa_core_config.py
│   ├── test_sqa_core_clients.py    ← M2: tests de idempotencia
│   ├── test_sqa_core_pdf_text.py   ← M3: tests de extracción de imágenes
│   ├── test_sqa_core_reporting.py
│   ├── test_sqa_core_image_analysis.py ← M1+M4: tests de visual + few-shot
│   ├── test_wf1_auditoria_requisitos.py ← M2+M4: idempotencia + few-shot
│   ├── test_wf2_inspeccion_arquitectura.py ← M1+M2+M4: visual + idempotencia + few-shot
│   ├── test_wf3_generacion_pruebas.py
│   └── test_wf4_orquestador.py
├── sqa/
│   ├── Checklists-Inspeccion-Estatica-v1.md
│   ├── PACS-Fase2-Herramientas.md
│   ├── WF4-MODO-PRODUCCION.md
│   ├── ROADMAP-MEJORAS-PRE-PRODUCCION.md
│   ├── checklists/
│   │   ├── brief.json
│   │   ├── ers.json
│   │   ├── das.json
│   │   ├── codigo.json
│   │   └── pac.json
│   └── reportes/
└── requirements.txt                ← M3: Pillow agregado
```

**Importante:** Esta rama NO modifica el código fuente del Equipo 58-1 (carpetas `src/`, `biblioteca-frontend/src/`). Solo agrega infraestructura SQA.

---

## 6. Métricas de Calidad del Código SQA

| Métrica | Valor |
|---|---|
| Tests totales | 99 |
| Tests pasando | 99 (100%) |
| Cobertura estimada | >90% (sqa_core) |
| Commits work-unit | 16 |
| Líneas de código Python SQA | ~2.800 |

---

## 7. Requisitos para Activar a Producción

1. **Aprobación del Líder General** (Alberto Rodríguez) — ✅ Este informe
2. **Aprobación del Líder Funcional** (Daniel) — Validación de mapeo artefacto→estándar
3. **Configurar secrets en GitHub:**
   - `JIRA_SERVER`, `JIRA_EMAIL`, `JIRA_API_TOKEN`
   - `CONFLUENCE_URL`, `CONFLUENCE_API_TOKEN`
   - `GEMINI_API_KEY`
   - `SONARQUBE_TOKEN` (para WF2)
4. **Cambiar `DRY_RUN: true` → `false`** en cada workflow YAML
5. **Activar `WF4_ORCHESTRATE_UPSTREAM=true`** para encadenamiento automático

El documento `sqa/WF4-MODO-PRODUCCION.md` contiene el procedimiento detallado.

---

## 8. Riesgos Identificados

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| Gemini quota exceeded en ejecución real | Media | Media | Retry/backoff implementado; fallback a modo texto; few-shot prompts mejoran precisión (M4) |
| SonarQube no disponible para WF2 | Baja | Alta | WF2 funciona sin SonarQube (solo con análisis DAS + visual) |
| Formato de imágenes incrustadas en PDFs | Baja | Media | Pillow convierte automáticamente a PNG válido (M3); imágenes corruptas se omiten graceful |
| Métricas de cobertura no definidas | Media | Baja | M5 postergado a espera de definición del líder de métricas |

**Riesgos MITIGADOS desde versión anterior:**
- ✅ Duplicación de tickets en re-runs — RESUELTO por M2 (idempotencia con `external_id`)
- ✅ Análisis visual de diagramas pendiente — RESUELTO por M1 (integrado en WF2)

---

## 9. Próximos Pasos Post-Aprobación

1. **Fusionar** la rama tracker `feature/sdd-workflows-slice-4-wf4` a `main`
2. **Configurar secrets** en GitHub
3. **Ejecutar WF4** con `WF4_ORCHESTRATE_UPSTREAM=true` en modo dry_run final
4. **Definir métricas de cobertura** (M5) con el líder de métricas
5. **Activar producción:** Cambiar `DRY_RUN=false` y crear tickets reales
6. **Cleanup legacy:** Remover `agente_sqa.py` y workflow obsoleto (M6)

---

## 10. Decisión Requerida

**¿Aprueba el Líder General (Alberto Rodríguez) las siguientes acciones?**

- [ ] **Aprobar las checklists v1.0** tal como están documentadas en `sqa/Checklists-Inspeccion-Estatica-v1.md`
- [ ] **Aprobar los Workflows 1-4** para pasar a producción (con mejoras M1-M4 aplicadas)
- [ ] **Autorizar la fusión** de la rama `feature/sdd-workflows-slice-4-wf4` a `main`
- [ ] **Aprobar la matriz de herramientas** declarada en `sqa/PACS-Fase2-Herramientas.md`
- [ ] **Autorizar ejecución de auditoría visual** sobre diagramas del DAS (ya integrada en WF2)

**Nota:** Hasta recibir esta aprobación, TODO permanece en modo `dry_run`. No se crearán tickets, no se modificará Confluence, y no se ejecutarán pruebas dinámicas.

---

*Informe generado por el Equipo SQA 11*
*Rama tracker: `feature/sdd-workflows-slice-4-wf4`*
*Commits: 16 work-unit commits, 99 tests passing*
*Mejoras implementadas: M3+M1 (Análisis Visual), M2 (Idempotencia Jira), M4 (Few-shot Prompts)*
