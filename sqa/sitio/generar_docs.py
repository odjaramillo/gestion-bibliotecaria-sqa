"""Genera el sitio de documentos SQA (site/docs/) desde un manifiesto curado.

Capa de presentacion documental: NO produce contenido (eso vive en los .md de
sqa/). Renderiza a HTML self-contained (sin dependencias externas: sin CDN,
sin fuentes remotas, sin fetch; el unico script es el conmutador de tema
inline, listo para GitHub Pages) unicamente los documentos declarados en
MANIFIESTO,
y publica un indice navegable en site/docs/index.html.

La publicacion es una decision explicita: el manifiesto es una lista blanca, no
un glob. Un borrador nuevo en sqa/ NO se publica solo; hay que agregarlo aqui.

Convive con el dashboard de metricas: generar_dashboard.py escribe
site/index.html y este modulo escribe site/docs/**. Un unico artefacto de Pages,
un unico deploy (ver .github/workflows/pages-dashboard.yml).

Uso:
    python sqa/metricas/generar_dashboard.py   # genera site/index.html
    python sqa/sitio/generar_docs.py           # genera site/docs/**
"""

import html
import re
import shutil
import unicodedata
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit

import markdown

# Raiz del repo, derivada del propio archivo (sqa/sitio/generar_docs.py).
RAIZ_REPO = Path(__file__).resolve().parent.parent.parent

# Base de trazabilidad: todo documento publicado enlaza a su fuente en el repo.
BLOB_BASE = "https://github.com/odjaramillo/gestion-bibliotecaria-sqa/blob/main"

# Extensiones de Python-Markdown habilitadas (ver requirements.txt y la
# desviacion registrada en PACS §6.3): tablas, bloques de codigo cercados,
# tabla de contenidos con anclas y atributos inline.
EXTENSIONES_MD = ["tables", "fenced_code", "toc", "attr_list"]


def slug_github(valor: str, separador: str = "-") -> str:
    """Genera el ancla de un encabezado como lo hace GitHub.

    Los indices internos de los documentos (PACS, plan, estrategia, checklists)
    estan escritos contra el slugger de GitHub, y sus reglas difieren de las de
    Python-Markdown en dos puntos que rompen enlaces:

      1. GitHub conserva los acentos (``#1-propósito-y-alcance``); el slugify
         por defecto translitera a ASCII (``1-proposito-y-alcance``).
      2. GitHub borra la puntuacion y recien despues convierte cada espacio en
         un guion, sin colapsar los repetidos: ``WF4 — Inyeccion`` produce
         ``wf4--inyeccion`` (doble guion). Python-Markdown colapsa a uno solo.

    Replicar el slugger de GitHub mantiene los indices internos navegables.
    """
    valor = unicodedata.normalize("NFC", valor).strip().lower()
    valor = re.sub(r"[^\w\s-]", "", valor, flags=re.UNICODE)  # fuera la puntuacion
    return re.sub(r"\s", separador, valor.strip())            # espacios -> guiones


CONFIG_TOC = {"toc": {"slugify": lambda valor, separador: slug_github(valor, separador)}}


@dataclass(frozen=True)
class Documento:
    """Entrada del manifiesto: un markdown que SI se publica."""

    fuente: str        # ruta relativa a la raiz del repo
    slug: str          # nombre de archivo publicado (sin .html)
    titulo: str        # titulo visible en el indice y en la pagina
    codigo: str        # identificador del entregable ("" si no tiene)
    descripcion: str   # una linea, para el indice
    seccion: str       # "entregable" | "anexo"

    @property
    def destino(self) -> str:
        return f"{self.slug}.html"

    @property
    def url_fuente(self) -> str:
        return f"{BLOB_BASE}/{quote(self.fuente)}"


@dataclass(frozen=True)
class Activo:
    """Archivo binario que se copia tal cual al sitio (no se renderiza)."""

    fuente: str        # ruta relativa a la raiz del repo
    destino: str       # ruta relativa a site/docs/
    titulo: str
    codigo: str
    descripcion: str
    en_indice: bool    # si se lista como entregable en el indice


