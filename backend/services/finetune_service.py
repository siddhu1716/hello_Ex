import os
import time
import threading
import uuid
from typing import Dict, Optional, Any, List

from config import settings
from utils.parse_utils import parse_whatsapp_pairs

# Optional heavy deps
try:
    import torch  # type: ignore
    from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments  # type: ignore
    from trl import SFTTrainer  # type: ignore
    from peft import LoraConfig  # type: ignore
    HAVE_TRAIN_DEPS = True
except Exception:
    HAVE_TRAIN_DEPS = False


class FinetuneService:
    """Background finetune jobs. If FINETUNE_ENABLED and deps available, run LoRA SFT; else mock."""

    def __init__(self):
        self.jobs: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()

    def start_job(self, dataset_hint: Optional[str] = None) -> str:
        job_id = f"ft_{uuid.uuid4().hex}"
        with self._lock:
            self.jobs[job_id] = {"status": "queued", "dataset": dataset_hint or "memory"}
        t = threading.Thread(target=self._run_mock_job, args=(job_id,), daemon=True)
        t.start()
        return job_id

    def start_job_from_whatsapp_text(
        self,
        text: str,
        user_of_interest: str,
        model_name: Optional[str] = None,
        epochs: int = 1,
        lr: float = 2e-4,
        max_seq_len: int = 512,
        lora_r: int = 16,
        lora_alpha: int = 32,
        lora_dropout: float = 0.1,
    ) -> str:
        pairs = parse_whatsapp_pairs(text, user_of_interest=user_of_interest)
        job_id = f"ft_{uuid.uuid4().hex}"
        out_dir = os.path.join(settings.FINETUNE_OUTPUT_DIR, job_id)
        os.makedirs(out_dir, exist_ok=True)
        with self._lock:
            self.jobs[job_id] = {
                "status": "queued",
                "pairs": pairs,
                "out_dir": out_dir,
                "model": model_name or settings.FINETUNE_DEFAULT_MODEL,
            }
        if settings.FINETUNE_ENABLED and HAVE_TRAIN_DEPS:
            t = threading.Thread(
                target=self._run_train_job,
                args=(
                    job_id,
                    pairs,
                    model_name or settings.FINETUNE_DEFAULT_MODEL,
                    epochs,
                    lr,
                    max_seq_len,
                    lora_r,
                    lora_alpha,
                    lora_dropout,
                    out_dir,
                ),
                daemon=True,
            )
        else:
            t = threading.Thread(target=self._run_mock_job, args=(job_id,), daemon=True)
        t.start()
        return job_id

    def _run_mock_job(self, job_id: str):
        with self._lock:
            if job_id in self.jobs:
                self.jobs[job_id]["status"] = "running"
        time.sleep(2)
        with self._lock:
            if job_id in self.jobs:
                self.jobs[job_id]["status"] = "completed"
                self.jobs[job_id]["artifact"] = self.jobs[job_id].get("out_dir", "")

    def _run_train_job(
        self,
        job_id: str,
        pairs: List[Dict[str, str]],
        model_name: str,
        epochs: int,
        lr: float,
        max_seq_len: int,
        lora_r: int,
        lora_alpha: int,
        lora_dropout: float,
        out_dir: str,
    ):
        with self._lock:
            if job_id in self.jobs:
                self.jobs[job_id]["status"] = "running"
        try:
            # build plain text field dataset
            texts = [f"Instruction: {p['instruction']}\nResponse: {p['response']}" for p in pairs]
            # load model/tokenizer
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            if tokenizer.pad_token is None:
                tokenizer.pad_token = tokenizer.eos_token
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                load_in_4bit=True,
                torch_dtype=torch.float16,
                device_map="auto",
            )
            lora_cfg = LoraConfig(r=lora_r, lora_alpha=lora_alpha, lora_dropout=lora_dropout, bias="none", task_type="CAUSAL_LM")
            args = TrainingArguments(
                output_dir=out_dir,
                num_train_epochs=epochs,
                per_device_train_batch_size=2,
                gradient_accumulation_steps=8,
                learning_rate=lr,
                fp16=True,
                save_strategy="epoch",
                logging_steps=20,
                optim="paged_adamw_8bit",
            )
            trainer = SFTTrainer(
                model=model,
                tokenizer=tokenizer,
                train_dataset=texts,
                dataset_text_field=None,
                max_seq_length=max_seq_len,
                peft_config=lora_cfg,
                args=args,
            )
            trainer.train()
            with self._lock:
                if job_id in self.jobs:
                    self.jobs[job_id]["status"] = "completed"
                    self.jobs[job_id]["artifact"] = out_dir
        except Exception as e:
            with self._lock:
                if job_id in self.jobs:
                    self.jobs[job_id]["status"] = f"failed: {e}"

    def status(self, job_id: str) -> Dict[str, Any]:
        with self._lock:
            return self.jobs.get(job_id, {"status": "not_found"})


finetune_service = FinetuneService()
