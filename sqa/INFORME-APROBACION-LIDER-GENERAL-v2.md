# Propuesta de Infraestructura SQA Automatizada — Equipo 11
## Solicitud de Aprobación para el Líder General

**Para:** Alberto Rodríguez (Líder General, Equipo SQA 11)  
**De:** Oscar Jaramillo (Líder de Tecnología, Equipo SQA 11)  
**Fecha:** 2026-05-06  
**Asunto:** Presentación formal del Sistema de Automatización SQA desarrollado para auditar al Equipo 58-1

---

## 1. ¿Qué es esto y por qué lo hicimos?

El **Equipo 11** (SQA) tiene la misión de auditar el Sistema de Gestión Bibliotecaria desarrollado por el **Equipo 58-1**. Este sistema incluye:

- Documentación: BRIEF, ERS, DAS (PDFs)
- Código: Java 21 + Spring Boot (backend) + Vue 3 (frontend)
- 71 ítems de verificación de calidad que debemos revisar

**El problema:** Hacer esta auditoría manualmente toma semanas, es repetitiva, y es propenso a errores humanos. Además, algunos defectos solo se detectan analizando código o imágenes de diagramas con herramientas automatizadas.

**La solución que desarrollamos:** Un sistema de **6 workflows automatizados** que:
1. Leen los PDFs y código del Equipo 58-1
2. Aplican checklists de inspección basadas en estándares ISO/IEEE
3. Usan Inteligencia Artificial (Gemini) para detectar defectos que un humano podría pasar por alto
4. Generan reportes y tickets de seguimiento automáticamente
5. Generan el Plan de Aseguramiento de Calidad (PAC) de forma semi-automatizada

**Todo está en modo "simulación" (dry_run).** No hemos creado ningún ticket real ni modificado nada del Equipo 58-1. Este informe es para pedir tu aprobación antes de activarlo.

---

## 2. ¿Qué entregamos?

### 2.1 Checklists de Inspección Estática (5 documentos)

Basados en evidencia real de los artefactos del Equipo 58-1. Cada ítem cita página y sección exacta.

| Checklist | Estándar Internacional | Artefacto Auditado | Ítems |
|---|---|---|---|
| BRIEF | Prácticas de Ingeniería de Requisitos | BRIEF EQUIPO 58 1 - v1.1.pdf | 8 |
| ERS | ISO/IEC/IEEE 29148:2018 | ERS Equipo 58 1 v.1.2.pdf | 13 |
| DAS | ISO/IEC/IEEE 42010:2022 + C4 | DAS Equipo 58-1 v1.5.pdf | 19 |
| Código | ISO/IEC 25010 (estático) | Código Java/Vue | 16 |
| PAC | IEEE 730-2014 | Plan de Aseguramiento de Calidad | 15 |

**Total: 71 ítems de verificación.**

**¿Por qué esto es diferente a auditar "a mano"?**
- Cada ítem está **atado a evidencia concreta** (página X, línea Y del PDF)
- Usamos los **estándares que el artefacto declara seguir**, no estándares genéricos
- Los resultados se guardan automáticamente en formatos estructurados (JSON + Markdown)

---

### 2.2 Workflows Automatizados (6 scripts + GitHub Actions)

| Workflow | Qué hace | Para qué sirve |
|---|---|---|
| **WF1** — Auditoría de Requisitos | Lee el BRIEF/ERS, aplica checklist, detecta defectos con IA | Encuentra inconsistencias, versiones desfasadas, requisitos incompletos |
| **WF2** — Inspección Arquitectónica | Lee el DAS + imágenes de diagramas + datos de SonarQube | Detecta errores en diagramas C4, decisiones arquitectónicas inconsistentes, code smells |
| **WF3** — Plan de Pruebas | Genera casos de prueba automáticamente a partir de los requisitos | Acelera la creación de pruebas dinámicas (Fase 2) |
| **WF4** — Orquestador | Coordina WF1+WF2+WF3 y genera un reporte consolidado de Quality Gate | Da una visión única del estado de calidad del proyecto |
| **WF5** — Generador PAC | Lee el stack del proyecto, inventaria artefactos y genera el PAC estructurado | Reduce de horas a minutos la escritura del Plan de Aseguramiento de Calidad |
| **WF6** — Auditor PAC | Valida que el PAC cumple con los 15 ítems de la checklist IEEE 730-2014 | Garantiza que el plan no omita ningún apartado del estándar |

**Características técnicas:**
- Todo corre en **GitHub Actions** (pipelines automatizados en cada push)
- Usan el modelo de IA **Gemini** (Google) para análisis inteligente
- Generan reportes en **Markdown** (legibles) y **JSON** (procesables por otras herramientas)
- **NO modifican el código del Equipo 58-1** — solo auditan

