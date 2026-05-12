"""Extracción y normalización de tablas de auditoría desde PDFs."""
from __future__ import annotations

import logging
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

import fitz

from scripts.sqa_core.pdf_text import extract_page_texts_from_pdf

logger = logging.getLogger("sqa_core.pdf_auditoria")

# Palabras clave que indican un resultado con defecto.
_PALABRAS_DEFECTO = {"FALLA", "NO CUMPLE", "PARCIAL", "BLOQUEADO", "FAIL"}

# Mapeo de encabezados normalizados -> nombre canónico.
_MAPA_HEADERS = {
    "ID": "id",
    "METRICA": "metrica",
    "ATRIBUTO": "metrica",
    "CRITERIO DE VERIFICACION": "criterio",
    "CRITERIO DE INTEGRACION": "criterio",
    "RESULTADO": "resultado",
    "OBSERVACION SQA": "observacion",
    "ANALISIS SQA": "observacion",
}

# Encabezados esperados (canónicos) en orden.
_HEADERS_CANONICOS = ["id", "metrica", "criterio", "resultado", "observacion"]


def _normalizar_texto(texto: str) -> str:
    """Limpia texto extraído: quiebras de línea, espacios múltiples, reemplaza �."""
    if not texto:
        return ""
    texto = texto.replace("\n", " ")
    texto = re.sub(r"\s+", " ", texto)
    texto = texto.strip()
    # Reemplazar el carácter de reemplazo Unicode (sustitución) por un espacio
    texto = texto.replace("\ufffd", " ")
    return texto


def _normalizar_header(header: str) -> str | None:
    """Normaliza un encabezado de tabla a su nombre canónico o None."""
    limpio = _normalizar_texto(header).upper()
    limpio = (
        unicodedata.normalize("NFKD", limpio)
        .encode("ASCII", "ignore")
        .decode("ASCII")
    )
    return _MAPA_HEADERS.get(limpio)


def _detectar_defecto(resultado: str, observacion: str) -> bool:
    """Determina si una fila representa un defecto."""
    resultado_upper = resultado.upper()
    for palabra in _PALABRAS_DEFECTO:
        if palabra in resultado_upper:
            return True
    # Si hay observación sustantiva y el resultado no es "CUMPLE" simple,
    # lo tratamos como observación relevante.
    if observacion and resultado_upper not in {"CUMPLE", "APROBADO", "OK"}:
        return True
    return False


@dataclass
class FilaAuditoria:
    """Fila individual de una tabla de auditoría."""

    id: str
    metrica: str
    criterio: str
    resultado: str
    observacion: str
    pagina: int = 0
    es_defecto: bool = False


@dataclass
class DocumentoAuditoria:
    """Documento completo extraído de un PDF de auditoría."""

    nombre: str
    pdf_path: str
    filas: list[FilaAuditoria] = field(default_factory=list)

    def filas_con_defecto(self) -> list[FilaAuditoria]:
        """Devuelve únicamente las filas marcadas como defecto."""
        return [f for f in self.filas if f.es_defecto]


