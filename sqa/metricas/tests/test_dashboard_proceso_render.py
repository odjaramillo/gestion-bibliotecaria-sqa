"""Render tests for the process + distribution dashboard sections.

Locks the risk-bearing presentation logic added alongside the process metrics:
HTML escaping of label / week text (the injection surface), empty-data
handling, the SVG div-by-zero guard, and the visible-contract label ``Meta:``.
"""

import generar_dashboard as gd


# --- distribution bars --------------------------------------------------

def test_barras_escapes_html_in_labels():
    html = gd._barras({"tipo:<script>x</script>": 1})
    assert "<script>" not in html
    assert "&lt;script&gt;" in html


def test_barras_strips_taxonomy_prefix():
    html = gd._barras({"rol:lider-tec": 3})
    assert ">lider-tec<" in html
    assert "rol:" not in html


def test_barras_empty_group_renders_placeholder():
    assert "Sin datos" in gd._barras({})


def test_barras_scales_widest_to_full_width():
    html = gd._barras({"a": 10, "b": 5})
    assert "width:100.0%" in html


# --- weekly trend SVG ---------------------------------------------------

def test_svg_tendencia_empty_is_placeholder():
    assert "Sin datos" in gd._svg_tendencia([])


def test_svg_tendencia_all_zero_week_does_not_crash():
    # maximo == 0 -> el guard ``or 1`` evita la división por cero
    out = gd._svg_tendencia([{"semana": "2026-W01", "abiertos": 0, "cerrados": 0}])
    assert "<svg" in out and "</svg>" in out


def test_svg_tendencia_escapes_week_label():
    out = gd._svg_tendencia([{"semana": "<b>W", "abiertos": 1, "cerrados": 0}])
    assert "<b>W" not in out
    assert "&lt;b&gt;W" in out


# --- process section ----------------------------------------------------

def test_seccion_proceso_none_is_omitted():
    assert gd._seccion_proceso(None) == ""


def test_seccion_proceso_no_closed_shows_nd_and_cycle_time_note():
    html = gd._seccion_proceso({
        "lead_time": {"n": 0, "mediana_dias": None, "promedio_dias": None, "p90_dias": None},
        "tendencia": [],
    })
    assert "N/D" in html
    assert "cycle time no es derivable" in html


def test_seccion_proceso_renders_lead_time_days_and_legend():
    html = gd._seccion_proceso({
        "lead_time": {"n": 6, "mediana_dias": 7.3, "promedio_dias": 7.2, "p90_dias": 14.2},
        "tendencia": [{"semana": "2026-W26", "abiertos": 9, "cerrados": 1}],
    })
    assert "7.3 d" in html
    assert "Abiertos" in html and "Cerrados" in html
    assert "<script" not in html


# --- fiabilidad umbral label (visible contract) -------------------------

def test_fiab_umbral_txt_uses_meta_label():
    txt = gd._fiab_umbral_txt({"valor": 50, "comparador": ">=", "ratificado": False}, "%")
    assert txt.startswith("Meta:")
    assert "50" in txt and "[PROP]" in txt
