from typing import Optional, List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.ai_service import ai_service
from services.embedding_service import memory_store
from services.eleven_service import tts_service
from utils.text_utils import sanitize_text, build_prompt, append_message

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    persona: Optional[str] = "default"
    mode: Optional[str] = "text"
    tts: Optional[bool] = False


class ChatResponse(BaseModel):
    reply_text: str
    audio_url: Optional[str] = None
    sentiment: Optional[str] = None


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not req.message or not req.message.strip():
        raise HTTPException(status_code=400, detail="message is required")

    user_text = sanitize_text(req.message)
    # persist user message
    append_message("user", user_text)

    # retrieve naive top-k memories
    memories: List[str] = memory_store.retrieve(user_text, top_k=5)

    prompt = build_prompt(persona=req.persona or "default", context_memories=memories, user_input=user_text)

    reply_text, sentiment = await ai_service.generate_reply(prompt)
    # persist assistant reply
    append_message("assistant", reply_text)

    audio_url = None
    if req.tts:
        try:
            audio_url = await tts_service.speak(reply_text, voice_id=None)
        except Exception:
            audio_url = None

    return ChatResponse(reply_text=reply_text, audio_url=audio_url, sentiment=sentiment)
