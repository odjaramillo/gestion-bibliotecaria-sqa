# M7 — Generación Semi-Automatizada del Plan de Aseguramiento de Calidad (PAC)

**Informe para el Líder de Métricas**  
**Proyecto:** Sistema de Gestión Bibliotecaria — Ecosistema SQA  
**Fecha:** mayo 2026

---

## 1. Carta de Presentación

### ¿Qué es M7 y por qué existe?

M7 es el módulo que le permite generar el **Plan de Aseguramiento de Calidad (PAC)** de su proyecto en minutos, en lugar de escribirlo a mano durante horas.

### ¿Qué problema resuelve?

Hoy el PAC se escribe manualmente. Eso significa:
- Secciones repetitivas que copiamos de proyecto en proyecto.
- Riesgo de olvidar algún apartado del estándar IEEE 730-2014.
- Desfasaje entre el stack real del sistema y lo que dice el plan.

### ¿Cuál es el entregable?

Un documento `pac_generado.md` que cumple con IEEE 730-2014, armado en forma **semi-automatizada**:
- El sistema descubre solo el stack tecnológico (Java, Vue, dependencias, etc.).
- Usted completa una simple planilla YAML con objetivos, roles y métricas.
- Gemini da formato profesional a las secciones que usted rellena.

### ¿Por qué importa?

Porque el PAC es el contrato de calidad de su proyecto. Sin él, no hay manera de demostrar — ni ante el equipo ni ante un auditor — que el software se construyó con criterios medibles.

---

## 2. ¿Qué es un PAC?

El **Plan de Aseguramiento de Calidad (PAC)** es el documento que define:
- Qué atributos de calidad se persiguen (funcionalidad, fiabilidad, usabilidad, etc.).
- Quién se encarga de cada tarea de control.
- Qué métricas se van a medir y cuál es el valor mínimo aceptable.
- Cómo se manejan los riesgos y el cronograma de auditorías.

Nosotros seguimos el estándar **IEEE 730-2014**, que es el estándar internacional para planes de aseguramiento de calidad de software. Toda empresa que desarrolle software crítico o institucional lo exige.

> **En una oración:** el PAC responde "¿cómo sabemos que este sistema es de calidad?" antes de que el usuario lo use.

---

## 3. ¿Qué hace el generador?

### Lo que se genera automáticamente

| Sección | ¿Quién la arma? | ¿Qué contiene? |
|---------|-----------------|----------------|
| Stack tecnológico | 🤖 Sistema | Java version, Spring Boot, Vue.js, dependencias clave. Lee `pom.xml` y `package.json` en vivo. |
| Inventario de artefactos | 🤖 Sistema | Lista de documentos (ERS, DAS, BRIEF) y archivos de código fuente. |
| Estándares aplicables | 🤖 Sistema | ISO 25010, IEEE 29148, IEEE 42010, según el tipo de artefacto. |
| Herramientas y CI/CD | 🤖 Sistema | Maven, JUnit, GitHub Actions, ESLint, etc. |

### Lo que necesita el líder

| Sección | ¿Qué debe definir usted? |
|---------|--------------------------|
| Objetivos de calidad | ¿Qué atributos ISO 25010 priorizan? ¿Con qué peso? |
| Roles del equipo | Nombres, emails y responsabilidades. |
| Umbrales de métricas | ¿Cuánto es "suficiente" cobertura de revisiones? ¿Cuántos defectos por entregable se toleran? |
| Riesgos | ¿Qué puede salir mal y cómo lo mitigamos? |
| Cronograma | Fechas de inicio, fin y entregables por fase. |

### ¿Dónde entra Gemini?

Gemini toma los datos que usted escribió en la planilla y les da formato de texto profesional. **Nunca inventa contenido**: si usted no completó un campo, Gemini deja un marcador `[COMPLETAR]` para que lo revise.

### El resultado final

Un archivo `sqa/pac_generado.md` con:
- Portada del proyecto.
- 12 secciones numeradas alineadas con IEEE 730-2014.
- Tablas, listas de verificación y referencias cruzadas.
- Listo para entregar al docente o al auditor.

