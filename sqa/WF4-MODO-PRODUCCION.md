# WF4 — Modo Producción

## Checklist de Activación

**ESTADO ACTUAL:** `dry_run: true`

**INSTRUCCIÓN CRÍTICA:** NO activar el modo producción hasta que el **Líder General (Alberto Rodríguez)** apruebe formalmente las checklists de inspección estática.

---

## Cambios Necesarios para Pasar a Producción

### 1. Variable de Entorno `DRY_RUN`

```yaml
# .github/workflows/wf4_orquestador.yml
env:
  DRY_RUN: false   # <-- Cambiar de true a false
```

También puede inyectarse como secret:

```bash
export DRY_RUN=false
```

### 2. Credenciales de Jira

El script `scripts/wf4_orquestador.py` debe recibir las siguientes variables de entorno:

| Variable | Descripción | Ejemplo |
|---|---|---|
| `JIRA_SERVER` | URL base de la instancia Jira | `https://sqa11.atlassian.net` |
| `JIRA_EMAIL` | Correo del bot de SQA | `sqa-bot@empresa.com` |
| `JIRA_API_TOKEN` | Token API de Jira | `ATATT3xFfGF0...` |
| `JIRA_PROJECT_KEY` | Clave del proyecto SQA | `SQA11` |

**En GitHub Actions:**

```yaml
- name: Ejecutar WF4 Orquestador
  env:
    DRY_RUN: false
    JIRA_SERVER: ${{ secrets.JIRA_SERVER }}
    JIRA_EMAIL: ${{ secrets.JIRA_EMAIL }}
    JIRA_API_TOKEN: ${{ secrets.JIRA_API_TOKEN }}
    JIRA_PROJECT_KEY: ${{ secrets.JIRA_PROJECT_KEY }}
  run: python scripts/wf4_orquestador.py
```

### 3. Credenciales de Confluence

| Variable | Descripción | Ejemplo |
|---|---|---|
| `CONFLUENCE_URL` | URL base de Confluence | `https://sqa11.atlassian.net/wiki` |
| `CONFLUENCE_SPACE` | Clave del espacio | `SQA` |
| `CONFLUENCE_API_TOKEN` | Token API (puede reusar el de Jira en Atlassian Cloud) | `ATATT3xFfGF0...` |

### 4. Dependencias Adicionales

Si se implementa extracción de texto de PDFs para verificación real, descomentar en `requirements.txt`:

```text
PyMuPDF>=1.24.0
```

Esto habilitaría `fitz` para leer contenido de los PDFs en `documentacion/`.

---

## Payload JSON de Ejemplo para Jira

### Crear Issue Principal de Inspección

```json
{
  "project": {
    "key": "SQA11"
  },
  "issuetype": {
    "name": "Inspección"
  },
  "summary": "Inspección Estática: ERS Equipo 58-1 v1.2",
  "description": "Checklist de inspección estática según ISO/IEC/IEEE 29148:2018\n\nArtefacto: ERS Equipo 58 1 v.1.2.pdf\nChecklist Version: 1.0",
  "customfield_10001": "ERS"
}
```

### Crear Subtarea por Defecto

```json
{
  "project": {
    "key": "SQA11"
  },
  "issuetype": {
    "name": "Subtarea"
  },
  "parent": {
    "key": "SQA-123"
  },
  "summary": "[ERS-02] Inconsistencia de versión (1.1 vs 1.2)",
  "description": "**Checklist ID:** ERS-02\n**Severidad:** Media\n\n**Descripción:** La versión en portada (1.1) no coincide con la del histórico (1.2).\n\n**Evidencia:** Página 1 vs Página 2",
  "priority": {
    "name": "Medium"
  }
}
```

---

## Payload de Ejemplo para Confluence

### Crear Página de Acta de Inspección

```json
{
  "type": "page",
  "title": "Acta de Inspección: ERS Equipo 58-1 v1.2 — 2026-05-05",
  "space": {
    "key": "SQA"
  },
  "ancestors": [
    {
      "id": "12345678"
    }
  ],
  "body": {
    "storage": {
      "value": "<h1>Acta de Inspección</h1><p><strong>Fecha:</strong> 2026-05-05</p><p><strong>Inspector:</strong> WF4 Orquestador</p><p><strong>Estándar:</strong> ISO/IEC/IEEE 29148:2018</p><table>...</table>",
      "representation": "storage"
    }
  }
}
```

---

## Lógica de Calidad (Quality Gate)

Un artefacto **NO puede pasar** a los workflows posteriores hasta que:

1. Todas las subtareas del checklist estén en estado `DONE`, **O**
2. Los defectos encontrados estén documentados como **Bugs Documentales** en Jira con su ID de checklist.

El WF4 debe bloquear físicamente (fail CI) si hay defectos `Crítica` o `Alta` sin justificación escrita del Líder General.

---

## Responsables de Aprobación

| Rol | Nombre | Acción Requerida |
|---|---|---|
| Líder General | Alberto Rodríguez | Aprobación formal de checklists |
| Líder Tecnológico | Oscar | Validación técnica de integración CI |
| Líder Funcional | Daniel | Validación de mapeo artefacto→estándar |

---

## Registro de Cambios

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| 1.0 | 2026-05-05 | SQA 11 | Documento inicial — modo dry_run |

---

**Fin del documento**
