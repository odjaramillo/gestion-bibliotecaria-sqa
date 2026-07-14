"""Genera el dashboard HTML del proceso SQA a partir del reporte de KPIs.

Capa de presentacion: NO calcula metricas (eso lo hace calcular_kpi.py).
Lee sqa/metricas/reporte_kpi.json y produce un index.html self-contained
(sin dependencias externas: sin CDN, sin fuentes remotas, sin fetch; el unico
script es el conmutador de tema inline) listo para GitHub Pages.

Tema dual: la paleta oscura es la de base (:root); la clara se activa por
prefers-color-scheme o forzada con el conmutador (data-theme en <html>).
Por eso ningun SVG ni estilo inline lleva colores hardcodeados: todo resuelve
via custom properties, que el SVG inline hereda de la pagina.

Uso:
    python sqa/metricas/calcular_kpi.py            # genera reporte_kpi.json
    python sqa/metricas/generar_dashboard.py       # genera site/index.html
"""

import html
import json
import math
from datetime import datetime, timezone
from pathlib import Path

# Etiquetas legibles para cada agrupacion de la taxonomia de labels.
GRUPOS = {
    "por_tipo": "Tipo",
    "por_area": "Área",
    "por_severidad": "Severidad",
    "por_fase": "Fase",
    "por_iso": "Característica ISO 25010",
    "por_rol": "Rol",
}

# Paleta clara (GitHub-light-like). Se inyecta dos veces en el CSS: bajo la
# media query (tema del sistema) y bajo [data-theme="light"] (tema forzado por
# el conmutador), para que el override explicito gane en ambos sentidos.
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
  --good: #1a7f37;
  --bad: #d1242f;
  --nd: #59636e;
  --amber: #9a6700;
  --serie-abiertos: #0969da;
  --serie-cerrados: #1a7f37;
  --badge-auto-bg: rgba(9,105,218,.08);
  --badge-auto-ink: #0969da;
  --badge-auto-line: rgba(9,105,218,.4);
  --badge-decl-bg: rgba(154,103,0,.10);
  --badge-decl-ink: #9a6700;
  --badge-decl-line: rgba(154,103,0,.5);
  --bar-fill-2: #218bff;
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
  --good: #3fb950;
  --bad: #f85149;
  --nd: #8b949e;
  --amber: #e3b341;
  --serie-abiertos: #4493f8;
  --serie-cerrados: #3fb950;
  --badge-auto-bg: rgba(68,147,248,.14);
  --badge-auto-ink: #79b8ff;
  --badge-auto-line: rgba(68,147,248,.4);
  --badge-decl-bg: rgba(210,153,34,.14);
  --badge-decl-ink: #e3b341;
  --badge-decl-line: rgba(158,106,3,.6);
  --bar-fill-2: #6db3ff;
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
  margin: 0; padding: 2.5rem 1.25rem; line-height: 1.5;
  background:
    radial-gradient(1100px 540px at 18% -12%, var(--halo), transparent 70%),
    radial-gradient(900px 480px at 85% -14%, var(--halo-2), transparent 72%),
    var(--bg);
  color: var(--ink);
  -webkit-font-smoothing: antialiased;
}
.wrap { max-width: 1080px; margin: 0 auto; }

a:focus-visible, button:focus-visible, summary:focus-visible {
  outline: 2px solid var(--accent); outline-offset: 2px; border-radius: 6px;
}

/* Header */
.masthead { margin-bottom: 2.75rem; padding-top: .5rem; }
.eyebrow {
  display: inline-block; font-size: .72rem; font-weight: 700; letter-spacing: .14em;
  text-transform: uppercase; color: var(--accent);
  border: 1px solid var(--accent-line); background: var(--accent-tint);
  border-radius: 999px; padding: .22rem .75rem; margin-bottom: 1rem;
}
h1 { font-size: 2.3rem; margin: 0 0 .45rem; letter-spacing: -.02em; line-height: 1.15; }
@supports (-webkit-background-clip: text) or (background-clip: text) {
  .masthead h1 {
    background: linear-gradient(105deg, var(--ink) 55%, var(--accent));
    -webkit-background-clip: text; background-clip: text;
    -webkit-text-fill-color: transparent; color: transparent;
  }
}
.sub { color: var(--ink-muted); margin: 0; font-size: .9rem; }

