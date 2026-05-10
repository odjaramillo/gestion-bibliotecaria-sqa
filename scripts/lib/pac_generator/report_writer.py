"""ReportWriter: Escribe el reporte JSON wf_pac_summary.json."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


class ReportWriter:
    """Genera el resumen JSON del workflow wf_pac_generator."""

    def __init__(self, report_dir: Path | str) -> None:
        self.report_dir = Path(report_dir)

    def write_summary(
        self,
        pac_path: Path,
        status: str,
        sections_total: int,
        sections_auto: int,
        sections_manual: int,
        sections_completed: int,
        issues: list[str],
    ) -> Path:
        """Escribe el archivo de resumen del PAC.

        Args:
            pac_path: Ruta al archivo PAC generado.
            status: Estado general (EXITOSO, PARCIAL, FALLIDO).
            sections_total: Total de secciones.
            sections_auto: Secciones automáticas.
            sections_manual: Secciones manuales.
            sections_completed: Secciones completadas.
            issues: Lista de problemas encontrados.

        Returns:
            Ruta al archivo JSON escrito.
        """
        self.report_dir.mkdir(parents=True, exist_ok=True)

        now = datetime.now()
        filename = f"{now.strftime('%Y%m%d_%H%M%S')}_wf_pac_summary.json"
        file_path = self.report_dir / filename

        cobertura = 0.0
        if sections_total > 0:
            cobertura = sections_completed / sections_total

        payload = {
            "workflow": "wf_pac_generator",
            "fecha_ejecucion": now.isoformat(),
            "estado": status,
            "archivo_pac": str(pac_path),
            "resumen": {
                "total_secciones": sections_total,
                "secciones_auto": sections_auto,
                "secciones_manual": sections_manual,
                "secciones_completadas": sections_completed,
                "secciones_pendientes": sections_total - sections_completed,
            },
            "metricas": {
                "cobertura_secciones": f"{cobertura:.1%}",
            },
            "issues": issues,
        }

        file_path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return file_path
