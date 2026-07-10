"""TDD tests for the fiabilidad composition layer (construir_fiabilidad).

Acceptance criteria: design Decision 3 (estado always computed), Decision 4
(auto wins for M-02/03/04), REQ-DMR-02 (declared registry never overrides auto),
REQ-MDR-03 (None -> N/D + estado nd). Also covers the CI-log warning trace
emitted when an AUTO metric degrades to N/D.

The auto artifact paths are module-level constants so tests monkeypatch them to
point at fixtures (valid) or nonexistent paths (degraded), keeping the suite
deterministic regardless of whether a local ``target/`` build is present.
"""

import json

import calcular_kpi
from conftest import FIXTURES_DIR

VALID_JACOCO = str(FIXTURES_DIR / "jacoco_valid.xml")
VALID_SUREFIRE = str(FIXTURES_DIR / "surefire_valid")
ABSENT_JACOCO = str(FIXTURES_DIR / "does_not_exist.xml")
ABSENT_SUREFIRE = str(FIXTURES_DIR / "surefire_absent")

ORDEN = ["M-01", "M-02", "M-03", "M-04", "M-05", "M-06"]


def _por_id(bloque: dict) -> dict:
    return {m["id"]: m for m in bloque["metricas"]}


def _auto_ok(monkeypatch):
    monkeypatch.setattr(calcular_kpi, "JACOCO_XML", VALID_JACOCO)
    monkeypatch.setattr(calcular_kpi, "SUREFIRE_DIR", VALID_SUREFIRE)


def _auto_degradado(monkeypatch):
    monkeypatch.setattr(calcular_kpi, "JACOCO_XML", ABSENT_JACOCO)
    monkeypatch.setattr(calcular_kpi, "SUREFIRE_DIR", ABSENT_SUREFIRE)


# --- fixed ordering + structure -----------------------------------------

def test_fixed_metric_order_m01_to_m06(monkeypatch):
    _auto_ok(monkeypatch)
    bloque = calcular_kpi.construir_fiabilidad(calcular_kpi.DECLARADO_JSON)
    assert [m["id"] for m in bloque["metricas"]] == ORDEN
    assert bloque["schema_version"] == calcular_kpi.FIABILIDAD_SCHEMA_VERSION


def test_auto_metrics_carry_fuente_auto_and_declared_carry_fuente_declarado(monkeypatch):
    _auto_ok(monkeypatch)
    metricas = _por_id(calcular_kpi.construir_fiabilidad(calcular_kpi.DECLARADO_JSON))
    for auto_id in ("M-02", "M-03", "M-04"):
        assert metricas[auto_id]["fuente"] == "auto"
    for decl_id in ("M-01", "M-05", "M-06"):
        assert metricas[decl_id]["fuente"] == "declarado"


# --- None -> N/D + estado nd propagation through _entrada ----------------

def test_degraded_auto_metric_propagates_nd_value_and_state(monkeypatch):
    _auto_degradado(monkeypatch)
    metricas = _por_id(calcular_kpi.construir_fiabilidad(calcular_kpi.DECLARADO_JSON))
    for auto_id in ("M-02", "M-03", "M-04"):
        assert metricas[auto_id]["valor"] == "N/D"
        assert metricas[auto_id]["estado"] == "nd"


# --- auto wins: declared registry M-02/03/04 keys are ignored ------------

def test_declared_registry_cannot_override_auto_metrics(monkeypatch, tmp_path):
    _auto_ok(monkeypatch)
    # A malicious/incorrect registry that tries to hand-declare auto metrics.
    registro = tmp_path / "declarado.json"
    registro.write_text(json.dumps({
        "schema_version": 1,
        "metricas": [
            {"id": "M-02", "valor": 0.0, "unidad": "%",
             "umbral": {"valor": 70, "comparador": ">="}},
            {"id": "M-03", "valor": 0.0, "unidad": "%",
             "umbral": {"valor": 100, "comparador": ">="}},
            {"id": "M-04", "valor": 0.0, "unidad": "%",
             "umbral": {"valor": 60, "comparador": ">="}},
            {"id": "M-01", "valor": 0.5, "unidad": "defectos/modulo",
             "umbral": {"valor": 1.0, "comparador": "<="}},
        ],
    }), encoding="utf-8")
    metricas = _por_id(calcular_kpi.construir_fiabilidad(str(registro)))
    # Auto values come from the JaCoCo/Surefire fixtures, NOT the 0.0 declared.
    assert metricas["M-02"]["valor"] == 80.0
    assert metricas["M-03"]["valor"] == 100.0
    assert metricas["M-04"]["valor"] == 60.0
    # A declared metric present in the registry is honored.
    assert metricas["M-01"]["valor"] == 0.5


# --- missing / invalid registry -> declared metrics degrade to nd --------

def test_missing_registry_degrades_all_declared_to_nd(monkeypatch):
    _auto_ok(monkeypatch)
    metricas = _por_id(calcular_kpi.construir_fiabilidad(str(FIXTURES_DIR / "no_such_registry.json")))
    for decl_id in ("M-01", "M-05", "M-06"):
        assert metricas[decl_id]["valor"] == "N/D"
        assert metricas[decl_id]["estado"] == "nd"


def test_invalid_registry_json_degrades_all_declared_to_nd(monkeypatch, tmp_path):
    _auto_ok(monkeypatch)
    bad = tmp_path / "bad.json"
    bad.write_text("{ not valid json", encoding="utf-8")
    metricas = _por_id(calcular_kpi.construir_fiabilidad(str(bad)))
    for decl_id in ("M-01", "M-05", "M-06"):
        assert metricas[decl_id]["valor"] == "N/D"
        assert metricas[decl_id]["estado"] == "nd"


# --- CI-log warning trace when an AUTO metric degrades to N/D ------------

def test_degraded_auto_metrics_emit_stderr_warning(monkeypatch, capsys):
    _auto_degradado(monkeypatch)
    calcular_kpi.construir_fiabilidad(calcular_kpi.DECLARADO_JSON)
    err = capsys.readouterr().err
    assert "WARN: M-02" in err
    assert "WARN: M-03" in err
    assert "WARN: M-04" in err


def test_healthy_auto_metrics_emit_no_warning(monkeypatch, capsys):
    _auto_ok(monkeypatch)
    calcular_kpi.construir_fiabilidad(calcular_kpi.DECLARADO_JSON)
    err = capsys.readouterr().err
    assert "WARN:" not in err
