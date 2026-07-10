"""TDD tests for the process metrics layer (lead time + weekly trend).

These metrics derive purely from the GitHub issue export fields ``createdAt`` /
``closedAt`` / ``state``. Only LEAD TIME (open -> close) is measured: the export
carries no "work started" signal, so cycle time is NOT derivable and is not
reported (metric honesty — never fabricate a value we cannot measure).
"""

import calcular_kpi as ck


def _issue(number, state, created, closed=None):
    return {
        "number": number, "state": state,
        "createdAt": created, "closedAt": closed, "labels": [],
    }


# --- lead time ----------------------------------------------------------

def test_lead_time_ignores_open_issues():
    issues = [_issue(1, "OPEN", "2026-06-01T00:00:00Z")]
    stats = ck.lead_time_stats(issues)
    assert stats["n"] == 0
    assert stats["mediana_dias"] is None


def test_lead_time_computes_days_between_open_and_close():
    # opened Jun 1, closed Jun 6 -> 5 days
    issues = [_issue(1, "CLOSED", "2026-06-01T00:00:00Z", "2026-06-06T00:00:00Z")]
    stats = ck.lead_time_stats(issues)
    assert stats["n"] == 1
    assert stats["mediana_dias"] == 5.0
    assert stats["promedio_dias"] == 5.0


def test_lead_time_median_of_multiple():
    issues = [
        _issue(1, "CLOSED", "2026-06-01T00:00:00Z", "2026-06-02T00:00:00Z"),  # 1d
        _issue(2, "CLOSED", "2026-06-01T00:00:00Z", "2026-06-04T00:00:00Z"),  # 3d
        _issue(3, "CLOSED", "2026-06-01T00:00:00Z", "2026-06-10T00:00:00Z"),  # 9d
    ]
    stats = ck.lead_time_stats(issues)
    assert stats["n"] == 3
    assert stats["mediana_dias"] == 3.0


def test_lead_time_skips_negative_or_missing_timestamps():
    issues = [
        _issue(1, "CLOSED", "2026-06-06T00:00:00Z", "2026-06-01T00:00:00Z"),  # closed < created
        _issue(2, "CLOSED", "2026-06-01T00:00:00Z", None),                    # no closedAt
        _issue(3, "CLOSED", None, "2026-06-05T00:00:00Z"),                    # no createdAt
    ]
    stats = ck.lead_time_stats(issues)
    assert stats["n"] == 0


# --- weekly trend -------------------------------------------------------

def test_tendencia_counts_openings_and_closings_by_iso_week():
    issues = [
        _issue(1, "CLOSED", "2026-06-01T00:00:00Z", "2026-06-03T00:00:00Z"),
        _issue(2, "OPEN", "2026-06-02T00:00:00Z"),
    ]
    tendencia = ck.tendencia_semanal(issues)
    # Jun 1-3 2026 all fall in ISO week 2026-W23
    semana = next(t for t in tendencia if t["semana"] == "2026-W23")
    assert semana["abiertos"] == 2
    assert semana["cerrados"] == 1


def test_tendencia_sorted_and_spans_distinct_weeks():
    issues = [
        _issue(1, "OPEN", "2026-06-01T00:00:00Z"),   # W23
        _issue(2, "OPEN", "2026-06-15T00:00:00Z"),   # W25
    ]
    tendencia = ck.tendencia_semanal(issues)
    semanas = [t["semana"] for t in tendencia]
    assert semanas == sorted(semanas)
    assert "2026-W23" in semanas and "2026-W25" in semanas


def test_tendencia_empty_when_no_issues():
    assert ck.tendencia_semanal([]) == []


# --- P90 (linear-interpolation percentile — the risk-bearing math) ------

def test_p90_interpolates_between_ranks():
    # días [1, 3, 9] -> P90 = 7.8 (k = 1.8, entre rank 1 y 2)
    issues = [
        _issue(1, "CLOSED", "2026-06-01T00:00:00Z", "2026-06-02T00:00:00Z"),  # 1d
        _issue(2, "CLOSED", "2026-06-01T00:00:00Z", "2026-06-04T00:00:00Z"),  # 3d
        _issue(3, "CLOSED", "2026-06-01T00:00:00Z", "2026-06-10T00:00:00Z"),  # 9d
    ]
    assert ck.lead_time_stats(issues)["p90_dias"] == 7.8


def test_p90_single_value_equals_that_value():
    issues = [_issue(1, "CLOSED", "2026-06-01T00:00:00Z", "2026-06-06T00:00:00Z")]
    assert ck.lead_time_stats(issues)["p90_dias"] == 5.0


def test_p90_two_values_interpolates():
    # días [2, 8] -> P90 = 7.4 (k = 0.9)
    issues = [
        _issue(1, "CLOSED", "2026-06-01T00:00:00Z", "2026-06-03T00:00:00Z"),  # 2d
        _issue(2, "CLOSED", "2026-06-01T00:00:00Z", "2026-06-09T00:00:00Z"),  # 8d
    ]
    assert ck.lead_time_stats(issues)["p90_dias"] == 7.4


# --- _parse_iso tolerance -----------------------------------------------

def test_parse_iso_canonical_z():
    dt = ck._parse_iso("2026-06-01T10:00:00Z")
    assert dt is not None and dt.year == 2026 and dt.hour == 10


def test_parse_iso_tolerates_fractional_and_offset():
    assert ck._parse_iso("2026-06-01T10:00:00.500Z") is not None
    assert ck._parse_iso("2026-06-01T10:00:00+00:00") is not None


def test_parse_iso_rejects_garbage():
    assert ck._parse_iso("not-a-date") is None
    assert ck._parse_iso(None) is None
    assert ck._parse_iso(12345) is None


# --- gap-filled contiguous weeks ----------------------------------------

def test_tendencia_fills_zero_activity_weeks():
    issues = [
        _issue(1, "OPEN", "2026-06-01T00:00:00Z"),   # W23
        _issue(2, "OPEN", "2026-06-15T00:00:00Z"),   # W25
    ]
    tendencia = ck.tendencia_semanal(issues)
    semanas = [t["semana"] for t in tendencia]
    assert "2026-W24" in semanas  # semana intermedia sin actividad, en cero
    intermedia = next(t for t in tendencia if t["semana"] == "2026-W24")
    assert intermedia["abiertos"] == 0 and intermedia["cerrados"] == 0


# --- reporte wiring -----------------------------------------------------

def test_lead_time_stats_handles_empty_list():
    stats = ck.lead_time_stats([])
    assert stats["n"] == 0
    assert stats["mediana_dias"] is None
    assert stats["p90_dias"] is None
