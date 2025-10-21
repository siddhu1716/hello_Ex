import io
import json
import os
from typing import List, Tuple

from config import settings
from services.embedding_service import memory_store
from services.whisper_service import whisper_service
from utils.cleaning_utils import clean_text, chunk_text


TEXT_EXTS = {".txt", ".md"}
JSON_EXTS = {".json"}
AUDIO_EXTS = {".wav", ".mp3", ".m4a", ".ogg"}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}


def _ext(path: str) -> str:
    _, ext = os.path.splitext(path.lower())
    return ext


def _ingest_text_content(raw: str, tags: List[str]) -> List[str]:
    cleaned = clean_text(raw)
    chunks = chunk_text(cleaned)
    ids: List[str] = []
    for ch in chunks:
        if ch:
            mem_id = memory_store.add(ch, tags)
            ids.append(mem_id)
    return ids


def ingest_text_file(data: bytes, filename: str, source: str | None, tags: List[str]) -> List[str]:
    try:
        text = data.decode("utf-8", errors="ignore")
    except Exception:
        text = ""
    tags_all = tags + ([source] if source else [])
    return _ingest_text_content(text, tags_all)


def ingest_json_file(data: bytes, filename: str, source: str | None, tags: List[str]) -> List[str]:
    tags_all = tags + ([source] if source else [])
    try:
        obj = json.loads(data.decode("utf-8", errors="ignore"))
    except Exception:
        return []
    texts: List[str] = []
    # simple conventions: {messages:[{text:...}]}, or {chats:[{content:...}]}
    if isinstance(obj, dict):
        arr = obj.get("messages") or obj.get("chats") or []
        if isinstance(arr, list):
            for it in arr:
                if isinstance(it, dict):
                    t = it.get("text") or it.get("content") or ""
                    if isinstance(t, str):
                        texts.append(t)
                    elif isinstance(t, list):
                        # telegram exports sometimes have rich parts list
                        parts = [p for p in t if isinstance(p, str)]
                        texts.append(" ".join(parts))
    elif isinstance(obj, list):
        for it in obj:
            if isinstance(it, str):
                texts.append(it)
            elif isinstance(it, dict):
                t = it.get("text") or it.get("content") or ""
                if isinstance(t, str):
                    texts.append(t)
    ids: List[str] = []
    for t in texts:
        ids += _ingest_text_content(t, tags_all)
    return ids


def ingest_audio_file(data: bytes, filename: str, source: str | None, tags: List[str]) -> List[str]:
    transcript, _conf, _lang = whisper_service.transcribe.__wrapped__(whisper_service, data, filename)  # type: ignore
    tags_all = tags + ([source] if source else [])
    return _ingest_text_content(transcript, tags_all)


def ingest_image_file(data: bytes, filename: str, source: str | None, tags: List[str]) -> List[str]:
    # For now, skip image OCR; placeholder returns empty list
    return []


def ingest_any(data: bytes, filename: str, source: str | None, tags: List[str]) -> Tuple[str, List[str]]:
    ext = _ext(filename)
    if ext in TEXT_EXTS:
        return "text", ingest_text_file(data, filename, source, tags)
    if ext in JSON_EXTS:
        return "json", ingest_json_file(data, filename, source, tags)
    if ext in AUDIO_EXTS:
        return "audio", ingest_audio_file(data, filename, source, tags)
    if ext in IMAGE_EXTS:
        return "image", ingest_image_file(data, filename, source, tags)
    # default: try text decode
    return "unknown", ingest_text_file(data, filename, source, tags)
