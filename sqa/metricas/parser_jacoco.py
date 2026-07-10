"""JaCoCo XML parser for reliability metrics M-02 and M-04.

Standalone, dependency-free (stdlib ``xml.etree.ElementTree`` only). Reads the
regresion-scoped ``jacoco.xml`` produced by ``jacoco:report``.

Contract (design Decision 2): every public function returns ``float | None``
(or a plain dict for ``*_detalle``) and NEVER raises. Missing files, malformed
XML, missing counters, or zero denominators all resolve to ``None`` so the
dashboard can always publish (absence of data is itself information).

- M-02: branch coverage restricted to ``PrestamoService`` and
  ``AmonestacionService``; value = min of the two per-class ratios
  (design Decision 5). If either target class is absent or uncomputable the
  metric degrades to ``None``.
- M-04: report-level instruction coverage taken from the INSTRUCTION counter
  that is a DIRECT child of ``<report>`` (a descendant search would wrongly
  match per-method/per-class counters).
"""

import xml.etree.ElementTree as ET
from pathlib import Path

SERVICE_PACKAGE = "com/biblioteca/service"
TARGET_CLASSES = {
    "PrestamoService": f"{SERVICE_PACKAGE}/PrestamoService",
    "AmonestacionService": f"{SERVICE_PACKAGE}/AmonestacionService",
}


def _load_report(xml_path: str) -> ET.Element | None:
    """Parse the JaCoCo XML and return the ``<report>`` root, or ``None``."""
    try:
        return ET.parse(Path(xml_path)).getroot()
    except (FileNotFoundError, OSError, ET.ParseError):
        return None


def _ratio(counter: ET.Element | None) -> float | None:
    """Return covered / (covered + missed) as a 1-decimal percentage."""
    if counter is None:
        return None
    try:
        covered = int(counter.attrib["covered"])
        missed = int(counter.attrib["missed"])
    except (KeyError, ValueError):
        return None
    total = covered + missed
    if total == 0:
        return None
    return round(covered / total * 100, 1)


def _class_branch_ratio(report: ET.Element, class_name: str) -> float | None:
    node = report.find(
        f'./package[@name="{SERVICE_PACKAGE}"]/class[@name="{class_name}"]'
        '/counter[@type="BRANCH"]'
    )
    return _ratio(node)


def branch_coverage_detalle(xml_path: str) -> dict:
    """Per-class branch coverage for the target service classes.

    Returns a dict keyed by short class name; a value is ``None`` when that
    class is absent or its BRANCH counter is missing / zero-denominator.
    """
    report = _load_report(xml_path)
    if report is None:
        return {short: None for short in TARGET_CLASSES}
    return {
        short: _class_branch_ratio(report, full)
        for short, full in TARGET_CLASSES.items()
    }


def branch_coverage(xml_path: str) -> float | None:
    """M-02: min branch coverage across the target classes, or ``None``.

    Degrades to ``None`` if ANY target class ratio is unavailable, so the
    metric never reports a partial value that hides a missing service.
    """
    ratios = branch_coverage_detalle(xml_path).values()
    if any(r is None for r in ratios):
        return None
    return min(ratios)


def instruction_coverage(xml_path: str) -> float | None:
    """M-04: report-level instruction coverage, or ``None``."""
    report = _load_report(xml_path)
    if report is None:
        return None
    # Direct child of <report> only — not a descendant search.
    return _ratio(report.find('./counter[@type="INSTRUCTION"]'))