---

## 4. Instrucciones paso a paso

Siga esta checklist en orden. No se saltee pasos.

- [ ] **Paso 1:** Copie la plantilla a su directorio de trabajo.
  ```bash
  cp sqa/templates/pac_config.yaml mi_pac_config.yaml
  ```
- [ ] **Paso 2:** Ábralo con cualquier editor de texto (Bloc de notas, VS Code, Nano) y complete los campos marcados con `[COMPLETAR]`.
- [ ] **Paso 3:** Guarde el archivo.
- [ ] **Paso 4:** Ejecute el generador:
  ```bash
  python scripts/wf_pac_generator.py --config mi_pac_config.yaml
  ```
- [ ] **Paso 5:** Revise el documento generado en `sqa/pac_generado.md`.
- [ ] **Paso 6:** Ejecute el auditor para validar:
  ```bash
  python scripts/wf_pac_auditor.py --pac sqa/pac_generado.md
  ```
- [ ] **Paso 7:** Si el auditor dice **APROBADO**, terminó. Si dice **PARCIAL** o **RECHAZADO**, corrija los campos que indica y vuelva al paso 4.

> **Consejo:** No necesita saber Python. Solo copie y pegue los comandos tal cual aparecen arriba.

---

## 5. Guía de llenado de `pac_config.yaml`

A continuación explicamos cada sección de la planilla. Los campos que dicen `[COMPLETAR]` son obligatorios.

### `proyecto`

| Campo | Significado | Ejemplo para este proyecto | ¿Qué pasa si lo deja vacío? |
|-------|-------------|----------------------------|-----------------------------|
| `name` | Nombre comercial del sistema | `Sistema de Gestión Bibliotecaria` | Aparece `[COMPLETAR]` en la portada. |
| `version` | Versión actual del software | `1.0.0` | El PAC queda sin número de versión. |
| `descripcion` | Para qué sirve el sistema, en 2-3 líneas | `Sistema web para gestión de préstamos, catálogo y usuarios de biblioteca.` | Gemini no puede formatear una descripción vacía. |

### `lider`

| Campo | Significado | Ejemplo | ¿Qué pasa si lo deja vacío? |
|-------|-------------|---------|-----------------------------|
| `nombre` | Nombre completo del líder de métricas | `Ana López` | El PAC no tiene firma ni responsable identificado. |
| `email` | Correo institucional | `alopez@institucion.edu` | No hay canal de contacto en el documento. |
| `rol` | Cargo dentro del equipo SQA | `Líder de Métricas y Aseguramiento de Calidad` | Se usa el valor por defecto. |

### `objetivos_calidad`

Asigne un peso de **0 a 100** a cada atributo ISO 25010. La suma no necesita ser 100; los pesos son relativos.

| Atributo | ¿Qué mide? | Ejemplo | ¿Qué pasa si deja todo en 0? |
|----------|-----------|---------|------------------------------|
| `funcionalidad` | ¿Hace lo que pide el usuario? | `40` | El PAC no muestra prioridades de calidad. |
| `fiabilidad` | ¿Funciona sin fallar? | `30` | Idem. |
| `usabilidad` | ¿Es fácil de usar? | `30` | Idem. |
| `eficiencia` | ¿Rinde bien con muchos usuarios? | `0` | Se omite del plan. Esto está bien si no es prioridad. |
| `mantenibilidad` | ¿Es fácil de corregir o ampliar? | `0` | Idem. |
| `seguridad` | ¿Protege datos y accesos? | `0` | Idem. |

### `roles`

Liste los nombres de las personas que ocupan cada puesto SQA.

| Rol | Ejemplo | ¿Qué pasa si lo deja vacío? |
|-----|---------|-----------------------------|
| `lider_metricas` | `Ana López` | La sección de organización queda incompleta. |
| `responsable_sqa` | `Carlos Ruiz` | Idem. |
| `auditor_requisitos` | `María González` | Idem. |
| `auditor_arquitectura` | `Juan Pérez` | Idem. |
| `escriba` | `Lucía Martínez` | Idem. |

