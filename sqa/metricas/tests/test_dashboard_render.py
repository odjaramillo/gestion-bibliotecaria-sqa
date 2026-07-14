"""Render tests for the fiabilidad cards (FIX 2 — metric honesty).

A degraded AUTO N/D (broken artifact) must read differently from a declared
N/D (pending sign-off), and the diagnostic ``detalle`` must reach the card.
"""

import generar_dashboard as gd


def _card(**over) -> str:
    base = {
        "id": "M-02", "nombre": "Cobertura de rama", "unidad": "%",
        "umbral": {"valor": 70, "comparador": ">="}, "fuente": "auto",
        "valor": "N/D", "estado": "nd", "detalle": None,
        "justificacion": None, "responsable": None,
    }
    base.update(over)
    return gd._card_fiabilidad(base)


def test_auto_nd_reads_as_broken_artifact():
    html = _card(fuente="auto", valor="N/D")
    assert "no disponible" in html or "no medible" in html
    assert "Pendiente de ratificación" not in html


def test_declared_nd_reads_as_pending_ratification():
    html = _card(id="M-01", nombre="Densidad de defectos",
                 unidad="defectos/modulo", fuente="declarado", valor="N/D")
    assert "Pendiente de ratificación" in html
    assert "no disponible" not in html


def test_auto_m02_surfaces_per_class_detalle():
    html = _card(fuente="auto", valor=60.7,
                 detalle={"PrestamoService": 60.7, "AmonestacionService": 100.0})
    assert "PrestamoService: 60.7%" in html
    assert "AmonestacionService: 100%" in html


def test_auto_m03_surfaces_suite_counts():
    html = _card(id="M-03", nombre="Tasa de exito", fuente="auto", valor=100.0,
                 detalle={"tests": 34, "failures": 0, "errors": 0, "skipped": 0})
    assert "34 tests" in html
    assert "0 fallos" in html
