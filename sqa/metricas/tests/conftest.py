"""pytest configuration for the reliability-metrics parser suite.

Inserts the ``sqa/metricas`` directory onto ``sys.path`` so the standalone
parser modules (``parser_jacoco``, ``parser_surefire``) and ``calcular_kpi``
can be imported the same way they are resolved at runtime, when the scripts
are executed as ``python sqa/metricas/calcular_kpi.py`` (script dir on path).
"""

import sys
from pathlib import Path

METRICAS_DIR = Path(__file__).resolve().parent.parent
if str(METRICAS_DIR) not in sys.path:
    sys.path.insert(0, str(METRICAS_DIR))

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
