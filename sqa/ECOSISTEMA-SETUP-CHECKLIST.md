# Checklist de activación — Ecosistema SQA en GitHub

**Equipo 58-1 — Gestión Bibliotecaria**
**Estado del repo:** los archivos del ecosistema (labels, templates, workflows, CI, métricas)
ya están en el repositorio. Esta lista cubre lo que **NO se puede automatizar desde el código**
y requiere acciones manuales del equipo (cuentas externas, tokens, configuración de UI).

Referencia completa: [`PLAN_ECOSISTEMA_SQA.md`](../PLAN_ECOSISTEMA_SQA.md).

---

## 1. Sincronizar la taxonomía de etiquetas

```bash
gh label sync -f .github/labels.yml
```

Tras el primer push a `main`, el workflow `sync-labels.yml` lo hace solo cuando cambia
`.github/labels.yml`. La primera vez conviene correrlo a mano para no depender del trigger.

- [ ] `gh label list` muestra todas las etiquetas (`tipo:`, `area:`, `severidad:`, `estado:`, `rol:`, `fase:`, `iso:`).

---

## 2. GitHub Projects v2 (tablero compartido para el docente)

```bash
# Crea el tablero. Anotar el número N que devuelve.
gh project create --owner "@me" --title "SQA — Gestión Bibliotecaria Equipo 58-1"
```

- [ ] Reemplazar `REEMPLAZAR_N` en `.github/workflows/pr-project.yml` (línea `project-url`) por el número real.
- [ ] Crear el secret `PROJECT_TOKEN` (Settings → Secrets → Actions): PAT con scopes `repo` y `project`.
- [ ] Configurar campos del tablero (Status, Fase, Severidad, Rol) y las 5 vistas (ver Plan §7.3–7.4).

> El `GITHUB_TOKEN` por defecto **no** alcanza para Projects v2 — por eso se usa `PROJECT_TOKEN`.

---

## 3. Milestones (⚠️ el plan tenía un error aquí)

`gh milestone create` **no existe** en la CLI de `gh`. Los milestones se crean vía API:

```bash
gh api repos/odjaramillo/gestion-bibliotecaria-sqa/milestones \
  -f title="Fase 1 — Técnicas Estáticas" \
  -f description="Inspección, walkthrough y auditoría sobre ERS y DAS" \
  -f due_on="2026-07-13T23:59:59Z"

gh api repos/odjaramillo/gestion-bibliotecaria-sqa/milestones \
  -f title="Fase 2 — Técnicas Dinámicas" \
  -f description="Pruebas unitarias, integración, sistema y aceptación + CI" \
  -f due_on="2026-08-31T23:59:59Z"
```

- [ ] Ajustar las fechas `due_on` (formato ISO 8601 UTC) a las reales de entrega.
- [ ] Verificar con `gh api repos/odjaramillo/gestion-bibliotecaria-sqa/milestones --jq '.[].title'`.

---

## 4. SonarCloud

El repositorio ya es **público**, así que el plan gratuito de SonarCloud aplica sin costo.

- [ ] Iniciar sesión en [sonarcloud.io](https://sonarcloud.io) con GitHub e importar el repo.
- [ ] Copiar **Project Key** y **Organization Key** → reemplazarlos en:
  - `sonar-project.properties`
  - `.github/workflows/ci-static.yml` (args `sonar.projectKey` / `sonar.organization`)
  - `.github/workflows/ci-tests.yml` (idem)
- [ ] Crear el secret `SONAR_TOKEN` (Settings → Secrets → Actions).

> Los workflows ya están protegidos con `if: ${{ env.SONAR_TOKEN != '' }}`: si el secret no
> existe, el paso de Sonar se salta sin romper el pipeline. El resto del análisis estático
> (Checkstyle, SpotBugs, PMD) corre igual y publica los XML como artefactos.

---

## 5. Acceso del docente

- [x] **Repositorio público** → el docente ve issues, PRs, Actions y commits sin ser colaborador.
- [ ] Asegurar que el tablero Projects v2 sea visible (Settings del proyecto → Visibility: Public).
- [ ] Compartir el enlace único:
  ```
  Repositorio:  https://github.com/odjaramillo/gestion-bibliotecaria-sqa
  Tablero SQA:  https://github.com/users/odjaramillo/projects/N
  SonarCloud:   https://sonarcloud.io/project/overview?id=<PROJECT_KEY>
  ```

---

## 6. Entregables que NO produce este ecosistema (recordatorio de rúbrica)

El ecosistema técnico cubre la trazabilidad, automatización y métricas, pero la rúbrica
exige además dos artefactos de documentación que el equipo debe elaborar aparte:

- [ ] **Infograma del Ecosistema Tecnológico** — diagrama visual de herramientas e integración
  (GitHub Issues/Projects ↔ Actions ↔ SonarCloud ↔ métricas ↔ IA). Apéndice del PACS.
- [ ] **Reflexión crítica sobre el ecosistema** — ventajas, limitaciones, oportunidades de mejora,
  y qué herramientas de IA apoyan el proceso y cómo. Apéndice del PACS.

> Ambos pesan en la rúbrica (5 pts el criterio de ecosistema, 5 pts la reflexión en Fase 2).

---

## 7. Verificación local (cuando haya Java 21 + Maven)

```bash
# Análisis estático local (no requiere los servicios externos)
./mvnw compile checkstyle:check spotbugs:check pmd:check -DskipTests

# Cobertura (puede no generar nada si aún no hay tests — esperado en Fase 1)
./mvnw test jacoco:report
```

- [ ] `./mvnw compile checkstyle:check` termina sin error de compilación.
