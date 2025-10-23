import json
import os
from typing import List

from config import settings


def sanitize_text(text: str) -> str:
    return (text or "").strip()


def build_prompt(persona: str, context_memories: List[str], user_input: str) -> str:
    parts = [
        "System: You are emulating the persona described by the user. Speak kindly and empathetically, acknowledging emotions but not reinforcing negative loops.",
        "",
        "Context:",
        "\n".join(context_memories or []),
        "",
        f"Persona: {persona}",
        "",
        f"User: {user_input}",
        "AI:",
    ]
    return "\n".join(parts)


def simple_embed(text: str) -> List[float]:
    # Deterministic toy embedding: character frequency of lowercase letters + length scalar
    text = (text or "").lower()
    vec = [0] * 26
    for ch in text:
        i = ord(ch) - ord('a')
        if 0 <= i < 26:
            vec[i] += 1
    vec.append(min(len(text) / 100.0, 1.0))
    return [float(x) for x in vec]


def append_message(role: str, content: str) -> None:
    os.makedirs(os.path.dirname(settings.MESSAGES_FILE), exist_ok=True)
    rec = {"role": role, "content": content}
    with open(settings.MESSAGES_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")


def get_recent_messages(n: int) -> List[dict]:
    """Read the last n JSONL messages from the messages file."""
    path = settings.MESSAGES_FILE
    if not os.path.exists(path) or n <= 0:
        return []
    msgs: List[dict] = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()[-n:]
        for ln in lines:
            try:
                obj = json.loads(ln)
                if isinstance(obj, dict) and "role" in obj and "content" in obj:
                    msgs.append(obj)
            except Exception:
                continue
    except Exception:
        return []
    return msgs
