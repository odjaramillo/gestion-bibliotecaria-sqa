"""Tests para scripts.sqa_core.pdf_auditoria."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Mockear fitz antes de importar el módulo SQA
if "fitz" not in sys.modules:
    sys.modules["fitz"] = MagicMock()

from scripts.sqa_core.pdf_auditoria import (
    DocumentoAuditoria,
    ExtractorAuditoriaPdf,
    FilaAuditoria,
    _detectar_defecto,
    _normalizar_header,
    _normalizar_texto,
)


class TestNormalizarTexto(unittest.TestCase):
    """Tests para la utilidad de normalización de texto."""

    def test_reemplaza_quiebras_de_linea(self):
        resultado = _normalizar_texto("línea1\nlínea2")
        self.assertEqual(resultado, "línea1 línea2")

    def test_colapsa_espacios_multiples(self):
        resultado = _normalizar_texto("mucho    espacio")
        self.assertEqual(resultado, "mucho espacio")

    def test_reemplaza_caracter_reemplazo(self):
        resultado = _normalizar_texto("texto\ufffdroto")
        self.assertEqual(resultado, "texto roto")

    def test_devuelve_vacio_para_none(self):
        resultado = _normalizar_texto("")
        self.assertEqual(resultado, "")


class TestNormalizarHeader(unittest.TestCase):
    """Tests para normalización de encabezados de tabla."""

    def test_id(self):
        self.assertEqual(_normalizar_header("ID"), "id")

    def test_metrica_con_acento(self):
        self.assertEqual(_normalizar_header("MÉTRICA"), "metrica")

    def test_atributo(self):
        self.assertEqual(_normalizar_header("Atributo"), "metrica")

    def test_criterio_de_verificacion(self):
        self.assertEqual(_normalizar_header("CRITERIO DE VERIFICACIÓN"), "criterio")

    def test_resultado(self):
        self.assertEqual(_normalizar_header("Resultado"), "resultado")

    def test_observacion_sqa(self):
        self.assertEqual(_normalizar_header("OBSERVACIÓN SQA"), "observacion")

    def test_header_desconocido(self):
        self.assertIsNone(_normalizar_header("Foo"))


class TestDetectarDefecto(unittest.TestCase):
    """Tests para la heurística de detección de defectos."""

    def test_falla_es_defecto(self):
        self.assertTrue(_detectar_defecto("FALLA", "obs"))

    def test_no_cumple_es_defecto(self):
        self.assertTrue(_detectar_defecto("NO CUMPLE", "obs"))

    def test_parcial_es_defecto(self):
        self.assertTrue(_detectar_defecto("PARCIAL", "obs"))

    def test_bloqueado_es_defecto(self):
        self.assertTrue(_detectar_defecto("BLOQUEADO", "obs"))

    def test_cumple_no_es_defecto(self):
        self.assertFalse(_detectar_defecto("CUMPLE", ""))

    def test_observacion_con_resultado_raro(self):
        self.assertTrue(_detectar_defecto("AVISO", "algo que observar"))

    def test_cumple_con_observacion_no_es_defecto(self):
        self.assertFalse(_detectar_defecto("CUMPLE", "algo que observar"))


class TestExtractorAuditoriaPdf(unittest.TestCase):
    """Tests para ExtractorAuditoriaPdf usando mocks de PyMuPDF."""

    @patch("scripts.sqa_core.pdf_auditoria.fitz")
    def test_extrae_filas_correctamente(self, mock_fitz):
        extractor = ExtractorAuditoriaPdf()

        mock_doc = MagicMock()
        mock_doc.__len__ = MagicMock(return_value=1)

        mock_page = MagicMock()
        mock_tabla = MagicMock()
        mock_tabla.extract.return_value = [
            ["ID", "MÉTRICA", "CRITERIO", "RESULTADO", "OBSERVACIÓN"],
            [
                "REQ-01",
                "Cobertura",
                ">80%",
                "FALLA",
                "Cobertura en 75%",
            ],
            [
                "REQ-02",
                "Seguridad",
                "JWT",
                "CUMPLE",
                "OK",
            ],
        ]
        mock_tables = MagicMock()
        mock_tables.tables = [mock_tabla]
        mock_page.find_tables.return_value = mock_tables
        mock_doc.__getitem__ = MagicMock(return_value=mock_page)

        mock_fitz.open.return_value.__enter__ = MagicMock(return_value=mock_doc)
        mock_fitz.open.return_value.__exit__ = MagicMock(return_value=False)

        doc = extractor.extraer("/fake/auditoria.pdf")

        self.assertEqual(doc.nombre, "auditoria")
        self.assertEqual(len(doc.filas), 2)
        self.assertEqual(doc.filas[0].id, "REQ-01")
        self.assertTrue(doc.filas[0].es_defecto)
        self.assertFalse(doc.filas[1].es_defecto)

    @patch("scripts.sqa_core.pdf_auditoria.fitz")
    def test_deduplica_ids_repetidos(self, mock_fitz):
        extractor = ExtractorAuditoriaPdf()

        mock_doc = MagicMock()
        mock_doc.__len__ = MagicMock(return_value=1)

        mock_page = MagicMock()
        mock_tabla = MagicMock()
        mock_tabla.extract.return_value = [
            ["ID", "MÉTRICA", "CRITERIO", "RESULTADO", "OBSERVACIÓN"],
            ["REQ-01", "A", "B", "FALLA", "obs1"],
            ["REQ-01", "A", "B", "FALLA", "obs2"],
        ]
        mock_tables = MagicMock()
        mock_tables.tables = [mock_tabla]
        mock_page.find_tables.return_value = mock_tables
        mock_doc.__getitem__ = MagicMock(return_value=mock_page)

        mock_fitz.open.return_value.__enter__ = MagicMock(return_value=mock_doc)
        mock_fitz.open.return_value.__exit__ = MagicMock(return_value=False)

        doc = extractor.extraer("/fake/dup.pdf")
        ids = [f.id for f in doc.filas]
        self.assertEqual(ids, ["REQ-01", "REQ-01-1"])

    @patch("scripts.sqa_core.pdf_auditoria.fitz")
    def test_descarta_tablas_sin_headers_reconocidos(self, mock_fitz):
        extractor = ExtractorAuditoriaPdf()

        mock_doc = MagicMock()
        mock_doc.__len__ = MagicMock(return_value=1)

        mock_page = MagicMock()
        mock_tabla = MagicMock()
        mock_tabla.extract.return_value = [
            ["Foo", "Bar", "Baz"],
            ["1", "2", "3"],
        ]
        mock_tables = MagicMock()
        mock_tables.tables = [mock_tabla]
        mock_page.find_tables.return_value = mock_tables
        mock_doc.__getitem__ = MagicMock(return_value=mock_page)

        mock_fitz.open.return_value.__enter__ = MagicMock(return_value=mock_doc)
        mock_fitz.open.return_value.__exit__ = MagicMock(return_value=False)

        doc = extractor.extraer("/fake/no_tabla.pdf")
        self.assertEqual(len(doc.filas), 0)

    @patch("scripts.sqa_core.pdf_auditoria.fitz")
    def test_fallback_texto_cuando_no_hay_tablas(self, mock_fitz):
        extractor = ExtractorAuditoriaPdf()

        mock_doc = MagicMock()
        mock_doc.__len__ = MagicMock(return_value=1)

        mock_page = MagicMock()
        mock_tables = MagicMock()
        mock_tables.tables = []
        mock_page.find_tables.return_value = mock_tables
        mock_doc.__getitem__ = MagicMock(return_value=mock_page)

        mock_fitz.open.return_value.__enter__ = MagicMock(return_value=mock_doc)
        mock_fitz.open.return_value.__exit__ = MagicMock(return_value=False)

        with patch(
            "scripts.sqa_core.pdf_auditoria.extract_page_texts_from_pdf"
        ) as mock_text:
            mock_text.return_value = {
                1: "REQ-01    Cobertura    >80%    FALLA    Cobertura baja\nOtra línea",
            }
            doc = extractor.extraer("/fake/fallback.pdf")

        self.assertEqual(len(doc.filas), 1)
        self.assertEqual(doc.filas[0].id, "REQ-01")
        self.assertTrue(doc.filas[0].es_defecto)


class TestDocumentoAuditoria(unittest.TestCase):
    """Tests para la dataclass DocumentoAuditoria."""

    def test_filas_con_defecto(self):
        filas = [
            FilaAuditoria("R1", "M1", "C1", "CUMPLE", "OK", 1, False),
            FilaAuditoria("R2", "M2", "C2", "FALLA", "Mal", 1, True),
        ]
        doc = DocumentoAuditoria(nombre="test", pdf_path="/fake.pdf", filas=filas)
        defectos = doc.filas_con_defecto()
        self.assertEqual(len(defectos), 1)
        self.assertEqual(defectos[0].id, "R2")


if __name__ == "__main__":
    unittest.main()
