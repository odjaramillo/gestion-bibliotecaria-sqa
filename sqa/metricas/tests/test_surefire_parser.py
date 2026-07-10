"""TDD tests for the Surefire parser (M-03 regresion pass rate).

Acceptance criteria: spec REQ-RMI-03 (M-03), REQ-RMI-04/05 (degradation).
Pass rate = (tests - failures - errors - skipped) / (tests - skipped) * 100.
Artifacts are regresion-scoped by Maven ``-Dgroups`` (design Decision 4), so
no tag-parsing happens here — the parser aggregates the present TEST-*.xml.
"""

import parser_surefire
from conftest import FIXTURES_DIR


def _dir(name: str) -> str:
    return str(FIXTURES_DIR / name)


def test_pass_rate_all_green_is_100():
    # 12 + 8 = 20 tests, 0 failures/errors/skipped -> 100.0
    assert parser_surefire.pass_rate(_dir("surefire_valid")) == 100.0


def test_pass_rate_with_failures_and_errors():
    # 40 tests, 2 failures, 1 error, 0 skipped -> (40-2-1-0)/(40-0) = 92.5
    assert parser_surefire.pass_rate(_dir("surefire_failures")) == 92.5


def test_pass_rate_excludes_skipped_from_both_numerator_and_denominator():
    # 10 tests, 0 fail/err, 2 skipped -> (10-0-0-2)/(10-2) = 8/8 = 100.0
    assert parser_surefire.pass_rate(_dir("surefire_skipped")) == 100.0


def test_pass_rate_zero_denominator_returns_none():
    # tests == 0 -> denominator 0 -> None (empty regresion universe)
    assert parser_surefire.pass_rate(_dir("surefire_zero")) is None


def test_pass_rate_missing_directory_returns_none():
    assert parser_surefire.pass_rate(_dir("surefire_absent")) is None


def test_detalle_reports_aggregated_counts():
    detalle = parser_surefire.pass_rate_detalle(_dir("surefire_failures"))
    assert detalle == {
        "tests": 40,
        "failures": 2,
        "errors": 1,
        "skipped": 0,
    }


# --- degradation paths (regression coverage of the never-raises contract) --

def test_pass_rate_malformed_xml_returns_none():
    # Truncated/unclosed testsuite tag -> ParseError swallowed -> None.
    assert parser_surefire.pass_rate(_dir("surefire_malformed")) is None


def test_pass_rate_non_integer_attribute_returns_none():
    # tests="doce" is not an int -> ValueError swallowed -> None.
    assert parser_surefire.pass_rate(_dir("surefire_noninteger")) is None


def test_pass_rate_empty_but_existing_directory_returns_none():
    # Directory exists but holds no TEST-*.xml (only .gitkeep) -> empty glob -> None.
    assert parser_surefire.pass_rate(_dir("surefire_empty")) is None


def test_pass_rate_all_skipped_returns_none():
    # tests == skipped (5 == 5) -> denominator 0 -> no honest ratio -> None.
    assert parser_surefire.pass_rate(_dir("surefire_all_skipped")) is None