# ---------------------------------------------------------------------------
# MANIFIESTO — lista blanca de publicacion (issue #3)
# ---------------------------------------------------------------------------
# Orden significativo: es el orden en que aparecen en el indice.
MANIFIESTO: tuple[Documento, ...] = (
    Documento(
        fuente="sqa/PACS.md",
        slug="pacs",
        titulo="Plan de Aseguramiento de la Calidad del Software (PACS)",
        codigo="PACS",
        descripcion=(
            "Entregable central: plan SQA consolidado F1+F2 conforme a IEEE 730 — "
            "organización, riesgos, actividades, métricas y registros."
        ),
        seccion="entregable",
    ),
    Documento(
        fuente="sqa/fase1/informe-revision-requisitos-f1.md",
        slug="informe-revision-requisitos-f1",
        titulo="Informe de Revisión de Requisitos — Fase 1",
        codigo="INF-REV-001",
        descripcion=(
            "Resultado de la inspección estática de ERS y DAS: hallazgos, severidad "
            "y trazabilidad a los issues de corrección."
        ),
        seccion="entregable",
    ),
    Documento(
        fuente="sqa/fase1/Checklists-Inspeccion-Estatica-v1.md",
        slug="checklists-inspeccion-estatica",
        titulo="Sistema de Checklists de Inspección Estática v1",
        codigo="",
        descripcion=(
            "El instrumento con el que se ejecutó la revisión de Fase 1: checklists "
            "de brief, ERS, DAS, código y PACS."
        ),
        seccion="entregable",
    ),
    Documento(
        fuente="sqa/fase2/estaticas/2026-06-02_walkthrough-fiabilidad-sut-biblioteca.md",
        slug="walkthrough-fiabilidad",
        titulo="Walkthrough de Fiabilidad del SUT",
        codigo="",
        descripcion=(
            "Técnica estática de Fase 2: recorrido guiado del SUT centrado en madurez "
            "y tolerancia a fallos (ISO/IEC 25010)."
        ),
        seccion="entregable",
    ),
    Documento(
        fuente="sqa/fase2/planificacion/2026-06-09_estrategia-de-pruebas-fiabilidad.md",
        slug="estrategia-pruebas-fiabilidad",
        titulo="Estrategia de Pruebas de Fiabilidad",
        codigo="EST-FIAB-001",
        descripcion=(
            "Enfoque por sub-característica, niveles de prueba, política de suites y "
            "etiquetas, y métricas de calidad asociadas."
        ),
        seccion="entregable",
    ),
    Documento(
        fuente="sqa/fase2/planificacion/2026-06-09_plan-de-pruebas-fiabilidad.md",
        slug="plan-pruebas-fiabilidad",
        titulo="Plan de Pruebas de Fiabilidad",
        codigo="PP-FIAB-001",
        descripcion=(
            "Plan conforme a ISO/IEC/IEEE 29119-3: contexto, riesgos, estrategia, "
            "cronograma, trazabilidad y gestión de incidencias."
        ),
        seccion="entregable",
    ),
    Documento(
        fuente="sqa/fase2/planificacion/2026-06-24_especificacion-casos-prueba-fiabilidad.md",
        slug="especificacion-casos-prueba-fiabilidad",
        titulo="Especificación de Casos de Prueba de Fiabilidad",
        codigo="TCS-FIAB-001",
        descripcion=(
            "Casos de prueba diseñados para las sub-características de fiabilidad, "
            "con precondiciones, pasos y resultados esperados."
        ),
        seccion="entregable",
    ),
    Documento(
        fuente="sqa/fase2/dinamicas/2026-07-19_informe-resultados-pruebas-fiabilidad.md",
        slug="informe-resultados-pruebas-fiabilidad",
        titulo="Informe de Resultados de Pruebas de Fiabilidad",
        codigo="INF-RES-001",
        descripcion=(
            "Resultado de la ejecución dinámica de Fase 2: los cuatro niveles de "
            "prueba, las incidencias trazadas y las seis métricas de fiabilidad "
            "ratificadas — cierre de la fase."
        ),
        seccion="entregable",
    ),
    Documento(
        fuente="sqa/anexos/infograma-ecosistema.md",
        slug="infograma-ecosistema",
        titulo="Anexo — Infograma del Ecosistema Tecnológico",
        codigo="ANX-ECO-001",
        descripcion=(
            "Vista de una página del ecosistema SQA: cómo encajan repositorio, CI, "
            "métricas y documentos."
        ),
        seccion="anexo",
    ),
    Documento(
        fuente="sqa/anexos/reflexion-critica-ecosistema.md",
        slug="reflexion-critica-ecosistema",
        titulo="Anexo — Reflexión Crítica sobre el Ecosistema Tecnológico",
        codigo="ANX-REF-001",
        descripcion=(
            "Qué funcionó, qué no y qué se aprendió del ecosistema tecnológico "
            "montado para el proceso SQA."
        ),
        seccion="anexo",
    ),
    Documento(
        fuente="sqa/fase2/dinamicas/2026-07-19_reflexion-desempeno-equipo.md",
        slug="reflexion-desempeno-equipo",
        titulo="Anexo — Reflexión de Desempeño del Equipo",
        codigo="",
        descripcion=(
            "Criterio f) de la rúbrica: roles aplicados con liderazgo y sinergia — "
            "evidencia por rol, handoffs trazables y reflexión sobre el desempeño."
        ),
        seccion="anexo",
    ),
    Documento(
        fuente="sqa/anexos/herramientas-fase2.md",
        slug="herramientas-fase2",
        titulo="Anexo — Matriz de Herramientas Tecnológicas (Fase 2)",
        codigo="",
        descripcion=(
            "Herramienta por herramienta: propósito, justificación y dónde se usa "
            "dentro del proceso de Fase 2."
        ),
        seccion="anexo",
    ),
    Documento(
        fuente="sqa/fase2/planificacion/2026-06-24_casos-diferidos-fiabilidad.md",
        slug="casos-diferidos-fiabilidad",
        titulo="Anexo A — Casos de Prueba Diferidos (Fiabilidad)",
        codigo="ANX-FIAB-001",
        descripcion=(
            "Casos diseñados pero diferidos, con el motivo del diferimiento: la "
            "deuda de prueba declarada, no escondida."
        ),
        seccion="anexo",
    ),
    Documento(
        fuente="sqa/fase2/dinamicas/tc-fiab-017-evidencia.md",
        slug="tc-fiab-017-evidencia",
        titulo="Anexo — Evidencia de ejecución manual TC-FIAB-017",
        codigo="",
        descripcion=(
            "Evidencia del único caso ejecutado manualmente: entorno, pasos reales y "
            "resultado observado."
        ),
        seccion="anexo",
    ),
    Documento(
        fuente="sqa/anexos/simulacion-ic-sprints.md",
        slug="simulacion-ic-sprints",
        titulo="Anexo — Simulación de Integración Continua por Sprints del SUT",
        codigo="ANX-SIM-IC-001",
        descripcion=(
            "Anexo reconciliador de la rama simulacion-desarrollo: tabla Sprint → commit / tag / "
            "ci-fiabilidad run real, PRs y workflow runs del proyecto, declaración de los siete "
            "desvíos (TC-FIAB-002/003 nunca implementados, Controller monolítico, M-02 60.7% vs "
            "70% planificado, ejecución tardía del plan) y refinamiento explícito de INF-RES-001 §2.4."
        ),
        seccion="anexo",
    ),
    Documento(
        fuente="sqa/anexos/demo-ic-sprints.md",
        slug="demo-ic-sprints",
        titulo="Anexo — Guía de Demo de la Simulación de IC por Sprints",
        codigo="ANX-SIM-DEMO-001",
        descripcion=(
            "Guía corta para mostrar al docente la simulación: re-corrido de workflows en vivo "
            "(ci-fiabilidad, ci-e2e), inspección local de la traza por sprint en "
            "simulacion-desarrollo, y levantada local del SUT (backend H2 con JDK 21, frontend "
            "Vue 3 en puerto 5173)."
        ),
        seccion="anexo",
    ),
)