### `umbrales`

Defina el valor mínimo aceptable para cada métrica. Estos números son los que el auditor va a controlar.

| Métrica | Significado | Ejemplo | ¿Qué pasa si lo deja vacío? |
|---------|-------------|---------|-----------------------------|
| `cobertura_revisiones` | % de artefactos revisados sobre el total planificado | `100.0` | El PAC no tiene meta de revisión. |
| `densidad_defectos_max` | Máximo de defectos admitidos por cada mil líneas de código (KLOC) | `0.5` | No hay límite de calidad definido. |
| `cobertura_pruebas_min` | % mínimo de código cubierto por pruebas automáticas | `80.0` | Se omite si el proyecto no tiene pruebas unitarias. |

### `riesgos`

Cada riesgo tiene tres partes:
- `descripcion`: ¿Qué puede salir mal?
- `mitigacion`: ¿Qué hacemos para evitarlo o reducirlo?
- `aceptado`: `true` si el equipo decidió convivir con ese riesgo, `false` si va a mitigarse activamente.

| Campo | Ejemplo | ¿Qué pasa si lo deja vacío? |
|-------|---------|-----------------------------|
| `descripcion` | `Retraso en entrega de artefactos por parte del equipo de desarrollo` | La sección de riesgos queda incompleta. |
| `mitigacion` | `Revisiones tempranas y checkpoints semanales` | Idem. |
| `aceptado` | `false` | Se asume que no está aceptado. |

### `cronograma`

Mapee las actividades de SQA a las fases del proyecto.

| Campo | Significado | Ejemplo | ¿Qué pasa si lo deja vacío? |
|-------|-------------|---------|-----------------------------|
| `fase` | Nombre de la fase | `Fase 1: Pre-producción` | El cronograma queda incompleto. |
| `inicio` | Fecha de inicio (formato `YYYY-MM-DD`) | `2026-05-01` | No hay fecha de referencia. |
| `fin` | Fecha de fin (formato `YYYY-MM-DD`) | `2026-05-15` | Idem. |
| `entregables` | Lista de productos que se entregan en esa fase | `PAC generado y aprobado` | El auditor no sabe qué esperar. |

---

## 6. Ejemplo completo relleno

A continuación le presentamos una planilla `pac_config.yaml` **completamente rellena** basada en las métricas que usted ya nos proporcionó. Puede copiar este contenido, guardarlo como `mi_pac_config.yaml` y ejecutar el generador inmediatamente.

```yaml
# =============================================================================
# Configuración para el Plan de Aseguramiento de Calidad (PAC)
# =============================================================================
# Copie este contenido, guárdelo como mi_pac_config.yaml y ejecútelo.
# =============================================================================

proyecto:
  name: "Sistema de Gestión Bibliotecaria"
  version: "1.0.0"
  descripcion: |
    Sistema web para gestión de préstamos, catálogo y usuarios de biblioteca.
    Incluye backend en Java con Spring Boot y frontend en Vue.js.

lider:
  nombre: "Ana López"
  email: "alopez@institucion.edu"
  rol: "Líder de Métricas y Aseguramiento de Calidad"

objetivos_calidad:
  funcionalidad: 40
  fiabilidad: 30
  usabilidad: 30
  eficiencia: 0
  mantenibilidad: 0
  portabilidad: 0
  seguridad: 0
  compatibilidad: 0

roles:
  lider_metricas: "Ana López"
  responsable_sqa: "Carlos Ruiz"
  auditor_requisitos: "María González"
  auditor_arquitectura: "Juan Pérez"
  escriba: "Lucía Martínez"

umbrales:
  cobertura_revisiones: 100.0
  densidad_defectos_max: 0.5
  cobertura_pruebas_min: 80.0

riesgos:
  - descripcion: "Retraso en entrega de artefactos por parte del equipo de desarrollo"
    mitigacion: "Revisiones tempranas y checkpoints semanales"
    aceptado: false
  - descripcion: "Cambios de requisitos durante la fase de auditoría"
    mitigacion: "Congelar requisitos previo a cada inspección formal"
    aceptado: false

cronograma:
  - fase: "Fase 1: Pre-producción"
    inicio: "2026-05-01"
    fin: "2026-05-15"
    entregables:
      - "PAC generado y aprobado"
      - "Checklists de auditoría definidas"
  - fase: "Fase 2: Auditoría de Requisitos y Arquitectura"
    inicio: "2026-05-16"
    fin: "2026-05-30"
    entregables:
      - "Informe WF1: Auditoría de Requisitos"
      - "Informe WF2: Inspección de Arquitectura"
  - fase: "Fase 3: Generación de Pruebas"
    inicio: "2026-06-01"
    fin: "2026-06-15"
    entregables:
      - "Casos de prueba generados"
      - "Informe WF3: Cobertura de Pruebas"
  - fase: "Fase 4: Orquestación y Métricas"
    inicio: "2026-06-16"
    fin: "2026-06-30"
    entregables:
      - "Dashboard de métricas"
      - "Informe WF4: Estado de Calidad"
```

