"""Tests de navegacion del sitio de documentos (TOC, pager, tema dual).

Invariantes nuevas: los documentos largos llevan una tabla de contenidos
plegada cuyas anclas usan los ids del slugger de GitHub (no se re-sluggea);
cada documento pagina en el orden del MANIFIESTO; el indice muestra el conteo
de cada seccion; y el CSS declara la paleta clara sin perder la oscura.
"""

import re

import pytest
from contexto_sitio import RAIZ_REPO

import generar_docs as gd


@pytest.fixture(scope="module")
def docs(tmp_path_factory):
    """Genera el sitio de documentos en un directorio temporal, una sola vez."""
    raiz = tmp_path_factory.mktemp("sitio_nav")
    gd.generar_docs(output_dir=str(raiz / "docs"), raiz=RAIZ_REPO)
    return raiz / "docs"


def _leer(docs, nombre):
    return (docs / nombre).read_text(encoding="utf-8")


# --- tema dual --------------------------------------------------------------

def test_css_declara_esquema_dual():
    assert "color-scheme: light dark" in gd.CSS
    assert "@media (prefers-color-scheme: light)" in gd.CSS


def test_css_tiene_focus_visible():
    assert ":focus-visible" in gd.CSS


def test_css_permite_forzar_tema_en_ambos_sentidos():
    # El override de data-theme debe ganar a la media query en ambos sentidos.
    assert ':root[data-theme="light"]' in gd.CSS
    assert ':root[data-theme="dark"]' in gd.CSS
    # La direccion "sistema claro, usuario fuerza oscuro" depende del guard
    # :not() DENTRO de la media query: sin el, la paleta clara del sistema
    # pisaria el oscuro forzado. Se asserta el guard, no solo el selector.
    inicio = gd.CSS.index("@media (prefers-color-scheme: light)")
    fin = gd.CSS.index(':root[data-theme="light"]')
    bloque_media = gd.CSS[inicio:fin]
    assert ':not([data-theme="dark"])' in bloque_media


def test_css_respeta_reduced_motion():
    assert "prefers-reduced-motion" in gd.CSS


def test_todas_las_paginas_llevan_conmutador_de_tema(docs):
    nombres = [d.destino for d in gd.MANIFIESTO] + ["index.html"]
    for nombre in nombres:
        contenido = _leer(docs, nombre)
        assert 'class="theme-toggle"' in contenido, nombre
        assert "localStorage" in contenido, nombre
        assert "<script src=" not in contenido, nombre


# --- tabla de contenidos ------------------------------------------------------

def test_documento_largo_lleva_toc_plegado(docs):
    pacs = _leer(docs, "pacs.html")
    assert '<details class="toc">' in pacs
    assert "Contenido del documento" in pacs


def test_documento_corto_no_lleva_toc(docs):
    # casos-diferidos-fiabilidad.md tiene menos de 4 h2: no amerita TOC.
    corto = _leer(docs, "casos-diferidos-fiabilidad.html")
    assert '<details class="toc">' not in corto


def test_toc_usa_los_ids_del_slugger_github(docs):
    # "## Histórico de Revisiones" -> id "histórico-de-revisiones" (acentos
    # conservados). El TOC debe reutilizar ese id, no re-sluggear.
    pacs = _leer(docs, "pacs.html")
    toc = re.search(r'<details class="toc">.*?</details>', pacs, re.S)
    assert toc is not None
    assert 'href="#histórico-de-revisiones"' in toc.group(0)


def test_todas_las_anclas_del_toc_tienen_destino(docs):
    for doc in gd.MANIFIESTO:
        contenido = _leer(docs, doc.destino)
        toc = re.search(r'<details class="toc">.*?</details>', contenido, re.S)
        if toc is None:
            continue
        for ancla in re.findall(r'href="#([^"]+)"', toc.group(0)):
            assert f'id="{ancla}"' in contenido, (
                f"{doc.destino}: el ancla #{ancla} del TOC no tiene destino"
            )


def test_toc_sintetico_anida_h3_bajo_su_h2():
    texto = (
        "## Sección 1\n\n### Detalle Añadido\n\ntexto\n\n"
        "## Sección 2\n\n## Sección 3\n\n## Sección 4\n"
    )
    _, toc = gd._render_con_toc(texto, "sqa/PACS.md")
    assert 'href="#sección-1"' in toc
    assert 'href="#detalle-añadido"' in toc


def test_toc_sintetico_bajo_el_umbral_no_se_emite():
    texto = "## Uno\n\n## Dos\n\n## Tres\n"
    _, toc = gd._render_con_toc(texto, "sqa/PACS.md")
    assert toc == ""


# --- pager anterior / siguiente ----------------------------------------------

def test_pager_primer_documento_solo_tiene_siguiente(docs):
    primero, segundo = gd.MANIFIESTO[0], gd.MANIFIESTO[1]
    contenido = _leer(docs, primero.destino)
    assert 'class="pager-prev"' not in contenido
    assert f'<a class="pager-next" href="{segundo.destino}"' in contenido


def test_pager_ultimo_documento_solo_tiene_anterior(docs):
    ultimo, penultimo = gd.MANIFIESTO[-1], gd.MANIFIESTO[-2]
    contenido = _leer(docs, ultimo.destino)
    assert 'class="pager-next"' not in contenido
    assert f'<a class="pager-prev" href="{penultimo.destino}"' in contenido


def test_pager_documento_intermedio_enlaza_ambos_vecinos(docs):
    idx = 3
    doc = gd.MANIFIESTO[idx]
    contenido = _leer(docs, doc.destino)
    assert f'<a class="pager-prev" href="{gd.MANIFIESTO[idx - 1].destino}"' in contenido
    assert f'<a class="pager-next" href="{gd.MANIFIESTO[idx + 1].destino}"' in contenido
    assert "Anterior" in contenido
    assert "Siguiente" in contenido
    assert gd.MANIFIESTO[idx + 1].titulo in contenido


# --- volver arriba -------------------------------------------------------------

def test_documento_tiene_volver_arriba(docs):
    contenido = _leer(docs, "pacs.html")
    assert 'id="top"' in contenido
    assert 'href="#top"' in contenido
    assert "Volver arriba" in contenido


# --- conteos en el indice -------------------------------------------------------

def test_indice_muestra_conteo_por_seccion(docs):
    indice = _leer(docs, "index.html")
    entregables = (
        sum(d.seccion == "entregable" for d in gd.MANIFIESTO)
        + sum(a.en_indice for a in gd.ACTIVOS)
    )
    anexos = sum(d.seccion == "anexo" for d in gd.MANIFIESTO)
    assert f'<span class="sec-count">{entregables}</span>' in indice
    assert f'<span class="sec-count">{anexos}</span>' in indice
