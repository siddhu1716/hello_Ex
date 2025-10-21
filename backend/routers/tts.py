from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.eleven_service import tts_service

router = APIRouter()


class TTSRequest(BaseModel):
    text: str
    voice_id: Optional[str] = None


class TTSResponse(BaseModel):
    audio_url: str


@router.post("/tts/speak", response_model=TTSResponse)
async def tts_speak(req: TTSRequest):
    if not req.text or not req.text.strip():
        raise HTTPException(status_code=400, detail="text is required")
    url = await tts_service.speak(req.text, voice_id=req.voice_id)
    if not url:
        raise HTTPException(status_code=500, detail="failed to synthesize audio")
    return TTSResponse(audio_url=url)
