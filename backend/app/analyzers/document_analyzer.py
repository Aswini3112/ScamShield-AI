"""
Document text extraction — PDF (via PyMuPDF), plain text, and image fallback.
"""
from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

ALLOWED_MIME_TYPES = {
    "application/pdf",
    "text/plain",
    "image/png",
    "image/jpeg",
    "image/webp",
    "image/gif",
}

MAX_TEXT_CHARS = 8000


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from PDF using PyMuPDF (fitz)."""
    try:
        import fitz  # PyMuPDF

        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text_parts = []
        for page in doc:
            text_parts.append(page.get_text())
        doc.close()
        return "\n".join(text_parts)[:MAX_TEXT_CHARS]
    except ImportError:
        logger.warning("PyMuPDF not installed — PDF extraction unavailable.")
        return ""
    except Exception as e:
        logger.warning("PDF extraction failed: %s", e)
        return ""


def extract_text_from_document(file_bytes: bytes, content_type: str, filename: str) -> str:
    """
    Dispatch text extraction based on content type.
    Never executes uploaded files.
    """
    ct = content_type.lower()
    fn = filename.lower()

    if ct == "application/pdf" or fn.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)

    if ct == "text/plain" or fn.endswith(".txt"):
        try:
            return file_bytes.decode("utf-8", errors="replace")[:MAX_TEXT_CHARS]
        except Exception:
            return ""

    if ct.startswith("image/") or fn.endswith((".png", ".jpg", ".jpeg", ".webp")):
        from app.analyzers.image_analyzer import _try_ocr
        return _try_ocr(file_bytes)[:MAX_TEXT_CHARS]

    return ""
