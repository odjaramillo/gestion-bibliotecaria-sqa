# Solicitud de firma — Líder de Métricas (Fiabilidad M-01..M-06)

**Proyecto:** Sistema de Gestión Bibliotecaria — Equipo 58-1
**Referencia:** Issue #24 · Fase 2 (Técnicas Dinámicas)
**Fecha de solicitud:** 2026-07-10
**Estándar:** ISO/IEC 25010 — Fiabilidad (Madurez + Tolerancia a Fallos)

---

## Qué se necesita

El dashboard de métricas ya está en producción, pero **tres métricas declaradas
siguen en N/D** y **ninguno de los umbrales está ratificado** (aparecen marcados
`[PROP]` = propuesto). Se requiere tu firma para dos cosas:

1. **Fijar el valor** de las métricas declaradas M-01, M-05, M-06.
2. **Ratificar los umbrales** (metas) de las seis métricas.

> Nota importante: el **estado de cumplimiento siempre lo calcula la herramienta**
> a partir del valor y el umbral. No se declara "cumple/no cumple" a mano. Tu
> firma fija el *valor declarado* y la *meta*, no el veredicto.

---

## A. Valores declarados pendientes (acción requerida)

Hoy están en N/D. Necesitamos el valor y su evidencia.

| ID | Métrica | Unidad | Valor hoy | Meta propuesta | Necesitamos |
|----|---------|--------|-----------|----------------|-------------|
| **M-01** | Densidad de Defectos de Fiabilidad | defectos/módulo | N/D | ≤ 1.0 | Conteo de issues `tipo:defecto` por módulo afectado |
| **M-05** | Entradas Inválidas Controladas | % | N/D | ≥ 80 | % de entradas inválidas rechazadas de forma controlada (casos TC-FIAB) |
| **M-06** | Operaciones con Guarda de Estado | % | N/D | ≥ 80 | % de operaciones críticas con guarda de estado verificada (préstamos / amonestaciones) |

**Para cada una, por favor indicá:**
- Valor numérico declarado.
- Evidencia / justificación (de dónde sale el número).
- Responsable.

---

## B. Ratificación de umbrales (acción requerida)

Todos los umbrales están hoy como **propuestos, no ratificados**. Necesitamos tu
firma para pasarlos a ratificados (y que se quite el `[PROP]` del dashboard).

| ID | Fuente | Valor actual | Meta propuesta | ¿Ratificás la meta? |
|----|--------|--------------|----------------|---------------------|
| M-01 | Declarada | N/D | ≤ 1.0 defectos/módulo | ☐ Sí ☐ Ajustar a: ____ |
| M-02 | Automática | 60.7 % | ≥ 50 % | ☐ Sí ☐ Ajustar a: ____ |
| M-03 | Automática | 100 % | ≥ 100 % | ☐ Sí ☐ Ajustar a: ____ |
| M-04 | Automática | 38.1 % | ≥ 30 % | ☐ Sí ☐ Ajustar a: ____ |
| M-05 | Declarada | N/D | ≥ 80 % | ☐ Sí ☐ Ajustar a: ____ |
| M-06 | Declarada | N/D | ≥ 80 % | ☐ Sí ☐ Ajustar a: ____ |

> **Criterio a considerar (indicación del docente):** en la práctica no se fijan
> metas altas; se fija lo que efectivamente se puede alcanzar y se documenta el
> máximo aparte. Las metas automáticas (M-02 = 50 %, M-04 = 30 %) ya se
> calibraron con ese criterio. **Las metas declaradas M-05 y M-06 siguen en
> 80 %** — conviene revisar si ese piso es realista para la fase o si debería
> bajarse a un valor alcanzable.

---

## Cómo se aplica (referencia técnica, para el equipo)

- **Valores declarados** → `sqa/metricas/metricas_fiabilidad.json` (campos
  `valor`, `evidencia`, `justificacion`, `responsable`).
- **Umbrales** → `ratificado: true` en el registro declarado y en `AUTO_META`
  (dentro de `sqa/metricas/calcular_kpi.py`) para las automáticas.
- El estado se recalcula solo al regenerar el reporte.

---

## Firma

- **Nombre (Líder de Métricas):** ____________________
- **Fecha:** ____________________
- **Observaciones:** ____________________

_Esta firma constituye la ratificación formal de los valores y umbrales de las
métricas de Fiabilidad (ISO/IEC 25010) para la Fase 2, y cierra el issue #24._
