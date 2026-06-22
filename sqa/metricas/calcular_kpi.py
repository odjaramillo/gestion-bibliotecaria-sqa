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
taxonomía de etiquetas (tipo, area, severidad, fase, iso, rol).
"""

import json
from collections import Counter
from pathlib import Path


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
    }

    output_path = Path("sqa/metricas/reporte_kpi.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(metricas, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Reporte KPI generado: {output_path}")
    return metricas


if __name__ == "__main__":
    generar_reporte_metricas()
