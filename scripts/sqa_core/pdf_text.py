"""PDF text extraction and chunking for frozen documentation."""
from __future__ import annotations

import io
import logging
from pathlib import Path

import fitz

try:
    from PIL import Image
except ImportError:
    Image = None

logger = logging.getLogger("sqa_core.pdf_text")

DEFAULT_CHUNK_SIZE = 4000


def extract_text_from_pdf(pdf_path: str | Path) -> str:
    """Extract plain text from all pages of a PDF."""
    path = Path(pdf_path)
    logger.info("Extrayendo texto de PDF: %s", path)
    text_parts: list[str] = []
    with fitz.open(path) as doc:
        for page in doc:
            text_parts.append(page.get_text())
    return "".join(text_parts)


def extract_images_from_pdf(
    pdf_path: str | Path,
    output_dir: Path,
    min_width: int = 200,
    min_height: int = 200,
) -> list[Path]:
    """Extrae imágenes embebidas de un PDF filtrando por tamaño mínimo.

    Args:
        pdf_path: Ruta al archivo PDF.
        output_dir: Directorio donde se guardarán las imágenes extraídas.
        min_width: Ancho mínimo en píxeles para conservar la imagen.
        min_height: Alto mínimo en píxeles para conservar la imagen.

    Returns:
        Lista de rutas a las imágenes guardadas.
    """
    path = Path(pdf_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    pdf_name = path.stem
    extracted: list[Path] = []

    logger.info("Extrayendo imágenes de PDF: %s", path)
    with fitz.open(path) as doc:
        for page_num in range(len(doc)):
            page = doc[page_num]
            images = page.get_images(full=True)
            for img_index, img in enumerate(images, start=1):
                xref = img[0]
                try:
                    base_image = doc.extract_image(xref)
                except Exception as exc:
                    logger.warning("Error extrayendo imagen xref=%s: %s", xref, exc)
                    continue
                width = base_image.get("width", 0)
                height = base_image.get("height", 0)
                if width < min_width or height < min_height:
                    logger.debug(
                        "Imagen descartada por tamaño (%sx%s): xref=%s",
                        width,
                        height,
                        xref,
                    )
                    continue
                image_bytes = base_image["image"]
                try:
                    img = Image.open(io.BytesIO(image_bytes))
                    if img.mode not in ("RGB", "RGBA"):
                        img = img.convert("RGB")
                    png_buffer = io.BytesIO()
                    img.save(png_buffer, format="PNG")
                    png_bytes = png_buffer.getvalue()
                except Exception as exc:
                    logger.warning(
                        "Error convirtiendo imagen xref=%s a PNG: %s", xref, exc
                    )
                    continue
                image_filename = f"{pdf_name}_page{page_num + 1}_img{img_index}.png"
                image_path = output_dir / image_filename
                image_path.write_bytes(png_bytes)
                extracted.append(image_path)
                logger.info("Imagen guardada: %s (%sx%s)", image_path, width, height)

    logger.info("Total imágenes extraídas: %d", len(extracted))
    return extracted


def extract_page_texts_from_pdf(pdf_path: str | Path) -> dict[int, str]:
    """Extrae el texto de cada página de un PDF indexado por número de página.

    Args:
        pdf_path: Ruta al archivo PDF.

    Returns:
        Diccionario {número_de_página: texto}.
    """
    path = Path(pdf_path)
    page_texts: dict[int, str] = {}
    logger.info("Extrayendo texto por página de PDF: %s", path)
    with fitz.open(path) as doc:
        for page_num in range(len(doc)):
            page = doc[page_num]
            page_texts[page_num + 1] = page.get_text()
    return page_texts


def chunk_text(text: str, max_chars: int = DEFAULT_CHUNK_SIZE) -> list[str]:
    """Split *text* into chunks of at most *max_chars*.

    Tries to split on word boundaries to keep chunks readable.
    """
    if not text:
        return []

    chunks: list[str] = []
    words = text.split(" ")
    current = ""

    for word in words:
        candidate = f"{current} {word}" if current else word
        if len(candidate) <= max_chars:
            current = candidate
        else:
            if current:
                chunks.append(current)
            current = word
            # If a single word exceeds max_chars, force-split it
            while len(current) > max_chars:
                chunks.append(current[:max_chars])
                current = current[max_chars:]

    if current:
        chunks.append(current)

    return chunks
