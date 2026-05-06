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

**La solución que desarrollamos:** Un sistema de **4 workflows automatizados** que:
1. Leen los PDFs y código del Equipo 58-1
2. Aplican checklists de inspección basadas en estándares ISO/IEEE
3. Usan Inteligencia Artificial (Gemini) para detectar defectos que un humano podría pasar por alto
4. Generan reportes y tickets de seguimiento automáticamente

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

### 2.2 Workflows Automatizados (4 scripts + GitHub Actions)

| Workflow | Qué hace | Para qué sirve |
|---|---|---|
| **WF1** — Auditoría de Requisitos | Lee el BRIEF/ERS, aplica checklist, detecta defectos con IA | Encuentra inconsistencias, versiones desfasadas, requisitos incompletos |
| **WF2** — Inspección Arquitectónica | Lee el DAS + imágenes de diagramas + datos de SonarQube | Detecta errores en diagramas C4, decisiones arquitectónicas inconsistentes, code smells |
| **WF3** — Plan de Pruebas | Genera casos de prueba automáticamente a partir de los requisitos | Acelera la creación de pruebas dinámicas (Fase 2) |
| **WF4** — Orquestador | Coordina WF1+WF2+WF3 y genera un reporte consolidado de Quality Gate | Da una visión única del estado de calidad del proyecto |

**Características técnicas:**
- Todo corre en **GitHub Actions** (pipelines automatizados en cada push)
- Usan el modelo de IA **Gemini** (Google) para análisis inteligente
- Generan reportes en **Markdown** (legibles) y **JSON** (procesables por otras herramientas)
- **NO modifican el código del Equipo 58-1** — solo auditan

---

### 2.3 Mejoras Implementadas (Pre-Producción)

Antes de pedirte la aprobación, implementamos 3 mejoras críticas:

#### Mejora 1: Análisis Visual de Diagramas con IA
**¿El problema?** Los diagramas C4 y UML del DAS están en PDFs como imágenes. Un análisis de texto no puede ver si una flecha falta o si un actor está ausente.

**¿La solución?**
- Extraemos automáticamente las imágenes de los PDFs
- La IA (Gemini multimodal) "mira" los diagramas y detecta defectos visuales
- Ejemplos de lo que detecta: *"Actor externo mencionado en el ERS pero ausente en el diagrama"*, *"Relación sin dirección ni protocolo"*

#### Mejora 2: Idempotencia en Jira
**¿El problema?** Si el workflow se ejecuta 2 veces, crearía tickets duplicados en Jira.

**¿La solución?** Antes de crear un ticket, buscamos si ya existe uno con el mismo identificador. Si existe, lo actualizamos en lugar de duplicarlo.

#### Mejora 3: Mejores Prompts de IA (Few-Shot)
**¿El problema?** La IA a veces reporta "defectos" que en realidad son preferencias estilísticas (falsos positivos).

**¿La solución?** Le enseñamos a la IA con ejemplos concretos: *"Esto SÍ es un defecto"* vs *"Esto NO es un defecto, es solo cosmético"*. Esto reduce los falsos positivos.

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
- Los 4 workflows automatizados (funcionamiento técnico)
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

---

## 6. Métricas de Calidad de lo que construimos

| Métrica | Valor | Significado |
|---|---|---|
| Tests automatizados | 99 | Cada función crítica tiene un test que la verifica |
| Tests pasando | 99/99 (100%) | Nada está roto |
| Cobertura estimada | >90% | La mayoría del código SQA está probado |
| Commits | 16 | Cada cambio fue un "paquete" coherente (código + tests juntos) |
| Líneas de código SQA | ~2.800 | Sistema completo pero enfocado |

---

## 7. Riesgos y Mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| La IA se queda sin quota (Gemini) | Media | Media | Tenemos retry automático + fallback a modo texto |
| SonarQube no está disponible | Baja | Alta | WF2 funciona igual solo con análisis de documentos + visual |
| Imágenes de PDFs en formato raro | Baja | Media | Convertimos automáticamente a PNG. Si falla, se omite graceful |
| Duplicación de tickets (re-run) | **Resuelto** | — | M2 implementa idempotencia con búsqueda previa en Jira |

---

## 8. Estructura del Repositorio

```
gestion-bibliotecaria-sqa/
├── src/                          ← Código del Equipo 58-1 (NO TOCAMOS)
├── biblioteca-frontend/src/      ← Frontend del Equipo 58-1 (NO TOCAMOS)
├── documentacion/                ← PDFs del Equipo 58-1 (NO TOCAMOS)
├── scripts/sqa_core/             ← Motor SQA compartido
│   ├── image_analysis.py         ← Análisis visual de diagramas
│   ├── pdf_text.py               ← Extracción de texto e imágenes de PDFs
│   ├── clients.py                ← Clientes Jira/Confluence/Gemini/Sonar
│   ├── reporting.py              ← Generación de reportes
│   └── config.py                 ← Configuración
├── scripts/wf1_auditoria_requisitos.py
├── scripts/wf2_inspeccion_arquitectura.py
├── scripts/wf3_generacion_pruebas.py
├── scripts/wf4_orquestador.py
├── tests/scripts/                ← 99 tests automatizados
├── sqa/
│   ├── Checklists-Inspeccion-Estatica-v1.md
│   ├── PACS-Fase2-Herramientas.md
│   └── INFORME-APROBACION-LIDER-GENERAL.md  ← Este documento
└── .github/workflows/            ← Pipelines de CI/CD
```

---

## 9. Decisión Requerida del Líder General

**¿Aprueba el Líder General (Alberto Rodríguez) las siguientes acciones?**

- [ ] **Aprobar las 5 checklists de inspección** documentadas en `sqa/Checklists-Inspeccion-Estatica-v1.md`
- [ ] **Aprobar los 4 workflows automatizados** para su uso en producción
- [ ] **Autorizar la fusión** de esta rama al repositorio principal (`main`)
- [ ] **Aprobar la matriz de herramientas** declarada en `sqa/PACS-Fase2-Herramientas.md`
- [ ] **Autorizar la activación** de `DRY_RUN=false` una vez configuradas las credenciales

**Hasta recibir esta aprobación, TODO permanece en modo simulación.** No se crearán tickets reales, no se modificará Confluence, y no se tocará el código del Equipo 58-1.

---

## Anexos para Revisión

| Documento | Descripción | Ubicación |
|---|---|---|
| Checklists de Inspección | 71 ítems de verificación con evidencia | `sqa/Checklists-Inspeccion-Estatica-v1.md` |
| Matriz de Herramientas | Herramientas declaradas para Fase 1 y Fase 2 | `sqa/PACS-Fase2-Herramientas.md` |
| Reportes de prueba | Ejemplos de reportes generados por WF4 | `sqa/reportes/` |
| Roadmap de mejoras | Mejoras pendientes post-aprobación | `sqa/ROADMAP-MEJORAS-PRE-PRODUCCION.md` |

---

*Documento generado por el Equipo SQA 11*  
*Fecha: 2026-05-06*  
*Estado: Pendiente de aprobación del Líder General*
