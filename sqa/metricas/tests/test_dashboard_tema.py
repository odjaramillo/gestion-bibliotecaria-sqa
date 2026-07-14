"""Render tests for the dual-theme presentation layer (UI/UX polish).

Dark stays the default palette; a light palette activates via
``prefers-color-scheme: light``. For that to work, no SVG fragment nor
state color may hardcode a hex value: everything must resolve through
CSS custom properties (inline SVG inherits the page CSS).
"""

import json

import generar_dashboard as gd


# --- dual theme -----------------------------------------------------------

def test_css_declares_dual_color_scheme():
    assert "color-scheme: light dark" in gd.CSS
    assert "@media (prefers-color-scheme: light)" in gd.CSS


def test_css_light_palette_overrides_core_tokens():
    light = gd.CSS.split("@media (prefers-color-scheme: light)", 1)[1]
    for token in ("--bg:", "--surface:", "--border:", "--ink:",
                  "--accent:", "--good:", "--bad:"):
        assert token in light, f"la paleta clara no redefine {token}"


def test_css_has_focus_visible_outline():
    assert ":focus-visible" in gd.CSS


def test_css_data_theme_override_wins_both_ways():
    # El conmutador estampa data-theme en <html>; esos overrides deben ganar
    # a la media query en ambos sentidos (claro forzado y oscuro forzado).
    assert ':root[data-theme="light"]' in gd.CSS
    assert ':root[data-theme="dark"]' in gd.CSS
    # La direccion "sistema claro, usuario fuerza oscuro" depende del guard
    # :not() DENTRO de la media query: sin el, la paleta clara del sistema
    # pisaria el oscuro forzado. Se asserta el guard, no solo el selector.
    inicio = gd.CSS.index("@media (prefers-color-scheme: light)")
    fin = gd.CSS.index(':root[data-theme="light"]')
    bloque_media = gd.CSS[inicio:fin]
    assert ':not([data-theme="dark"])' in bloque_media


def test_css_guards_reduced_motion():
    assert "prefers-reduced-motion" in gd.CSS


# --- SVG fragments must not hardcode colors --------------------------------

def test_donut_uses_classes_not_hex():
    svg = gd._svg_donut(75.0)
    assert "#30363d" not in svg
    assert "#e6edf3" not in svg
    assert 'class="donut-track"' in svg
    assert 'class="donut-arc"' in svg


def test_donut_nd_uses_classes_not_hex():
    svg = gd._svg_donut_nd()
    assert "#" not in svg
    assert 'class="donut-track"' in svg


def test_tendencia_svg_uses_classes_not_hex():
    out = gd._svg_tendencia([{"semana": "2026-W01", "abiertos": 2, "cerrados": 1}])
    for hexcolor in ("#30363d", "#e6edf3", "#9aa4b2", "#4493f8", "#3fb950"):
        assert hexcolor not in out, f"color hardcodeado {hexcolor} en el SVG"
    assert 'class="axis"' in out
    assert 'class="serie-abiertos"' in out
    assert 'class="serie-cerrados"' in out


def test_fiab_card_uses_state_class_instead_of_inline_style():
    html = gd._card_fiabilidad({
        "id": "M-03", "nombre": "Tasa de exito", "unidad": "%", "valor": 100.0,
        "estado": "cumple", "fuente": "auto",
        "umbral": {"valor": 95, "comparador": ">=", "ratificado": True},
        "detalle": None,
    })
    assert "fiab-cumple" in html
    assert "style=" not in html


def test_fiab_card_no_cumple_uses_its_state_class():
    # Frontera del semaforo de tres estados: no_cumple tiene su propia clase
    # (no cae al fallback nd ni reutiliza la de cumple).
    html = gd._card_fiabilidad({
        "id": "M-02", "nombre": "Cobertura de rama", "unidad": "%", "valor": 60.7,
        "estado": "no_cumple", "fuente": "auto",
        "umbral": {"valor": 70, "comparador": ">=", "ratificado": True},
        "detalle": None,
    })
    assert 'class="fiab-card fiab-no-cumple"' in html
    assert "No cumple" in html
    assert "style=" not in html


def test_legend_dots_use_series_classes():
    html = gd._seccion_proceso({
        "lead_time": {"n": 1, "mediana_dias": 1, "promedio_dias": 1, "p90_dias": 1},
        "tendencia": [{"semana": "2026-W01", "abiertos": 1, "cerrados": 1}],
    })
    assert 'class="legend-dot serie-abiertos"' in html
    assert 'class="legend-dot serie-cerrados"' in html
    assert "style=" not in html


# --- user-visible Spanish must carry accents --------------------------------

def test_group_titles_are_accented():
    assert gd.GRUPOS["por_area"] == "Área"
    assert gd.GRUPOS["por_iso"] == "Característica ISO 25010"


def test_section_titles_are_accented():
    dist = gd._seccion_distribucion({})
    assert "Distribución de issues" in dist
    proc = gd._seccion_proceso({"lead_time": {}, "tendencia": []})
    assert "Métricas de proceso" in proc
    fiab = gd._seccion_fiabilidad({"metricas": [
        {"id": "M-01", "nombre": "Densidad", "estado": "nd",
         "valor": "N/D", "fuente": "declarado"},
    ]})
    assert "Métricas de Fiabilidad" in fiab
    assert "regresión" in fiab


def test_full_document_nav_pill_and_accents(tmp_path):
    reporte = tmp_path / "reporte_kpi.json"
    reporte.write_text(json.dumps({
        "total_issues": 10, "cerrados": 5, "tasa_resolucion_pct": 50.0,
        "por_tipo": {"tipo:tarea": 3}, "por_area": {}, "por_severidad": {},
        "por_fase": {}, "por_iso": {}, "por_rol": {},
    }), encoding="utf-8")
    out = tmp_path / "index.html"
    gd.generar_dashboard(str(reporte), str(out))
    doc = out.read_text(encoding="utf-8")

    # Mismo patron de navegacion (pills .nav) que las paginas de documentos.
    assert '<nav class="nav">' in doc
    assert 'href="docs/index.html"' in doc
    assert "docs-link" not in doc

    # Conmutador de tema: boton visible + script inline (sin recursos externos).
    assert 'class="theme-toggle"' in doc
    assert "localStorage" in doc
    assert "<script src=" not in doc

    assert "Tasa de resolución" in doc
    assert "Dashboard de Métricas" in doc
    assert "vía" in doc
    assert "automáticamente" in doc
