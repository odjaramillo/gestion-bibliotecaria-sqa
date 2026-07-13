"""Bootstrap de importacion para la suite del generador del sitio.

Inserta ``sqa/sitio`` en ``sys.path`` para poder importar ``generar_docs`` igual
que en runtime, cuando el script se ejecuta como ``python sqa/sitio/generar_docs.py``
(el directorio del script queda en el path).

Deliberadamente NO es un ``conftest.py``: pytest importa cada conftest sin
paquete como el modulo de nivel superior ``conftest``, y ``sqa/metricas/tests``
ya publica el suyo (del que sus tests importan ``FIXTURES_DIR``). Un segundo
``conftest.py`` lo pisaria y romperia esa suite al correr ambas juntas.
"""

import sys
from pathlib import Path

SITIO_DIR = Path(__file__).resolve().parent.parent
if str(SITIO_DIR) not in sys.path:
    sys.path.insert(0, str(SITIO_DIR))

RAIZ_REPO = SITIO_DIR.parent.parent
