"""Renderizador de contenido de auditoría a Confluence Storage Format (XHTML)."""
from __future__ import annotations

import logging
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from scripts.sqa_core.pdf_auditoria import DocumentoAuditoria, FilaAuditoria

logger = logging.getLogger("sqa_core.xhtml_confluence")

# Tags permitidos en Confluence Storage Format (subset seguro).
_NS_CONFLUENCE = "http://www.w3.org/1999/xhtml"


def _escapar_texto(texto: str) -> str:
    """Escapa entidades XML básicas y elimina caracteres de control."""
    if not texto:
        return ""
    # Eliminar caracteres de control excepto tab, newline, carriage return
    texto = "".join(
        ch for ch in texto if ord(ch) >= 32 or ch in ("\t", "\n", "\r")
    )
    texto = texto.replace("&", "&amp;")
    texto = texto.replace("<", "&lt;")
    texto = texto.replace(">", "&gt;")
    texto = texto.replace('"', "&quot;")
    return texto


def _elemento(tag: str, texto: str | None = None, atributos: dict[str, str] | None = None) -> ET.Element:
    """Crea un elemento XML con namespace XHTML de Confluence."""
    ns_tag = f"{{{_NS_CONFLUENCE}}}{tag}" if not tag.startswith("{") else tag
    elem = ET.Element(ns_tag, atributos or {})
    if texto is not None:
        elem.text = texto
    return elem


def _subelemento(padre: ET.Element, tag: str, texto: str | None = None, atributos: dict[str, str] | None = None) -> ET.Element:
    """Crea y adjunta un subelemento al padre."""
    elem = _elemento(tag, texto=texto, atributos=atributos)
    padre.append(elem)
    return elem


def _parrafo_con_etiqueta(padre: ET.Element, etiqueta: str, valor: str) -> ET.Element:
    """Crea un <p> con un <strong>etiqueta:</strong> seguido del valor."""
    p = _subelemento(padre, "p")
    strong = _subelemento(p, "strong", f"{etiqueta}:")
    # Añadir espacio y valor como tail del strong
    strong.tail = f" {valor}"
    return p


def _generar_tabla(filas: Iterable[FilaAuditoria]) -> ET.Element:
    """Genera un elemento <table> XHTML con las filas de auditoría."""
    table = _elemento("table")
    thead = _subelemento(table, "thead")
    tr_head = _subelemento(thead, "tr")
    for header in ("ID", "Métrica/Atributo", "Criterio", "Resultado", "Observación"):
        _subelemento(tr_head, "th", header)

    tbody = _subelemento(table, "tbody")
    for fila in filas:
        tr = _subelemento(tbody, "tr")
        # Destacar visualmente filas con defecto
        if fila.es_defecto:
            tr.set("style", "background-color: #ffcccc;")
        _subelemento(tr, "td", fila.id)
        _subelemento(tr, "td", fila.metrica)
        _subelemento(tr, "td", fila.criterio)
        _subelemento(tr, "td", fila.resultado)
        _subelemento(tr, "td", fila.observacion)
    return table


def _generar_lista_defectos(filas: Iterable[FilaAuditoria]) -> ET.Element | None:
    """Genera una lista <ul> con los defectos encontrados, o None si no hay."""
    defectos = [f for f in filas if f.es_defecto]
    if not defectos:
        return None
    ul = _elemento("ul")
    for fila in defectos:
        texto = f"[{fila.id}] {fila.metrica}: {fila.resultado} - {fila.observacion}"
        _subelemento(ul, "li", texto)
    return ul


@dataclass
class MetadataPagina:
    """Metadatos opcionales para inyectar en el XHTML de Confluence."""

    nombre_artefacto: str = ""
    estandar_iso: str = ""
    checklist_referencia: str = ""


