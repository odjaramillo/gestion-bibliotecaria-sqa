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
    "por_tipo": "Tipo",
    "por_area": "Area",
    "por_severidad": "Severidad",
    "por_fase": "Fase",
    "por_iso": "Caracteristica ISO 25010",
    "por_rol": "Rol",
}

CSS = """
:root {
  color-scheme: dark;
  --bg: #0d1117;
  --surface: #161b22;
  --surface-2: #1c2230;
  --border: #30363d;
  --border-soft: #21262d;
  --ink: #e6edf3;
  --ink-muted: #9aa4b2;
  --ink-faint: #6e7681;
  --accent: #4493f8;
  --good: #3fb950;
  --bad: #f85149;
  --nd: #8b949e;
  --amber: #e3b341;
}
* { box-sizing: border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  margin: 0; padding: 2.5rem 1.25rem; line-height: 1.5;
  background:
    radial-gradient(1200px 600px at 50% -10%, rgba(68,147,248,.10), transparent 70%),
    var(--bg);
  color: var(--ink);
  -webkit-font-smoothing: antialiased;
}
.wrap { max-width: 1080px; margin: 0 auto; }

/* Header */
.masthead { margin-bottom: 2.25rem; }
.eyebrow {
  display: inline-block; font-size: .72rem; font-weight: 700; letter-spacing: .12em;
  text-transform: uppercase; color: var(--accent);
  border: 1px solid rgba(68,147,248,.35); background: rgba(68,147,248,.08);
  border-radius: 999px; padding: .2rem .7rem; margin-bottom: .9rem;
}
h1 { font-size: 1.9rem; margin: 0 0 .35rem; letter-spacing: -.01em; }
.sub { color: var(--ink-muted); margin: 0; font-size: .9rem; }

/* KPI hero tiles */
.kpis { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin: 1.75rem 0 2.75rem; }
.kpi {
  position: relative; background: var(--surface); border: 1px solid var(--border);
  border-radius: 12px; padding: 1.25rem 1.35rem; overflow: hidden;
}
.kpi::before {
  content: ""; position: absolute; inset: 0 0 auto 0; height: 3px;
  background: linear-gradient(90deg, var(--border), var(--border));
}
.kpi.accent::before { background: linear-gradient(90deg, var(--accent), #7cc3ff); }
.kpi .n { font-size: 2.4rem; font-weight: 800; line-height: 1; font-variant-numeric: tabular-nums; }
.kpi.accent .n { color: var(--accent); }
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
  border-radius: 12px; padding: 1.2rem 1.3rem; display: flex; flex-direction: column; gap: .75rem;
}
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
.fiab-foot { display: flex; flex-wrap: wrap; align-items: center; gap: .5rem; margin-top: auto; }
.fiab-umbral { font-size: .78rem; color: var(--ink-muted); }
.fiab-nota { font-size: .74rem; color: var(--ink-faint); font-style: italic; width: 100%; }
.badge { display: inline-block; padding: .14rem .55rem; border-radius: 999px; font-size: .68rem; font-weight: 700; letter-spacing: .02em; }
.badge-auto { background: rgba(68,147,248,.14); color: #79b8ff; border: 1px solid rgba(68,147,248,.4); }
.badge-decl { background: rgba(210,153,34,.14); color: #e3b341; border: 1px solid rgba(158,106,3,.6); }

/* Distribucion de issues (taxonomia de labels -> barras) */
.dist-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; }
.dist-card { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 1.15rem 1.3rem; }
.dist-title { font-size: .74rem; text-transform: uppercase; letter-spacing: .07em; color: var(--ink-muted); font-weight: 700; margin: 0 0 1rem; }
.bar-row { display: grid; grid-template-columns: minmax(64px, 34%) 1fr auto; align-items: center; gap: .7rem; margin-bottom: .7rem; }
.bar-row:last-child { margin-bottom: 0; }
.bar-label { font-size: .85rem; color: var(--ink); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.bar-track { height: 9px; background: var(--surface-2); border-radius: 999px; overflow: hidden; }
.bar-fill { display: block; height: 100%; min-width: 4px; border-radius: 999px; background: linear-gradient(90deg, var(--accent), #6db3ff); }
.bar-val { font-size: .85rem; font-weight: 700; font-variant-numeric: tabular-nums; color: var(--ink); text-align: right; min-width: 2ch; }
.empty { color: var(--ink-faint); font-style: italic; font-size: .85rem; margin: 0; }

footer { margin-top: 3.5rem; color: var(--ink-faint); font-size: .8rem; border-top: 1px solid var(--border-soft); padding-top: 1.25rem; }
code { background: var(--surface); border: 1px solid var(--border-soft); padding: .08rem .35rem; border-radius: 5px; font-size: .85em; }
"""


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

    es_nd = not _es_numero(valor)
    if fuente == "auto":
        # Una N/D automatica NO es un placeholder: significa artefacto ausente
        # o no medible. Se distingue en la nota de la N/D declarada (pendiente).
        if es_nd:
            nota = "Artefacto no disponible / no medible"
        else:
            nota = _detalle_texto(m.get("detalle")) or "Suite de regresion"
    else:
        if es_nd:
            nota = "Pendiente de ratificacion"
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
        '<div class="sec-head"><h2>Metricas de Fiabilidad</h2></div>'
        '<p class="sec-desc">Metricas de producto M-01 a M-06 (ISO/IEC 25010). Las automaticas se '
        'miden sobre la suite de regresion (JaCoCo / Surefire); las declaradas las mantiene el '
        'Lider de Metricas. La meta mostrada es el objetivo de la fase; los valores marcados '
        '[PROP] estan propuestos, no ratificados.</p>'
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
        '<div class="sec-head"><h2>Distribucion de issues</h2></div>'
        '<p class="sec-desc">Reparto de los issues del repositorio segun la taxonomia de '
        'etiquetas. Cada barra se escala al maximo de su propio grupo.</p>'
        '<div class="rule"></div>'
        f'<div class="dist-grid">{"".join(tarjetas)}</div></section>'
    )


def generar_dashboard(
    reporte_path: str = "sqa/metricas/reporte_kpi.json",
    output_path: str = "site/index.html",
) -> Path:
    data = json.loads(Path(reporte_path).read_text(encoding="utf-8"))
    generado = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    fiabilidad_html = _seccion_fiabilidad(data.get("fiabilidad"))
    distribucion_html = _seccion_distribucion(data)

    documento = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Dashboard de Metricas SQA - Equipo 58-1</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
  <header class="masthead">
    <span class="eyebrow">Proceso SQA</span>
    <h1>Dashboard de Metricas del Proceso SQA</h1>
    <p class="sub">Sistema de Gestion Bibliotecaria &middot; Equipo 58-1 &middot; Generado {generado}</p>
  </header>

  <div class="kpis">
    <div class="kpi"><div class="n">{data.get("total_issues", 0)}</div><div class="l">Issues totales</div></div>
    <div class="kpi"><div class="n">{data.get("cerrados", 0)}</div><div class="l">Cerrados</div></div>
    <div class="kpi accent"><div class="n">{data.get("tasa_resolucion_pct", 0)}%</div><div class="l">Tasa de resolucion</div></div>
  </div>

  {fiabilidad_html}

  {distribucion_html}

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
    out.write_text(documento, encoding="utf-8")
    print(f"Dashboard generado: {out}")
    return out


if __name__ == "__main__":
    generar_dashboard()
