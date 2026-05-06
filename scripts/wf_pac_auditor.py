#!/usr/bin/env python3
"""Workflow PAC Auditor: Valida un PAC generado contra el checklist IEEE 730-2014.

Este script lee un documento PAC en markdown y un checklist JSON, verifica
que cada ítem del checklist tenga su sección correspondiente en el PAC con
contenido sustantivo, y genera un reporte JSON de auditoría.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Mapeo ítem → sección del PAC (basado en evidence_location y categoría)
ITEM_TO_SECTION: dict[str, str] = {
    "PAC-01": "4",
    "PAC-02": "4",
    "PAC-03": "4",
    "PAC-04": "5",
    "PAC-05": "5",
    "PAC-06": "5",
    "PAC-07": "3",
    "PAC-08": "6",
    "PAC-09": "7",
    "PAC-10": "8",
    "PAC-11": "8",
    "PAC-12": "8",
    "PAC-13": "10",
    "PAC-14": "10",
    "PAC-15": "11",
}

# Ítems críticos: si alguno está pendiente → RECHAZADO
CRITICAL_ITEMS: set[str] = {"PAC-01", "PAC-04", "PAC-07", "PAC-10"}


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Construye y parsea los argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        description="Audita un PAC contra el checklist IEEE 730-2014"
    )
    parser.add_argument(
        "--pac",
        default="sqa/pac_generado.md",
        help="Ruta al archivo pac_generado.md",
    )
    parser.add_argument(
        "--checklist",
        default="sqa/checklists/pac.json",
        help="Ruta al checklist JSON",
    )
    parser.add_argument(
        "--output",
        default="sqa/reportes/wf_pac_audit.json",
        help="Ruta de salida para el reporte de auditoría",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Imprimir hallazgos detallados en stdout",
    )
    return parser.parse_args(argv)


def _read_checklist(path: Path) -> dict[str, Any]:
    """Lee el checklist JSON y retorna su contenido como dict."""
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def _read_pac(path: Path) -> str:
    """Lee el archivo PAC markdown y retorna su contenido."""
    with path.open(encoding="utf-8") as f:
        return f.read()


def _parse_sections(pac_content: str) -> dict[str, str]:
    """Extrae las secciones numeradas del PAC.

    Retorna un dict ``{número_sección: contenido}`` donde el contenido
    incluye todo el texto después del heading ``## N.`` hasta el siguiente
    ``## `` o fin de archivo.
    """
    sections: dict[str, str] = {}
    pattern = re.compile(r"^## (\d+)\.\s+(.+)$", re.MULTILINE)
    matches = list(pattern.finditer(pac_content))

    for i, match in enumerate(matches):
        section_num = match.group(1)
        start = match.end()
        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(pac_content)
        content = pac_content[start:end].strip()
        sections[section_num] = content

    return sections


def _validate_section(content: str) -> tuple[bool, str | None]:
    """Valida que una sección tenga contenido sustantivo y sin placeholders.

    Returns:
        ``(is_valid, reason)`` donde *reason* es ``None`` si la sección es
        válida, o un string explicando la falla.
    """
    if not content:
        return False, "Sección vacía (solo contiene el encabezado)"

    if "[COMPLETAR" in content:
        placeholder_match = re.search(r"\[COMPLETAR[^\]]*\]", content)
        placeholder = placeholder_match.group(0) if placeholder_match else "[COMPLETAR...]"
        return False, f"Sección contiene placeholder {placeholder}"

    if len(content) < 50:
        return (
            False,
            f"Sección tiene contenido insuficiente ({len(content)} caracteres)",
        )

    return True, None


def _audit(pac_path: Path, checklist_path: Path) -> tuple[dict[str, Any], int]:
    """Ejecuta la auditoría del PAC contra el checklist.

    Returns:
        ``(report, exit_code)`` donde *report* es el dict del reporte de
        auditoría y *exit_code* es 0 (APROBADO), 1 (PARCIAL) o 2 (RECHAZADO).
    """
    pac_content = _read_pac(pac_path)
    checklist = _read_checklist(checklist_path)
    sections = _parse_sections(pac_content)

    # Validar todas las secciones numeradas del 1 al 12
    all_section_numbers = [str(i) for i in range(1, 13)]
    secciones_completadas: list[str] = []
    secciones_pendientes: list[str] = []
    section_status: dict[str, tuple[bool, str | None]] = {}

    for num in all_section_numbers:
        content = sections.get(num, "")
        is_valid, reason = _validate_section(content)
        section_status[num] = (is_valid, reason)
        if is_valid:
            secciones_completadas.append(num)
        else:
            secciones_pendientes.append(num)

    # Evaluar cada ítem del checklist
    items = checklist.get("items", [])
    hallazgos: list[dict[str, str]] = []
    items_aprobados = 0
    items_pendientes = 0

    for item in items:
        item_id = item.get("id", "")
        section_num = ITEM_TO_SECTION.get(item_id)
        if not section_num:
            continue

        is_valid, reason = section_status.get(section_num, (False, "Sección no encontrada"))

        if is_valid:
            items_aprobados += 1
        else:
            items_pendientes += 1
            severity = "Alta" if item_id in CRITICAL_ITEMS else "Media"
            hallazgos.append(
                {
                    "id": item_id,
                    "categoria": item.get("category", ""),
                    "estado": "PENDIENTE",
                    "motivo": reason or "Sección no encontrada",
                    "severidad": severity,
                }
            )

    total_items = len(items)
    cobertura = (items_aprobados / total_items * 100) if total_items > 0 else 0.0

    # Determinar estado global
    critical_pending = any(h["id"] in CRITICAL_ITEMS for h in hallazgos)

    if items_pendientes == 0:
        estado = "APROBADO"
        exit_code = 0
    elif critical_pending or items_pendientes > (total_items / 2):
        estado = "RECHAZADO"
        exit_code = 2
    else:
        estado = "PARCIAL"
        exit_code = 1

    report: dict[str, Any] = {
        "workflow": "wf_pac_auditor",
        "fecha_ejecucion": datetime.now(timezone.utc).isoformat(),
        "estado": estado,
        "archivo_pac": str(pac_path),
        "total_items": total_items,
        "items_aprobados": items_aprobados,
        "items_pendientes": items_pendientes,
        "cobertura": f"{cobertura:.1f}%",
        "hallazgos": hallazgos,
        "secciones_completadas": secciones_completadas,
        "secciones_pendientes": secciones_pendientes,
    }

    return report, exit_code


def main(argv: list[str] | None = None) -> int:
    """Punto de entrada del auditor PAC.

    Returns:
        Código de salida: 0 APROBADO, 1 PARCIAL, 2 RECHAZADO.
    """
    args = _parse_args(argv)

    pac_path = Path(args.pac)
    checklist_path = Path(args.checklist)
    output_path = Path(args.output)

    if not pac_path.exists():
        print(f"ERROR: Archivo PAC no encontrado: {pac_path}", file=sys.stderr)
        return 2

    if not checklist_path.exists():
        print(f"ERROR: Checklist no encontrado: {checklist_path}", file=sys.stderr)
        return 2

    report, exit_code = _audit(pac_path, checklist_path)

    # Escribir reporte JSON
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    if args.verbose:
        print("\n=== Auditoría PAC ===")
        print(f"Estado: {report['estado']}")
        print(f"Items aprobados: {report['items_aprobados']}/{report['total_items']}")
        print(f"Cobertura: {report['cobertura']}")
        if report["hallazgos"]:
            print("\nHallazgos:")
            for h in report["hallazgos"]:
                print(f"  - {h['id']} ({h['severidad']}): {h['motivo']}")
        print(f"\nReporte escrito: {output_path}")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