/* Navegacion (pills; misma identidad que las paginas de documentos) */
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

/* KPI hero tiles */
.kpis { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin: 1.75rem 0 2.75rem; }
.kpi {
  position: relative; background: var(--surface); border: 1px solid var(--border);
  border-radius: 14px; padding: 1.3rem 1.4rem; overflow: hidden;
  transition: transform .15s ease, box-shadow .15s ease, border-color .15s ease;
}
.kpi:hover { transform: translateY(-2px); box-shadow: 0 8px 24px var(--sombra); border-color: var(--accent-line); }
.kpi::before {
  content: ""; position: absolute; inset: 0 0 auto 0; height: 3px;
  background: linear-gradient(90deg, var(--border), var(--border));
}
.kpi.accent::before { background: linear-gradient(90deg, var(--accent), var(--accent-2)); }
.kpi .n { font-size: 2.4rem; font-weight: 800; line-height: 1; font-variant-numeric: tabular-nums; }
.kpi.accent .n { color: var(--accent); }
@supports (-webkit-background-clip: text) or (background-clip: text) {
  .kpi.accent .n {
    background: linear-gradient(120deg, var(--accent), var(--accent-2));
    -webkit-background-clip: text; background-clip: text;
    -webkit-text-fill-color: transparent; color: transparent;
  }
}
.kpi .l { color: var(--ink-muted); font-size: .78rem; text-transform: uppercase; letter-spacing: .06em; margin-top: .55rem; }

/* Section scaffolding */
section { margin-bottom: 2.75rem; }
.sec-head { display: flex; align-items: baseline; gap: .6rem; margin-bottom: .35rem; }
h2 { font-size: 1.15rem; margin: 0; letter-spacing: -.01em; }
.sec-desc { color: var(--ink-muted); font-size: .85rem; margin: .1rem 0 1.1rem; max-width: 62ch; }
.rule { height: 1px; background: var(--border-soft); margin-bottom: 1.25rem; }

/* Metricas de Fiabilidad (ISO/IEC 25010) */
.fiab-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(288px, 1fr)); gap: 1rem; }
.fiab-card {
  background: var(--surface); border: 1px solid var(--border); border-left-width: 4px;
  border-radius: 14px; padding: 1.25rem 1.35rem; display: flex; flex-direction: column; gap: .75rem;
  transition: transform .15s ease, box-shadow .15s ease;
}
.fiab-card:hover { transform: translateY(-2px); box-shadow: 0 8px 24px var(--sombra); }
.fiab-card.fiab-cumple { border-left-color: var(--good); }
.fiab-card.fiab-no-cumple { border-left-color: var(--bad); }
.fiab-card.fiab-nd { border-left-color: var(--nd); }
.fiab-head { display: flex; justify-content: space-between; align-items: baseline; gap: .5rem; }
.fiab-nombre { font-size: .98rem; font-weight: 600; line-height: 1.25; }
.fiab-id {
  font-size: .68rem; color: var(--ink-muted); font-weight: 700; letter-spacing: .06em;
  border: 1px solid var(--border); border-radius: 6px; padding: .12rem .4rem; flex: 0 0 auto;
}
.fiab-body { display: flex; align-items: center; gap: 1.1rem; }
.fiab-visual { flex: 0 0 auto; line-height: 0; }
.fiab-meta { display: flex; flex-direction: column; gap: .4rem; min-width: 0; }
.fiab-valor { font-size: 2rem; font-weight: 800; font-variant-numeric: tabular-nums; line-height: 1; }
.fiab-estado { display: inline-flex; align-items: center; gap: .45rem; font-size: .82rem; font-weight: 600; }
.fiab-dot { width: .7rem; height: .7rem; border-radius: 50%; display: inline-block; flex: 0 0 auto; }
.fiab-cumple .fiab-dot { background: var(--good); }
.fiab-no-cumple .fiab-dot { background: var(--bad); }
.fiab-nd .fiab-dot { background: var(--nd); }
.fiab-foot { display: flex; flex-wrap: wrap; align-items: center; gap: .5rem; margin-top: auto; }
.fiab-umbral { font-size: .78rem; color: var(--ink-muted); }
.fiab-nota { font-size: .74rem; color: var(--ink-faint); font-style: italic; width: 100%; }
.badge { display: inline-block; padding: .14rem .55rem; border-radius: 999px; font-size: .68rem; font-weight: 700; letter-spacing: .02em; }
.badge-auto { background: var(--badge-auto-bg); color: var(--badge-auto-ink); border: 1px solid var(--badge-auto-line); }
.badge-decl { background: var(--badge-decl-bg); color: var(--badge-decl-ink); border: 1px solid var(--badge-decl-line); }