# Activos binarios copiados al sitio. El PDF de la auditoria estatica ES un
# entregable de Fase 2 (tecnica estatica), pero no se renderiza: se enlaza.
# El SVG es el activo que embebe el infograma.
ACTIVOS: tuple[Activo, ...] = (
    Activo(
        fuente="sqa/fase2/estaticas/2026-06-02_auditoria-estatica-fiabilidad-iso25010.pdf",
        destino="assets/2026-06-02_auditoria-estatica-fiabilidad-iso25010.pdf",
        titulo="Auditoría Estática de Fiabilidad (ISO/IEC 25010)",
        codigo="PDF",
        descripcion=(
            "Técnica estática de Fase 2 en formato PDF: auditoría del SUT contra las "
            "sub-características de fiabilidad."
        ),
        en_indice=True,
    ),
    Activo(
        fuente="sqa/anexos/infograma-ecosistema.svg",
        destino="assets/infograma-ecosistema.svg",
        titulo="Infograma del ecosistema (SVG)",
        codigo="",
        descripcion="Imagen embebida por el anexo ANX-ECO-001.",
        en_indice=False,
    ),
)


# ---------------------------------------------------------------------------
# Estilos — misma paleta y tipografia que el dashboard (generar_dashboard.py).
# Los documentos deben leerse como el mismo producto que el dashboard.
# Tema dual: paleta oscura por defecto (:root); la clara entra por
# prefers-color-scheme o forzada via data-theme (conmutador inline).
# ---------------------------------------------------------------------------

# Paleta clara (GitHub-light-like). Se inyecta dos veces: bajo la media query
# (tema del sistema) y bajo [data-theme="light"] (tema forzado), para que el
# override explicito gane en ambos sentidos.
_PALETA_CLARA = """\
  color-scheme: light;
  --bg: #f6f8fa;
  --surface: #ffffff;
  --surface-2: #eff2f5;
  --border: #d0d7de;
  --border-soft: #d8dee4;
  --ink: #1f2328;
  --ink-muted: #59636e;
  --ink-faint: #6e7781;
  --accent: #0969da;
  --accent-2: #218bff;
  --accent-tint: rgba(9,105,218,.06);
  --accent-line: rgba(9,105,218,.35);
  --accent-hover: rgba(9,105,218,.5);
  --halo: rgba(9,105,218,.07);
  --halo-2: rgba(26,127,55,.04);
  --sombra: rgba(31,35,40,.12);
"""

