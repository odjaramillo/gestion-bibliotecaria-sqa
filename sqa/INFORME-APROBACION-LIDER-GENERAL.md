# Informe de Avance SQA — Revisión para Aprobación del Líder General
**Para:** Alberto Rodríguez (Líder General, Equipo SQA 11)  
**De:** Oscar Jaramillo (Líder de Tecnología, Equipo SQA 11)  
**Fecha:** 2026-05-05  
**Asunto:** Checklists de Inspección Estática + Workflow 4 — Pendiente de Aprobación

---

## 1. Resumen Ejecutivo

Se ha desarrollado la infraestructura base del Sistema de Checklists de Inspección Estática y el Workflow 4 (Orquestador de Quality Gates) en modo **dry_run** (sin impactar Jira ni Confluence).

**Estado:** ✅ Listo para revisión. **NO activado en producción** hasta aprobación del Líder General.

---

## 2. Alcance de lo Entregado

### 2.1 Checklists de Inspección Estática (5 documentos)
Cada checklist está basada en **evidencia real** de los artefactos del Equipo 58-1 (NO son plantillas genéricas).

| Checklist | Estándar | Artefacto Auditado | Ítems |
|---|---|---|---|
| BRIEF | Prácticas de IR | BRIEF EQUIPO 58 1 - v1.1.pdf | 8 |
| ERS | ISO/IEC/IEEE 29148 | ERS Equipo 58 1 v.1.2.pdf | 13 |
| DAS | ISO/IEC/IEEE 42010 + C4 | DAS Equipo 58-1 v1.5.pdf | 19 |
| Código | ISO/IEC 25010 (estático) | Código fuente Java/Vue | 16 |
| PAC | IEEE 730 | Plan de Aseguramiento de Calidad (Equipo 11) | 15 |

**Total:** 71 ítems de verificación binaria (Cumple / No Cumple / Parcial).

### 2.2 Workflow 4 — Orquestador de Quality Gates
- **Script Python:** `scripts/wf4_orquestador.py`
- **GitHub Action:** `.github/workflows/wf4_orquestador.yml`
- **Modo:** `dry_run = true` (NO crea tickets reales)
- **Salida:** Reporte Markdown en `sqa/reportes/`

### 2.3 Matriz de Herramientas Fase 2
Documento complementario declarando las herramientas tecnológicas que se usarán en la Fase 2 (Pruebas Dinámicas), con justificación técnica de cada elección.

---

## 3. Hallazgos Principales (Ejecución de Prueba)

Se ejecutó el WF4 en modo simulado sobre los artefactos reales. Resultados:

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

### Defectos de Alta Severidad
- **ERS-07:** HU5 tiene contradicción interna (regla dice "una amonestación", criterio dice "una o varias")
- **DAS-05:** Decisiones arquitectónicas con fechas futuras imposibles (21/06 y 26/06 en doc del 17/06)
- **COD-01:** Controller monolítico de 458 líneas manejando 6 dominios (viola SRP)
- **COD-06:** Dependencia duplicada en pom.xml

---

## 4. Correcciones Aplicadas vs Checklists Originales de IA

Las checklists originales (generadas por IA genérica) tenían errores graves que fueron corregidos:

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
feature/sqa-checklists-wf4
├── .github/workflows/
│   └── wf4_orquestador.yml          ← GitHub Action (modo dry_run)
├── scripts/
│   └── wf4_orquestador.py           ← Orquestador Python
├── sqa/
│   ├── Checklists-Inspeccion-Estatica-v1.md   ← Documento maestro
│   ├── PACS-Fase2-Herramientas.md             ← Matriz de herramientas
│   ├── WF4-MODO-PRODUCCION.md                 ← Guía de activación
│   ├── checklists/
│   │   ├── brief.json
│   │   ├── ers.json
│   │   ├── das.json
│   │   ├── codigo.json
│   │   └── pac.json
│   └── reportes/
│       └── 2026-05-05_07-19-05_wf4_reporte.md ← Reporte de prueba
└── requirements.txt                  ← Dependencias Python
```

**Importante:** Esta rama NO modifica el código fuente del Equipo 58-1 (carpetas `src/`, `biblioteca-frontend/src/`). Solo agrega infraestructura SQA.

---

## 6. Requisitos para Activar a Producción

Una vez aprobado este informe, se requieren los siguientes cambios para pasar de `dry_run` a producción:

1. **Aprobación del Líder General** (Alberto Rodríguez) — ✅ Este informe
2. **Configurar secrets en GitHub:**
   - `JIRA_SERVER`, `JIRA_EMAIL`, `JIRA_API_TOKEN`
   - `CONFLUENCE_URL`, `CONFLUENCE_API_TOKEN`
   - `GEMINI_API_KEY` (para auditoría con IA en WF1)
3. **Cambiar `DRY_RUN: true` → `false`** en `.github/workflows/wf4_orquestador.yml`
4. **Descomentar bloques de código** marcados con `# PRODUCCION:` en `scripts/wf4_orquestador.py`
5. **Instalar PyMuPDF** (comentado actualmente para extracción de texto de PDFs)

El documento `sqa/WF4-MODO-PRODUCCION.md` contiene el procedimiento detallado.

---

## 7. Riesgos Identificados

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| El docente cuestione el descarte de INVEST | Media | Media | Justificación documentada: el ERS no declara INVEST |
| Fechas futuras del DAS sean atribuidas a nosotros | Baja | Alta | Evidencia con página exacta (Pág. 5, ID-5 e ID-6) |
| Checklists sean consideradas "demasiado duras" | Media | Media | Cada ítem está justificado con estándar y evidencia |
| Falta de tiempo para implementar WF1-WF3 | Alta | Alta | WF4 es la base; WF1-WF3 se pueden paralelizar |

---

## 8. Próximos Pasos Sugeridos

Una vez aprobado este informe:

1. **Fusionar esta rama a `main`** (solo infraestructura SQA, no toca código del SUT)
2. **Implementar WF1** — Auditoría Estática de Requisitos (extracción IA de PDFs, validación 29148)
3. **Implementar WF2** — Inspección Arquitectónica (SonarQube, análisis estático de código)
4. **Implementar WF3** — Generación del Plan de Pruebas (Casos de Prueba en Jira, esqueletos de código)

---

## 9. Decisión Requerida

**¿Aprueba el Líder General (Alberto Rodríguez) las siguientes acciones?**

- [ ] **Aprobar las checklists** tal como están documentadas en `sqa/Checklists-Inspeccion-Estatica-v1.md`
- [ ] **Aprobar el Workflow 4** para pasar a producción (crear tickets reales en Jira)
- [ ] **Autorizar la fusión** de la rama `feature/sqa-checklists-wf4` a `main`
- [ ] **Aprobar la matriz de herramientas** declarada en `sqa/PACS-Fase2-Herramientas.md`

**Nota:** Hasta recibir esta aprobación, TODO permanece en modo `dry_run`. No se crearán tickets, no se modificará Confluence, y no se ejecutarán pruebas dinámicas.

---

*Informe generado automáticamente por el Equipo SQA 11*  
*Rama: `feature/sqa-checklists-wf4`*  
*Commit: `b250db6`*