---

### 2.3 Mejoras Implementadas (Pre-Producción)

Antes de pedirte la aprobación, implementamos 5 mejoras críticas:

#### Mejora 1 (M1): Análisis Visual de Diagramas con IA
**¿El problema?** Los diagramas C4 y UML del DAS están en PDFs como imágenes. Un análisis de texto no puede ver si una flecha falta o si un actor está ausente.

**¿La solución?**
- Extraemos automáticamente las imágenes de los PDFs
- La IA (Gemini multimodal) "mira" los diagramas y detecta defectos visuales
- Ejemplos de lo que detecta: *"Actor externo mencionado en el ERS pero ausente en el diagrama"*, *"Relación sin dirección ni protocolo"*

#### Mejora 2 (M2): Idempotencia en Jira
**¿El problema?** Si el workflow se ejecuta 2 veces, crearía tickets duplicados en Jira.

**¿La solución?** Antes de crear un ticket, buscamos si ya existe uno con el mismo identificador. Si existe, lo actualizamos en lugar de duplicarlo.

#### Mejora 3 (M3): Mejores Prompts de IA (Few-Shot)
**¿El problema?** La IA a veces reporta "defectos" que en realidad son preferencias estilísticas (falsos positivos).

**¿La solución?** Le enseñamos a la IA con ejemplos concretos: *"Esto SÍ es un defecto"* vs *"Esto NO es un defecto, es solo cosmético"*. Esto reduce los falsos positivos.

#### Mejora 4 (M4): Corrección Crítica — Extracción de Imágenes
**¿El problema?** Los checklists validaban imágenes de PDFs pero el motor NO las extraía.

**¿La solución?** Detectamos que los checklists validaban imágenes de PDFs pero el motor NO las extraía. Implementamos extracción automática de imágenes de PDFs para asegurar que la auditoría sea completa. Las imágenes extraídas se encuentran en `sqa/extracted_images/`.

#### Mejora 5 (M7): Generación Semi-Automatizada del PAC
**¿El problema?** El Plan de Aseguramiento de Calidad (PAC) se escribe manualmente. Eso genera secciones repetitivas, riesgo de omitir apartados del estándar IEEE 730-2014, y desfasaje entre el stack real del sistema y lo que declara el plan.

**¿La solución?**
- **Generador semi-automatizado** (`scripts/wf_pac_generator.py`): Lee el stack del proyecto (`pom.xml`, `package.json`), inventaria artefactos y genera un PAC estructurado en segundos. El output es `sqa/pac_generado.md`.
- **Auditor de PAC** (`scripts/wf_pac_auditor.py`): Valida que el PAC cumple con los 15 ítems de la checklist IEEE 730-2014.
- **Template de configuración** (`sqa/templates/pac_config.yaml`): El líder de métricas completa una planilla YAML con objetivos de calidad (ISO 25010) con pesos, roles del equipo, umbrales de métricas, riesgos identificados y mitigaciones, y cronograma por fase.
- Incorpora las métricas que nos proporcionó el líder: **Cobertura de Revisiones** (meta: 100%) y **Densidad de Defectos** (meta: 0.5 defectos/KLOC).

---

## 3. Hallazgos que ya detectamos (ejemplo)

Ejecutamos los workflows en modo simulación y ya encontramos defectos reales:

| Artefacto | Defecto | Severidad |
|---|---|---|
| BRIEF | Backlog en formato visual (imagen) sin referencia textual — dificulta trazabilidad automática | Media |
| ERS | Versión en portada (1.1) no coincide con histórico (1.2) | Media |
| ERS | Contradicción interna: regla dice "una amonestación a la vez", criterio dice "una o varias" | **Crítica** |
| DAS | Fechas de decisiones arquitectónicas posteriores a la fecha del documento | **Crítica** |
| DAS | Error conceptual: "alto cohesivo" aplicado a un SPA | Media |
| Código | Backend NO valida complejidad de contraseña (a pesar de que el ERS lo exige) | **Brecha de seguridad** |
| Código | Validación de contraseña en frontend está COMENTADA | **Brecha de seguridad** |
| Código | Credenciales de base de datos hardcodeadas (`password=admin`) | **Exposición de credenciales** |
| Código | Sin manejo global de excepciones — riesgo de exponer stack traces al usuario | **Fuga de información** |

