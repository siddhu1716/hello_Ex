from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from services.whisper_service import whisper_service

router = APIRouter()


class STTResponse(BaseModel):
    transcript: str
    confidence: float | None = None
    language: str | None = None


@router.post("/stt/upload", response_model=STTResponse)
async def stt_upload(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="audio file is required")
    data = await file.read()
    transcript, confidence, language = await whisper_service.transcribe(data, filename=file.filename)
    return STTResponse(transcript=transcript, confidence=confidence, language=language)
