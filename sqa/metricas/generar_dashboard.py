"""Genera el dashboard HTML del proceso SQA a partir del reporte de KPIs.

Capa de presentacion: NO calcula metricas (eso lo hace calcular_kpi.py).
Lee sqa/metricas/reporte_kpi.json y produce un index.html self-contained
(sin dependencias externas) listo para desplegar en GitHub Pages.

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
    "por_tipo": "Por tipo",
    "por_area": "Por area",
    "por_severidad": "Por severidad",
    "por_fase": "Por fase",
    "por_iso": "Por caracteristica ISO 25010",
    "por_rol": "Por rol",
}

CSS = """
:root { color-scheme: light dark; }
* { box-sizing: border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  margin: 0; padding: 2rem; line-height: 1.5;
  background: #0d1117; color: #e6edf3;
}
.wrap { max-width: 960px; margin: 0 auto; }
h1 { font-size: 1.6rem; margin: 0 0 .25rem; }
.sub { color: #8b949e; margin: 0 0 2rem; font-size: .9rem; }
.cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; margin-bottom: 2.5rem; }
.card { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 1.25rem; }
.card .n { font-size: 2.2rem; font-weight: 700; }
.card .l { color: #8b949e; font-size: .85rem; text-transform: uppercase; letter-spacing: .03em; }
.card.accent .n { color: #2f81f7; }
section { margin-bottom: 2rem; }
h2 { font-size: 1.05rem; border-bottom: 1px solid #30363d; padding-bottom: .4rem; }
table { width: 100%; border-collapse: collapse; }
td { padding: .45rem .25rem; border-bottom: 1px solid #21262d; }
td.v { text-align: right; font-variant-numeric: tabular-nums; font-weight: 600; }
.empty { color: #8b949e; font-style: italic; }
footer { margin-top: 3rem; color: #8b949e; font-size: .8rem; border-top: 1px solid #30363d; padding-top: 1rem; }
code { background: #161b22; padding: .1rem .35rem; border-radius: 4px; }

/* Metricas de Fiabilidad (ISO/IEC 25010) */
.fiab-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; margin-top: 1rem; }
.fiab-card { background: #161b22; border: 1px solid #30363d; border-left-width: 4px; border-radius: 8px; padding: 1.1rem; display: flex; flex-direction: column; gap: .6rem; }
.fiab-head { display: flex; justify-content: space-between; align-items: baseline; gap: .5rem; }
.fiab-nombre { font-size: .95rem; font-weight: 600; }
.fiab-id { font-size: .72rem; color: #8b949e; font-weight: 700; letter-spacing: .04em; }
.fiab-body { display: flex; align-items: center; gap: 1rem; }
.fiab-visual { flex: 0 0 auto; line-height: 0; }
.fiab-meta { display: flex; flex-direction: column; gap: .35rem; }
.fiab-valor { font-size: 1.9rem; font-weight: 700; font-variant-numeric: tabular-nums; }
.fiab-estado { display: inline-flex; align-items: center; gap: .4rem; font-size: .82rem; font-weight: 600; }
.fiab-dot { width: .7rem; height: .7rem; border-radius: 50%; display: inline-block; }
.fiab-umbral { font-size: .78rem; color: #8b949e; }
.fiab-nota { font-size: .72rem; color: #6e7681; font-style: italic; }
.badge { display: inline-block; padding: .12rem .5rem; border-radius: 999px; font-size: .7rem; font-weight: 700; align-self: flex-start; }
.badge-auto { background: rgba(47,129,247,.15); color: #58a6ff; border: 1px solid #1f6feb; }
.badge-decl { background: rgba(210,153,34,.15); color: #e3b341; border: 1px solid #9e6a03; }
"""


def _tabla(grupo: dict) -> str:
    if not grupo:
        return '<p class="empty">Sin datos.</p>'
    filas = "".join(
        f"<tr><td>{label}</td><td class='v'>{count}</td></tr>"
        for label, count in sorted(grupo.items(), key=lambda kv: (-kv[1], kv[0]))
    )
    return f"<table><tbody>{filas}</tbody></table>"


# Semaforo: estado -> (color, etiqueta). Solo cumple/no_cumple/nd (spec A2:
# la banda "en riesgo" no esta ratificada).
FIAB_ESTADO = {
    "cumple":    ("#3fb950", "Cumple"),
    "no_cumple": ("#f85149", "No cumple"),
    "nd":        ("#8b949e", "N/D"),
}

# Fuente -> (etiqueta, clase de badge). Auto (azul) vs Declarada (ambar).
FIAB_FUENTE = {
    "auto":      ("Automática", "badge-auto"),
    "declarado": ("Declarada", "badge-decl"),
}

_DONUT_RADIO = 42


def _es_numero(valor) -> bool:
    return isinstance(valor, (int, float)) and not isinstance(valor, bool)


def _svg_donut(pct: float, color: str) -> str:
    """Dona SVG inline (sin script/CDN, CSP/Pages safe) para metricas %."""
    circ = 2 * math.pi * _DONUT_RADIO
    dash = max(0.0, min(100.0, pct)) / 100 * circ
    return (
        f'<svg viewBox="0 0 100 100" width="88" height="88" role="img" '
        f'aria-label="{pct:g} por ciento">'
        f'<circle cx="50" cy="50" r="{_DONUT_RADIO}" fill="none" stroke="#30363d" stroke-width="9"/>'
        f'<circle cx="50" cy="50" r="{_DONUT_RADIO}" fill="none" stroke="{color}" stroke-width="9" '
        f'stroke-linecap="round" stroke-dasharray="{dash:.2f} {circ:.2f}" '
        f'transform="rotate(-90 50 50)"/>'
        f'<text x="50" y="56" text-anchor="middle" font-size="20" font-weight="700" '
        f'fill="#e6edf3">{pct:g}%</text></svg>'
    )


def _svg_donut_nd() -> str:
    return (
        '<svg viewBox="0 0 100 100" width="88" height="88" role="img" aria-label="No disponible">'
        f'<circle cx="50" cy="50" r="{_DONUT_RADIO}" fill="none" stroke="#30363d" stroke-width="9" '
        'stroke-dasharray="4 6"/>'
        '<text x="50" y="56" text-anchor="middle" font-size="16" font-weight="700" '
        'fill="#8b949e">N/D</text></svg>'
    )


def _fiab_umbral_txt(umbral, unidad: str) -> str:
    if not isinstance(umbral, dict):
        return ""
    comparador = umbral.get("comparador", "")
    valor = umbral.get("valor", "")
    sufijo = "%" if unidad == "%" else (f" {unidad}" if unidad else "")
    prop = "" if umbral.get("ratificado", False) else " [PROP]"
    return f"Umbral: {comparador} {valor}{sufijo}{prop}"


def _card_fiabilidad(m: dict) -> str:
    estado = m.get("estado", "nd")
    color, estado_label = FIAB_ESTADO.get(estado, FIAB_ESTADO["nd"])
    valor = m.get("valor")
    unidad = m.get("unidad") or ""
    es_pct = unidad == "%"

    if es_pct and _es_numero(valor):
        visual = _svg_donut(float(valor), color)
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

    if fuente == "auto":
        nota = "Suite de regresion"
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
    <div class="fiab-card" style="border-left-color:{color}">
      <div class="fiab-head"><span class="fiab-nombre">{nombre}</span><span class="fiab-id">{metric_id}</span></div>
      <div class="fiab-body">
        {visual_html}
        <div class="fiab-meta">
          <div class="fiab-valor">{valor_txt}</div>
          <div class="fiab-estado"><span class="fiab-dot" style="background:{color}"></span>{estado_label}</div>
        </div>
      </div>
      <div class="fiab-umbral">{umbral_txt}</div>
      {fuente_badge}
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
        '<section><h2>Metricas de Fiabilidad (ISO/IEC 25010)</h2>'
        '<p class="sub">Metricas de producto M-01 a M-06. Las automaticas se miden sobre '
        'la suite de regresion (JaCoCo / Surefire); las declaradas las mantiene el Lider '
        'de Metricas. Los umbrales marcados [PROP] estan propuestos, no ratificados.</p>'
        f'<div class="fiab-grid">{cards}</div></section>'
    )


def generar_dashboard(
    reporte_path: str = "sqa/metricas/reporte_kpi.json",
    output_path: str = "site/index.html",
) -> Path:
    data = json.loads(Path(reporte_path).read_text(encoding="utf-8"))
    generado = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    fiabilidad_html = _seccion_fiabilidad(data.get("fiabilidad"))

    secciones = "".join(
        f"<section><h2>{titulo}</h2>{_tabla(data.get(clave, {}))}</section>"
        for clave, titulo in GRUPOS.items()
    )

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Dashboard de Metricas SQA - Equipo 58-1</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
  <h1>Dashboard de Metricas del Proceso SQA</h1>
  <p class="sub">Sistema de Gestion Bibliotecaria - Equipo 58-1 - Generado: {generado}</p>

  <div class="cards">
    <div class="card"><div class="n">{data.get("total_issues", 0)}</div><div class="l">Issues totales</div></div>
    <div class="card"><div class="n">{data.get("cerrados", 0)}</div><div class="l">Cerrados</div></div>
    <div class="card accent"><div class="n">{data.get("tasa_resolucion_pct", 0)}%</div><div class="l">Tasa de resolucion</div></div>
  </div>

  {fiabilidad_html}

  {secciones}

  <footer>
    Datos derivados de los issues del repositorio via <code>gh issue list</code> +
    <code>calcular_kpi.py</code>. Metricas agrupadas por la taxonomia de etiquetas
    (tipo / area / severidad / fase / iso / rol). Generado automaticamente por GitHub Actions.
  </footer>
</div>
</body>
</html>
"""

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"Dashboard generado: {out}")
    return out


if __name__ == "__main__":
    generar_dashboard()
