---
name: Defecto de Prueba
about: Registrar un defecto encontrado mediante técnica dinámica (Fase 2)
title: '[DEFECTO] '
labels:
  - 'tipo:defecto'
  - 'fase:fase-2'
  - 'estado:abierto'
assignees: []
---

<!--
Completar TODOS los campos marcados como OBLIGATORIO.
El campo "Referencia ERS" es trazabilidad mandatoria según ISO 12207.
-->

## Nivel de prueba

<!--
OBLIGATORIO. Marcar solo uno.
-->

- [ ] Unitaria
- [ ] Integración
- [ ] Sistema
- [ ] Aceptación

---

## Enfoque de prueba

<!--
OBLIGATORIO. Marcar solo uno.
-->

- [ ] Caja blanca (basada en estructura interna)
- [ ] Caja negra (basada en especificación de requisitos)
- [ ] Caja gris (combinación de ambas)

---

## Identificador del caso de prueba

<!--
OBLIGATORIO. ID asignado en el Plan de Pruebas.
Ejemplo: CP-001, TC-AUTH-03
-->

**ID caso de prueba:** <!-- CP-XXX -->

---

## Componente / Clase afectada

<!--
OBLIGATORIO. Clase Java, endpoint REST o componente Vue donde se manifiesta el defecto.
Ejemplo: "LibroService.java — método buscarPorIsbn()", "GET /api/libros/isbn/{isbn}"
-->

**Archivo / clase:** <!-- ruta relativa -->  
**Método / endpoint:** <!-- nombre exacto -->  
**Línea aproximada:** <!-- número de línea si aplica -->

---

## Referencia ERS

<!--
OBLIGATORIO. Trazabilidad hacia el requisito que la prueba verifica.
Sin este campo la trazabilidad bidireccional exigida por ISO 12207 está incompleta.
-->

**Identificador ERS:** <!-- ERS-RF-XXX -->  
**Descripción del requisito:** <!-- Breve paráfrasis del requisito -->

---

## Pasos para reproducir

<!--
OBLIGATORIO. Secuencia numerada, precisa y reproducible.
-->

1. 
2. 
3. 

---

## Comportamiento esperado

<!--
OBLIGATORIO. Qué debería ocurrir según ERS o el plan de pruebas.
-->

---

## Comportamiento actual (defecto)

<!--
OBLIGATORIO. Qué ocurrió realmente. Incluir stacktrace, respuesta HTTP o salida de consola.
-->

```
<!-- Pegar aquí la salida, error o log -->
```

---

## Severidad

<!--
OBLIGATORIO. Marcar solo una. Actualizar etiqueta severidad:* del issue.
-->

- [ ] `severidad:critica`
- [ ] `severidad:mayor`
- [ ] `severidad:menor`
- [ ] `severidad:observacion`

---

## Característica ISO/IEC 25010 afectada

<!--
OBLIGATORIO. Marcar la característica que este defecto viola.
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

## Evidencia adjunta

<!--
Adjuntar capturas de pantalla, logs de ejecución, o reporte JUnit/Surefire.
Si el pipeline de CI detectó este defecto, enlazar el run de GitHub Actions.
-->

**Run de CI (si aplica):** <!-- URL del workflow run -->

---

## Rol que registra

- [ ] `rol:lider-gral`
- [ ] `rol:lider-tec`
- [ ] `rol:tester`
- [ ] `rol:metricas`
- [ ] `rol:escriba`
