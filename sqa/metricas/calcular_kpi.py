"""Cálculo de KPIs SQA a partir del export de issues de GitHub.

Uso:
    # 1. Exportar issues como JSON con gh CLI:
    #    gh issue list --state all --limit 500 \
    #      --json number,title,state,labels,createdAt,closedAt,assignees \
    #      > sqa/metricas/issues_export.json
    #
    # 2. Procesar:
    #    python sqa/metricas/calcular_kpi.py

Genera sqa/metricas/reporte_kpi.json con métricas GQM/PSM agrupadas por
taxonomía de etiquetas (tipo, area, severidad, fase, iso, rol) y, de forma
aditiva, un bloque "fiabilidad" (ISO/IEC 25010) con las métricas M-01..M-06.

Las métricas automáticas M-02/M-03/M-04 se derivan de los artefactos de la
suite de regresión (JaCoCo + Surefire). Las métricas declaradas M-01/M-05/M-06
se leen de metricas_fiabilidad.json. El estado de cumplimiento SIEMPRE lo
calcula evaluar_estado (nunca se declara a mano).
"""

import json
import sys
from collections import Counter
from pathlib import Path

import parser_jacoco
import parser_surefire

# Rutas canónicas de los artefactos de la suite de regresión (Decision 4).
JACOCO_XML = "target/site/jacoco/jacoco.xml"
SUREFIRE_DIR = "target/surefire-reports"
DECLARADO_JSON = "sqa/metricas/metricas_fiabilidad.json"

FIABILIDAD_SCHEMA_VERSION = 1

# Metadatos de las métricas automáticas (no viven en el registro declarado).
#
# Umbrales = META PRÁCTICA de la fase (piso alcanzable), no la meta aspiracional
# ISO/IEC 25010. Criterio del docente: en la práctica no se fijan metas altas; se
# fija lo que efectivamente se implementó y se documenta el máximo aparte. El
# valor ISO aspiracional queda registrado aquí como referencia de fondo pero NO
# se renderiza en el dashboard (una sola vara a la vista). Baselines redondos de
# Fase 2 — el número real de JaCoCo/Surefire cae donde caiga.
AUTO_META = {
    "M-02": {
        "nombre": "Cobertura de Decisión/Rama (servicios)",
        "unidad": "%",
        # Meta práctica F2: >=50%. Aspiracional ISO (fondo, no se muestra): 70%.
        "umbral": {"valor": 50, "comparador": ">=", "ratificado": False},
    },
    "M-03": {
        "nombre": "Tasa de Pruebas que Pasan",
        "unidad": "%",
        "umbral": {"valor": 100, "comparador": ">=", "ratificado": False},
    },
    "M-04": {
        "nombre": "Cobertura de Instrucciones",
        "unidad": "%",
        # Meta práctica F2: >=30%. Aspiracional ISO (fondo, no se muestra): 60%.
        "umbral": {"valor": 30, "comparador": ">=", "ratificado": False},
    },
}

# Metadatos de respaldo para las métricas declaradas: garantizan que las
# tarjetas M-01/M-05/M-06 rendericen (en N/D) aunque falte o falle el registro.
DECLARADO_META = {
    "M-01": {
        "nombre": "Densidad de Defectos de Fiabilidad",
        "unidad": "defectos/modulo",
        "umbral": {"valor": 1.0, "comparador": "<=", "ratificado": False},
    },
    "M-05": {
        "nombre": "Entradas Inválidas Controladas",
        "unidad": "%",
        "umbral": {"valor": 80, "comparador": ">=", "ratificado": False},
    },
    "M-06": {
        "nombre": "Operaciones con Guarda de Estado",
        "unidad": "%",
        "umbral": {"valor": 80, "comparador": ">=", "ratificado": False},
    },
}

# Orden de render fijo M-01..M-06 (declarado / auto / auto / auto / declarado / declarado).
ORDEN_FIABILIDAD = ["M-01", "M-02", "M-03", "M-04", "M-05", "M-06"]
IDS_DECLARADOS = ("M-01", "M-05", "M-06")
SENTINEL_ND = "N/D"

# Motivos de degradacion por metrica automatica. Se emiten a stderr cuando el
# valor cae a N/D para dejar una traza greppable en el log de CI (una N/D
# automatica NO es un placeholder: significa artefacto ausente o no medible).
_DEGRADACION_AUTO = {
    "M-02": "branch coverage degraded to N/D (jacoco.xml missing or unparseable)",
    "M-03": "regresion pass rate degraded to N/D (surefire reports missing, empty or all-skipped)",
    "M-04": "instruction coverage degraded to N/D (jacoco.xml missing or unparseable)",
}


def _advertir_degradacion(metric_id: str) -> None:
    """Emite a stderr una advertencia cuando una metrica auto cae a N/D."""
    motivo = _DEGRADACION_AUTO.get(metric_id, "degraded to N/D")
    print(f"WARN: {metric_id} {motivo}", file=sys.stderr)


def _es_numero(valor) -> bool:
    return isinstance(valor, (int, float)) and not isinstance(valor, bool)


