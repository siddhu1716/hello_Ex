from typing import Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
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


@router.post("/finetune/whatsapp", response_model=FinetuneStartResponse)
async def finetune_whatsapp(
    file: UploadFile = File(..., description="Raw WhatsApp exported .txt file"),
    user_of_interest: str = Form(..., description="Name of the user whose replies should be learned"),
    model_name: Optional[str] = Form(None),
    epochs: int = Form(1),
    lr: float = Form(2e-4),
    max_seq_len: int = Form(512),
    lora_r: int = Form(16),
    lora_alpha: int = Form(32),
    lora_dropout: float = Form(0.1),
):
    data = await file.read()
    try:
        text = data.decode("utf-8", errors="ignore")
    except Exception:
        raise HTTPException(status_code=400, detail="invalid text file")
    job_id = finetune_service.start_job_from_whatsapp_text(
        text=text,
        user_of_interest=user_of_interest,
        model_name=model_name,
        epochs=epochs,
        lr=lr,
        max_seq_len=max_seq_len,
        lora_r=lora_r,
        lora_alpha=lora_alpha,
        lora_dropout=lora_dropout,
    )
    return FinetuneStartResponse(job_id=job_id, status="queued")
