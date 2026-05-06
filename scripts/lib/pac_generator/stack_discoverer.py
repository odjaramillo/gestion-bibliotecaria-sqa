"""StackDiscoverer: Extrae el stack tecnológico del SUT desde pom.xml y package.json.

El módulo parsea los archivos de build del backend (Maven) y del frontend (npm)
para producir un inventario determinista del stack.  Toda la salida se ordena
alfabéticamente para garantizar idempotencia.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET


def _ns(tag: str) -> str:
    """Return the fully-qualified Maven POM tag with default namespace."""
    return f"{{{http://maven.apache.org/POM/4.0.0}}}{tag}"


def parse_pom(path: Path) -> dict[str, Any]:
    """Parse a ``pom.xml`` and extract structured stack information.

    Returns:
        dict with keys: ``artifact_id``, ``version``, ``name``, ``description``,
        ``java_version``, ``spring_boot_version``, ``dependencies`` (list),
        ``build_tool``.

    Raises:
        FileNotFoundError: If *path* does not exist.
        ET.ParseError: If the XML is malformed.
    """
    if not path.exists():
        raise FileNotFoundError(f"pom.xml no encontrado: {path}")

    tree = ET.parse(path)
    root = tree.getroot()

    def text(tag: str) -> str | None:
        elem = root.find(_ns(tag))
        return elem.text.strip() if elem is not None and elem.text else None

    parent = root.find(_ns("parent"))
    spring_boot_version = None
    if parent is not None:
        v = parent.find(_ns("version"))
        if v is not None and v.text:
            spring_boot_version = v.text.strip()

    java_version = None
    props = root.find(_ns("properties"))
    if props is not None:
        jv = props.find(_ns("java.version"))
        if jv is not None and jv.text:
            java_version = jv.text.strip()

    dependencies: list[dict[str, str]] = []
    deps = root.find(_ns("dependencies"))
    if deps is not None:
        for dep in deps.findall(_ns("dependency")):
            g = dep.find(_ns("groupId"))
            a = dep.find(_ns("artifactId"))
            v = dep.find(_ns("version"))
            if g is not None and a is not None:
                dependencies.append({
                    "groupId": g.text.strip() if g.text else "",
                    "artifactId": a.text.strip() if a.text else "",
                    "version": v.text.strip() if v is not None and v.text else "",
                })

    return {
        "artifact_id": text("artifactId") or "",
        "version": text("version") or "",
        "name": text("name") or "",
        "description": text("description") or "",
        "java_version": java_version or "",
        "spring_boot_version": spring_boot_version or "",
        "dependencies": sorted(dependencies, key=lambda d: d["artifactId"]),
        "build_tool": "Maven",
    }


def parse_package_json(path: Path) -> dict[str, Any]:
    """Parse a ``package.json`` and extract structured stack information.

    Returns:
        dict with keys: ``name``, ``version``, ``vue_version``,
        ``dependencies`` (list), ``dev_dependencies`` (list), ``build_tool``.

    Raises:
        FileNotFoundError: If *path* does not exist.
        json.JSONDecodeError: If the JSON is malformed.
    """
    if not path.exists():
        raise FileNotFoundError(f"package.json no encontrado: {path}")

    data = json.loads(path.read_text(encoding="utf-8"))

    deps = data.get("dependencies", {})
    dev_deps = data.get("devDependencies", {})

    return {
        "name": data.get("name", ""),
        "version": data.get("version", ""),
        "vue_version": deps.get("vue", "").lstrip("^~"),
        "dependencies": sorted([{"name": k, "version": v.lstrip("^~")} for k, v in deps.items()]),
        "dev_dependencies": sorted([{"name": k, "version": v.lstrip("^~")} for k, v in dev_deps.items()]),
        "build_tool": "npm / vue-cli",
    }
