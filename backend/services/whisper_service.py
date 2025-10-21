import io
import asyncio
from typing import Tuple, Optional

from config import settings


class WhisperService:
    """Whisper STT with mock and optional local mode."""

    def __init__(self):
        self._local_model = None
        if settings.WHISPER_MODE == "local":
            try:
                import whisper  # type: ignore

                self._local_model = whisper.load_model("base")
            except Exception:
                self._local_model = None

    async def transcribe(self, audio_bytes: bytes, filename: Optional[str] = None) -> Tuple[str, Optional[float], Optional[str]]:
        if settings.WHISPER_MODE == "local" and self._local_model is not None:
            return await asyncio.to_thread(self._local_transcribe, audio_bytes)
        # mock fallback
        return "I still miss our late-night calls.", 0.97, "en"

    def _local_transcribe(self, audio_bytes: bytes) -> Tuple[str, Optional[float], Optional[str]]:
        import tempfile
        import os

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio_bytes)
            tmp.flush()
            path = tmp.name
        try:
            result = self._local_model.transcribe(path)
            txt = result.get("text", "") or "(no speech)"
            lang = result.get("language") or "en"
            conf = None
            return txt.strip(), conf, lang
        finally:
            try:
                os.remove(path)
            except Exception:
                pass


whisper_service = WhisperService()
