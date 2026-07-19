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
import math
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
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
        "umbral": {"valor": 50, "comparador": ">=", "ratificado": True},
    },
    "M-03": {
        "nombre": "Tasa de Pruebas que Pasan",
        "unidad": "%",
        "umbral": {"valor": 100, "comparador": ">=", "ratificado": True},
    },
    "M-04": {
        "nombre": "Cobertura de Instrucciones",
        "unidad": "%",
        # Meta práctica F2: >=30%. Aspiracional ISO (fondo, no se muestra): 60%.
        "umbral": {"valor": 30, "comparador": ">=", "ratificado": True},
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


# --- Métricas de PROCESO (derivadas del export de issues, sin artefactos) ----
# Miden cómo fluye el trabajo del equipo, no el producto. Se calculan sólo con
# createdAt / closedAt / state, que ya vienen en el export de gh.

def _parse_iso(ts):
    """Parsea un timestamp ISO-8601 UTC de GitHub y lo normaliza a UTC.

    Acepta el formato canónico ``...Z`` (segundos) y tolera variantes ISO
    (fracciones de segundo, offset ``+00:00``) para que una deriva menor del
    formato del export no descarte issues de forma silenciosa. None si es
    genuinamente inválido.
    """
    if not isinstance(ts, str):
        return None
    try:
        return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        pass
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return None
    return dt.astimezone(timezone.utc) if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def _percentil(ordenados, p):
    """Percentil ``p`` (0-100) por interpolación lineal sobre una lista ordenada."""
    if not ordenados:
        return None
    if len(ordenados) == 1:
        return ordenados[0]
    k = (len(ordenados) - 1) * p / 100
    inf, sup = math.floor(k), math.ceil(k)
    if inf == sup:
        return ordenados[int(k)]
    return ordenados[inf] * (sup - k) + ordenados[sup] * (k - inf)


def lead_time_stats(issues) -> dict:
    """Lead time (apertura → cierre) en días para los issues cerrados.

    SÓLO se mide lead time. El export de GitHub no trae una señal de "inicio de
    trabajo", así que el cycle time no es derivable de forma fiable y NO se
    reporta (honestidad de la métrica: no se fabrica un valor no medible).
    """
    dias = []
    for it in issues:
        if it.get("state") != "CLOSED":
            continue
        creado = _parse_iso(it.get("createdAt"))
        cerrado = _parse_iso(it.get("closedAt"))
        if creado and cerrado and cerrado >= creado:
            dias.append((cerrado - creado).total_seconds() / 86400)
    if not dias:
        return {"n": 0, "mediana_dias": None, "promedio_dias": None, "p90_dias": None}
    dias.sort()
    return {
        "n": len(dias),
        "mediana_dias": round(_percentil(dias, 50), 1),
        "promedio_dias": round(sum(dias) / len(dias), 1),
        "p90_dias": round(_percentil(dias, 90), 1),
    }


def _semana_iso(dt: datetime) -> str:
    """Etiqueta de semana ISO ordenable, p.ej. ``2026-W23``."""
    anio, semana, _ = dt.isocalendar()
    return f"{anio}-W{semana:02d}"


def _lunes_iso(dt: datetime) -> datetime:
    """Lunes (inicio) de la semana ISO que contiene ``dt``."""
    return dt - timedelta(days=dt.isoweekday() - 1)


def tendencia_semanal(issues) -> list:
    """Aperturas vs cierres de issues por semana ISO, orden cronológico.

    Emite un rango CONTIGUO de semanas entre la primera y la última actividad:
    las semanas sin movimiento se incluyen en cero para no dar una falsa
    continuidad en el gráfico (dos semanas no consecutivas lado a lado).
    """
    aperturas, cierres, fechas = Counter(), Counter(), []
    for it in issues:
        creado = _parse_iso(it.get("createdAt"))
        if creado:
            aperturas[_semana_iso(creado)] += 1
            fechas.append(creado)
        if it.get("state") == "CLOSED":
            cerrado = _parse_iso(it.get("closedAt"))
            if cerrado:
                cierres[_semana_iso(cerrado)] += 1
                fechas.append(cerrado)
    if not fechas:
        return []
    cursor, fin = _lunes_iso(min(fechas)), _lunes_iso(max(fechas))
    semanas = []
    while cursor <= fin:
        etiqueta = _semana_iso(cursor)
        semanas.append({
            "semana": etiqueta,
            "abiertos": aperturas.get(etiqueta, 0),
            "cerrados": cierres.get(etiqueta, 0),
        })
        cursor += timedelta(days=7)
    return semanas


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
        # Bloque aditivo de métricas de PROCESO (flujo de trabajo del equipo).
        "proceso": {
            "lead_time": lead_time_stats(data),
            "tendencia": tendencia_semanal(data),
        },
    }

    output_path = Path("sqa/metricas/reporte_kpi.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(metricas, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Reporte KPI generado: {output_path}")
    return metricas


if __name__ == "__main__":
    generar_reporte_metricas()
