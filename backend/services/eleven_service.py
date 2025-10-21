import os
import uuid
import asyncio
import requests

from config import settings
from utils.audio_utils import generate_dummy_wav


class ElevenService:
    """ElevenLabs TTS with mock fallback that generates a local WAV file."""

    def __init__(self):
        self.session = requests.Session()

    async def speak(self, text: str, voice_id: str | None = None) -> str | None:
        # If API key and voice present, try ElevenLabs
        if settings.ELEVEN_API_KEY and (voice_id or settings.ELEVEN_VOICE_ID):
            try:
                return await asyncio.to_thread(self._elevenlabs_speak, text, voice_id)
            except Exception:
                pass
        # Fallback: generate a dummy wav so the pipeline works
        return await asyncio.to_thread(self._mock_speak, text)

    def _elevenlabs_speak(self, text: str, voice_id: str | None) -> str | None:
        vid = voice_id or settings.ELEVEN_VOICE_ID
        url = f"{settings.ELEVEN_BASE_URL.rstrip('/')}/text-to-speech/{vid}"
        headers = {
            "xi-api-key": settings.ELEVEN_API_KEY,
            "accept": "audio/mpeg",
            "content-type": "application/json",
        }
        payload = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
        }
        resp = self.session.post(url, headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        audio_bytes = resp.content
        fname = f"tts_{uuid.uuid4().hex}.mp3"
        out_path = os.path.join(settings.AUDIO_DIR, fname)
        with open(out_path, "wb") as f:
            f.write(audio_bytes)
        return f"/static/audio/{fname}"

    def _mock_speak(self, text: str) -> str | None:
        fname = f"tts_{uuid.uuid4().hex}.wav"
        out_path = os.path.join(settings.AUDIO_DIR, fname)
        generate_dummy_wav(text, out_path)
        return f"/static/audio/{fname}"


tts_service = ElevenService()
