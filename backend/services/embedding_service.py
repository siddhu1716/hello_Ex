import os
import json
import uuid
from typing import List, Tuple

import numpy as np

from config import settings
from utils.text_utils import simple_embed


class MemoryStore:
    """Very simple on-disk JSONL memory store with naive vector search."""

    def __init__(self, path: str):
        self.path = path
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        # lazy load index
        self._cache: List[Tuple[str, List[float], List[str]]] = []  # (id, vec, tags)
        self._loaded = False

    def _load(self):
        if self._loaded:
            return
        self._cache = []
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        obj = json.loads(line)
                        self._cache.append((obj["id"], obj["vector"], obj.get("tags", [])))
                    except Exception:
                        continue
        self._loaded = True

    def add(self, text: str, tags: List[str]) -> str:
        self._load()
        vec = simple_embed(text)
        mem_id = f"mem_{uuid.uuid4().hex}"
        rec = {"id": mem_id, "text": text, "vector": vec, "tags": tags}
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec) + "\n")
        self._cache.append((mem_id, vec, tags))
        return mem_id

    def retrieve(self, query: str, top_k: int = 5) -> List[str]:
        self._load()
        if not self._cache:
            return []
        q = np.array(simple_embed(query), dtype=np.float32)
        scored: List[Tuple[float, str]] = []
        for mem_id, vec, _tags in self._cache:
            v = np.array(vec, dtype=np.float32)
            # cosine similarity
            denom = (np.linalg.norm(q) * np.linalg.norm(v)) + 1e-8
            sim = float(np.dot(q, v) / denom)
            scored.append((sim, mem_id))
        scored.sort(reverse=True, key=lambda x: x[0])
        id_to_text = {}
        # rebuild id_to_text from file for simplicity
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                for line in f:
                    obj = json.loads(line)
                    id_to_text[obj["id"]] = obj.get("text", "")
        except Exception:
            pass
        results = []
        for _sim, mid in scored[:top_k]:
            results.append(id_to_text.get(mid, ""))
        return results


memory_store = MemoryStore(settings.MEMORY_FILE)
