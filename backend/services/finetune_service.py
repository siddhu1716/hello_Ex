import time
import threading
import uuid
from typing import Dict, Optional


class FinetuneService:
    """Mock finetuning service: start a job and mark it complete after a delay."""

    def __init__(self):
        self.jobs: Dict[str, Dict[str, str]] = {}
        self._lock = threading.Lock()

    def start_job(self, dataset_hint: Optional[str] = None) -> str:
        job_id = f"ft_{uuid.uuid4().hex}"
        with self._lock:
            self.jobs[job_id] = {"status": "queued", "dataset": dataset_hint or "memory"}
        t = threading.Thread(target=self._run_job, args=(job_id,), daemon=True)
        t.start()
        return job_id

    def _run_job(self, job_id: str):
        with self._lock:
            if job_id in self.jobs:
                self.jobs[job_id]["status"] = "running"
        time.sleep(3)
        with self._lock:
            if job_id in self.jobs:
                self.jobs[job_id]["status"] = "completed"

    def status(self, job_id: str) -> Dict[str, str]:
        with self._lock:
            return self.jobs.get(job_id, {"status": "not_found"})


finetune_service = FinetuneService()
