# Guía de Demo — Simulación de Integración Continua por Sprints del SUT

| Campo | Valor |
|---|---|
| Documento | Guía corta para mostrar al docente la simulación de la IC del SUT sobre la rama `simulacion-desarrollo` (issue #79) |
| Identificador | ANX-SIM-DEMO-001 |
| Versión | 1.0 |
| Fecha | 2026-07-19 |
| Equipo SQA | Equipo 11 — Proyecto 16 (rol `lider-tec`) |
| Anexo hermano | [`simulacion-ic-sprints.md`](simulacion-ic-sprints.md) — la traza formal Sprint→commit/tag/run que la demo recorre |
| Estado | Emitido |

---

## 1. Propósito

El docente tiene ~10–15 minutos para ver la simulación declarada en PP-FIAB-001 §5.2. Esta guía está escrita para que la corrida sea corta, repetible y no requiera nada que no esté en el repositorio. Tres pasos, en este orden:

1. **Re-correr los workflows en vivo** (1–2 min) — demuestra que la IC declarada existe.
2. **Inspeccionar la traza por sprint en `simulacion-desarrollo`** (3–4 min) — los 5 commits y los 5 runs reales.
3. **Levantar la app local** (5–7 min) — el SUT del Equipo 58-1 corre sobre la rama, y el dashboard de métricas publica los M-01..M-06.

---

## 2. Re-correr los workflows en vivo (1–2 min)

Hay dos formas; ambas ejecutan la misma lógica. La primera es la más rápida para una demo:

### 2.1 Disparador desde la interfaz de GitHub

En el navegador, sobre la rama `simulacion-desarrollo`:

1. Ir a **Actions** → seleccionar el workflow `CI Fiabilidad — Simulacion Desarrollo` en el panel izquierdo.
2. Click en **Run workflow** (botón a la derecha del título) → confirmar `Branch: simulacion-desarrollo` → **Run workflow**.
3. Esperar ~30–60 s. La pantalla de runs se actualiza; abrir el run en curso → job `test-fiabilidad` → ver los pasos:
   - `Ejecutar suite regresion (gate) con cobertura JaCoCo` — 1 min, debe pasar.
   - `Ejecutar suite defecto-conocido (informativa, no bloquea)` — 10–30 s, también pasa (las pruebas con `@Tag("defecto-conocido")` fallan como esperan, pero el `continue-on-error: true` deja el job en verde).
   - `Publicar reporte JaCoCo como artefacto` — adjunta `jacoco-coverage-report` con el XML.

### 2.2 Disparador desde la línea de comandos (CLI)

Requiere `gh` autenticado (`gh auth status` → `Logged in to github.com account odjaramillo`):

```bash
# Disparar ci-fiabilidad sobre la rama simulada
gh workflow run ci-fiabilidad.yml --ref simulacion-desarrollo

# Disparar también el workflow e2e contra main (la suite Playwright no
# corre sobre simulacion-desarrollo por la mecánica documentada en
# simulacion-ic-sprints.md §4 desvio G; main es donde se ejecuta)
gh workflow run ci-e2e.yml --ref main
```

Esperar ~30 s y listar:

```bash
gh run list --workflow "ci-fiabilidad.yml" --branch simulacion-desarrollo --limit 1 \
  --json databaseId,status,conclusion,url --jq '.[] | "\(.status)/\(.conclusion)  \(.url)"'
```

### 2.3 Links directos a los runs de la traza original (los del push del 2026-07-19)

| Sprint | Run real (en verde) |
|---|---|
| S0 | [run #29710403835](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/actions/runs/29710403835) |
| S1 | [run #29710462088](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/actions/runs/29710462088) |
| S2 | [run #29710476918](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/actions/runs/29710476918) |
| S3 | [run #29710541583](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/actions/runs/29710541583) |
| S4 | [run #29710568145](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/actions/runs/29710568145) |

Y los tags, visibles en [`/tags`](https://github.com/odjaramillo/gestion-bibliotecaria-sqa/tags):

```bash
git ls-remote --tags origin | grep -E 'refs/tags/sprint-[0-4]$'
# debe listar los 5 tags
```

---

## 3. Inspeccionar la traza por sprint en `simulacion-desarrollo` (3–4 min)

Sobre una copia local del repositorio:

```bash
# 1. Asegurarse de estar en main limpio
git checkout main && git pull

# 2. Traer la rama de simulación y los 5 tags
git fetch origin
git checkout simulacion-desarrollo

# 3. Ver los 5 commits en orden
git log --oneline 2c28118~1..3c05025
# Esperado: 5 commits, todos con scope feat(sut)/chore(sut), cada uno
# declarando el re-commit simulado del codigo de Equipo 58-1.

# 4. Ver los tags sobre los commits correctos
git tag -l 'sprint-*' --format='%(refname:short) -> %(objectname:short) %(subject)'
# Esperado: 5 tags sprint-0..sprint-4 sobre los 5 commits.

# 5. Diff contra main: todo el codigo del SUT del Equipo 58-1 esta en
# esta rama, pero main no la ve (la rama NO se mergea).
git log --oneline main..simulacion-desarrollo | wc -l   # esperado: 5
git diff main...simulacion-desarrollo --stat | tail -1   # lineas del delta
```

Lo que se está viendo:

- **5 commits acumulativos hacia adelante**: S0 deja solo el skeleton + `ci-fiabilidad.yml`; cada commit subsiguiente suma componentes del SUT. El SUT en `main` queda intacto: la rama es declarativa.
- **Cada mensaje declara honestidad**: en el cuerpo del commit está escrito *re-commit simulado del codigo de Equipo 58-1 para PP-FIAB-001 §5.2*, con la razón del re-commit y lo que NO se hace (no se rellena con código nuevo lo que el Equipo 58-1 no implementó).
- **El Controller entra monolítico en S4**: el diff de S4 lo muestra; no es un bug, es la forma del SUT del Equipo 58-1 — el plan asumía granularidad por dominio, el SUT no lo admite.

El anexo [`simulacion-ic-sprints.md`](simulacion-ic-sprints.md) tiene la tabla formal Sprint → commit/tag/run/URL para llevarla impresa o en otra pestaña.

---

## 4. Levantar la app local (5–7 min)

El SUT del Equipo 58-1 corre sobre `simulacion-desarrollo` con H2 (perfil `test`) o con MySQL 8.0 (perfil por defecto). Para la demo es suficiente con **H2** porque no se necesita persistencia entre reinicios y la app levanta en segundos.

### 4.1 Prerrequisitos verificados

- **JDK 21 (Temurin)**. Verificar:
  ```bash
  /usr/lib/jvm/java-21-openjdk-amd64/bin/java -version
  # openjdk version "21.0.x" ...
  ```
  Si el `java` por defecto es otro (típicamente JDK 25 en sistemas nuevos), exportar `JAVA_HOME` antes de cualquier `mvn`/`mvnw`:
  ```bash
  export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
  export PATH="$JAVA_HOME/bin:$PATH"
  ```
  Sin esta variable, el wrapper falla con errores de compilación incompatibles (el spike de factibilidad obs #1529 lo documenta como gotcha de entorno).
- **Maven Wrapper** (`.mvnw`, ya commiteado). No requiere instalación global de Maven.
- **Node 18+ y npm 9+** (para el frontend Vue 3). El repositorio trae `package-lock.json` y `biblioteca-frontend/node_modules/` ya instalado en este checkout, pero por seguridad:
  ```bash
  cd biblioteca-frontend && npm ci
  ```
- **MySQL 8.0** (opcional). Si está disponible, la app usa la conexión de `src/main/resources/application.properties` (`jdbc:mysql://localhost:3306/biblioteca_db` con `root`/`admin`). Si no, el perfil `test` (H2) es suficiente para la demo.

### 4.2 Backend (Spring Boot)

Sobre `simulacion-desarrollo`, en una terminal:

```bash
# 1. Asegurar JDK 21 (exportar si no esta por defecto)
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
export PATH="$JAVA_HOME/bin:$PATH"

# 2. Levantar la app con H2 (perfil test, sin MySQL)
./mvnw spring-boot:run -Dspring-boot.run.profiles=test
# Espera ~20-30s. Log final: "Started GestionBibliotecariaApplication ..."
# Puerto por defecto: 8080.
```

Verificación rápida desde otra terminal:

```bash
# GET /api/libros: debe devolver [] (base vacia) o 401 si la app esta
# bajo SecurityConfig con autenticacion requerida. Ambos son validos.
curl -i http://localhost:8080/api/libros
# Esperado: HTTP 200 [] (con el codigo del Equipo 58-1 sobre H2) o
# HTTP 401 (si la configuracion de Spring Security esta activa).

# POST /api/usuarios/registro: alta de un usuario de prueba
curl -i -X POST http://localhost:8080/api/usuarios/registro \
  -H 'Content-Type: application/json' \
  -d '{"nombre":"Demo","correo":"demo@biblioteca.test","contrasena":"clave","rol":"USUARIO"}'
# Esperado: HTTP 200 "Usuario registrado con exito."
```

### 4.3 Frontend (Vue 3)

En otra terminal:

```bash
cd biblioteca-frontend

# Levantar el dev server. Vue CLI escucha en el puerto 5173 (pineado en
# playwright.config.js para no chocar con el backend en 8080) y proxy
# /api -> http://localhost:8080 (ver vue.config.js).
npm run serve
# Espera ~10-20s. Log final: "App running at: http://localhost:5173"
```

Abrir <http://localhost:5173> en el navegador. El frontend hace login contra `/api/login` y consume los endpoints del backend a través del proxy. **Si la pantalla de login no responde**, casi siempre es porque el backend no está levantado o está en otro puerto.

### 4.4 Apagar la app

Ctrl-C en cada terminal. El backend cierra el contexto Spring y libera el puerto 8080; el frontend cierra el dev server de webpack.

### 4.5 Verificación de la suite JVM (si hay tiempo)

Sobre `simulacion-desarrollo`, en una tercera terminal:

```bash
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
export PATH="$JAVA_HOME/bin:$PATH"

# Solo el gate regresion (~30s)
./mvnw test -Dgroups=regresion -DfailIfNoTests=true

# Suite completa regresion + defecto-conocido (~1-2 min)
./mvnw verify -Dgroups=regresion -DfailIfNoTests=true
./mvnw test -Dgroups=defecto-conocido -DfailIfNoTests=false \
    -Djacoco.skip=true
```

> **Lectura honesta del resultado.** El gate `regresion` debe pasar **en verde** (8 clases, 23 tests, 0 fallos, 0 errores). La suite `defecto-conocido` ejecuta pruebas que **fallan como esperan** (codifican defectos reales del SUT del Equipo 58-1 — WT-01, WT-04, TCOND-M6 — y eso es la señal, no un bug). El warning de JaCoCo sobre `com.biblioteca.service.PrestamoService: branches covered ratio is 0.60, but expected minimum is 0.70` es **informativo y esperado**: M-02 = 60.7% es la métrica real del SUT, no la planificada (≥ 70%). Ver `sqa/anexos/simulacion-ic-sprints.md` §4 desvio C.

---

## 5. El dashboard de métricas (referencia)

El [dashboard publicado en GitHub Pages](https://odjaramillo.github.io/gestion-bibliotecaria-sqa/) muestra los seis M-01..M-06 ratificados del SUT. La fuente de datos es el artefacto `metricas/reporte_kpi.json` recalculado por `sqa/metricas/calcular_kpi.py` en cada push a `main` (workflow `ci-metricas.yml`). El `simulacion-desarrollo` no recalcula las métricas — el SUT no cambió — pero el dashboard sigue siendo la lectura oficial de los M-01..M-06.

> **Si la demo se hace offline.** El dashboard requiere Pages, que requiere red. La misma información está en `metricas/reporte_kpi.json` dentro del checkout local; abrir el archivo y leer la sección M-01..M-06 da los mismos números.

---

## 6. Tiempo estimado

| Paso | Minutos |
|---|---|
| Disparar workflow `ci-fiabilidad` en vivo y observar la corrida | 1–2 |
| Recorrer `git log` / `git tag` sobre `simulacion-desarrollo` con la tabla del anexo al lado | 3–4 |
| Levantar backend (`./mvnw spring-boot:run`) + smoke con `curl` | 2–3 |
| Levantar frontend (`npm run serve`) y mostrar la pantalla de login | 2–4 |
| Mostrar el dashboard de métricas (online) o `metricas/reporte_kpi.json` (offline) | 1 |
| **Total** | **9–14 min** |

Para una demo corta, saltear el paso 4 (app local) y mostrar solo el paso 2 (traza por sprint) lleva la corrida a **3–5 min**.

---

## 7. Si algo no anda

| Síntoma | Causa más probable | Solución |
|---|---|---|
| `./mvnw` falla con `release version 21 not supported` | JDK por defecto no es 21 | `export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64` y reintentar |
| `git checkout simulacion-desarrollo` dice "branch not found" | el fetch no trajo la rama | `git fetch origin && git checkout simulacion-desarrollo` |
| Workflow `ci-fiabilidad` run en rojo | cambio reciente rompió el build | abrir el run, leer el log del job `test-fiabilidad`, generalmente el warning de JaCoCo es lo unico "rojo" y NO falla el job — el run queda en verde |
| Frontend en blanco tras login | backend no levantado o proxy mal apuntado | confirmar `./mvnw spring-boot:run` activo en :8080 y `biblioteca-frontend/vue.config.js` con `proxy: 'http://localhost:8080'` |
| Tests `defecto-conocido` fallan en local | comportamiento esperado, codifican WT-01/WT-04/TCOND-M6 | ver INF-RES-001 §4.1..§4.3 y el Javadoc de cada test (`@see INC-WT-XX`); el `continue-on-error: true` del workflow los absorbe |

---

## 8. Control de versiones

| Versión | Fecha | Autor | Cambios |
|---|---|---|---|
| 1.0 | 2026-07-19 | Equipo SQA — rol `lider-tec` | Emisión de la guía de demo de la simulación de IC por sprints del SUT (issue #79): re-corrido de workflows por CLI y por UI, inspección local de la traza por sprint en `simulacion-desarrollo`, levantada local del backend (H2, JDK 21) y del frontend (Vue 3, puerto 5173), troubleshooting de los gotchas de entorno más comunes. |