_CSS_BASE = """
:root {
  color-scheme: light dark;
  --bg: #0d1117;
  --surface: #161b22;
  --surface-2: #1c2230;
  --border: #30363d;
  --border-soft: #21262d;
  --ink: #e6edf3;
  --ink-muted: #9aa4b2;
  --ink-faint: #6e7681;
  --accent: #4493f8;
  --accent-2: #7cc3ff;
  --accent-tint: rgba(68,147,248,.08);
  --accent-line: rgba(68,147,248,.35);
  --accent-hover: rgba(68,147,248,.5);
  --halo: rgba(68,147,248,.10);
  --halo-2: rgba(63,185,80,.05);
  --sombra: rgba(1,4,9,.55);
}
/* Tema del sistema; un data-theme explicito (conmutador) lo pisa. */
@media (prefers-color-scheme: light) {
  :root:not([data-theme="dark"]) {
__PALETA_CLARA__
  }
}
:root[data-theme="light"] {
__PALETA_CLARA__
}
:root[data-theme="dark"] { color-scheme: dark; }

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  margin: 0; padding: 2.5rem 1.25rem; line-height: 1.6;
  background:
    radial-gradient(1100px 540px at 18% -12%, var(--halo), transparent 70%),
    radial-gradient(900px 480px at 85% -14%, var(--halo-2), transparent 72%),
    var(--bg);
  color: var(--ink);
  -webkit-font-smoothing: antialiased;
  overflow-x: hidden;
}
.wrap { max-width: 1080px; margin: 0 auto; }

a:focus-visible, button:focus-visible, summary:focus-visible {
  outline: 2px solid var(--accent); outline-offset: 2px; border-radius: 6px;
}

/* Header */
.masthead { margin-bottom: 2.5rem; padding-top: .5rem; }
.eyebrow {
  display: inline-block; font-size: .72rem; font-weight: 700; letter-spacing: .14em;
  text-transform: uppercase; color: var(--accent);
  border: 1px solid var(--accent-line); background: var(--accent-tint);
  border-radius: 999px; padding: .22rem .75rem; margin-bottom: 1rem;
}
h1 { font-size: 2.1rem; margin: 0 0 .45rem; letter-spacing: -.02em; line-height: 1.2; }
@supports (-webkit-background-clip: text) or (background-clip: text) {
  .masthead h1 {
    background: linear-gradient(105deg, var(--ink) 55%, var(--accent));
    -webkit-background-clip: text; background-clip: text;
    -webkit-text-fill-color: transparent; color: transparent;
  }
}
.sub { color: var(--ink-muted); margin: 0; font-size: .9rem; }

/* Navegacion (misma en indice y en cada documento) */
.nav { display: flex; flex-wrap: wrap; align-items: center; gap: .5rem; margin: 1.1rem 0 0; }
.nav a {
  font-size: .78rem; font-weight: 600; text-decoration: none; color: var(--ink-muted);
  border: 1px solid var(--border); background: var(--surface);
  border-radius: 999px; padding: .3rem .8rem;
  transition: color .15s ease, border-color .15s ease;
}
.nav a:hover { color: var(--accent); border-color: var(--accent-hover); }
.theme-toggle {
  font: inherit; font-size: .78rem; font-weight: 600; color: var(--ink-muted);
  border: 1px solid var(--border); background: var(--surface);
  border-radius: 999px; padding: .3rem .8rem; cursor: pointer;
  transition: color .15s ease, border-color .15s ease;
}
.theme-toggle:hover { color: var(--accent); border-color: var(--accent-hover); }

/* Indice de documentos */
section { margin-bottom: 2.75rem; }
.sec-head { display: flex; align-items: baseline; gap: .6rem; margin-bottom: .35rem; }
h2 { font-size: 1.15rem; margin: 0; letter-spacing: -.01em; }
.sec-count {
  font-size: .72rem; font-weight: 700; color: var(--ink-muted);
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 999px; padding: .1rem .6rem;
}
.sec-desc { color: var(--ink-muted); font-size: .85rem; margin: .1rem 0 1.1rem; max-width: 62ch; }
.rule { height: 1px; background: var(--border-soft); margin-bottom: 1.25rem; }
.doc-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; }
.doc-card {
  background: var(--surface); border: 1px solid var(--border); border-radius: 14px;
  padding: 1.2rem 1.35rem; display: flex; flex-direction: column; gap: .55rem;
  transition: transform .15s ease, box-shadow .15s ease, border-color .15s ease;
}
.doc-card:hover { transform: translateY(-2px); box-shadow: 0 8px 24px var(--sombra); border-color: var(--accent-hover); }
.doc-head { display: flex; justify-content: space-between; align-items: baseline; gap: .5rem; }
.doc-titulo { font-size: .98rem; font-weight: 600; line-height: 1.3; }
.doc-titulo a { color: var(--ink); text-decoration: none; }
.doc-titulo a:hover { color: var(--accent); }
.doc-id {
  font-size: .68rem; color: var(--ink-muted); font-weight: 700; letter-spacing: .06em;
  border: 1px solid var(--border); border-radius: 6px; padding: .12rem .4rem; flex: 0 0 auto;
}
.doc-desc { color: var(--ink-muted); font-size: .85rem; margin: 0; }
.doc-foot { margin-top: auto; display: flex; flex-wrap: wrap; gap: .8rem; padding-top: .35rem; }
.doc-foot a { font-size: .76rem; color: var(--ink-faint); text-decoration: none; }
.doc-foot a:hover { color: var(--accent); }

/* Tabla de contenidos del documento (plegada por defecto) */
.toc { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; margin: 0 0 1.5rem; }
.toc summary {
  cursor: pointer; padding: .85rem 1.25rem; font-size: .88rem; font-weight: 600;
  color: var(--ink-muted); transition: color .15s ease;
}
.toc summary:hover { color: var(--accent); }
.toc[open] summary { border-bottom: 1px solid var(--border-soft); }
.toc nav { padding: .7rem 1.25rem 1rem; }
.toc ul { margin: 0; padding-left: 1.2rem; }
.toc li { font-size: .85rem; margin: .3rem 0; }
.toc a { color: var(--ink-muted); text-decoration: none; }
.toc a:hover { color: var(--accent); }

/* Cuerpo del documento renderizado */
.md { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; padding: 1.85rem 2.1rem; }
.md > :first-child { margin-top: 0; }
.md h1 { font-size: 1.5rem; margin: 2rem 0 .75rem; letter-spacing: -.01em; }
.md h2 {
  font-size: 1.2rem; margin: 1.9rem 0 .7rem; padding: 0 0 .35rem .75rem;
  border-bottom: 1px solid var(--border-soft); border-left: 3px solid var(--accent);
}
.md h3 { font-size: 1.02rem; margin: 1.6rem 0 .6rem; }
.md h4, .md h5, .md h6 { font-size: .92rem; margin: 1.3rem 0 .5rem; color: var(--ink-muted); }
/* Medida de lectura acotada; las tablas conservan el ancho completo. */
.md p, .md li { font-size: .92rem; max-width: 74ch; }
.md a { color: var(--accent); text-decoration: none; }
.md a:hover { text-decoration: underline; }
.md hr { border: 0; height: 1px; background: var(--border-soft); margin: 2rem 0; }
.md blockquote {
  margin: 1.1rem 0; padding: .35rem 1.1rem; color: var(--ink-muted);
  border-left: 3px solid var(--accent-line); background: var(--surface-2);
  border-radius: 0 8px 8px 0; max-width: 74ch;
}
.md code {
  background: var(--surface-2); border: 1px solid var(--border-soft);
  padding: .08rem .35rem; border-radius: 5px; font-size: .85em;
}
.md pre {
  background: var(--surface-2); border: 1px solid var(--border-soft); border-radius: 8px;
  padding: .9rem 1rem; overflow-x: auto;
}
.md pre code { background: none; border: 0; padding: 0; font-size: .82rem; }
.md img { max-width: 100%; height: auto; display: block; }
/* Las tablas largas hacen scroll dentro de su contenedor: el body nunca lo hace. */
.tabla-scroll { overflow-x: auto; margin: 1.2rem 0; border: 1px solid var(--border); border-radius: 8px; }
.md table { border-collapse: collapse; width: 100%; font-size: .84rem; }
.md th, .md td { text-align: left; padding: .55rem .75rem; border-bottom: 1px solid var(--border-soft); vertical-align: top; }
.md th { background: var(--surface-2); color: var(--ink-muted); text-transform: uppercase; font-size: .7rem; letter-spacing: .06em; white-space: nowrap; }
.md tr:last-child td { border-bottom: 0; }

/* Pager anterior / siguiente (orden del manifiesto) */
.pager { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1.5rem; }
.pager a {
  display: flex; flex-direction: column; gap: .3rem;
  background: var(--surface); border: 1px solid var(--border); border-radius: 14px;
  padding: .95rem 1.2rem; text-decoration: none;
  transition: transform .15s ease, box-shadow .15s ease, border-color .15s ease;
}
.pager a:hover { transform: translateY(-2px); box-shadow: 0 8px 24px var(--sombra); border-color: var(--accent-hover); }
.pager-prev { grid-column: 1; }
.pager-next { grid-column: 2; text-align: right; }
.pager-dir { font-size: .7rem; font-weight: 700; text-transform: uppercase; letter-spacing: .07em; color: var(--ink-faint); }
.pager-titulo { font-size: .88rem; font-weight: 600; color: var(--ink); line-height: 1.35; }
.pager a:hover .pager-titulo { color: var(--accent); }
@media (max-width: 640px) {
  .pager { grid-template-columns: 1fr; }
  .pager-prev, .pager-next { grid-column: auto; text-align: left; }
}

footer { margin-top: 3.5rem; color: var(--ink-faint); font-size: .8rem; border-top: 1px solid var(--border-soft); padding-top: 1.25rem; }
footer a { color: var(--ink-muted); text-decoration: none; }
footer a:hover { color: var(--accent); }

@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  *, *::before, *::after {
    animation-duration: .01ms !important; animation-iteration-count: 1 !important;
    transition-duration: .01ms !important;
  }
}
"""

