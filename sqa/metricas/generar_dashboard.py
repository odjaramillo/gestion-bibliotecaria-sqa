"""Genera el dashboard HTML del proceso SQA a partir del reporte de KPIs.

Capa de presentacion: NO calcula metricas (eso lo hace calcular_kpi.py).
Lee sqa/metricas/reporte_kpi.json y produce un index.html self-contained
(sin dependencias externas) listo para desplegar en GitHub Pages.

Uso:
    python sqa/metricas/calcular_kpi.py            # genera reporte_kpi.json
    python sqa/metricas/generar_dashboard.py       # genera site/index.html
"""

import json
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
"""


def _tabla(grupo: dict) -> str:
    if not grupo:
        return '<p class="empty">Sin datos.</p>'
    filas = "".join(
        f"<tr><td>{label}</td><td class='v'>{count}</td></tr>"
        for label, count in sorted(grupo.items(), key=lambda kv: (-kv[1], kv[0]))
    )
    return f"<table><tbody>{filas}</tbody></table>"


def generar_dashboard(
    reporte_path: str = "sqa/metricas/reporte_kpi.json",
    output_path: str = "site/index.html",
) -> Path:
    data = json.loads(Path(reporte_path).read_text(encoding="utf-8"))
    generado = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

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
