# Informe de Avance SQA — Revisión para Aprobación del Líder General
**Para:** Alberto Rodríguez (Líder General, Equipo SQA 11)  
**De:** Oscar Jaramillo (Líder de Tecnología, Equipo SQA 11)  
**Fecha:** 2026-05-05  
**Asunto:** Checklists v1.0 + Workflows 1-4 + Análisis Visual — Pendiente de Aprobación

---

## 1. Resumen Ejecutivo

Se ha desarrollado la infraestructura completa del Sistema de Checklists de Inspección Estática y los 4 Workflows de automatización SQA en modo **dry_run**.

**Estado:** ✅ Listo para revisión. **NO activado en producción** hasta aprobación del Líder General.

**Novedades desde el informe anterior:**
- WF1, WF2, WF3 implementados formalmente (no solo WF4)
- Módulo de análisis visual de diagramas con IA (Gemini multimodal)
- 74 tests automatizados, todos pasando
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

**Limitación conocida v1.0:** La auditoría de diagramas (C4, UML) en las checklists se basa en texto extraído de PDFs. Se detectaron 30+ imágenes incrustadas en los documentos que aún no fueron auditadas visualmente. El módulo de análisis visual está implementado y listo para usarse en v1.1.

### 2.2 Workflows Implementados

| Workflow | Script | GitHub Action | Estado |
|---|---|---|---|
| **WF1** — Auditoría Estática de Requisitos | `scripts/wf1_auditoria_requisitos.py` | `.github/workflows/wf1_auditoria_requisitos.yml` | ✅ dry_run |
| **WF2** — Inspección Arquitectónica y Código | `scripts/wf2_inspeccion_arquitectura.py` | `.github/workflows/wf2_inspeccion_arquitectura.yml` | ✅ dry_run |
| **WF3** — Generación del Plan de Pruebas | `scripts/wf3_generacion_pruebas.py` | `.github/workflows/wf3_generacion_pruebas.yml` | ✅ dry_run |
| **WF4** — Orquestador de Quality Gates | `scripts/wf4_orquestador.py` | `.github/workflows/wf4_orquestador.yml` | ✅ dry_run |

**Características comunes:**
- Todos usan `gemini-3.1-flash-lite-preview` para análisis con IA
- Todos usan el núcleo compartido `scripts/sqa_core/`
- Todos generan reportes Markdown locales (NO crean tickets reales aún)

### 2.3 Módulo de Análisis Visual (Nuevo)
- **Script:** `scripts/sqa_core/image_analysis.py`
- **Capacidad:** Analiza imágenes de diagramas C4, UML y wireframes usando Gemini multimodal
- **Salida:** Hallazgos estructurados con severidad (Crítica/Alta/Media/Baja)
- **Estado:** Implementado y testeado (12 tests). Pendiente de integrar en WF2 para v1.1.

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
feature/sdd-workflows
├── .github/workflows/
│   ├── wf1_auditoria_requisitos.yml
│   ├── wf2_inspeccion_arquitectura.yml
│   ├── wf3_generacion_pruebas.yml
│   └── wf4_orquestador.yml
├── scripts/
│   ├── sqa_core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── clients.py
│   │   ├── pdf_text.py
│   │   ├── reporting.py
│   │   └── image_analysis.py      ← NUEVO: análisis visual
│   ├── wf1_auditoria_requisitos.py
│   ├── wf2_inspeccion_arquitectura.py
│   ├── wf3_generacion_pruebas.py
│   ├── wf4_orquestador.py
│   └── agente_sqa.py              ← POC (obsoleto, será removido)
├── tests/scripts/                  ← NUEVO: 74 tests
│   ├── test_sqa_core_config.py
│   ├── test_sqa_core_clients.py
│   ├── test_sqa_core_pdf_text.py
│   ├── test_sqa_core_reporting.py
│   ├── test_sqa_core_image_analysis.py
│   ├── test_wf1_auditoria_requisitos.py
│   ├── test_wf2_inspeccion_arquitectura.py
│   ├── test_wf3_generacion_pruebas.py
│   └── test_wf4_orquestador.py
├── sqa/
│   ├── Checklists-Inspeccion-Estatica-v1.md
│   ├── PACS-Fase2-Herramientas.md
│   ├── WF4-MODO-PRODUCCION.md
│   ├── checklists/
│   │   ├── brief.json
│   │   ├── ers.json
│   │   ├── das.json
│   │   ├── codigo.json
│   │   └── pac.json
│   └── reportes/
└── requirements.txt
```

**Importante:** Esta rama NO modifica el código fuente del Equipo 58-1 (carpetas `src/`, `biblioteca-frontend/src/`). Solo agrega infraestructura SQA.

---

## 6. Métricas de Calidad del Código SQA

| Métrica | Valor |
|---|---|
| Tests totales | 74 |
| Tests pasando | 74 (100%) |
| Cobertura estimada | >90% (sqa_core) |
| Commits work-unit | 14 |
| Líneas de código Python SQA | ~2.500 |

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
| Checklists v1.0 no cubren análisis visual de diagramas | Alta | Media | Módulo implementado; se integrará en v1.1 post-aprobación |
| Gemini quota exceeded en ejecución real | Media | Media | Retry/backoff implementado; fallback a modo texto |
| SonarQube no disponible para WF2 | Baja | Alta | WF2 funciona sin SonarQube (solo con análisis DAS) |
| Duplicación de tickets en re-runs | Media | Media | Idempotencia por checksum pendiente para v1.1 |

---

## 9. Próximos Pasos Post-Aprobación

1. **Fusionar** la rama tracker `feature/sdd-workflows` a `main`
2. **Configurar secrets** en GitHub
3. **Ejecutar WF4** con `WF4_ORCHESTRATE_UPSTREAM=true` en modo dry_run final
4. **Auditoría visual v1.1:** Ejecutar análisis de imágenes sobre los 30+ diagramas del DAS
5. **Activar producción:** Cambiar `DRY_RUN=false` y crear tickets reales

---

## 10. Decisión Requerida

**¿Aprueba el Líder General (Alberto Rodríguez) las siguientes acciones?**

- [ ] **Aprobar las checklists v1.0** tal como están documentadas en `sqa/Checklists-Inspeccion-Estatica-v1.md`
- [ ] **Aprobar los Workflows 1-4** para pasar a producción
- [ ] **Autorizar la fusión** de la rama `feature/sdd-workflows` a `main`
- [ ] **Aprobar la matriz de herramientas** declarada en `sqa/PACS-Fase2-Herramientas.md`
- [ ] **Autorizar ejecución de auditoría visual v1.1** sobre diagramas del DAS (post-merge)

**Nota:** Hasta recibir esta aprobación, TODO permanece en modo `dry_run`. No se crearán tickets, no se modificará Confluence, y no se ejecutarán pruebas dinámicas.

---

*Informe generado por el Equipo SQA 11*  
*Rama tracker: `feature/sdd-workflows`*  
*Commits: 14 work-unit commits, 74 tests passing*