CSS = _CSS_BASE.replace("__PALETA_CLARA__", _PALETA_CLARA)

# Conmutador de tema: script inline minimo (sin recursos externos). Corre en
# <head> antes del primer paint para evitar el destello de tema incorrecto.
# Duplicado deliberado de generar_dashboard.py (misma convencion que la paleta):
# la clave "tema" de localStorage y los valores de data-theme son un contrato
# compartido; ambos bloques deben cambiar juntos.
SCRIPT_TEMA = """\
<script>
(function () {
  var guardado = null;
  try { guardado = localStorage.getItem("tema"); } catch (e) { /* sin storage */ }
  if (guardado === "light" || guardado === "dark") {
    document.documentElement.setAttribute("data-theme", guardado);
  }
  window.alternarTema = function () {
    var raiz = document.documentElement;
    var actual = raiz.getAttribute("data-theme") ||
      (window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark");
    var nuevo = actual === "dark" ? "light" : "dark";
    raiz.setAttribute("data-theme", nuevo);
    try { localStorage.setItem("tema", nuevo); } catch (e) { /* sin storage */ }
  };
})();
</script>"""

BOTON_TEMA = (
    '<button class="theme-toggle" type="button" onclick="alternarTema()" '
    'aria-label="Cambiar entre tema claro y oscuro">◐ Tema</button>'
)