class ExtractorAuditoriaPdf:
    """Extrae tablas de auditoría de archivos PDF usando PyMuPDF.

    Responsabilidades:
      - Abrir el PDF y buscar tablas con ``page.find_tables()``.
      - Normalizar encabezados ignorando acentos/mayúsculas.
      - Convertir filas a :class:`FilaAuditoria` detectando defectos.
      - Si no encuentra tablas, hacer fallback a extracción de texto por página.
    """

    def __init__(self) -> None:
        self._seen_ids: dict[str, int] = {}

    def extraer(self, pdf_path: str | Path) -> DocumentoAuditoria:
        """Extrae todas las tablas de auditoría del PDF indicado.

        Args:
            pdf_path: Ruta al archivo PDF.

        Returns:
            :class:`DocumentoAuditoria` con las filas extraídas y normalizadas.
        """
        path = Path(pdf_path)
        logger.info("Extrayendo auditoría de PDF: %s", path)
        doc = DocumentoAuditoria(nombre=path.stem, pdf_path=str(path))

        with fitz.open(path) as pdf_doc:
            for page_num in range(len(pdf_doc)):
                page = pdf_doc[page_num]
                page_idx = page_num + 1
                tablas = page.find_tables()
                if tablas.tables:
                    for tabla in tablas.tables:
                        filas = self._procesar_tabla(tabla, page_idx)
                        doc.filas.extend(filas)
                else:
                    logger.debug(
                        "Página %s sin tablas detectadas en %s", page_idx, path.name
                    )

        if not doc.filas:
            logger.warning(
                "No se encontraron tablas en %s; intentando fallback de texto.", path
            )
            doc.filas = self._fallback_texto(path)

        logger.info(
            "Extracción completada: %s filas (%s defectos) en %s",
            len(doc.filas),
            len(doc.filas_con_defecto()),
            path.name,
        )
        return doc

    def _procesar_tabla(
        self, tabla, pagina: int
    ) -> list[FilaAuditoria]:
        """Procesa una tabla de PyMuPDF y devuelve filas de auditoría."""
        filas_extraidas: list[FilaAuditoria] = []
        raw_rows = tabla.extract()
        if not raw_rows:
            return filas_extraidas

        # Primera fila como encabezados
        headers_raw = raw_rows[0]
        headers = [_normalizar_header(str(h)) if h else None for h in headers_raw]

        # Verificar que tengamos al menos los headers mínimos
        if not any(h in _HEADERS_CANONICOS for h in headers if h):
            logger.debug("Tabla descartada: encabezados no reconocidos %s", headers_raw)
            return filas_extraidas

        for raw in raw_rows[1:]:
            fila_dict: dict[str, str] = {}
            for idx, val in enumerate(raw):
                if idx < len(headers) and headers[idx]:
                    fila_dict[headers[idx]] = _normalizar_texto(str(val) if val is not None else "")

            id_val = fila_dict.get("id", "")
            if not id_val:
                continue

            # Deduplicar IDs repetidos agregando sufijo
            id_unico = self._unicificar_id(id_val)

            resultado = fila_dict.get("resultado", "")
            observacion = fila_dict.get("observacion", "")
            es_defecto = _detectar_defecto(resultado, observacion)

            fila = FilaAuditoria(
                id=id_unico,
                metrica=fila_dict.get("metrica", ""),
                criterio=fila_dict.get("criterio", ""),
                resultado=resultado,
                observacion=observacion,
                pagina=pagina,
                es_defecto=es_defecto,
            )
            filas_extraidas.append(fila)

        return filas_extraidas

    def _unicificar_id(self, id_val: str) -> str:
        """Asegura IDs únicos agregando sufijo numérico en caso de duplicado."""
        if id_val not in self._seen_ids:
            self._seen_ids[id_val] = 0
            return id_val
        self._seen_ids[id_val] += 1
        return f"{id_val}-{self._seen_ids[id_val]}"

    def _fallback_texto(self, path: Path) -> list[FilaAuditoria]:
        """Fallback: extrae texto plano por página y busca filas de auditoría.

        Este método no garantiza la misma calidad que ``find_tables``,
        pero evita devolver un documento vacío cuando las tablas no son
        detectadas por PyMuPDF.
        """
        filas: list[FilaAuditoria] = []
        page_texts = extract_page_texts_from_pdf(path)
        for pagina, texto in page_texts.items():
            # Buscar líneas que parezcan filas de auditoría con 4-5 columnas separadas por 2+ espacios
            for linea in texto.split("\n"):
                partes = [p.strip() for p in re.split(r"\s{2,}", linea) if p.strip()]
                if len(partes) >= 4:
                    # Heurística: la primera parte debe parecer un ID (alphanumeric con guiones)
                    if re.match(r"^[A-Z]+[-\s]?\w+", partes[0], re.IGNORECASE):
                        id_unico = self._unicificar_id(partes[0])
                        resultado = partes[3] if len(partes) > 3 else ""
                        observacion = partes[4] if len(partes) > 4 else ""
                        es_defecto = _detectar_defecto(resultado, observacion)
                        filas.append(
                            FilaAuditoria(
                                id=id_unico,
                                metrica=partes[1] if len(partes) > 1 else "",
                                criterio=partes[2] if len(partes) > 2 else "",
                                resultado=resultado,
                                observacion=observacion,
                                pagina=pagina,
                                es_defecto=es_defecto,
                            )
                        )
        return filas
