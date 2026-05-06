"""ArtifactInventory: Inventaria artefactos del proyecto SUT.

Escanea ``documentacion/`` para PDFs, y los directorios de código fuente
para contar líneas de código (LOC) por paquete o componente.  Los resultados
se ordenan alfabéticamente para garantizar idempotencia.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any


def _count_lines(path: Path) -> int:
    """Return the number of non-empty lines in a file."""
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return 0
    return sum(1 for line in text.splitlines() if line.strip())


def scan_documentation(doc_dir: Path) -> list[dict[str, str]]:
    """List all PDF files in *doc_dir* with their names.

    Returns:
        Sorted list of dicts with keys ``filename`` and ``path`` (relative).
    """
    if not doc_dir.exists():
        return []

    pdfs = [
        {
            "filename": p.name,
            "path": str(p.relative_to(doc_dir.parent)),
        }
        for p in doc_dir.iterdir()
        if p.is_file() and p.suffix.lower() == ".pdf"
    ]
    return sorted(pdfs, key=lambda d: d["filename"])


def scan_java_source(src_dir: Path) -> dict[str, Any]:
    """Scan Java source files under *src_dir*.

    Returns:
        dict with ``total_files``, ``total_loc``, and ``packages``
        (sorted list of {package, files, loc}).
    """
    if not src_dir.exists():
        return {"total_files": 0, "total_loc": 0, "packages": []}

    packages: dict[str, dict[str, Any]] = {}
    total_files = 0
    total_loc = 0

    for java_file in sorted(src_dir.rglob("*.java")):
        rel = java_file.relative_to(src_dir)
        package = str(rel.parent).replace("/", ".").replace("\\", ".")
        if package == ".":
            package = "default"

        loc = _count_lines(java_file)
        total_files += 1
        total_loc += loc

        if package not in packages:
            packages[package] = {"package": package, "files": 0, "loc": 0}
        packages[package]["files"] += 1
        packages[package]["loc"] += loc

    return {
        "total_files": total_files,
        "total_loc": total_loc,
        "packages": sorted(packages.values(), key=lambda d: d["package"]),
    }


def scan_vue_source(src_dir: Path) -> dict[str, Any]:
    """Scan Vue source files under *src_dir*.

    Returns:
        dict with ``total_files``, ``total_loc``, and ``components``
        (sorted list of {component, loc}).
    """
    if not src_dir.exists():
        return {"total_files": 0, "total_loc": 0, "components": []}

    components: list[dict[str, Any]] = []
    total_files = 0
    total_loc = 0

    for vue_file in sorted(src_dir.rglob("*.vue")):
        rel = vue_file.relative_to(src_dir)
        name = str(rel.with_suffix("")).replace("/", ".").replace("\\", ".")
        loc = _count_lines(vue_file)
        total_files += 1
        total_loc += loc
        components.append({"component": name, "loc": loc})

    return {
        "total_files": total_files,
        "total_loc": total_loc,
        "components": sorted(components, key=lambda d: d["component"]),
    }
