"""TDD tests for evaluar_estado (compliance evaluation).

Acceptance criteria: spec REQ-MDR-03 (N/D neutral), REQ-MDR-04 (inclusive
boundary). Design Decision 3: estado is computed for BOTH auto and declared
metrics, never hand-written. Enum: ``cumple`` | ``no_cumple`` | ``nd``.

The ``amarillo`` / "en riesgo" band is NOT ratified (spec A2 open), so the
tool reports only cumple/no_cumple/nd.
"""

import calcular_kpi

GTE = {"valor": 70, "comparador": ">="}
LTE = {"valor": 1.0, "comparador": "<="}


# --- higher-is-better (>=) : M-02/M-03/M-04/M-05/M-06 --------------------

def test_gte_above_threshold_is_cumple():
    assert calcular_kpi.evaluar_estado(72.4, GTE) == "cumple"


def test_gte_exactly_at_threshold_is_cumple_inclusive():
    # REQ-MDR-04: valor == umbral -> cumple (verde inclusive)
    assert calcular_kpi.evaluar_estado(70.0, GTE) == "cumple"


def test_gte_just_below_threshold_is_no_cumple():
    assert calcular_kpi.evaluar_estado(69.9, GTE) == "no_cumple"


def test_m03_hundred_percent_gate_boundary():
    gate = {"valor": 100, "comparador": ">="}
    assert calcular_kpi.evaluar_estado(100.0, gate) == "cumple"
    assert calcular_kpi.evaluar_estado(99.9, gate) == "no_cumple"


# --- lower-is-better banded (<=) : M-01 ---------------------------------

def test_lte_at_verde_bound_is_cumple_inclusive():
    # REQ-MDR-04: M-01 verde bound = 1.0, valor = 1.0 -> cumple
    assert calcular_kpi.evaluar_estado(1.0, LTE) == "cumple"


def test_lte_above_verde_bound_is_no_cumple():
    # valor = 1.1 -> not verde
    assert calcular_kpi.evaluar_estado(1.1, LTE) == "no_cumple"


# --- N/D neutral state (REQ-MDR-03) -------------------------------------

def test_none_valor_is_nd():
    assert calcular_kpi.evaluar_estado(None, GTE) == "nd"


def test_sentinel_string_valor_is_nd():
    assert calcular_kpi.evaluar_estado("N/D", GTE) == "nd"


def test_missing_or_invalid_umbral_is_nd():
    assert calcular_kpi.evaluar_estado(72.4, None) == "nd"
    assert calcular_kpi.evaluar_estado(72.4, {"comparador": ">="}) == "nd"
