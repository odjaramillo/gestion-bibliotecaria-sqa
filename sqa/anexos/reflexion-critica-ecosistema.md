# Anexo — Reflexión Crítica sobre el Ecosistema Tecnológico

| Campo | Valor |
|---|---|
| Documento | Reflexión crítica sobre el ecosistema tecnológico — apéndice de `sqa/PACS.md` §4.3 |
| Identificador | ANX-REF-001 |
| Versión | 1.0 |
| Fecha | 2026-07-12 |
| Equipo SQA | Equipo 11 — Proyecto 16 |
| Issue | #10 |
| Estado | Emitido |

---

## 1. Propósito y alcance

Este anexo satisface el criterio **e) Ecosistema tecnológico** de la rúbrica en su componente de **análisis crítico**: las decisiones tomadas en la selección e integración de herramientas, qué herramientas de IA apoyan el proceso y cómo, y las ventajas, limitaciones y oportunidades de mejora del ecosistema resultante.

Es el complemento argumentativo del [infograma](infograma-ecosistema.md) (ANX-ECO-001): aquel **muestra** el ecosistema; este lo **juzga**.

La reflexión se apoya en evidencia verificable del repositorio —commits, workflows, artefactos— y no en apreciaciones generales. Cada afirmación puede rastrearse.

---

## 2. El punto de partida: qué se construyó en Fase 1 y por qué se desmanteló

Cualquier reflexión sobre este ecosistema debe empezar por reconocer que **el ecosistema actual es el segundo**. El primero se abandonó.

En Fase 1, el Equipo 11 construyó un sistema de agentes de IA sobre Gemini: siete workflows encadenados (`wf1_auditoria_requisitos`, `wf2_inspeccion_arquitectura`, `wf3_generacion_pruebas`, `wf4_orquestador` y un `wf7` que publicaba a Confluence con integración a Jira), respaldados por un paquete `scripts/` con clientes, prompts *few-shot* y una suite de 99 tests automatizados. Era una pieza de ingeniería considerable.

**No funcionó como sistema de aseguramiento de la calidad.** Tres hechos, verificables en el historial:

1. **Nunca se ejecutó de verdad.** Los cuatro workflows de análisis quedaron declarados en estado `dry_run` (`herramientas-fase2.md` §6). Producían tests de sí mismos, no evidencia sobre el SUT.
2. **La IA alucinaba, y hubo que contenerla.** Existe un commit cuyo mensaje es, literalmente, `security(wf1-wf4): blinda workflows contra alucinaciones de Gemini` (`900e4ba`), que añade validación de esquema y recorte de salidas en los cuatro agentes. El equipo descubrió en carne propia que un modelo generativo produce salidas *plausibles*, no necesariamente *verdaderas*.
3. **El resultado fue insuficiente.** El commit de desmantelamiento (`a25fab4`) lo consigna sin eufemismos: *«Fase 1 obtuvo 15/30; este material no aportó a la nueva línea»*.

El diagnóstico retrospectivo es incómodo pero claro: **se optimizó la sofisticación de la herramienta y no la producción de evidencia**. Los 99 tests probaban los agentes; ninguno probaba el SUT. La rúbrica no pedía un orquestador de agentes: pedía checklists aplicadas, hallazgos registrados, revisiones documentadas.

La decisión de borrarlo entero (`38b0069`, `a25fab4`) y migrar a un ecosistema nativo de GitHub fue **la decisión técnica más importante del proyecto**, y se tomó contra el costo hundido de 99 tests y varias semanas de trabajo. La lección que el equipo extrae no es *«la IA no sirve»*, sino una más precisa y más útil, que estructura todo lo que sigue:

> **Una herramienta de aseguramiento vale por la evidencia que produce, no por su complejidad. Si no deja una traza auditable sobre el sistema bajo prueba, no pertenece al ecosistema.**

---

## 3. Decisiones de selección e integración del ecosistema actual

### 3.1 GitHub-native por encima de Jira + Confluence

**Decisión.** Todo el ecosistema vive en GitHub: issues, tablero, CI, análisis estático, métricas y publicación. Se descartaron Jira y Confluence, que el enunciado admitía.

**Razón — y no es de comodidad.** IEEE 730 exige revisión por pares de los entregables. Al vivir los documentos como markdown en `sqa/` y revisarse por Pull Request, **la aprobación queda registrada en la misma herramienta que custodia el artefacto**. Un Confluence habría partido la cadena de evidencia en dos: el documento en un lado, su aprobación en otro, unidos por un enlace que nadie audita. La trazabilidad dejó de ser una promesa documental para volverse una propiedad estructural del repositorio.

**Costo asumido.** Se resignó la comodidad de un editor WYSIWYG y de los tableros ricos de Jira. Para un equipo de cinco personas que ya trabaja en Git, el intercambio fue favorable.

