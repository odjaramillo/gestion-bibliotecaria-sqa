"""Tests for scripts.sqa_core.pdf_text."""
from __future__ import annotations

import sys
import unittest
from unittest.mock import MagicMock, patch

# Mock missing third-party modules before importing SQA code
if "fitz" not in sys.modules:
    sys.modules["fitz"] = MagicMock()

from scripts.sqa_core.pdf_text import chunk_text, extract_text_from_pdf


class TestExtractTextFromPdf(unittest.TestCase):
    """Tests for PDF text extraction."""

    @patch("scripts.sqa_core.pdf_text.fitz")
    def test_extracts_text_from_all_pages(self, mock_fitz):
        mock_doc = MagicMock()
        mock_page1 = MagicMock()
        mock_page1.get_text.return_value = "Page one content.\n"
        mock_page2 = MagicMock()
        mock_page2.get_text.return_value = "Page two content.\n"
        mock_doc.__iter__ = MagicMock(return_value=iter([mock_page1, mock_page2]))
        mock_fitz.open.return_value.__enter__ = MagicMock(return_value=mock_doc)
        mock_fitz.open.return_value.__exit__ = MagicMock(return_value=False)

        result = extract_text_from_pdf("/fake/path.pdf")
        self.assertEqual(result, "Page one content.\nPage two content.\n")

    @patch("scripts.sqa_core.pdf_text.fitz")
    def test_returns_empty_string_for_empty_pdf(self, mock_fitz):
        mock_doc = MagicMock()
        mock_doc.__iter__ = MagicMock(return_value=iter([]))
        mock_fitz.open.return_value.__enter__ = MagicMock(return_value=mock_doc)
        mock_fitz.open.return_value.__exit__ = MagicMock(return_value=False)

        result = extract_text_from_pdf("/fake/empty.pdf")
        self.assertEqual(result, "")


class TestChunkText(unittest.TestCase):
    """Tests for text chunking."""

    def test_empty_text_returns_empty_list(self):
        result = chunk_text("", max_chars=100)
        self.assertEqual(result, [])

    def test_single_chunk_when_text_fits(self):
        result = chunk_text("Short text", max_chars=100)
        self.assertEqual(result, ["Short text"])

    def test_splits_into_multiple_chunks(self):
        text = "a" * 150
        result = chunk_text(text, max_chars=50)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], "a" * 50)
        self.assertEqual(result[1], "a" * 50)
        self.assertEqual(result[2], "a" * 50)

    def test_splits_on_word_boundary_when_possible(self):
        text = "word1 word2 word3 word4 word5"
        result = chunk_text(text, max_chars=12)
        self.assertTrue(all(len(c) <= 12 for c in result))
        self.assertEqual(" ".join(result), text)

    def test_exact_boundary_no_extra_chunk(self):
        text = "a" * 100
        result = chunk_text(text, max_chars=100)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], text)


if __name__ == "__main__":
    unittest.main()