class RenderizadorXhtmlConfluence:
    """Convierte un :class:`DocumentoAuditoria` a XHTML válido para Confluence.

    Responsabilidades:
      - Generar tags ``h1``, ``h2``, ``p``, ``ul``, ``li``, ``table``
        válidos según el Storage Format de Confluence.
      - Escapar todo texto para evitar XHTML mal formado.
      - Inyectar metadatos opcionales (artefacto, ISO, checklist).
      - Incluir lista de defectos y tabla completa.
    """

    def renderizar(
        self,
        documento: DocumentoAuditoria,
        metadata: MetadataPagina | None = None,
        tickets: dict[str, str] | None = None,
    ) -> str:
        """Renderiza el documento como string XHTML.

        Args:
            documento: Estructura extraída del PDF de auditoría.
            metadata: Metadatos opcionales para encabezados.
            tickets: Mapa ``{fila_id: issue_key}`` para enlazar defectos con Jira.

        Returns:
            String XHTML válido (self-closing tags, namespace implícito).
        """
        metadata = metadata or MetadataPagina()
        tickets = tickets or {}

        root = _elemento("div")

        # Título principal
        _subelemento(root, "h1", f"Auditoría: {documento.nombre}")

        # Metadatos
        if metadata.nombre_artefacto:
            _parrafo_con_etiqueta(root, "Artefacto", metadata.nombre_artefacto)
        if metadata.estandar_iso:
            _parrafo_con_etiqueta(root, "Estándar ISO", metadata.estandar_iso)
        if metadata.checklist_referencia:
            _parrafo_con_etiqueta(root, "Checklist", metadata.checklist_referencia)

        # Resumen
        total = len(documento.filas)
        defectos = len(documento.filas_con_defecto())
        _subelemento(
            root,
            "p",
            f"Total de ítems auditados: {total} | Defectos detectados: {defectos}",
        )

        # Sección de defectos
        if defectos:
            _subelemento(root, "h2", "Defectos Detectados")
            lista_defectos = _generar_lista_defectos(documento.filas)
            if lista_defectos is not None:
                root.append(lista_defectos)
            # Enlaces a tickets de Jira si existen
            if tickets:
                _subelemento(root, "h2", "Tickets de Seguimiento (Jira)")
                ul_tickets = _subelemento(root, "ul")
                for fila in documento.filas_con_defecto():
                    key = tickets.get(fila.id)
                    if key:
                        li = _subelemento(ul_tickets, "li")
                        li.text = f"[{fila.id}] "
                        a = _subelemento(
                            li,
                            "a",
                            key,
                            {"href": f"https://jira.example.com/browse/{key}"},
                        )
        else:
            _subelemento(root, "p", "✅ No se detectaron defectos en esta auditoría.")

        # Tabla completa
        _subelemento(root, "h2", "Tabla de Auditoría Completa")
        tabla = _generar_tabla(documento.filas)
        root.append(tabla)

        # Convertir a string XML
        ET.register_namespace("", _NS_CONFLUENCE)
        xhtml_str = ET.tostring(root, encoding="unicode", method="xml")
        # Asegurar que el texto escapado no se vuelva a escapar por ElementTree
        # (ET ya escapa textos, pero los <strong> inyectados manualmente en texto
        #  deben ser reemplazados por tags reales si se quiere formato rico).
        xhtml_str = self._restaurar_tags_html_simples(xhtml_str)
        return xhtml_str

    @staticmethod
    def _restaurar_tags_html_simples(xhtml: str) -> str:
        """Reemplaza entidades de tags HTML simples inyectadas como texto.

        Confluence Storage permite un subconjunto de tags HTML básicos;
        esta función restaura ``<strong>`` y ``<em>`` que fueron escritos
        literalmente como texto para evitar que ElementTree los escape.
        """
        # Reemplazar escapados por tags reales (solo etiquetas seguras)
        reemplazos = {
            "&lt;strong&gt;": "<strong>",
            "&lt;/strong&gt;": "</strong>",
            "&lt;em&gt;": "<em>",
            "&lt;/em&gt;": "</em>",
        }
        for viejo, nuevo in reemplazos.items():
            xhtml = xhtml.replace(viejo, nuevo)
        return xhtml

    @staticmethod
    def validar_xhtml(xhtml: str) -> bool:
        """Valida que el string sea XML bien formado (parser estricto).

        Args:
            xhtml: String XHTML a validar.

        Returns:
            ``True`` si es XML parseable, ``False`` en caso contrario.
        """
        try:
            ET.fromstring(xhtml)
            return True
        except ET.ParseError as exc:
            logger.warning("XHTML inválido: %s", exc)
            return False
