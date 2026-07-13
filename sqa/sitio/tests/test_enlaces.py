"""Tests de reescritura de enlaces.

Un documento publicado no puede tener enlaces rotos: los que apuntan a otro
documento publicado se resuelven local (slug), y los que apuntan a algo que NO
se publica (codigo, workflows, PDFs de documentacion) se resuelven al blob de
GitHub en ``main``. Nada queda en 404.
"""

import contexto_sitio  # noqa: F401  (bootstrap de sys.path para generar_docs)
import generar_docs as gd

BLOB = gd.BLOB_BASE


def test_enlace_a_documento_publicado_se_vuelve_slug_local():
    # anexos/herramientas-fase2.md -> ../PACS.md
    assert gd._reescribir_destino("../PACS.md", "sqa/anexos/herramientas-fase2.md") == "pacs.html"


def test_enlace_publicado_en_el_mismo_directorio_se_vuelve_slug_local():
    destino = gd._reescribir_destino(
        "infograma-ecosistema.md", "sqa/anexos/reflexion-critica-ecosistema.md"
    )
    assert destino == "infograma-ecosistema.html"


def test_enlace_publicado_hacia_abajo_se_vuelve_slug_local():
    destino = gd._reescribir_destino("fase1/informe-revision-requisitos-f1.md", "sqa/PACS.md")
    assert destino == "informe-revision-requisitos-f1.html"


def test_enlace_publicado_conserva_el_fragmento():
    destino = gd._reescribir_destino("../PACS.md#63-dispensas-y-desviaciones", "sqa/anexos/x.md")
    assert destino == "pacs.html#63-dispensas-y-desviaciones"


def test_enlace_a_documento_no_publicado_apunta_al_blob_de_github():
    # ECOSISTEMA-ESTADO.md es un documento interno: NO se publica.
    destino = gd._reescribir_destino("../ECOSISTEMA-ESTADO.md", "sqa/anexos/infograma-ecosistema.md")
    assert destino == f"{BLOB}/sqa/ECOSISTEMA-ESTADO.md"


def test_enlace_a_codigo_fuente_apunta_al_blob_de_github():
    destino = gd._reescribir_destino("../src/test/java/com/biblioteca/unit", "sqa/PACS.md")
    assert destino == f"{BLOB}/src/test/java/com/biblioteca/unit"


def test_enlace_a_pdf_de_documentacion_apunta_al_blob_de_github_con_espacios_codificados():
    destino = gd._reescribir_destino("../documentacion/DAS%20Equipo%2058-1%20v1.5.pdf", "sqa/PACS.md")
    assert destino == f"{BLOB}/documentacion/DAS%20Equipo%2058-1%20v1.5.pdf"


def test_enlace_a_markdown_no_publicado_con_espacios_apunta_al_blob():
    destino = gd._reescribir_destino(
        "../fase2/planificacion/Generacion%20de%20Casos%20de%20Pueba.md",
        "sqa/anexos/reflexion-critica-ecosistema.md",
    )
    assert destino == f"{BLOB}/sqa/fase2/planificacion/Generacion%20de%20Casos%20de%20Pueba.md"


def test_url_absoluta_pasa_sin_tocar():
    url = "https://github.com/odjaramillo/gestion-bibliotecaria-sqa/issues/34"
    assert gd._reescribir_destino(url, "sqa/PACS.md") == url


def test_ancla_interna_pasa_sin_tocar():
    assert gd._reescribir_destino("#63-dispensas-y-desviaciones", "sqa/PACS.md") == (
        "#63-dispensas-y-desviaciones"
    )


def test_activo_binario_publicado_resuelve_al_asset_copiado():
    # El PDF de la auditoria se copia al sitio: se enlaza local, no al blob.
    destino = gd._reescribir_destino(
        "fase2/estaticas/2026-06-02_auditoria-estatica-fiabilidad-iso25010.pdf", "sqa/PACS.md"
    )
    assert destino == "assets/2026-06-02_auditoria-estatica-fiabilidad-iso25010.pdf"


def test_imagen_del_infograma_resuelve_al_svg_copiado():
    html_render = gd.renderizar_markdown(
        "![Infograma](infograma-ecosistema.svg)", "sqa/anexos/infograma-ecosistema.md"
    )
    assert 'src="assets/infograma-ecosistema.svg"' in html_render


def test_las_anclas_del_indice_interno_conservan_acentos():
    # Con el slugify por defecto, "#1-propósito" apuntaria a un id "1-proposito".
    html_render = gd.renderizar_markdown("## 1. Propósito y alcance\n", "sqa/PACS.md")
    assert 'id="1-propósito-y-alcance"' in html_render


def test_las_anclas_no_colapsan_los_guiones_que_github_genera():
    # GitHub borra la raya y convierte cada espacio en guion: "wf4--inyección".
    html_render = gd.renderizar_markdown(
        "## 6. Diseño del WF4 — Inyección de Checklists\n",
        "sqa/fase1/Checklists-Inspeccion-Estatica-v1.md",
    )
    assert 'id="6-diseño-del-wf4--inyección-de-checklists"' in html_render
