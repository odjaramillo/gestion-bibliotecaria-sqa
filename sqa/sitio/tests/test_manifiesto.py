"""Tests del manifiesto de publicacion (lista blanca, issue #3).

La publicacion es una decision explicita: lo que entra al sitio esta declarado,
y lo que NO debe publicarse (enunciados del docente, notas internas, material de
referencia con copyright) no puede colarse por un descuido.
"""

import pytest
from contexto_sitio import RAIZ_REPO

import generar_docs as gd

# Documentos que NO deben publicarse jamas. No es un glob invertido: es un
# oraculo independiente del manifiesto, escrito a mano (issue #3).
PROHIBIDOS = (
    "sqa/fase1/Enunciado_Docente_FASE1.md",
    "sqa/fase2/Enunciado_Docente_FINAL.md",
    "sqa/ECOSISTEMA-ESTADO.md",
    "sqa/ECOSISTEMA-SETUP-CHECKLIST.md",
    "sqa/README.md",
    "sqa/REPORTE-ECOSISTEMA.md",
    "sqa/fase2/dinamicas/README.md",
    "sqa/fase2/planificacion/Generacion de Casos de Pueba.md",
    "sqa/metricas/solicitud-firma-lider-metricas.md",
)

PREFIJOS_PROHIBIDOS = ("sqa/referencias/",)

ENTRADAS = (*gd.MANIFIESTO, *gd.ACTIVOS)


@pytest.mark.parametrize("entrada", ENTRADAS, ids=lambda e: e.fuente)
def test_toda_fuente_del_manifiesto_existe(entrada):
    assert (RAIZ_REPO / entrada.fuente).is_file(), f"Fuente ausente: {entrada.fuente}"


@pytest.mark.parametrize("prohibido", PROHIBIDOS)
def test_ningun_documento_prohibido_esta_en_el_manifiesto(prohibido):
    fuentes = {entrada.fuente for entrada in ENTRADAS}
    assert prohibido not in fuentes


def test_ninguna_fuente_proviene_de_un_directorio_prohibido():
    filtradas = [
        entrada.fuente
        for entrada in ENTRADAS
        if entrada.fuente.startswith(PREFIJOS_PROHIBIDOS)
    ]
    assert filtradas == []


def test_los_slugs_son_unicos():
    slugs = [doc.slug for doc in gd.MANIFIESTO]
    assert len(slugs) == len(set(slugs))


def test_las_secciones_son_las_declaradas():
    secciones = {doc.seccion for doc in gd.MANIFIESTO}
    assert secciones == {"entregable", "anexo"}


def test_toda_entrada_tiene_descripcion_para_el_indice():
    assert all(entrada.descripcion.strip() for entrada in ENTRADAS)


def test_validar_manifiesto_falla_fuerte_si_falta_una_fuente(tmp_path):
    # Raiz vacia: ninguna fuente existe -> el build debe romperse, no publicar
    # un sitio incompleto en silencio.
    with pytest.raises(FileNotFoundError):
        gd.validar_manifiesto(raiz=tmp_path)


def test_validar_manifiesto_pasa_contra_el_repositorio_real():
    gd.validar_manifiesto(raiz=RAIZ_REPO)
