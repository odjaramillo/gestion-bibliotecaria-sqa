---
name: Ítem de Auditoría
about: Registrar una no conformidad o hallazgo de auditoría formal (IEEE 730)
title: '[AUDITORÍA] '
labels:
  - 'tipo:no-conformidad'
  - 'estado:abierto'
assignees: []
---

<!--
Completar TODOS los campos marcados como OBLIGATORIO.
Este template soporta auditorías de proceso y de producto.
Referencia: IEEE 730 — Software Quality Assurance Plans.
-->

## Tipo de auditoría

<!--
OBLIGATORIO. Marcar solo uno.
-->

- [ ] Auditoría de producto (evalúa artefactos: ERS, DAS, código)
- [ ] Auditoría de proceso (evalúa el seguimiento del PACS)

---

## Fase

- [ ] `fase:fase-1`
- [ ] `fase:fase-2`

---

## Estándar de referencia

<!--
OBLIGATORIO. Indicar el estándar cuyo criterio fue evaluado.
-->

- [ ] IEEE 730 — Plan de Aseguramiento de la Calidad del Software
- [ ] ISO/IEC 12207 — Procesos del ciclo de vida del software
- [ ] ISO/IEC/IEEE 29148 — Requisitos de sistemas y software
- [ ] ISO/IEC 25010 — Modelo de calidad del producto software
- [ ] ISO/IEC/IEEE 42010 — Descripción de arquitectura
- [ ] Otro: <!-- especificar -->

---

## Criterio auditado

<!--
OBLIGATORIO. Qué criterio, cláusula o sección del estándar se evaluó.
Ejemplo: "IEEE 730 §4.3 — El PACS debe identificar métricas de calidad aplicables"
-->

**Cláusula / sección:** <!-- ej. IEEE 730 §4.3 -->  
**Descripción del criterio:** <!-- paráfrasis del criterio -->

---

## Evidencia encontrada

<!--
OBLIGATORIO. Qué se observó durante la auditoría. Cita o descripción objetiva.
-->

---

## No conformidad identificada

<!--
OBLIGATORIO si existe no conformidad. Si es conforme, indicar "CONFORME" y cerrar issue.
Describir con precisión la brecha entre lo observado y lo exigido por el estándar.
-->

---

## Área afectada

- [ ] `area:requisitos`
- [ ] `area:arquitectura`
- [ ] `area:codigo`
- [ ] `area:pruebas`
- [ ] `area:proceso`

---

## Severidad

- [ ] `severidad:critica`
- [ ] `severidad:mayor`
- [ ] `severidad:menor`
- [ ] `severidad:observacion`

---

## Recomendación

<!--
OBLIGATORIO. Acción correctiva específica que elimina la no conformidad.
Indicar responsable sugerido y plazo estimado.
-->

**Acción:** <!-- qué debe hacerse -->  
**Responsable sugerido:** <!-- rol -->  
**Plazo:** <!-- ej. antes de la entrega Fase 1 -->

---

## Rol auditor

- [ ] `rol:lider-gral`
- [ ] `rol:lider-tec`
- [ ] `rol:tester`
- [ ] `rol:metricas`
- [ ] `rol:escriba`
