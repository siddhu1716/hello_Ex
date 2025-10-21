from typing import List, Optional, Dict, Any
from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel

from services.ingestion_service import ingest_any

router = APIRouter()


class IngestSummary(BaseModel):
    filename: str
    kind: str
    embedding_ids: List[str]


class IngestResponse(BaseModel):
    total_files: int
    total_embeddings: int
    items: List[IngestSummary]


@router.post("/ingest/upload", response_model=IngestResponse)
async def ingest_upload(
    files: List[UploadFile] = File(...),
    source: Optional[str] = Form(None, description="e.g., whatsapp, telegram, instagram"),
    tags: Optional[str] = Form(None, description="comma-separated tags"),
):
    tag_list: List[str] = [t.strip() for t in (tags or "").split(",") if t.strip()]
    items: List[IngestSummary] = []
    total = 0
    for f in files:
        data = await f.read()
        kind, ids = ingest_any(data, f.filename, source, tag_list)
        total += len(ids)
        items.append(IngestSummary(filename=f.filename, kind=kind, embedding_ids=ids))
    return IngestResponse(total_files=len(files), total_embeddings=total, items=items)
