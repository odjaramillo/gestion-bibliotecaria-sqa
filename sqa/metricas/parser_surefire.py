"""Surefire XML parser for reliability metric M-03 (regresion pass rate).

Standalone, dependency-free (stdlib only). Aggregates every
``target/surefire-reports/TEST-*.xml`` produced by the regresion-scoped Maven
run (design Decision 4 — scope is enforced by ``-Dgroups=regresion``, so this
parser does NOT parse tags and MUST NOT re-inflate the value).

Pass rate = (tests - failures - errors - skipped) / (tests - skipped) * 100,
rounded to 1 decimal. Skipped tests leave both the numerator and denominator,
so an all-skipped suite has no honest denominator and degrades to ``None``.

Contract (design Decision 2): returns ``float | None`` and NEVER raises. A
missing/empty directory, malformed XML, or a zero denominator all resolve to
``None``.
"""

import xml.etree.ElementTree as ET
from pathlib import Path

REPORT_GLOB = "TEST-*.xml"
_COUNT_ATTRS = ("tests", "failures", "errors", "skipped")


def _aggregate(reports_dir: str) -> dict | None:
    """Sum the testsuite counters across all TEST-*.xml, or ``None``."""
    directory = Path(reports_dir)
    if not directory.is_dir():
        return None
    files = sorted(directory.glob(REPORT_GLOB))
    if not files:
        return None
    totals = {attr: 0 for attr in _COUNT_ATTRS}
    for xml_file in files:
        try:
            suite = ET.parse(xml_file).getroot()
        except (OSError, ET.ParseError):
            return None
        for attr in _COUNT_ATTRS:
            try:
                totals[attr] += int(suite.attrib.get(attr, 0))
            except ValueError:
                return None
    return totals


def pass_rate_detalle(reports_dir: str) -> dict | None:
    """Aggregated raw counts (tests/failures/errors/skipped), or ``None``."""
    return _aggregate(reports_dir)


def pass_rate(reports_dir: str = "target/surefire-reports") -> float | None:
    """M-03: regresion suite pass rate as a 1-decimal percentage, or ``None``."""
    totals = _aggregate(reports_dir)
    if totals is None:
        return None
    denominator = totals["tests"] - totals["skipped"]
    if denominator <= 0:
        return None
    passed = (
        totals["tests"]
        - totals["failures"]
        - totals["errors"]
        - totals["skipped"]
    )
    return round(passed / denominator * 100, 1)
