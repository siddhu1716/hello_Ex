import io
import json
import os
import time
import zipfile
from typing import List, Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from config import settings
from services.embedding_service import memory_store

router = APIRouter()


class MemoryUpload(BaseModel):
    text: str
    tags: Optional[List[str]] = None


class MemoryUploadResponse(BaseModel):
    status: str
    embedding_id: str


@router.post("/memory/upload", response_model=MemoryUploadResponse)
async def memory_upload(req: MemoryUpload):
    if not req.text or not req.text.strip():
        raise HTTPException(status_code=400, detail="text is required")
    mem_id = memory_store.add(req.text, tags=req.tags or [])
    return MemoryUploadResponse(status="stored", embedding_id=mem_id)


@router.get("/export")
async def export_data():
    # Aggregate files into zip in-memory
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        # messages and memory
        for name in [settings.MESSAGES_FILE, settings.MEMORY_FILE]:
            if os.path.exists(name):
                zf.write(name, arcname=os.path.basename(name))
        # audio folder
        if os.path.isdir(settings.AUDIO_DIR):
            for root, _, files in os.walk(settings.AUDIO_DIR):
                for f in files:
                    full = os.path.join(root, f)
                    arc = os.path.relpath(full, start=settings.DATA_DIR)
                    zf.write(full, arcname=arc)
        # report.txt placeholder
        report = f"helloEx export generated at {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        zf.writestr("report.txt", report)
    buf.seek(0)
    headers = {
        "Content-Disposition": "attachment; filename=helloex_export.zip"
    }
    return StreamingResponse(buf, media_type="application/zip", headers=headers)