# Umbral del TOC por documento: con menos de 4 secciones h2 no amerita indice.
TOC_MIN_H2 = 4


# ---------------------------------------------------------------------------
# Reescritura de enlaces
# ---------------------------------------------------------------------------
# Mapas de resolucion: ruta-en-el-repo -> ruta-en-el-sitio (relativa a site/docs/).
PUBLICADOS: dict[str, str] = {doc.fuente: doc.destino for doc in MANIFIESTO}
PUBLICADOS.update({activo.fuente: activo.destino for activo in ACTIVOS})

_ATRIBUTO_RE = re.compile(r'(?P<attr>\b(?:href|src)=")(?P<url>[^"]*)"')


def _resolver_ruta(destino: str, fuente_doc: str) -> str:
    """Resuelve un enlace relativo a ruta del repo (normalizada, sin ``..``).

    ``fuente_doc`` es la ruta del markdown que contiene el enlace; los enlaces
    se resuelven contra su directorio, igual que hace GitHub al renderizarlo.
    """
    base = Path(fuente_doc).parent
    partes: list[str] = []
    for parte in (base / unquote(destino)).parts:
        if parte == "..":
            if not partes:
                raise ValueError(
                    f"El enlace '{destino}' en {fuente_doc} escapa de la raiz del repositorio."
                )
            partes.pop()
        elif parte not in (".", ""):
            partes.append(parte)
    return "/".join(partes)


def _reescribir_destino(destino: str, fuente_doc: str) -> str:
    """Reescribe un destino de enlace del markdown a su equivalente publicable.

    Reglas (en orden):
      1. Anclas (``#seccion``) y URLs absolutas (``http(s)://``, ``mailto:``)
         pasan sin tocar.
      2. Enlace a un documento/activo PUBLICADO -> slug local (``pacs.html``).
      3. Cualquier otra ruta del repo (codigo, workflows, docs no publicados,
         ``documentacion/*.pdf``) -> URL absoluta al blob de GitHub en ``main``,
         para que ningun enlace quede en 404.
    """
    if not destino or destino.startswith("#"):
        return destino
    partes = urlsplit(destino)
    if partes.scheme or partes.netloc:
        return destino

    ruta_relativa, _, fragmento = destino.partition("#")
    sufijo = f"#{fragmento}" if fragmento else ""
    if not ruta_relativa:
        return destino

    ruta_repo = _resolver_ruta(ruta_relativa, fuente_doc)
    if ruta_repo in PUBLICADOS:
        return f"{PUBLICADOS[ruta_repo]}{sufijo}"
    return f"{BLOB_BASE}/{quote(ruta_repo)}{sufijo}"


def reescribir_enlaces(html_doc: str, fuente_doc: str) -> str:
    """Aplica la reescritura a cada ``href``/``src`` del HTML renderizado.

    Se opera sobre el HTML (no sobre el markdown) para cubrir de una sola vez
    enlaces inline, de referencia e imagenes.
    """

    def _sub(match: re.Match) -> str:
        destino = html.unescape(match.group("url"))
        nuevo = _reescribir_destino(destino, fuente_doc)
        return f'{match.group("attr")}{html.escape(nuevo, quote=True)}"'

    return _ATRIBUTO_RE.sub(_sub, html_doc)


def envolver_tablas(html_doc: str) -> str:
    """Envuelve cada ``<table>`` en un contenedor con scroll horizontal propio."""
    html_doc = html_doc.replace("<table>", '<div class="tabla-scroll"><table>')
    return html_doc.replace("</table>", "</table></div>")


# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------
def _tokens_h2(toc_tokens: list) -> list:
    """Aplana los toc_tokens de Python-Markdown a la lista de entradas h2.

    Los documentos suelen abrir con un h1 (titulo), asi que los h2 pueden venir
    anidados como hijos; se recorre cualquier nivel superior hasta encontrarlos.
    """
    encontrados = []
    for token in toc_tokens:
        if token["level"] == 2:
            encontrados.append(token)
        elif token["level"] < 2:
            encontrados.extend(_tokens_h2(token.get("children", [])))
    return encontrados


