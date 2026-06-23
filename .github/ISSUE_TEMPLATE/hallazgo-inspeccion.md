---
name: Hallazgo de Inspección / Walkthrough
about: Registrar un hallazgo encontrado mediante técnica estática (Fase 1)
title: '[HALLAZGO] '
labels:
  - 'tipo:hallazgo'
  - 'fase:fase-1'
  - 'estado:abierto'
assignees: []
---

<!--
Completar TODOS los campos marcados como OBLIGATORIO.
La trazabilidad hacia ERS o DAS es un requisito de la ISO/IEC 12207.
No cerrar este issue sin confirmar el campo "Referencia exacta".
-->

## Técnica aplicada

<!--
OBLIGATORIO. Marcar solo una.
-->

- [ ] Inspección formal
- [ ] Walkthrough
- [ ] Revisión técnica
- [ ] Auditoría de producto

---

## Documento / Artefacto revisado

<!--
OBLIGATORIO. Marcar el artefacto fuente del hallazgo.
-->

- [ ] ERS — Especificación de Requisitos de Software
- [ ] DAS — Documento de Arquitectura de Software
- [ ] Diagrama UML (clases, secuencia, despliegue)
- [ ] Código fuente

---

## Referencia exacta

<!--
OBLIGATORIO. Identificador preciso dentro del documento.
Ejemplos: "ERS-RF-012", "DAS Sección 3.2 — Capa de Servicio", "Página 8, párrafo 2"
Sin este campo no hay trazabilidad bidireccional (ISO 12207).
-->

**Identificador de requisito / componente:** <!-- ERS-XXX / DAS-XXX -->  
**Sección / página:** <!-- ej. Sección 4.1, página 12 -->  
**Versión del documento:** <!-- ej. ERS v1.2 -->

---

## Componente de arquitectura afectado

<!--
OPCIONAL si el hallazgo es en ERS. OBLIGATORIO si es en DAS o código.
Identificar la capa o componente según el DAS (ej. "Capa de Repositorio", "Controlador REST /prestamos").
-->

---

## Descripción del hallazgo

<!--
OBLIGATORIO. Describir con precisión qué está mal, incompleto o ambiguo.
-->

---

## Evidencia — cita literal

<!--
OBLIGATORIO. Transcribir el fragmento exacto del documento que sustenta el hallazgo.
Si es código, incluir el fragmento con su ruta de archivo y número de línea.
-->

```
<!-- Pegar aquí la cita literal o el fragmento de código -->
```

---

## Severidad

<!--
OBLIGATORIO. Marcar solo una. Actualizar la etiqueta del issue con el valor elegido.
-->

- [ ] `severidad:critica` — Compromete la integridad del sistema o proceso
- [ ] `severidad:mayor` — Afecta funcionalidad de manera significativa
- [ ] `severidad:menor` — Afecta calidad parcialmente, existe alternativa
- [ ] `severidad:observacion` — Mejora recomendada, sin impacto directo

---

## Característica ISO/IEC 25010 afectada

<!--
OBLIGATORIO. Marcar la característica principal. Actualizar la etiqueta iso:* del issue.
-->

- [ ] `iso:funcionalidad`
- [ ] `iso:confiabilidad`
- [ ] `iso:usabilidad`
- [ ] `iso:eficiencia`
- [ ] `iso:mantenibilidad`
- [ ] `iso:seguridad`
- [ ] `iso:compatibilidad`
- [ ] `iso:portabilidad`

---

## Propuesta de corrección

<!--
OBLIGATORIO. Indicar qué debería corregirse en el artefacto original.
Ser específico: qué sección, qué texto nuevo, qué criterio de aceptación.
-->

---

## Área

<!--
OBLIGATORIO. Actualizar la etiqueta area:* del issue.
-->

- [ ] `area:requisitos`
- [ ] `area:arquitectura`
- [ ] `area:codigo`
- [ ] `area:proceso`

---

## Rol que registra

<!--
OBLIGATORIO. Actualizar la etiqueta rol:* del issue.
-->

- [ ] `rol:lider-gral`
- [ ] `rol:lider-tec`
- [ ] `rol:tester`
- [ ] `rol:metricas`
- [ ] `rol:escriba`