**Nota importante sobre validación:** Durante la preparación de este informe detectamos que parte del contenido de los PDFs (especialmente del BRIEF y DAS) está en formato de imágenes (tablas, diagramas), no solo en texto. Por eso implementamos extracción automática de imágenes de PDFs para asegurar que la auditoria sea completa. Las imágenes extraídas se encuentran en `sqa/extracted_images/`.

---

## 4. ¿Qué necesitamos para activar producción?

### Paso 1: Tu aprobación como Líder General
Necesitamos que apruebes:
- Las 5 checklists de inspección (estándares aplicados, ítems verificables)
- Los 6 workflows automatizados (funcionamiento técnico)
- La fusión de esta rama al repositorio principal (`main`)

### Paso 2: Aprobación del Líder Funcional (Daniel)
Que valide que el mapeo artefacto→estándar es correcto.

### Paso 3: Configurar credenciales en GitHub
Secrets necesarios (nosotros no los tenemos, son del proyecto):
- `JIRA_SERVER`, `JIRA_EMAIL`, `JIRA_API_TOKEN`
- `CONFLUENCE_URL`, `CONFLUENCE_API_TOKEN`
- `GEMINI_API_KEY`
- `SONARQUBE_TOKEN` (opcional, para WF2)

### Paso 4: Activar
Una vez configurado, cambiamos de `DRY_RUN=true` (simulación) a `DRY_RUN=false` (producción).

---

## 5. ¿Qué pasa si no se aprueba?

| Escenario | Impacto |
|---|---|
| **Sin aprobación** | Seguimos auditando manualmente. Más lento, más errores humanos, no escalable. |
| **Sin análisis visual** | Los defectos en diagramas (flechas faltantes, actores ausentes) pasan desapercibidos. |
| **Sin idempotencia** | Si ejecutamos 2 veces, duplicamos tickets en Jira. Caos en el seguimiento. |
| **Sin few-shot** | La IA genera más falsos positivos. El equipo pierde tiempo revisando "defectos" que no lo son. |
| **Sin generador PAC** | El Plan de Aseguramiento de Calidad se escribe a mano durante horas, con riesgo de omitir apartados del estándar IEEE 730-2014. |

---

## 6. Métricas de Calidad de lo que construimos

| Métrica | Valor | Significado |
|---|---|---|
| Tests automatizados | 154 | Cada función crítica tiene un test que la verifica |
| Tests pasando | 154/154 (100%) | Nada está roto |
| Cobertura estimada | >90% | La mayoría del código SQA está probado |
| Commits | 130 | Cada cambio fue un "paquete" coherente (código + tests juntos) |
| Líneas de código SQA | ~8.100 | Sistema completo pero enfocado |
| Scripts SQA | 6 workflows (WF1-WF4 + PAC Generator + PAC Auditor) | Cada workflow cubre una fase de auditoría o generación de documentos |
| Checklists | 5 documentos, 71 ítems de verificación | Cobertura completa de estándares ISO/IEEE |
| Documentación técnica | 6 informes | Referencia técnica para el equipo y los líderes |

---

## 7. Riesgos y Mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| La IA se queda sin quota (Gemini) | Media | Media | Tenemos retry automático + fallback a modo texto |
| SonarQube no está disponible | Baja | Alta | WF2 funciona igual solo con análisis de documentos + visual |
| Imágenes de PDFs en formato raro | Baja | Media | Convertimos automáticamente a PNG. Si falla, se omite graceful |
| Duplicación de tickets (re-run) | **Resuelto** | — | M2 implementa idempotencia con búsqueda previa en Jira |
| Planilla PAC incompleta | Media | Media | El auditor detecta campos vacíos y devuelve `[COMPLETAR]` |

---

## 8. Estructura del Repositorio

```
gestion-bibliotecaria-sqa/
├── src/                          ← Código del Equipo 58-1 (NO TOCAMOS)
├── biblioteca-frontend/src/      ← Frontend del Equipo 58-1 (NO TOCAMOS)
├── documentacion/                ← PDFs del Equipo 58-1 (NO TOCAMOS)
├── scripts/
│   ├── sqa_core/                 ← Motor SQA compartido
│   │   ├── image_analysis.py
│   │   ├── pdf_text.py
│   │   ├── clients.py
│   │   ├── reporting.py
│   │   └── config.py
│   ├── lib/pac_generator/        ← ← ← NUEVO: Librerías del generador PAC
│   │   ├── config_reader.py
│   │   ├── stack_discoverer.py
│   │   ├── artifact_inventory.py
│   │   ├── gemini_client.py
│   │   ├── pac_assembler.py
│   │   └── report_writer.py
│   ├── wf1_auditoria_requisitos.py
│   ├── wf2_inspeccion_arquitectura.py
│   ├── wf3_generacion_pruebas.py
│   ├── wf4_orquestador.py
│   ├── wf_pac_generator.py       ← ← ← NUEVO
│   └── wf_pac_auditor.py         ← ← ← NUEVO
├── tests/scripts/                ← 154 tests automatizados
├── sqa/
│   ├── Checklists-Inspeccion-Estatica-v1.md
│   ├── PACS-Fase2-Herramientas.md
│   ├── ROADMAP-MEJORAS-PRE-PRODUCCION.md
│   ├── WF4-MODO-PRODUCCION.md
│   ├── M7-Informe-Lider.md       ← ← ← NUEVO
│   ├── templates/
│   │   └── pac_config.yaml       ← ← ← NUEVO
│   ├── checklists/               ← 5 checklists JSON
│   ├── reportes/                 ← Reportes generados
│   └── extracted_images/         ← Imágenes extraídas de PDFs
└── .github/workflows/            ← Pipelines de CI/CD
```