def evaluar_estado(valor, umbral) -> str:
    """Devuelve el estado de cumplimiento: ``cumple`` | ``no_cumple`` | ``nd``.

    Se aplica por igual a métricas automáticas y declaradas (Decision 3). La
    comparación en el umbral es inclusiva (REQ-MDR-04): para ``>=`` un valor
    igual al umbral cumple; para ``<=`` (menor-es-mejor, p.ej. M-01) un valor
    igual a la cota verde cumple. La banda "en riesgo" no está ratificada
    (spec A2), por lo que solo se reporta cumple/no_cumple/nd.
    """
    if not _es_numero(valor) or not isinstance(umbral, dict):
        return "nd"
    comparador = umbral.get("comparador")
    referencia = umbral.get("valor")
    if comparador not in (">=", "<=") or not _es_numero(referencia):
        return "nd"
    if comparador == ">=":
        return "cumple" if valor >= referencia else "no_cumple"
    return "cumple" if valor <= referencia else "no_cumple"


def _entrada(metric_id, nombre, valor, unidad, umbral, fuente,
             detalle=None, justificacion=None, responsable=None) -> dict:
    valor_normalizado = valor if _es_numero(valor) else SENTINEL_ND
    return {
        "id": metric_id,
        "nombre": nombre,
        "valor": valor_normalizado,
        "unidad": unidad,
        "umbral": umbral,
        "estado": evaluar_estado(valor, umbral),
        "fuente": fuente,
        "detalle": detalle,
        "justificacion": justificacion,
        "responsable": responsable,
    }


def _cargar_declaradas(declarado_path: str) -> dict:
    """Lee el registro declarado y devuelve {id: entry} para M-01/M-05/M-06.

    Registro ausente o inválido -> dict vacío (las tres métricas caerán a N/D
    vía los metadatos de respaldo). Se ignoran claves M-02/M-03/M-04 aunque
    aparezcan en el registro (REQ-DMR-02: auto manda para métricas auto).
    """
    try:
        data = json.loads(Path(declarado_path).read_text(encoding="utf-8"))
        entradas = data.get("metricas", [])
    except (FileNotFoundError, OSError, json.JSONDecodeError, AttributeError):
        return {}
    resultado = {}
    if isinstance(entradas, list):
        for entry in entradas:
            if isinstance(entry, dict) and entry.get("id") in IDS_DECLARADOS:
                resultado[entry["id"]] = entry
    return resultado


def _metrica_auto(metric_id: str) -> dict:
    meta = AUTO_META[metric_id]
    if metric_id == "M-02":
        valor = parser_jacoco.branch_coverage(JACOCO_XML)
        detalle = parser_jacoco.branch_coverage_detalle(JACOCO_XML)
    elif metric_id == "M-03":
        valor = parser_surefire.pass_rate(SUREFIRE_DIR)
        detalle = parser_surefire.pass_rate_detalle(SUREFIRE_DIR)
    else:  # M-04
        valor = parser_jacoco.instruction_coverage(JACOCO_XML)
        detalle = None
    if valor is None:
        _advertir_degradacion(metric_id)
    return _entrada(
        metric_id, meta["nombre"], valor, meta["unidad"], meta["umbral"],
        fuente="auto", detalle=detalle,
    )


def _metrica_declarada(metric_id: str, registro: dict) -> dict:
    meta = DECLARADO_META[metric_id]
    entry = registro.get(metric_id, {})
    return _entrada(
        metric_id,
        entry.get("nombre", meta["nombre"]),
        entry.get("valor", SENTINEL_ND),
        entry.get("unidad", meta["unidad"]),
        entry.get("umbral", meta["umbral"]),
        fuente="declarado",
        detalle=None,
        justificacion=entry.get("justificacion"),
        responsable=entry.get("responsable"),
    )


def construir_fiabilidad(
    declarado_path: str = DECLARADO_JSON,
) -> dict:
    """Compone el bloque ``fiabilidad`` con las seis métricas en orden fijo."""
    registro = _cargar_declaradas(declarado_path)
    metricas = []
    for metric_id in ORDEN_FIABILIDAD:
        if metric_id in AUTO_META:
            metricas.append(_metrica_auto(metric_id))
        else:
            metricas.append(_metrica_declarada(metric_id, registro))
    return {"schema_version": FIABILIDAD_SCHEMA_VERSION, "metricas": metricas}


def generar_reporte_metricas(issues_path: str = "sqa/metricas/issues_export.json") -> dict:
    data = json.loads(Path(issues_path).read_text(encoding="utf-8"))
    all_labels = [l["name"] for i in data for l in i.get("labels", [])]
    total = len(data)
    cerrados = sum(1 for i in data if i["state"] == "CLOSED")

    metricas = {
        "total_issues": total,
        "cerrados": cerrados,
        "tasa_resolucion_pct": round(cerrados / total * 100, 1) if total else 0,
        "por_tipo":      Counter(l for l in all_labels if l.startswith("tipo:")),
        "por_area":      Counter(l for l in all_labels if l.startswith("area:")),
        "por_severidad": Counter(l for l in all_labels if l.startswith("severidad:")),
        "por_fase":      Counter(l for l in all_labels if l.startswith("fase:")),
        "por_iso":       Counter(l for l in all_labels if l.startswith("iso:")),
        "por_rol":       Counter(l for l in all_labels if l.startswith("rol:")),
        # Bloque aditivo de métricas de producto (ISO/IEC 25010).
        "fiabilidad":    construir_fiabilidad(),
    }

    output_path = Path("sqa/metricas/reporte_kpi.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(metricas, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Reporte KPI generado: {output_path}")
    return metricas


if __name__ == "__main__":
    generar_reporte_metricas()