/* Donas SVG: los colores se heredan del CSS de la pagina (tema dual) */
.donut-track { stroke: var(--border); }
.donut-arc { stroke: var(--nd); transition: stroke .15s ease; }
.fiab-cumple .donut-arc { stroke: var(--good); }
.fiab-no-cumple .donut-arc { stroke: var(--bad); }
.donut-txt { fill: var(--ink); }
.donut-txt-nd { fill: var(--nd); }

/* Distribucion de issues (taxonomia de labels -> barras) */
.dist-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; }
.dist-card {
  background: var(--surface); border: 1px solid var(--border); border-radius: 14px;
  padding: 1.2rem 1.35rem;
  transition: transform .15s ease, box-shadow .15s ease, border-color .15s ease;
}
.dist-card:hover { transform: translateY(-2px); box-shadow: 0 8px 24px var(--sombra); border-color: var(--accent-line); }
.dist-title { font-size: .74rem; text-transform: uppercase; letter-spacing: .07em; color: var(--ink-muted); font-weight: 700; margin: 0 0 1rem; }
.bar-row { display: grid; grid-template-columns: minmax(64px, 34%) 1fr auto; align-items: center; gap: .7rem; margin-bottom: .7rem; }
.bar-row:last-child { margin-bottom: 0; }
.bar-label { font-size: .85rem; color: var(--ink); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.bar-track { height: 9px; background: var(--surface-2); border-radius: 999px; overflow: hidden; }
.bar-fill {
  display: block; height: 100%; min-width: 4px; border-radius: 999px;
  background: linear-gradient(90deg, var(--accent), var(--bar-fill-2));
  transform-origin: left; animation: crecer-barra .5s ease-out;
}
@keyframes crecer-barra { from { transform: scaleX(0); } }
.bar-val { font-size: .85rem; font-weight: 700; font-variant-numeric: tabular-nums; color: var(--ink); text-align: right; min-width: 2ch; }
.empty { color: var(--ink-faint); font-style: italic; font-size: .85rem; margin: 0; }

/* Metricas de proceso */
.proc-note { font-size: .78rem; color: var(--ink-faint); margin: .9rem 0 0; font-style: italic; }
.chart-card {
  background: var(--surface); border: 1px solid var(--border); border-radius: 14px;
  padding: 1.3rem 1.4rem; margin-top: 1rem;
}
.chart-card h3 { font-size: .74rem; text-transform: uppercase; letter-spacing: .07em; color: var(--ink-muted); font-weight: 700; margin: 0 0 1.1rem; }
.chart-scroll { overflow-x: auto; }
.chart-svg { width: 100%; max-width: 640px; height: auto; display: block; }
.axis { stroke: var(--border); }
.serie-abiertos { fill: var(--serie-abiertos); }
.serie-cerrados { fill: var(--serie-cerrados); }
.bar-num { fill: var(--ink); }
.week-label { fill: var(--ink-muted); }
.legend { display: flex; gap: 1.3rem; margin-top: 1rem; flex-wrap: wrap; }
.legend-item { display: inline-flex; align-items: center; gap: .45rem; font-size: .8rem; color: var(--ink-muted); }
.legend-dot { width: .7rem; height: .7rem; border-radius: 3px; display: inline-block; flex: 0 0 auto; }
.legend-dot.serie-abiertos { background: var(--serie-abiertos); }
.legend-dot.serie-cerrados { background: var(--serie-cerrados); }

footer { margin-top: 3.5rem; color: var(--ink-faint); font-size: .8rem; border-top: 1px solid var(--border-soft); padding-top: 1.25rem; }
code { background: var(--surface); border: 1px solid var(--border-soft); padding: .08rem .35rem; border-radius: 5px; font-size: .85em; }

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
# Duplicado deliberado de sqa/sitio/generar_docs.py (misma convencion que la
# paleta): la clave "tema" de localStorage y los valores de data-theme son un
# contrato compartido; ambos bloques deben cambiar juntos.
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


def _stripped(label: str) -> str:
    """Quita el prefijo de la taxonomia (``tipo:tarea`` -> ``tarea``)."""
    return label.split(":", 1)[1] if ":" in label else label


def _barras(grupo: dict) -> str:
    """Renderiza un grupo de la taxonomia como barras horizontales.

    Las barras se escalan al maximo del propio grupo (magnitud comparada dentro
    de la categoria). Cada fila lleva un ``title`` para el hover sin JS.
    """
    if not grupo:
        return '<p class="empty">Sin datos.</p>'
    items = sorted(grupo.items(), key=lambda kv: (-kv[1], kv[0]))
    maximo = max(grupo.values())
    filas = []
    for label, count in items:
        pct = (count / maximo * 100) if maximo else 0
        etiqueta = html.escape(_stripped(label))
        filas.append(
            f'<div class="bar-row" title="{html.escape(_stripped(label))}: {count}">'
            f'<span class="bar-label">{etiqueta}</span>'
            f'<span class="bar-track"><span class="bar-fill" style="width:{pct:.1f}%"></span></span>'
            f'<span class="bar-val">{count}</span>'
            f"</div>"
        )
    return "".join(filas)


# Semaforo: estado -> (clase CSS, etiqueta). Solo cumple/no_cumple/nd (spec A2:
# la banda "en riesgo" no esta ratificada). Los colores viven en el CSS por
# clase de estado, para que se adapten al tema activo.
FIAB_ESTADO = {
    "cumple":    ("fiab-cumple", "Cumple"),
    "no_cumple": ("fiab-no-cumple", "No cumple"),
    "nd":        ("fiab-nd", "N/D"),
}

# Fuente -> (etiqueta, clase de badge). Auto (azul) vs Declarada (ambar).
FIAB_FUENTE = {
    "auto":      ("Automática", "badge-auto"),
    "declarado": ("Declarada", "badge-decl"),
}

_DONUT_RADIO = 42


def _es_numero(valor) -> bool:
    return isinstance(valor, (int, float)) and not isinstance(valor, bool)


def _svg_donut(pct: float) -> str:
    """Dona SVG inline (sin script/CDN, CSP/Pages safe) para metricas %.

    Sin colores hardcodeados: el arco toma su stroke de la clase de estado de
    la tarjeta contenedora (.fiab-cumple / .fiab-no-cumple / .fiab-nd).
    """
    circ = 2 * math.pi * _DONUT_RADIO
    dash = max(0.0, min(100.0, pct)) / 100 * circ
    return (
        f'<svg viewBox="0 0 100 100" width="88" height="88" role="img" '
        f'aria-label="{pct:g} por ciento">'
        f'<circle class="donut-track" cx="50" cy="50" r="{_DONUT_RADIO}" fill="none" stroke-width="9"/>'
        f'<circle class="donut-arc" cx="50" cy="50" r="{_DONUT_RADIO}" fill="none" stroke-width="9" '
        f'stroke-linecap="round" stroke-dasharray="{dash:.2f} {circ:.2f}" '
        f'transform="rotate(-90 50 50)"/>'
        f'<text class="donut-txt" x="50" y="56" text-anchor="middle" font-size="20" '
        f'font-weight="700">{pct:g}%</text></svg>'
    )


def _svg_donut_nd() -> str:
    return (
        '<svg viewBox="0 0 100 100" width="88" height="88" role="img" aria-label="No disponible">'
        f'<circle class="donut-track" cx="50" cy="50" r="{_DONUT_RADIO}" fill="none" stroke-width="9" '
        'stroke-dasharray="4 6"/>'
        '<text class="donut-txt-nd" x="50" y="56" text-anchor="middle" font-size="16" '
        'font-weight="700">N/D</text></svg>'
    )


def _fiab_umbral_txt(umbral, unidad: str) -> str:
    if not isinstance(umbral, dict):
        return ""
    comparador = umbral.get("comparador", "")
    valor = umbral.get("valor", "")
    sufijo = "%" if unidad == "%" else (f" {unidad}" if unidad else "")
    prop = "" if umbral.get("ratificado", False) else " [PROP]"
    return f"Meta: {comparador} {valor}{sufijo}{prop}"


def _detalle_texto(detalle) -> str:
    """Formatea el detalle diagnostico de una metrica auto para la nota.

    M-02 -> cobertura por clase de servicio (surface la peor clase); M-03 ->
    conteos crudos de la suite de regresion. Cadena vacia si no hay detalle.
    """
    if not isinstance(detalle, dict):
        return ""
    if "PrestamoService" in detalle or "AmonestacionService" in detalle:
        partes = [
            f"{clase}: {ratio:g}%" if _es_numero(ratio) else f"{clase}: N/D"
            for clase, ratio in detalle.items()
        ]
        return " · ".join(partes)
    if "tests" in detalle:
        return (
            f"{detalle.get('tests', 0)} tests · "
            f"{detalle.get('failures', 0)} fallos · "
            f"{detalle.get('errors', 0)} errores · "
            f"{detalle.get('skipped', 0)} omitidos"
        )
    return ""


def _card_fiabilidad(m: dict) -> str:
    estado = m.get("estado", "nd")
    estado_cls, estado_label = FIAB_ESTADO.get(estado, FIAB_ESTADO["nd"])
    valor = m.get("valor")
    unidad = m.get("unidad") or ""
    es_pct = unidad == "%"

    if es_pct and _es_numero(valor):
        visual = _svg_donut(float(valor))
        valor_txt = f"{valor:g}%"
    elif _es_numero(valor):
        visual = ""
        valor_txt = f"{valor:g} {unidad}".strip()
    else:
        visual = _svg_donut_nd()
        valor_txt = "N/D"

    fuente = m.get("fuente", "")
    fuente_label, fuente_cls = FIAB_FUENTE.get(fuente, ("", ""))
    fuente_badge = (
        f'<span class="badge {fuente_cls}">Fuente: {fuente_label}</span>'
        if fuente_label else ""
    )

    es_nd = not _es_numero(valor)
    if fuente == "auto":
        # Una N/D automatica NO es un placeholder: significa artefacto ausente
        # o no medible. Se distingue en la nota de la N/D declarada (pendiente).
        if es_nd:
            nota = "Artefacto no disponible / no medible"
        else:
            nota = _detalle_texto(m.get("detalle")) or "Suite de regresión"
    else:
        if es_nd:
            nota = "Pendiente de ratificación"
        else:
            justificacion = m.get("justificacion") or ""
            responsable = m.get("responsable") or ""
            partes = [p for p in (justificacion,
                                  f"Responsable: {responsable}" if responsable else "") if p]
            nota = " — ".join(partes)
    nota_html = (
        f'<div class="fiab-nota" title="{html.escape(nota, quote=True)}">{html.escape(nota)}</div>'
        if nota else ""
    )

    visual_html = f'<div class="fiab-visual">{visual}</div>' if visual else ""
    nombre = html.escape(m.get("nombre") or "")
    metric_id = html.escape(m.get("id") or "")
    umbral_txt = html.escape(_fiab_umbral_txt(m.get("umbral"), unidad))

    return f"""
    <div class="fiab-card {estado_cls}">
      <div class="fiab-head"><span class="fiab-nombre">{nombre}</span><span class="fiab-id">{metric_id}</span></div>
      <div class="fiab-body">
        {visual_html}
        <div class="fiab-meta">
          <div class="fiab-valor">{valor_txt}</div>
          <div class="fiab-estado"><span class="fiab-dot"></span>{estado_label}</div>
        </div>
      </div>
      <div class="fiab-foot">
        <span class="fiab-umbral">{umbral_txt}</span>
        {fuente_badge}
      </div>
      {nota_html}
    </div>"""


def _seccion_fiabilidad(fiab) -> str:
    """Renderiza la seccion de metricas de fiabilidad. Ausente -> se omite."""
    if not fiab:
        return ""
    metricas = fiab.get("metricas") if isinstance(fiab, dict) else None
    if not metricas:
        return ""
    cards = "".join(_card_fiabilidad(m) for m in metricas)
    return (
        '<section>'
        '<div class="sec-head"><h2>Métricas de Fiabilidad</h2></div>'
        '<p class="sec-desc">Métricas de producto M-01 a M-06 (ISO/IEC 25010). Las automáticas se '
        'miden sobre la suite de regresión (JaCoCo / Surefire); las declaradas las mantiene el '
        'Líder de Métricas. La meta mostrada es el objetivo de la fase; los valores marcados '
        '[PROP] están propuestos, no ratificados.</p>'
        '<div class="rule"></div>'
        f'<div class="fiab-grid">{cards}</div></section>'
    )


def _seccion_distribucion(data: dict) -> str:
    """Renderiza la taxonomia de labels como una grilla de barras horizontales."""
    tarjetas = []
    for clave, titulo in GRUPOS.items():
        tarjetas.append(
            f'<div class="dist-card"><h3 class="dist-title">{html.escape(titulo)}</h3>'
            f'{_barras(data.get(clave, {}))}</div>'
        )
    return (
        '<section>'
        '<div class="sec-head"><h2>Distribución de issues</h2></div>'
        '<p class="sec-desc">Reparto de los issues del repositorio según la taxonomía de '
        'etiquetas. Cada barra se escala al máximo de su propio grupo.</p>'
        '<div class="rule"></div>'
        f'<div class="dist-grid">{"".join(tarjetas)}</div></section>'
    )


def _svg_tendencia(tendencia) -> str:
    """Barras verticales agrupadas (aperturas vs cierres por semana), SVG inline.

    Sin script ni CDN (CSP/Pages safe). Cada barra lleva su valor como etiqueta
    directa; el eje base ancla las barras. Semanas sin actividad no se emiten.
    Los colores de las series (.serie-abiertos / .serie-cerrados) viven en el
    CSS, para que el grafico se adapte al tema activo.
    """
    if not tendencia:
        return '<p class="empty">Sin datos.</p>'
    n = len(tendencia)
    maximo = max((max(t["abiertos"], t["cerrados"]) for t in tendencia), default=0) or 1
    slot, bw, gap = 104, 28, 10
    plot_h, pad_top, pad_bottom, pad_x = 150, 26, 32, 14
    ancho = pad_x * 2 + n * slot
    alto = pad_top + plot_h + pad_bottom
    base_y = pad_top + plot_h

    def _barra(x: float, val: int, clase: str) -> str:
        if not val:
            return ""
        h = val / maximo * plot_h
        if h < 3:
            h = 3
        y = base_y - h
        return (
            f'<rect class="{clase}" x="{x:.1f}" y="{y:.1f}" width="{bw}" height="{h:.1f}" rx="4"/>'
            f'<text class="bar-num" x="{x + bw / 2:.1f}" y="{y - 7:.1f}" text-anchor="middle" '
            f'font-size="13" font-weight="700">{val}</text>'
        )

    piezas = [
        f'<line class="axis" x1="{pad_x}" y1="{base_y}" x2="{ancho - pad_x}" y2="{base_y}" '
        f'stroke-width="1.5"/>'
    ]
    for i, t in enumerate(tendencia):
        cx = pad_x + i * slot + slot / 2
        piezas.append(_barra(cx - bw - gap / 2, t["abiertos"], "serie-abiertos"))
        piezas.append(_barra(cx + gap / 2, t["cerrados"], "serie-cerrados"))
        piezas.append(
            f'<text class="week-label" x="{cx:.1f}" y="{base_y + 20:.1f}" text-anchor="middle" '
            f'font-size="12">{html.escape(t["semana"])}</text>'
        )
    return (
        f'<svg class="chart-svg" viewBox="0 0 {ancho} {alto}" role="img" '
        f'aria-label="Aperturas y cierres de issues por semana">{"".join(piezas)}</svg>'
    )


def _seccion_proceso(proceso) -> str:
    """Renderiza la seccion de metricas de proceso. Ausente -> se omite."""
    if not isinstance(proceso, dict):
        return ""
    lead = proceso.get("lead_time") or {}
    tendencia = proceso.get("tendencia") or []
    cerrados = lead.get("n", 0)

    def _dias(v) -> str:
        return f"{v:g} d" if _es_numero(v) else "N/D"

    tiles = "".join(
        f'<div class="kpi"><div class="n">{valor}</div><div class="l">{etiqueta}</div></div>'
        for valor, etiqueta in (
            (_dias(lead.get("mediana_dias")), "Lead time mediano"),
            (_dias(lead.get("promedio_dias")), "Lead time promedio"),
            (_dias(lead.get("p90_dias")), "Lead time P90"),
            (str(cerrados), "Issues cerrados"),
        )
    )
    nota = (
        '' if cerrados else
        '<p class="proc-note">Aún no hay issues cerrados con fecha de cierre para medir '
        'lead time. Solo se mide lead time (apertura a cierre): el export no trae señal '
        'de inicio de trabajo, por lo que el cycle time no es derivable.</p>'
    )
    leyenda = (
        '<div class="legend">'
        '<span class="legend-item"><span class="legend-dot serie-abiertos"></span>Abiertos</span>'
        '<span class="legend-item"><span class="legend-dot serie-cerrados"></span>Cerrados</span>'
        '</div>'
    )
    return (
        '<section>'
        '<div class="sec-head"><h2>Métricas de proceso</h2></div>'
        '<p class="sec-desc">Cómo fluye el trabajo del equipo, derivado de las fechas de '
        'apertura y cierre de los issues. Complementa a las métricas de producto.</p>'
        '<div class="rule"></div>'
        f'<div class="kpis">{tiles}</div>{nota}'
        '<div class="chart-card"><h3>Aperturas vs cierres por semana</h3>'
        f'<div class="chart-scroll">{_svg_tendencia(tendencia)}</div>{leyenda}</div>'
        '</section>'
    )


def generar_dashboard(
    reporte_path: str = "sqa/metricas/reporte_kpi.json",
    output_path: str = "site/index.html",
) -> Path:
    data = json.loads(Path(reporte_path).read_text(encoding="utf-8"))
    generado = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    fiabilidad_html = _seccion_fiabilidad(data.get("fiabilidad"))
    proceso_html = _seccion_proceso(data.get("proceso"))
    distribucion_html = _seccion_distribucion(data)

    documento = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Dashboard de Métricas SQA - Equipo 58-1</title>
{SCRIPT_TEMA}
<style>{CSS}</style>
</head>
<body>
<div class="wrap" id="top">
  <header class="masthead">
    <span class="eyebrow">Proceso SQA</span>
    <h1>Dashboard de Métricas del Proceso SQA</h1>
    <p class="sub">Sistema de Gestión Bibliotecaria &middot; Equipo 58-1 &middot; Generado {generado}</p>
    <nav class="nav">
      <a href="docs/index.html">Documentos del proceso SQA</a>
      {BOTON_TEMA}
    </nav>
  </header>

  <div class="kpis">
    <div class="kpi"><div class="n">{data.get("total_issues", 0)}</div><div class="l">Issues totales</div></div>
    <div class="kpi"><div class="n">{data.get("cerrados", 0)}</div><div class="l">Cerrados</div></div>
    <div class="kpi accent"><div class="n">{data.get("tasa_resolucion_pct", 0)}%</div><div class="l">Tasa de resolución</div></div>
  </div>

  {fiabilidad_html}

  {proceso_html}

  {distribucion_html}

  <footer>
    Datos derivados de los issues del repositorio vía <code>gh issue list</code> +
    <code>calcular_kpi.py</code>. Métricas agrupadas por la taxonomía de etiquetas
    (tipo / area / severidad / fase / iso / rol). Generado automáticamente por GitHub Actions.
  </footer>
</div>
</body>
</html>
"""

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(documento, encoding="utf-8")
    print(f"Dashboard generado: {out}")
    return out


if __name__ == "__main__":
    generar_dashboard()