### 3.2 La taxonomía como código

**Decisión.** Las 34 etiquetas (`tipo` · `área` · `severidad` · `estado` · `rol` · `fase` · `iso`) se declaran en un archivo versionado y las sincroniza `sync-labels.yml`.

**Razón.** Una taxonomía que vive en la memoria del equipo se erosiona: alguien escribe `bug` donde correspondía `tipo:defecto` y la métrica se degrada en silencio. Al declararla como código, la clasificación se vuelve **verificable y reproducible**, que es la precondición para que `calcular_kpi.py` derive métricas de proceso confiables desde los issues.

### 3.3 La métrica se mide, no se declara

**Decisión.** Las métricas automáticas (M-02, M-03, M-04) se derivan de artefactos reales de ejecución —`jacoco.xml`, reportes Surefire, `issues_export.json`— y el dashboard distingue explícitamente las **medidas** de las **declaradas**.

**Razón.** Es el principio central del ecosistema y la corrección directa del error de Fase 1. Un número sin artefacto que lo respalde no es una métrica: es una afirmación. Las que hoy no pueden medirse automáticamente (M-01, M-05, M-06) se muestran como declaradas y esperan la firma del Líder de Métricas (#24) en lugar de disfrazarse de medición.

### 3.4 Dos universos de prueba

**Decisión.** La suite dinámica está partida en `@Tag("regresion")` —el gate de integración— y `@Tag("defecto-conocido")` —pruebas que codifican defectos reales del SUT y fallan de forma esperada, ejecutadas de modo informativo (`ci-tests.yml`).

**Razón.** El SUT está congelado: el Equipo 11 audita, no corrige. Sin esa partición, el equipo habría enfrentado un dilema falso —o el CI queda permanentemente en rojo, o no se escriben las pruebas que revelan los defectos—. La partición **convierte el defecto en evidencia sin destruir la señal del gate**: la cobertura y las métricas se calculan solo sobre `regresion`, de modo que el número publicado siga significando algo.

### 3.5 El instrumento de medición también se prueba

**Decisión.** `ci-metricas.yml` corre `pytest` sobre `calcular_kpi.py` y el generador del dashboard.

**Razón.** Un sistema de calidad que no verifica su propia herramienta de medición no tiene autoridad para publicar los números que produce. Es la aplicación del propio criterio del equipo sobre sí mismo.

---

## 4. Herramientas de IA en el proceso: cuáles, cómo, y qué se aprendió

El enunciado pregunta explícitamente **qué herramientas de IA apoyan el proceso y cómo**. La respuesta requiere distinguir tres usos con resultados muy distintos.

### 4.1 IA como agente autónomo — RETIRADA

Los workflows WF1–WF4 sobre Gemini (auditoría de requisitos, inspección arquitectónica con análisis visual de diagramas C4/UML, generación de plan de pruebas, orquestación de quality gates) representaban a la IA **ejecutando el proceso**.

Se retiraron. Las razones están en §2: nunca salieron de `dry_run`, requirieron blindaje explícito contra alucinaciones, y no produjeron evidencia auditable sobre el SUT.

**Conclusión.** La IA como agente autónomo dentro del gate de calidad **introdujo un riesgo que el ecosistema no podía absorber**: un modelo que alucina un hallazgo inexistente contamina el registro de defectos, y un registro de defectos contaminado invalida toda métrica derivada de él. En un sistema cuya premisa es *la métrica se mide, no se declara*, no hay lugar para un componente que **fabrica** afirmaciones plausibles.

### 4.2 IA como asistente de análisis, con salida revisada — RETENIDA

La **auditoría estática asistida con IA** sobre ISO/IEC 25010 sí produjo un entregable real y vigente: [`2026-06-02_auditoria-estatica-fiabilidad-iso25010.pdf`](../fase2/estaticas/2026-06-02_auditoria-estatica-fiabilidad-iso25010.pdf), declarado en `PACS.md` §5.1 como técnica estática completada.

La diferencia con §4.1 es estructural, no de herramienta: **aquí la IA no cierra el circuito**. Propone hallazgos; el equipo los valida contra el código, los clasifica en la taxonomía y los registra como issues trazables. La salida del modelo es *materia prima*, no *veredicto*.

### 4.3 IA como generador de artefactos — ÚTIL Y PELIGROSA A LA VEZ

El caso más instructivo del proyecto está en [`Generacion de Casos de Pueba.md`](../fase2/planificacion/Generacion%20de%20Casos%20de%20Pueba.md): la salida cruda de un LLM al que se le pidió especificar casos de prueba de Fiabilidad.

Produjo **24 casos** (`CT-FIA-01` … `CT-FIA-24`), impecablemente formateados, con datos de prueba y citas a ISO 25010, repartidos en **cuatro** sub-características: Madurez, Disponibilidad, Tolerancia a Fallos y Capacidad de Recuperación.

**El alcance aprobado del proyecto son dos**: Madurez y Tolerancia a Fallos (`objetivos.txt`, `EST-FIAB-001` §8). **La mitad de esa salida estaba fuera de alcance** — y era la mitad más convincente, porque nada en su forma delataba el error. El modelo no se equivocó en la sintaxis: se equivocó en el **encuadre**, que es precisamente lo que no puede delegarse.

Ese material se retrabajó a mano hasta convertirse en `TCS-FIAB-001` (11 casos, anclados al código, trazados a M-01..M-06) y `ANX-FIAB-001` (13 casos diferidos con justificación). La IA aceleró la redacción; **el criterio de alcance lo puso el equipo**.

### 4.4 El principio destilado

> **La IA propone; el estándar dispone; el humano firma.**

Toda salida de un modelo entra al ecosistema como **propuesta** y solo se convierte en **artefacto** después de atravesar el mismo control que cualquier otro entregable: validación contra la fuente, encuadre en el estándar aplicable, y revisión por pares registrada en un Pull Request. El ecosistema no distingue si un documento lo escribió una persona o un modelo; **exige la misma evidencia a los dos**. Esa simetría es deliberada, y es lo que permite usar IA sin degradar la confiabilidad del proceso.

---

## 5. Ventajas del ecosistema actual

- **Trazabilidad estructural.** Hallazgo → issue etiquetado → rama → Pull Request revisado → merge → métrica. La cadena no depende de que alguien recuerde documentarla: es el propio flujo de trabajo.
- **Evidencia sobre declaración.** Cada número publicado nace de un artefacto de ejecución. Lo que no se puede medir se marca como declarado, no se disimula.
- **Costo cero de infraestructura.** El ecosistema completo corre sobre el plan gratuito de GitHub y SonarCloud para repositorios públicos. No hay servidores, licencias ni credenciales que administrar.
- **Verificabilidad por terceros.** El repositorio es público: el docente audita issues, PRs, Actions, tablero y dashboard **sin credenciales y sin ser colaborador**. La transparencia no es un informe: es acceso directo a la fuente.
- **El proceso se prueba a sí mismo.** `ci-metricas.yml` verifica el instrumento de medición.
- **Reversibilidad.** Todo el ecosistema es texto versionado —workflows, etiquetas, documentos, el propio infograma—. Cualquier decisión puede auditarse y revertirse en el historial.

---

## 6. Limitaciones — lo que este ecosistema todavía no resuelve

Se enuncian sin atenuantes. Cada una tiene issue de seguimiento.

| # | Limitación | Impacto | Issue |
|---|---|---|---|
| L1 | **SonarCloud analiza sin datos de cobertura.** El scan corre en `ci-static.yml`, que compila sin ejecutar pruebas; el `jacoco.xml` nace en `ci-tests.yml`. Los dos insumos existen y nunca coinciden en el mismo job. | Cualquier Quality Gate basado en *coverage on new code* es hoy inaplicable. Riesgo de doble verdad si Sonar llegara a medir cobertura sobre un alcance distinto al de M-02. | [#31](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/31) |
| L2 | **Pruebas de aceptación (resuelta tras esta reflexión).** Era el único nivel dinámico sin implementar; se completó con Playwright end-to-end (`ci-e2e.yml`), de modo que los cuatro niveles del `PP-FIAB-001` quedan cubiertos. | La perspectiva del usuario final quedó verificada. Limitación cerrada. | [#34](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/34) |
| L3 | **M-01, M-05 y M-06 son valores declarados**, no medidos automáticamente, y sus umbrales siguen marcados `[PROP]` sin ratificación formal. | El dashboard lo señala explícitamente, pero un tercio del marco de métricas no se auto-verifica. | [#24](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/24) |
| L4 | **GitHub Pages admite un único deployment por repositorio**, hoy ocupado por el dashboard. Publicar los documentos exige integrarlos al mismo artefacto, no agregar un segundo workflow. | Restricción de plataforma, no de diseño. Condiciona cómo se publica la documentación SQA. | [#3](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/3) |
| L5 | **Desvío de herramienta en el nivel de sistema**: se planificó Postman/RestAssured y se implementó MockMvc. El desvío está justificado y registrado (`PACS.md` §5.1), pero revela que la selección de herramientas se hizo **antes** de validar su encaje real en el pipeline. | Menor en el resultado; relevante como aprendizaje de proceso. | — |
| L6 | **El SUT está congelado.** El Equipo 11 no puede corregir los defectos que encuentra: solo registrarlos. | El ciclo de aseguramiento queda abierto — se detecta, no se remedia. Es una restricción del encuadre académico, no una falla del ecosistema. | — |
| L7 | **La automatización del tablero es parcial.** La columna *Status* de Projects v2 no se sincroniza desde las etiquetas `estado:*`; hay dos fuentes de verdad para el mismo dato. | Riesgo de divergencia entre el tablero que ve el docente y las etiquetas que consumen las métricas. | [#11](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/11) |

---

## 7. Oportunidades de mejora

Ordenadas por relación entre valor y costo.

1. **Cerrar el circuito de cobertura hacia SonarCloud (#31).** Es la limitación de mayor impacto y la de arreglo más directo tras la migración a `sonar-maven-plugin`. Requiere una decisión de diseño —dónde vive el scan— preservando la invariante de un único análisis por `projectKey`.
2. **Implementar el nivel de aceptación con Playwright (#34).** Completa el `PP-FIAB-001` y cierra un desvío en lugar de abrirlo: Playwright ya estaba declarado como herramienta prevista.
3. **Ratificar M-01, M-05 y M-06 (#24).** Convierte un tercio del marco de métricas de *declarado* a *acordado*, y habilita fijar umbrales con autoridad.
4. **Unificar la fuente de verdad del estado (#11).** Que la columna del tablero se derive de las etiquetas elimina la divergencia de raíz en vez de administrarla.
5. **Publicar los documentos SQA en el sitio (#3).** Hoy la evidencia existe pero exige navegar el repositorio para leerla.
6. **Elevar `defecto-conocido` a informe formal de resultados.** Las pruebas que codifican defectos son la evidencia más valiosa que produjo la Fase 2 dinámica; hoy viven como código y merecen un informe que las consolide y las trace a los hallazgos del walkthrough.

---

## 8. Evaluación de la integración

La rúbrica no pide un inventario de herramientas sino una **evaluación de cómo se integran**. El criterio con el que el equipo la juzga es la continuidad de la cadena de evidencia: *¿puede seguirse un hallazgo desde su origen hasta la métrica publicada sin intervención manual ni salto de herramienta?*

**Cadenas completas.** El eje `commit → ci-tests → jacoco.xml/Surefire → calcular_kpi.py → dashboard → Pages` está cerrado de punta a punta: el dato nace de la ejecución real y llega publicado sin que nadie lo transcriba. Lo mismo el eje de proceso: `issue etiquetado → issues_export.json → KPIs de proceso`. Que la taxonomía sea código es lo que sostiene esa segunda cadena.

**Cadenas rotas.** Dos, ambas conocidas y registradas. El eje `ci-tests → SonarCloud` está **cortado** (L1): SonarCloud es hoy un satélite del ecosistema, no un integrante —analiza, pero no participa de la cadena de cobertura—. Y el eje `etiquetas estado:* → columna del tablero` está **duplicado** (L7): dos fuentes de verdad para un mismo dato.

**Veredicto.** La integración es **sólida en el eje de medición y débil en el eje de análisis estático**. El ecosistema mide bien lo que ejecuta y todavía no cierra el circuito con la herramienta que lo analiza. Es una brecha real, está identificada con causa raíz, y es la primera de la lista de mejoras.

Que el ecosistema pueda enunciar con precisión dónde está roto es, en sí mismo, el resultado del principio que lo ordena: **un sistema de calidad que no puede auditarse a sí mismo no está en condiciones de auditar a otro.**

---

## 9. Trazabilidad

- **Apéndice de**: [`sqa/PACS.md`](../PACS.md) §4.3
- **Complementa**: [`infograma-ecosistema.md`](infograma-ecosistema.md) (ANX-ECO-001) — el esquema visual del ecosistema aquí evaluado
- **Matriz operativa**: [`herramientas-fase2.md`](herramientas-fase2.md)
- **Evidencia citada**: commits `900e4ba` (blindaje contra alucinaciones), `38b0069` y `a25fab4` (desmantelamiento del sistema de agentes); workflows en `.github/workflows/`; `PACS.md` §5.1
- **Issues referenciados**: #3, #11, #24, #31, #34

---

## 10. Control de versiones

| Versión | Fecha | Autor | Cambios |
|---|---|---|---|
| 1.0 | 2026-07-12 | Equipo SQA — rol `metricas` | Emisión inicial de la reflexión crítica del ecosistema tecnológico (issue #10): decisiones de selección e integración, análisis del uso de IA en las tres modalidades aplicadas (agente autónomo retirado, asistente de análisis retenido, generador de artefactos supervisado), ventajas, siete limitaciones con issue de seguimiento, oportunidades priorizadas y evaluación de la integración por continuidad de la cadena de evidencia. |
