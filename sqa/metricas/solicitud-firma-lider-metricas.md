# Solicitud de firma — Líder de Métricas (Fiabilidad M-01..M-06)

**Proyecto:** Sistema de Gestión Bibliotecaria — Equipo 58-1
**Referencia:** Issue #24 · Fase 2 (Técnicas Dinámicas)
**Fecha de solicitud:** 2026-07-10
**Estándar:** ISO/IEC 25010 — Fiabilidad (Madurez + Tolerancia a Fallos)

---

## Estado — CERRADO (2026-07-19)

Ratificación completada para la Fase 2. Se fijaron las dos cosas pendientes:

1. **Valores** de las métricas declaradas M-01, M-05, M-06 (antes en N/D) — ver §A.
2. **Umbrales** (metas) de las seis métricas, pasados a ratificados (`[PROP]` retirado) — ver §B.

> Nota importante: el **estado de cumplimiento siempre lo calcula la herramienta**
> a partir del valor y el umbral. No se declara "cumple/no cumple" a mano. La
> ratificación fija el *valor declarado* y la *meta*, no el veredicto.

---

## A. Valores declarados — RATIFICADOS

Fijados sobre evidencia verificada de forma independiente (doble revisión ciega, 2026-07-19).

| ID | Métrica | Unidad | Valor | Meta | Evidencia |
|----|---------|--------|-------|------|-----------|
| **M-01** | Densidad de Defectos de Fiabilidad | defectos/módulo | **1.0** | ≤ 1.0 | 6 hallazgos de diseño (WT-01..WT-06) / 6 módulos críticos — walkthrough §5.2. Vista puntual divulgada: ~2.0 (auditoría 2026-06-02). |
| **M-05** | Entradas Inválidas Controladas | % | **55.6** | ≥ 80 | 10 condiciones controladas / 18 probadas — medido sobre la ejecución (JSON tipo incorrecto→HTTP 400, multipart→HTTP 413 vía manejadores por defecto de Spring; la fecha no parseable T2.2 sí da HTTP 500; ver #52). Robusto < 80% en todo alcance. |
| **M-06** | Operaciones con Guarda de Estado | % | **75.0** | ≥ 80 | 3 de 4 operaciones críticas de capa Service con guarda de precondición; sin guarda: `renovarPrestamo` (decrementa inventario sin verificar `>= 1`) — objetivos.txt Atributo 2.2, `PrestamoService.java:151-154`. |

> **M-05 y M-06 quedan en rojo (no cumple), y es correcto:** miden la fiabilidad del SUT (Equipo 58-1), no la calidad de la suite del Equipo 11. El valor cae donde cae; el umbral es la vara de calidad. Bajarlo para pintar de verde ocultaría el hallazgo. El estado lo calcula la herramienta, nunca se declara a mano.

---

## B. Ratificación de umbrales — RATIFICADOS

Todos los umbrales pasan a **ratificados** (`[PROP]` retirado del dashboard).

| ID | Fuente | Valor medido | Meta ratificada | Estado (lo calcula la herramienta) |
|----|--------|--------------|-----------------|------------------------------------|
| M-01 | Declarada | 1.0 | ≤ 1.0 defectos/módulo | ✅ cumple |
| M-02 | Automática | 60.7 % | ≥ 50 % | ✅ cumple |
| M-03 | Automática | 100 % | ≥ 100 % | ✅ cumple |
| M-04 | Automática | 38.1 % | ≥ 30 % | ✅ cumple |
| M-05 | Declarada | 55.6 % | ≥ 80 % | ❌ no cumple (hallazgo del SUT) |
| M-06 | Declarada | 75.0 % | ≥ 80 % | ❌ no cumple (hallazgo del SUT) |

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

## Ratificación

- **Ratificado por:** Líder de Métricas — Equipo SQA T 11 (cierre de rol/equipo)
- **Fecha:** 2026-07-19
- **Base de ratificación:** verificación independiente de los valores mediante doble revisión ciega contra la evidencia fuente (walkthrough §5.2, especificación TCS-FIAB-001 §4, marco `referencias/objetivos.txt` y código del SUT). No se declaró ningún estado a mano; el veredicto *cumple/no cumple* lo calcula `metricas/calcular_kpi.py`.

_Esta ratificación fija los valores y umbrales de las métricas de Fiabilidad (ISO/IEC 25010) para la Fase 2, y cierra el issue #24._