---

## 7. Preguntas frecuentes (FAQ)

**¿Y si no tengo API key de Gemini?**  
No hay problema. El generador funciona igual. Las secciones que Gemini formatearía quedarán con un marcador de posición indicando que el formateo no está disponible. Usted puede reemplazarlos a mano o pedirnos que lo formateemos en una segunda pasada.

**¿Puedo regenerar el PAC?**  
Sí, tantas veces como necesite. El proceso es **idempotente**: si corre el comando de nuevo con la misma configuración, obtiene el mismo resultado. Si cambia algo en la planilla, el nuevo PAC refleja esos cambios.

**¿Qué pasa si cambia el stack tecnológico?**  
Regenere el PAC. El sistema lee `pom.xml` y `package.json` en cada ejecución, así que si agregan una nueva dependencia o cambian de versión de Java, el PAC se actualiza solo.

**¿Puedo editar `pac_generado.md` directamente a mano?**  
Sí, pero no es lo recomendado. Si edita el markdown a mano y luego vuelve a correr el generador, sus cambios se pierden. Es mejor editar la planilla `pac_config.yaml` y regenerar.

**¿Cuánto tiempo toma?**  
- Llenar la planilla: **5 minutos** si ya tiene los datos.
- Generar el PAC: **10 segundos**.
- Auditar: **5 segundos**.
- Total: menos de 10 minutos para tener un PAC listo para entregar.

---

## 8. Métricas entregadas por el líder

A continuación documentamos textualmente las métricas que usted nos proporcionó y cómo se incorporan al PAC.

### 8.1 Cobertura de Revisiones

> **Fórmula:**  
> `Cobertura de Revisiones = (N° revisados / N° total) × 100`  
> **Meta:** 100%

**¿Qué significa?**  
De cada artefacto que planificamos revisar (ERS, DAS, código, BRIEF), ¿qué porcentaje efectivamente revisamos?

**¿Dónde va en la planilla?**  
En la sección `umbrales` del `pac_config.yaml`:

```yaml
umbrales:
  cobertura_revisiones: 100.0
```

### 8.2 Densidad de Defectos

> **Fórmula:**  
> `Densidad de Defectos = Total defectos / Tamaño del entregable`

**¿Qué significa?**  
Cuántos defectos encontramos por cada unidad de tamaño del entregable. En nuestro caso usamos **defectos por KLOC** (mil líneas de código).

**¿Dónde va en la planilla?**  
En la sección `umbrales` del `pac_config.yaml`:

```yaml
umbrales:
  densidad_defectos_max: 0.5
```

Esto significa: "Aceptamos como máximo 0.5 defectos por cada mil líneas de código." Si el indicador supera ese valor, el entregable debe pasar por una revisión adicional antes de ser aprobado.

---

*Fin del informe.*  
*Si tiene dudas, consúltenos antes de la primera ejecución. Estamos para ayudarle.*
