"""ConfigReader: Lee y valida la configuración del líder para el PAC.

Este módulo carga el archivo `pac_config.yaml` escrito por el líder de métricas
y lo valida contra un esquema estricto.  Los campos obligatorios se chequean
en tiempo de carga; si falta algo crítico se lanza `PacConfigError`.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


class PacConfigError(Exception):
    """Raised when pac_config.yaml is missing, malformed or invalid."""


@dataclass(frozen=True)
class PacConfig:
    """Immutable representation of the leader-provided PAC configuration."""

    proyecto: dict[str, Any]
    lider: dict[str, str]
    objetivos_calidad: dict[str, int]
    roles: dict[str, str]
    umbrales: dict[str, float]
    riesgos: list[dict[str, Any]]
    cronograma: list[dict[str, Any]]


def _validate_required_keys(data: dict[str, Any], required: set[str], ctx: str) -> None:
    """Ensure *data* contains every key in *required*."""
    missing = required - data.keys()
    if missing:
        raise PacConfigError(f"{ctx}: faltan campos obligatorios: {', '.join(sorted(missing))}")


def _validate_type(value: Any, expected: type, path: str) -> None:
    """Raise PacConfigError if *value* is not an instance of *expected*."""
    if not isinstance(value, expected):
        raise PacConfigError(
            f"{path}: se esperaba {expected.__name__}, se obtuvo {type(value).__name__}"
        )


def _validate_proyecto(proyecto: Any) -> None:
    _validate_type(proyecto, dict, "proyecto")
    _validate_required_keys(proyecto, {"name", "version", "descripcion"}, "proyecto")
    for key in ("name", "version", "descripcion"):
        _validate_type(proyecto[key], str, f"proyecto.{key}")


def _validate_lider(lider: Any) -> None:
    _validate_type(lider, dict, "lider")
    _validate_required_keys(lider, {"nombre", "email", "rol"}, "lider")
    for key in ("nombre", "email", "rol"):
        _validate_type(lider[key], str, f"lider.{key}")


def _validate_objetivos_calidad(objetivos: Any) -> None:
    _validate_type(objetivos, dict, "objetivos_calidad")
    if not objetivos:
        raise PacConfigError("objetivos_calidad: no puede estar vacío")
    for attr, weight in objetivos.items():
        _validate_type(weight, (int, float), f"objetivos_calidad.{attr}")
        if not (0 <= weight <= 100):
            raise PacConfigError(
                f"objetivos_calidad.{attr}: el peso debe estar entre 0 y 100, se obtuvo {weight}"
            )


def _validate_roles(roles: Any) -> None:
    _validate_type(roles, dict, "roles")
    if not roles:
        raise PacConfigError("roles: no puede estar vacío")
    for role, name in roles.items():
        _validate_type(name, str, f"roles.{role}")


def _validate_umbrales(umbrales: Any) -> None:
    _validate_type(umbrales, dict, "umbrales")
    if not umbrales:
        raise PacConfigError("umbrales: no puede estar vacío")
    for metric, target in umbrales.items():
        _validate_type(target, (int, float), f"umbrales.{metric}")


def _validate_riesgos(riesgos: Any) -> None:
    _validate_type(riesgos, list, "riesgos")
    for idx, riesgo in enumerate(riesgos):
        ctx = f"riesgos[{idx}]"
        _validate_type(riesgo, dict, ctx)
        _validate_required_keys(riesgo, {"descripcion", "mitigacion", "aceptado"}, ctx)
        for key in ("descripcion", "mitigacion"):
            _validate_type(riesgo[key], str, f"{ctx}.{key}")
        _validate_type(riesgo["aceptado"], bool, f"{ctx}.aceptado")


def _validate_cronograma(cronograma: Any) -> None:
    _validate_type(cronograma, list, "cronograma")
    for idx, item in enumerate(cronograma):
        ctx = f"cronograma[{idx}]"
        _validate_type(item, dict, ctx)
        _validate_required_keys(item, {"fase", "inicio", "fin", "entregables"}, ctx)
        for key in ("fase", "inicio", "fin"):
            _validate_type(item[key], str, f"{ctx}.{key}")
        _validate_type(item["entregables"], list, f"{ctx}.entregables")


def read_config(path: Path) -> PacConfig:
    """Load and validate a ``pac_config.yaml`` file.

    Args:
        path: Absolute or relative path to the YAML file.

    Returns:
        A frozen ``PacConfig`` dataclass.

    Raises:
        PacConfigError: If the file is missing, malformed, or violates the schema.
    """
    if not path.exists():
        raise PacConfigError(f"Archivo de configuración no encontrado: {path}")

    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise PacConfigError(f"Error de sintaxis YAML en {path}: {exc}") from exc

    if not isinstance(raw, dict):
        raise PacConfigError(f"El archivo YAML debe contener un diccionario raíz, se obtuvo {type(raw).__name__}")

    _validate_required_keys(raw, {"proyecto", "lider", "objetivos_calidad", "roles", "umbrales", "riesgos", "cronograma"}, "raíz")

    _validate_proyecto(raw["proyecto"])
    _validate_lider(raw["lider"])
    _validate_objetivos_calidad(raw["objetivos_calidad"])
    _validate_roles(raw["roles"])
    _validate_umbrales(raw["umbrales"])
    _validate_riesgos(raw["riesgos"])
    _validate_cronograma(raw["cronograma"])

    return PacConfig(
        proyecto=raw["proyecto"],
        lider=raw["lider"],
        objetivos_calidad=raw["objetivos_calidad"],
        roles=raw["roles"],
        umbrales=raw["umbrales"],
        riesgos=raw["riesgos"],
        cronograma=raw["cronograma"],
    )
