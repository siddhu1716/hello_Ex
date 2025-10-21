import os
import json
import uuid
import asyncio
from typing import Tuple, Optional

import requests

from config import settings


class AIService:
    """Proxy to model backends (vLLM OpenAI-compatible, Ollama, or generic), with a mock fallback."""

    def __init__(self):
        self.session = requests.Session()

    async def generate_reply(self, prompt: str) -> Tuple[str, Optional[str]]:
        # Try vLLM/OpenAI-compatible first
        if settings.OPENAI_BASE_URL and settings.OPENAI_MODEL and settings.OPENAI_API_KEY:
            try:
                return await asyncio.to_thread(self._openai_chat, prompt)
            except Exception:
                pass

        # Try Ollama chat
        if settings.OLLAMA_BASE_URL and settings.OLLAMA_MODEL:
            try:
                return await asyncio.to_thread(self._ollama_chat, prompt)
            except Exception:
                pass

        # Try generic model endpoint
        if settings.MODEL_BASE_URL:
            try:
                return await asyncio.to_thread(self._generic_infer, prompt)
            except Exception:
                pass

        # Fallback mock
        return self._mock_reply(prompt)

    def _openai_chat(self, prompt: str) -> Tuple[str, Optional[str]]:
        url = f"{settings.OPENAI_BASE_URL.rstrip('/')}/chat/completions"
        headers = {
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": settings.OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": "You are a compassionate persona for helloEx."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.8,
        }
        resp = self.session.post(url, headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        text = data.get("choices", [{}])[0].get("message", {}).get("content", "...")
        return text, "neutral"

    def _ollama_chat(self, prompt: str) -> Tuple[str, Optional[str]]:
        url = f"{settings.OLLAMA_BASE_URL.rstrip('/')}/api/chat"
        payload = {
            "model": settings.OLLAMA_MODEL,
            "messages": [
                {"role": "system", "content": "You are a compassionate persona for helloEx."},
                {"role": "user", "content": prompt},
            ],
            "stream": False,
        }
        resp = self.session.post(url, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        # ollama returns {message:{content:"..."}}
        msg = data.get("message", {})
        text = msg.get("content", "...")
        return text, "neutral"

    def _generic_infer(self, prompt: str) -> Tuple[str, Optional[str]]:
        path = settings.MODEL_PATH or "/model/infer"
        url = f"{settings.MODEL_BASE_URL.rstrip('/')}{path}"
        payload = {"prompt": prompt, "max_tokens": 200}
        resp = self.session.post(url, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        text = data.get("text") or data.get("reply") or json.dumps(data)[:200]
        return text, "neutral"

    def _mock_reply(self, prompt: str) -> Tuple[str, Optional[str]]:
        # simple echo-based mock
        reply = "I hear you. It’s okay to feel this way. "
        tail = prompt.strip().split("\n")[-1]
        if len(tail) > 160:
            tail = tail[:160] + "..."
        return reply + tail, "calm"


ai_service = AIService()
