"""TDD tests for the JaCoCo parser (M-02 branch, M-04 instruction).

Acceptance criteria: spec REQ-RMI-01 (M-02), REQ-RMI-02 (M-04),
REQ-RMI-04/05 (graceful degradation). Design Decision 5 (per-class min),
Decision 2 (never raises, returns float | None).
"""

from pathlib import Path

import parser_jacoco
from conftest import FIXTURES_DIR


def _fx(name: str) -> str:
    return str(FIXTURES_DIR / name)


# --- M-02 branch coverage (per-class min) --------------------------------

def test_branch_coverage_valid_returns_min_of_target_classes():
    # PrestamoService BRANCH = 8/(8+2) = 80.0; AmonestacionService = 9/(9+1) = 90.0
    # M-02 = min(80.0, 90.0) = 80.0
    assert parser_jacoco.branch_coverage(_fx("jacoco_valid.xml")) == 80.0


def test_branch_coverage_detail_lists_both_target_classes():
    detalle = parser_jacoco.branch_coverage_detalle(_fx("jacoco_valid.xml"))
    assert detalle == {"PrestamoService": 80.0, "AmonestacionService": 90.0}


def test_branch_coverage_missing_class_returns_none():
    # AmonestacionService absent -> M-02 cannot be aggregated over both -> None
    assert parser_jacoco.branch_coverage(_fx("jacoco_missing_class.xml")) is None


def test_branch_coverage_zero_denominator_returns_none():
    # covered + missed == 0 for both classes -> None (no honest ratio)
    assert parser_jacoco.branch_coverage(_fx("jacoco_zero_branch.xml")) is None


def test_branch_coverage_malformed_returns_none():
    assert parser_jacoco.branch_coverage(_fx("jacoco_malformed.xml")) is None


def test_branch_coverage_missing_file_returns_none():
    assert parser_jacoco.branch_coverage(_fx("does_not_exist.xml")) is None


# --- M-04 instruction coverage (report-level, direct child only) ---------

def test_instruction_coverage_valid_uses_report_level_counter():
    # Report-level INSTRUCTION = 600/(600+400) = 60.0.
    # Must NOT pick up the per-class INSTRUCTION counters (180/200, 90/100).
    assert parser_jacoco.instruction_coverage(_fx("jacoco_valid.xml")) == 60.0


def test_instruction_coverage_still_computed_when_a_class_is_missing():
    # M-04 is report-wide, independent of the per-class M-02 degradation.
    assert parser_jacoco.instruction_coverage(_fx("jacoco_missing_class.xml")) == 60.0


def test_instruction_coverage_malformed_returns_none():
    assert parser_jacoco.instruction_coverage(_fx("jacoco_malformed.xml")) is None


def test_instruction_coverage_missing_file_returns_none():
    assert parser_jacoco.instruction_coverage(_fx("does_not_exist.xml")) is None