---

## 9. M7 — Plan de Aseguramiento de Calidad (PAC)

### ¿Qué es?
El PAC es el documento que define cómo garantizamos la calidad del sistema. Seguimos el estándar IEEE 730-2014.

### ¿Qué desarrollamos?
- **Generador semi-automatizado** (`scripts/wf_pac_generator.py`): Lee el stack del proyecto, inventaria artefactos, y genera un PAC estructurado en segundos.
- **Auditor de PAC** (`scripts/wf_pac_auditor.py`): Valida que el PAC cumple con los 15 ítems de la checklist IEEE 730-2014.
- **Template de configuración** (`sqa/templates/pac_config.yaml`): El líder de métricas completa una planilla YAML con objetivos, roles, umbrales y cronograma.

### ¿Qué necesita el líder de métricas?
Completar la planilla `pac_config.yaml` con:
- Objetivos de calidad (ISO 25010) con pesos
- Roles del equipo SQA
- Umbrales de métricas (Cobertura de Revisiones: 100%, Densidad de Defectos: 0.5 defectos/KLOC)
- Riesgos identificados y mitigaciones
- Cronograma por fase

### ¿Qué se genera automáticamente?
- Stack tecnológico (de `pom.xml` y `package.json`)
- Inventario de artefactos (PDFs + código fuente)
- Estándares aplicables (de las checklists)
- Herramientas tecnológicas
- CI/CD (de `.github/workflows/`)

### Estado
- ✅ Generador implementado y testeado (55 tests)
- ✅ Auditor implementado y testeado (15 tests)
- ✅ Template con instrucciones listo
- ⏳ Pendiente: Líder de métricas completa la planilla

---

## 10. Decisión Requerida del Líder General

**¿Aprueba el Líder General (Alberto Rodríguez) las siguientes acciones?**

- [ ] **Aprobar las 5 checklists de inspección** documentadas en `sqa/Checklists-Inspeccion-Estatica-v1.md`
- [ ] **Aprobar los 6 workflows automatizados** para su uso en producción
- [ ] **Autorizar la fusión** de esta rama al repositorio principal (`main`)
- [ ] **Aprobar la matriz de herramientas** declarada en `sqa/PACS-Fase2-Herramientas.md`
- [ ] **Autorizar la activación** de `DRY_RUN=false` una vez configuradas las credenciales
- [ ] **Aprobar el generador semi-automatizado de PAC** (M7) y su checklist IEEE 730-2014

**Hasta recibir esta aprobación, TODO permanece en modo simulación.** No se crearán tickets reales, no se modificará Confluence, y no se tocará el código del Equipo 58-1.

---

## Anexos para Revisión

| Documento | Descripción | Ubicación |
|---|---|---|
| Checklists de Inspección | 71 ítems de verificación con evidencia | `sqa/Checklists-Inspeccion-Estatica-v1.md` |
| Matriz de Herramientas | Herramientas declaradas para Fase 1 y Fase 2 | `sqa/PACS-Fase2-Herramientas.md` |
| Reportes de prueba | Ejemplos de reportes generados por WF4 | `sqa/reportes/` |
| Roadmap de mejoras | Mejoras pendientes post-aprobación | `sqa/ROADMAP-MEJORAS-PRE-PRODUCCION.md` |
| M7 — Informe para el Líder | Guía de uso del generador PAC | `sqa/M7-Informe-Lider.md` |
| Plantilla PAC | Template YAML para el líder de métricas | `sqa/templates/pac_config.yaml` |

---

*Documento generado por el Equipo SQA 11*  
*Fecha: 2026-05-06*  
*Estado: Pendiente de aprobación del Líder General*
