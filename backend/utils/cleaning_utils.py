import re
from typing import List


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip())


def strip_control_chars(text: str) -> str:
    return re.sub(r"[\x00-\x1F\x7F]", "", text or "")


def clean_text(text: str) -> str:
    return normalize_whitespace(strip_control_chars(text))


def chunk_text(text: str, max_chars: int = 800) -> List[str]:
    text = text or ""
    if len(text) <= max_chars:
        return [text]
    chunks: List[str] = []
    start = 0
    while start < len(text):
        end = min(len(text), start + max_chars)
        # try split on sentence boundary
        slice_ = text[start:end]
        last_dot = slice_.rfind(".")
        if last_dot > 200:  # arbitrary
            end = start + last_dot + 1
        chunks.append(text[start:end].strip())
        start = end
    return [c for c in chunks if c]