def _toc_html(toc_tokens: list) -> str:
    """TOC plegado del documento (h2 con sus h3), o cadena vacia si es corto.

    Las anclas reutilizan los ids que ya genero el slugger de GitHub
    (CONFIG_TOC): NO se re-sluggea, o los enlaces divergirian del cuerpo.
    """
    h2s = _tokens_h2(toc_tokens)
    if len(h2s) < TOC_MIN_H2:
        return ""
    items = []
    for token in h2s:
        hijos = [t for t in token.get("children", []) if t["level"] == 3]
        sub = ""
        if hijos:
            sub = "<ul>" + "".join(
                f'<li><a href="#{html.escape(t["id"], quote=True)}">'
                f'{html.escape(t["name"])}</a></li>'
                for t in hijos
            ) + "</ul>"
        items.append(
            f'<li><a href="#{html.escape(token["id"], quote=True)}">'
            f'{html.escape(token["name"])}</a>{sub}</li>'
        )
    return (
        '<details class="toc"><summary>Contenido del documento</summary>'
        f'<nav><ul>{"".join(items)}</ul></nav></details>'
    )


def _render_con_toc(texto: str, fuente_doc: str) -> tuple[str, str]:
    """Markdown -> (cuerpo HTML con enlaces reescritos, TOC plegado o '')."""
    md = markdown.Markdown(extensions=EXTENSIONES_MD, extension_configs=CONFIG_TOC)
    cuerpo = md.convert(texto)
    cuerpo = envolver_tablas(reescribir_enlaces(cuerpo, fuente_doc))
    return cuerpo, _toc_html(md.toc_tokens)


def renderizar_markdown(texto: str, fuente_doc: str) -> str:
    """Markdown -> HTML self-contained, con enlaces ya reescritos."""
    cuerpo, _ = _render_con_toc(texto, fuente_doc)
    return cuerpo


def _pager_html(doc: Documento) -> str:
    """Pager anterior/siguiente segun el orden del MANIFIESTO.

    El primero no tiene anterior y el ultimo no tiene siguiente: se omite el
    slot, no se rellena con un placeholder.
    """
    idx = MANIFIESTO.index(doc)
    piezas = []
    if idx > 0:
        previo = MANIFIESTO[idx - 1]
        piezas.append(
            f'<a class="pager-prev" href="{html.escape(previo.destino, quote=True)}">'
            '<span class="pager-dir">&larr; Anterior</span>'
            f'<span class="pager-titulo">{html.escape(previo.titulo)}</span></a>'
        )
    if idx < len(MANIFIESTO) - 1:
        siguiente = MANIFIESTO[idx + 1]
        piezas.append(
            f'<a class="pager-next" href="{html.escape(siguiente.destino, quote=True)}">'
            '<span class="pager-dir">Siguiente &rarr;</span>'
            f'<span class="pager-titulo">{html.escape(siguiente.titulo)}</span></a>'
        )
    return f'<nav class="pager">{"".join(piezas)}</nav>'


def _cabecera(titulo: str, subtitulo: str, nav: str) -> str:
    return (
        '<header class="masthead">'
        '<span class="eyebrow">Documentos SQA</span>'
        f"<h1>{html.escape(titulo)}</h1>"
        f'<p class="sub">{subtitulo}</p>'
        f'<nav class="nav">{nav}{BOTON_TEMA}</nav>'
        "</header>"
    )


