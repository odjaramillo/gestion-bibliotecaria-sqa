"""Tests para scripts.sqa_core.xhtml_confluence."""
from __future__ import annotations

import unittest
import xml.etree.ElementTree as ET

from scripts.sqa_core.pdf_auditoria import DocumentoAuditoria, FilaAuditoria
from scripts.sqa_core.xhtml_confluence import (
    MetadataPagina,
    RenderizadorXhtmlConfluence,
    _escapar_texto,
    _generar_lista_defectos,
    _generar_tabla,
)


class TestEscaparTexto(unittest.TestCase):
    """Tests para la función de escape de texto XML."""

    def test_escapa_ampersand(self):
        self.assertEqual(_escapar_texto("A & B"), "A &amp; B")

    def test_escapa_menor_mayor(self):
        self.assertEqual(_escapar_texto("<tag>"), "&lt;tag&gt;")

    def test_escapa_comillas(self):
        self.assertEqual(_escapar_texto('"texto"'), "&quot;texto&quot;")

    def test_elimina_caracteres_control(self):
        self.assertEqual(_escapar_texto("texto\x00\x01"), "texto")

    def test_devuelve_vacio_para_none(self):
        self.assertEqual(_escapar_texto(""), "")


class TestGenerarTabla(unittest.TestCase):
    """Tests para la generación de tablas XHTML."""

    def test_genera_tabla_con_headers_correctos(self):
        filas = [
            FilaAuditoria("R1", "M1", "C1", "CUMPLE", "OK", 1, False),
        ]
        tabla = _generar_tabla(filas)
        headers = [th.text for th in tabla.findall(".//{http://www.w3.org/1999/xhtml}th")]
        self.assertEqual(
            headers,
            ["ID", "Métrica/Atributo", "Criterio", "Resultado", "Observación"],
        )

    def test_fila_defecto_tiene_estilo(self):
        filas = [
            FilaAuditoria("R1", "M1", "C1", "FALLA", "Mal", 1, True),
        ]
        tabla = _generar_tabla(filas)
        ns = "{http://www.w3.org/1999/xhtml}"
        rows = tabla.findall(f".//{ns}tr")
        self.assertEqual(len(rows), 2)  # header + data
        tr = rows[1]
        self.assertEqual(tr.get("style"), "background-color: #ffcccc;")

    def test_fila_sin_defecto_sin_estilo(self):
        filas = [
            FilaAuditoria("R1", "M1", "C1", "CUMPLE", "OK", 1, False),
        ]
        tabla = _generar_tabla(filas)
        ns = "{http://www.w3.org/1999/xhtml}"
        rows = tabla.findall(f".//{ns}tr")
        self.assertEqual(len(rows), 2)
        tr = rows[1]
        self.assertIsNone(tr.get("style"))


class TestGenerarListaDefectos(unittest.TestCase):
    """Tests para la generación de listas de defectos."""

    def test_devuelve_none_si_no_hay_defectos(self):
        filas = [
            FilaAuditoria("R1", "M1", "C1", "CUMPLE", "OK", 1, False),
        ]
        self.assertIsNone(_generar_lista_defectos(filas))

    def test_genera_lista_con_defectos(self):
        filas = [
            FilaAuditoria("R1", "M1", "C1", "FALLA", "Mal", 1, True),
        ]
        ul = _generar_lista_defectos(filas)
        self.assertIsNotNone(ul)
        li = ul.find("{http://www.w3.org/1999/xhtml}li")
        self.assertIsNotNone(li)
        self.assertIn("[R1]", li.text or "")


class TestRenderizadorXhtmlConfluence(unittest.TestCase):
    """Tests de integración para el renderizador completo."""

    def setUp(self):
        self.renderer = RenderizadorXhtmlConfluence()

    def test_renderiza_xhtml_valido(self):
        doc = DocumentoAuditoria(
            nombre="Test",
            pdf_path="/fake.pdf",
            filas=[
                FilaAuditoria("R1", "M1", "C1", "CUMPLE", "OK", 1, False),
            ],
        )
        xhtml = self.renderer.renderizar(doc)
        self.assertTrue(self.renderer.validar_xhtml(xhtml))

    def test_renderiza_con_defectos(self):
        doc = DocumentoAuditoria(
            nombre="Test",
            pdf_path="/fake.pdf",
            filas=[
                FilaAuditoria("R1", "M1", "C1", "FALLA", "Mal", 1, True),
            ],
        )
        xhtml = self.renderer.renderizar(doc)
        self.assertIn("Defectos Detectados", xhtml)
        self.assertIn("background-color: #ffcccc;", xhtml)

    def test_renderiza_sin_defectos(self):
        doc = DocumentoAuditoria(
            nombre="Test",
            pdf_path="/fake.pdf",
            filas=[
                FilaAuditoria("R1", "M1", "C1", "CUMPLE", "OK", 1, False),
            ],
        )
        xhtml = self.renderer.renderizar(doc)
        self.assertIn("No se detectaron defectos", xhtml)

    def test_renderiza_con_metadata(self):
        doc = DocumentoAuditoria(
            nombre="Test",
            pdf_path="/fake.pdf",
            filas=[],
        )
        meta = MetadataPagina(
            nombre_artefacto="DAS v1.5",
            estandar_iso="ISO 42010",
            checklist_referencia="CHK-01",
        )
        xhtml = self.renderer.renderizar(doc, metadata=meta)
        self.assertIn("DAS v1.5", xhtml)
        self.assertIn("ISO 42010", xhtml)
        self.assertIn("CHK-01", xhtml)

    def test_renderiza_con_tickets_jira(self):
        doc = DocumentoAuditoria(
            nombre="Test",
            pdf_path="/fake.pdf",
            filas=[
                FilaAuditoria("R1", "M1", "C1", "FALLA", "Mal", 1, True),
            ],
        )
        tickets = {"R1": "SQA-101"}
        xhtml = self.renderer.renderizar(doc, tickets=tickets)
        self.assertIn("SQA-101", xhtml)
        self.assertIn("https://jira.example.com/browse/SQA-101", xhtml)

    def test_tabla_completa_presente(self):
        doc = DocumentoAuditoria(
            nombre="Test",
            pdf_path="/fake.pdf",
            filas=[
                FilaAuditoria("R1", "M1", "C1", "CUMPLE", "OK", 1, False),
                FilaAuditoria("R2", "M2", "C2", "FALLA", "Mal", 1, True),
            ],
        )
        xhtml = self.renderer.renderizar(doc)
        # Debe contener la tabla completa
        self.assertIn("Tabla de Auditoría Completa", xhtml)
        # Ambas filas deben estar
        self.assertIn("R1", xhtml)
        self.assertIn("R2", xhtml)


class TestValidarXhtml(unittest.TestCase):
    """Tests para la utilidad de validación XHTML."""

    def test_xhtml_valido_devuelve_true(self):
        self.assertTrue(RenderizadorXhtmlConfluence.validar_xhtml("<div><p>Hola</p></div>"))

    def test_xhtml_invalido_devuelve_false(self):
        self.assertFalse(
            RenderizadorXhtmlConfluence.validar_xhtml("<div><p>Hola</div>")
        )


if __name__ == "__main__":
    unittest.main()
