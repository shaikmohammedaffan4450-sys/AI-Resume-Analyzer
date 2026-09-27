"""Small PDF text extraction helper used by the Flask endpoint."""

import re
from typing import BinaryIO

from pypdf import PdfReader


class ResumeParseError(Exception):
    """Raised when a PDF cannot provide usable resume text."""


def extract_text_from_pdf(pdf_stream: BinaryIO) -> str:
    """Extract and clean selectable text from a PDF file-like object."""
    try:
        reader = PdfReader(pdf_stream, strict=False)
        if reader.is_encrypted:
            raise ResumeParseError("This PDF is password-protected and cannot be read.")

        page_text = [page.extract_text() or "" for page in reader.pages]
    except ResumeParseError:
        raise
    except Exception as exc:
        raise ResumeParseError("This PDF could not be read. Try exporting it again as a PDF.") from exc

    # Normalize whitespace while keeping paragraph breaks useful for display.
    text = "\n".join(page_text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    text = text.strip()

    if not text:
        raise ResumeParseError(
            "No selectable text was found. Scanned image-only PDFs need OCR, which this version does not include."
        )

    return text