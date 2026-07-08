# sqa/ — Artefactos de Aseguramiento de la Calidad (Equipo T 11)

Índice de la carpeta de artefactos SQA del proyecto. Estructura organizada por entrega.

## Estructura

| Ruta | Contenido |
|---|---|
| `fase1/` | Entrega 1 — técnicas estáticas sobre requisitos y arquitectura |
| `fase1/Checklists-Inspeccion-Estatica-v1.md` | Checklist maestro de inspección estática (75 ítems: BRIEF, ERS, DAS, Código, PAC) |
| `fase1/gestion/` | Informes de gestión: aprobación del Líder General, resumen ejecutivo, roadmap de mejoras, informe M7, modo producción WF4 |
| `fase2/` | Entrega 2 — estáticas a código + técnicas dinámicas (fiabilidad ISO/IEC 25010:2023) |
| `fase2/planificacion/` | Estrategia de Pruebas y Plan de Pruebas de fiabilidad |
| `fase2/estaticas/` | Informes de revisión estática de Fase 2 (walkthrough, auditoría) |
| `fase2/dinamicas/` | Resultados de ejecución de pruebas, informes de incidencias y de resultados |

## Rutas congeladas — NO mover ni renombrar

Las siguientes rutas están referenciadas por los workflows de CI (WF1–WF7) y por los scripts de `scripts/`. Moverlas rompe la automatización:

| Ruta | Referenciada por |
|---|---|
| `checklists/*.json` | `wf4_orquestador.py`, `wf_pac_auditor.py`, `pac_assembler.py`, trigger de `wf4_orquestador.yml` |
| `reportes/` | Salida de WF1–WF7, trigger de `wf3_generacion_pruebas.yml` |
| `templates/pac_config.yaml` | `wf_pac_generator.py` (config por defecto), `wf5_generador_pac.yml` |
| `pac_config.yaml` | `wf5_generador_pac.yml` (argumento CLI) |
| `pac_generado.md` | `wf5_generador_pac.yml` (salida), `wf6_auditor_pac.yml` (entrada), tests |
| `anexos/herramientas-fase2.md` | `pac_assembler.py:321` (lectura directa) |
| `pdfs/` | Trigger de `wf7_agente_pdf_confluence.yml` |
| `extracted_images/` | Salida de `wf2_inspeccion_arquitectura.py` |
