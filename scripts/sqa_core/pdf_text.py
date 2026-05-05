"""PDF text extraction and chunking for frozen documentation."""
from __future__ import annotations

import logging
from pathlib import Path

import fitz

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
