from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.finetune_service import finetune_service

router = APIRouter()


class FinetuneStartRequest(BaseModel):
    dataset_hint: Optional[str] = None


class FinetuneStartResponse(BaseModel):
    job_id: str
    status: str


class FinetuneStatusResponse(BaseModel):
    job_id: str
    status: str


@router.post("/finetune/start", response_model=FinetuneStartResponse)
async def finetune_start(req: FinetuneStartRequest):
    job_id = finetune_service.start_job(dataset_hint=req.dataset_hint)
    return FinetuneStartResponse(job_id=job_id, status="queued")


@router.get("/finetune/status/{job_id}", response_model=FinetuneStatusResponse)
async def finetune_status(job_id: str):
    st = finetune_service.status(job_id)
    if st.get("status") == "not_found":
        raise HTTPException(status_code=404, detail="job not found")
    return FinetuneStatusResponse(job_id=job_id, status=st.get("status", "unknown"))
