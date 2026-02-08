"""Text extraction from .txt and .pdf files."""

import pathlib

import pymupdf


def extract_text(filepath: pathlib.Path) -> str:
    """Extract text content from a .txt or .pdf file.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file format is unsupported or the file is empty.
    """
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    suffix = filepath.suffix.lower()

    if suffix == ".txt":
        text = filepath.read_text(encoding="utf-8")
    elif suffix == ".pdf":
        text = _extract_pdf(filepath)
    else:
        raise ValueError(f"Unsupported file format: {suffix!r} (expected .txt or .pdf)")

    if not text.strip():
        raise ValueError(f"File is empty: {filepath}")

    return text


def _extract_pdf(filepath: pathlib.Path) -> str:
    doc = pymupdf.open(filepath)
    pages = [page.get_text() for page in doc]
    doc.close()
    return "\n".join(pages)
