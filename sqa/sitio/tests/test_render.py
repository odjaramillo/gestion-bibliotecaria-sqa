"""Tests de render del sitio de documentos.

Invariantes: el sitio es self-contained (sin dependencias externas: sin CDN,
sin fuentes remotas, sin scripts cargados por red — el unico script permitido
es el conmutador de tema inline), el indice lista todo el manifiesto, y generar
los documentos NO toca el dashboard (site/index.html) — un unico artefacto de
Pages, dos generadores.
"""

import re

import pytest
from contexto_sitio import RAIZ_REPO

import generar_docs as gd

# Referencias a recursos externos: <script src=...>, <link ... href="http...">,
# @import de una URL, url(http...) en CSS. Cualquiera romperia la invariante.
RE_SCRIPT_EXTERNO = re.compile(r"<script[^>]+src=", re.IGNORECASE)
RE_LINK_EXTERNO = re.compile(r'<link[^>]+href="https?://', re.IGNORECASE)
RE_IMPORT_EXTERNO = re.compile(r'@import\s+(?:url\()?["\']?https?://', re.IGNORECASE)
RE_CSS_URL_EXTERNA = re.compile(r'url\(\s*["\']?https?://', re.IGNORECASE)


@pytest.fixture(scope="module")
def sitio(tmp_path_factory):
    """Genera el sitio completo en un directorio temporal, una sola vez."""
    raiz = tmp_path_factory.mktemp("sitio")
    (raiz / "site").mkdir()
    (raiz / "site" / "index.html").write_text("DASHBOARD SENTINELA", encoding="utf-8")
    gd.generar_docs(output_dir=str(raiz / "site" / "docs"), raiz=RAIZ_REPO)
    return raiz / "site"


def test_generar_docs_no_toca_el_dashboard(sitio):
    dashboard = sitio / "index.html"
    assert dashboard.is_file()
    assert dashboard.read_text(encoding="utf-8") == "DASHBOARD SENTINELA"


def test_se_genera_una_pagina_por_documento_del_manifiesto(sitio):
    faltantes = [d.destino for d in gd.MANIFIESTO if not (sitio / "docs" / d.destino).is_file()]
    assert faltantes == []


def test_se_copian_los_activos_binarios(sitio):
    for activo in gd.ACTIVOS:
        copiado = sitio / "docs" / activo.destino
        assert copiado.is_file()
        assert copiado.stat().st_size > 0


def test_el_indice_lista_todas_las_entradas_del_manifiesto(sitio):
    indice = (sitio / "docs" / "index.html").read_text(encoding="utf-8")
    for doc in gd.MANIFIESTO:
        assert f'href="{doc.destino}"' in indice, f"El indice no enlaza {doc.destino}"
        assert doc.titulo in indice
    for activo in gd.ACTIVOS:
        if activo.en_indice:
            assert f'href="{activo.destino}"' in indice


def test_el_indice_enlaza_el_pdf_de_la_auditoria(sitio):
    indice = (sitio / "docs" / "index.html").read_text(encoding="utf-8")
    assert "assets/2026-06-02_auditoria-estatica-fiabilidad-iso25010.pdf" in indice


def _paginas_html(sitio):
    return sorted((sitio / "docs").glob("*.html"))


def test_ninguna_pagina_carga_script_externo(sitio):
    for pagina in _paginas_html(sitio):
        assert not RE_SCRIPT_EXTERNO.search(pagina.read_text(encoding="utf-8")), pagina.name


def test_ninguna_pagina_referencia_recursos_externos(sitio):
    for pagina in _paginas_html(sitio):
        contenido = pagina.read_text(encoding="utf-8")
        assert not RE_LINK_EXTERNO.search(contenido), f"{pagina.name}: <link> externo"
        assert not RE_IMPORT_EXTERNO.search(contenido), f"{pagina.name}: @import externo"
        assert not RE_CSS_URL_EXTERNA.search(contenido), f"{pagina.name}: url() externa en CSS"


def test_cada_pagina_enlaza_su_fuente_en_el_repositorio(sitio):
    for doc in gd.MANIFIESTO:
        contenido = (sitio / "docs" / doc.destino).read_text(encoding="utf-8")
        assert "Ver fuente en el repositorio" in contenido
        assert doc.url_fuente in contenido


def test_cada_pagina_navega_al_indice_y_al_dashboard(sitio):
    for doc in gd.MANIFIESTO:
        contenido = (sitio / "docs" / doc.destino).read_text(encoding="utf-8")
        assert 'href="index.html"' in contenido
        assert 'href="../index.html"' in contenido


def test_ninguna_pagina_enlaza_un_documento_prohibido_como_pagina_publicada(sitio):
    # Un documento no publicado solo puede aparecer como URL al blob de GitHub,
    # nunca como una pagina local del sitio.
    prohibidos_html = ("ecosistema-estado.html", "enunciado", "readme.html", "referencias/")
    for pagina in _paginas_html(sitio):
        contenido = pagina.read_text(encoding="utf-8").lower()
        for prohibido in prohibidos_html:
            assert f'href="{prohibido}' not in contenido, f"{pagina.name} -> {prohibido}"


def test_las_tablas_hacen_scroll_en_su_propio_contenedor(sitio):
    pacs = (sitio / "docs" / "pacs.html").read_text(encoding="utf-8")
    assert "<table>" in pacs
    assert pacs.count('<div class="tabla-scroll"><table>') == pacs.count("<table>")


def test_el_dashboard_enlaza_los_documentos():
    # El dashboard es la puerta de entrada del sitio: debe llevar a /docs.
    fuente = (RAIZ_REPO / "sqa" / "metricas" / "generar_dashboard.py").read_text(encoding="utf-8")
    assert 'href="docs/index.html"' in fuente