def _pagina(titulo_head: str, cuerpo: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(titulo_head)}</title>
{SCRIPT_TEMA}
<style>{CSS}</style>
</head>
<body>
<div class="wrap" id="top">
{cuerpo}
</div>
</body>
</html>
"""


def _pagina_documento(doc: Documento, generado: str) -> str:
    """Pagina de un documento: nav + TOC + cuerpo + pager + trazabilidad (DoD #3)."""
    fuente = RAIZ_REPO / doc.fuente
    cuerpo_md, toc = _render_con_toc(fuente.read_text(encoding="utf-8"), doc.fuente)
    url_fuente = doc.url_fuente
    nav = (
        '<a href="index.html">&larr; Índice de documentos</a>'
        '<a href="../index.html">Dashboard de métricas</a>'
        f'<a href="{html.escape(url_fuente, quote=True)}">Ver fuente en el repositorio</a>'
    )
    codigo = f"{html.escape(doc.codigo)} &middot; " if doc.codigo else ""
    subtitulo = f"{codigo}Sistema de Gestión Bibliotecaria &middot; Equipo 58-1"
    cuerpo = (
        f"{_cabecera(doc.titulo, subtitulo, nav)}"
        f"{toc}"
        f'<article class="md">{cuerpo_md}</article>'
        f"{_pager_html(doc)}"
        "<footer>"
        f'Fuente: <a href="{html.escape(url_fuente, quote=True)}">'
        f"Ver fuente en el repositorio</a> (<code>{html.escape(doc.fuente)}</code>). "
        f"Renderizado automáticamente el {generado} por <code>sqa/sitio/generar_docs.py</code>. "
        '<a href="#top">Volver arriba &uarr;</a>'
        "</footer>"
    )
    return _pagina(f"{doc.titulo} - Documentos SQA", cuerpo)


def _tarjeta(destino: str, titulo: str, codigo: str, descripcion: str, url_fuente: str) -> str:
    id_html = f'<span class="doc-id">{html.escape(codigo)}</span>' if codigo else ""
    return (
        '<div class="doc-card">'
        '<div class="doc-head">'
        f'<span class="doc-titulo"><a href="{html.escape(destino, quote=True)}">'
        f"{html.escape(titulo)}</a></span>{id_html}"
        "</div>"
        f'<p class="doc-desc">{html.escape(descripcion)}</p>'
        '<div class="doc-foot">'
        f'<a href="{html.escape(destino, quote=True)}">Abrir &rarr;</a>'
        f'<a href="{html.escape(url_fuente, quote=True)}">Ver fuente en el repositorio</a>'
        "</div></div>"
    )


def _pagina_indice(generado: str) -> str:
    """Indice del sitio de documentos: entregables + anexos + activos."""
    entregables = [
        _tarjeta(d.destino, d.titulo, d.codigo, d.descripcion, d.url_fuente)
        for d in MANIFIESTO
        if d.seccion == "entregable"
    ]
    entregables += [
        _tarjeta(
            a.destino,
            a.titulo,
            a.codigo,
            a.descripcion,
            f"{BLOB_BASE}/{quote(a.fuente)}",
        )
        for a in ACTIVOS
        if a.en_indice
    ]
    anexos = [
        _tarjeta(d.destino, d.titulo, d.codigo, d.descripcion, d.url_fuente)
        for d in MANIFIESTO
        if d.seccion == "anexo"
    ]
    nav = (
        '<a href="../index.html">Dashboard de métricas</a>'
        f'<a href="{BLOB_BASE}/sqa">Ver el directorio sqa/ en el repositorio</a>'
    )
    cuerpo = (
        f"{_cabecera('Documentos del proceso SQA', 'Equipo 58-1 &middot; Sistema de Gestión Bibliotecaria &middot; Generado ' + generado, nav)}"
        "<section>"
        '<div class="sec-head"><h2>Entregables</h2>'
        f'<span class="sec-count">{len(entregables)}</span></div>'
        '<p class="sec-desc">Documentos formales del proceso de aseguramiento de la '
        "calidad. Cada uno enlaza a su fuente en el repositorio.</p>"
        '<div class="rule"></div>'
        f'<div class="doc-grid">{"".join(entregables)}</div>'
        "</section>"
        "<section>"
        '<div class="sec-head"><h2>Anexos</h2>'
        f'<span class="sec-count">{len(anexos)}</span></div>'
        '<p class="sec-desc">Material de soporte: evidencia, matrices, reflexión y '
        "casos diferidos referenciados por los entregables.</p>"
        '<div class="rule"></div>'
        f'<div class="doc-grid">{"".join(anexos)}</div>'
        "</section>"
        "<footer>"
        "Publicación curada: solo se publican los documentos declarados en el "
        "manifiesto de <code>sqa/sitio/generar_docs.py</code>. Sitio self-contained "
        "(sin dependencias externas: sin CDN ni recursos remotos), desplegado junto "
        "al dashboard por <code>pages-dashboard.yml</code>."
        "</footer>"
    )
    return _pagina("Documentos SQA - Equipo 58-1", cuerpo)


# ---------------------------------------------------------------------------
# Orquestacion
# ---------------------------------------------------------------------------
def validar_manifiesto(raiz: Path = RAIZ_REPO) -> None:
    """Falla fuerte si falta una fuente declarada.

    Un entregable ausente en silencio es peor que un build roto: el sitio se
    publicaria incompleto sin que nadie lo note.
    """
    faltantes = [
        entrada.fuente
        for entrada in (*MANIFIESTO, *ACTIVOS)
        if not (raiz / entrada.fuente).is_file()
    ]
    if faltantes:
        raise FileNotFoundError(
            "Fuentes del manifiesto ausentes (no se publica un sitio incompleto): "
            + ", ".join(faltantes)
        )


def generar_docs(output_dir: str = "site/docs", raiz: Path = RAIZ_REPO) -> Path:
    """Genera site/docs/**: una pagina por documento del manifiesto + indice.

    No toca site/index.html (el dashboard): escribe unicamente bajo output_dir.
    """
    validar_manifiesto(raiz)
    generado = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    salida = Path(output_dir)
    salida.mkdir(parents=True, exist_ok=True)

    for activo in ACTIVOS:
        destino = salida / activo.destino
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(raiz / activo.fuente, destino)

    for doc in MANIFIESTO:
        (salida / doc.destino).write_text(_pagina_documento(doc, generado), encoding="utf-8")

    indice = salida / "index.html"
    indice.write_text(_pagina_indice(generado), encoding="utf-8")

    print(
        f"Documentos generados: {len(MANIFIESTO)} paginas + {len(ACTIVOS)} activos "
        f"en {salida} (indice: {indice})"
    )
    return indice


if __name__ == "__main__":
    generar_docs()
