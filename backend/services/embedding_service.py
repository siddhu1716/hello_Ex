import os
import json
import uuid
from typing import List, Tuple

import numpy as np

from config import settings
from utils.text_utils import simple_embed

# Optional imports for Chroma, Milvus and sentence-transformers
try:
    import chromadb  # type: ignore
    from sentence_transformers import SentenceTransformer  # type: ignore
except Exception:
    chromadb = None  # type: ignore
    SentenceTransformer = None  # type: ignore

try:
    from pymilvus import (
        connections,
        FieldSchema,
        CollectionSchema,
        DataType,
        Collection,
        utility,
    )  # type: ignore
except Exception:
    connections = None  # type: ignore
    FieldSchema = CollectionSchema = DataType = Collection = utility = None  # type: ignore


class _FileMemoryStore:
    """Very simple on-disk JSONL memory store with naive vector search."""

    def __init__(self, path: str):
        self.path = path
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
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
            denom = (np.linalg.norm(q) * np.linalg.norm(v)) + 1e-8
            sim = float(np.dot(q, v) / denom)
            scored.append((sim, mem_id))
        scored.sort(reverse=True, key=lambda x: x[0])
        id_to_text: dict[str, str] = {}
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                for line in f:
                    obj = json.loads(line)
                    id_to_text[obj["id"]] = obj.get("text", "")
        except Exception:
            pass
        results: List[str] = []
        for _sim, mid in scored[:top_k]:
            results.append(id_to_text.get(mid, ""))
        return results


class _MilvusMemoryStore:
    """Milvus-backed vector store using sentence-transformers embeddings."""

    def __init__(self):
        if connections is None or SentenceTransformer is None:
            raise RuntimeError("Milvus or sentence-transformers not installed.")
        # connect
        conn_kwargs = {
            "host": settings.MILVUS_HOST,
            "port": settings.MILVUS_PORT,
        }
        # optional auth/db
        if settings.MILVUS_USER and settings.MILVUS_PASSWORD:
            conn_kwargs.update({"user": settings.MILVUS_USER, "password": settings.MILVUS_PASSWORD})
        if settings.MILVUS_DB:
            conn_kwargs.update({"db_name": settings.MILVUS_DB})
        connections.connect(**conn_kwargs)

        self.collection_name = settings.MILVUS_COLLECTION
        self.metric_type = settings.MILVUS_METRIC_TYPE
        self.index_type = settings.MILVUS_INDEX_TYPE
        # embedder
        self.embedder = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)
        dim = getattr(self.embedder, "get_sentence_embedding_dimension", lambda: None)()
        if not dim:
            # compute once
            dim = len(self.embedder.encode(["dim_probe"])[0])

        # create collection if needed
        if not utility.has_collection(self.collection_name):
            fields = [
                FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, max_length=64),
                FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=int(dim)),
                FieldSchema(name="tags", dtype=DataType.VARCHAR, max_length=512),
                FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
            ]
            schema = CollectionSchema(fields=fields, description="memory embeddings")
            self.collection = Collection(name=self.collection_name, schema=schema)
            # index
            if self.index_type.upper() == "HNSW":
                index_params = {"index_type": "HNSW", "metric_type": self.metric_type, "params": {"M": 8, "efConstruction": 64}}
            else:
                index_params = {"index_type": self.index_type, "metric_type": self.metric_type, "params": {}}
            self.collection.create_index(field_name="embedding", index_params=index_params)
        else:
            self.collection = Collection(self.collection_name)
        self.collection.load()

    def _embed(self, texts: List[str]) -> List[List[float]]:
        return self.embedder.encode(texts, normalize_embeddings=True).tolist()

    def add(self, text: str, tags: List[str]) -> str:
        mem_id = f"mem_{uuid.uuid4().hex}"
        emb = self._embed([text])[0]
        tags_str = ",".join(tags or [])
        self.collection.insert([[mem_id], [emb], [tags_str], [text]])
        # flush is optional in newer versions; keep for durability
        self.collection.flush()
        return mem_id

    def retrieve(self, query: str, top_k: int = 5) -> List[str]:
        if not query:
            return []
        qvec = self._embed([query])[0]
        search_params = {"metric_type": self.metric_type, "params": {"ef": 128}} if self.index_type.upper() == "HNSW" else {"metric_type": self.metric_type, "params": {}}
        hits = self.collection.search(data=[qvec], anns_field="embedding", param=search_params, limit=top_k, output_fields=["text"])
        results: List[str] = []
        if hits and len(hits) > 0:
            for hit in hits[0]:
                ent = hit.entity
                try:
                    results.append(ent.get("text"))
                except Exception:
                    pass
        return results


class _ChromaMemoryStore:
    """Chroma-backed vector store using sentence-transformers embeddings."""

    def __init__(self, persist_dir: str, model_name: str):
        if chromadb is None or SentenceTransformer is None:
            raise RuntimeError("ChromaDB or sentence-transformers not installed. Install extras in requirements.txt")
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(name="memories")
        self.embedder = SentenceTransformer(model_name)

    def _embed(self, texts: List[str]) -> List[List[float]]:
        vecs = self.embedder.encode(texts, normalize_embeddings=True).tolist()
        return vecs

    def add(self, text: str, tags: List[str]) -> str:
        mem_id = f"mem_{uuid.uuid4().hex}"
        embeddings = self._embed([text])
        self.collection.add(ids=[mem_id], documents=[text], embeddings=embeddings, metadatas=[{"tags": tags}])
        return mem_id

    def retrieve(self, query: str, top_k: int = 5) -> List[str]:
        qvec = self._embed([query])[0]
        res = self.collection.query(query_embeddings=[qvec], n_results=top_k)
        docs = (res.get("documents") or [[]])[0]
        return [d for d in docs if isinstance(d, str)]


def _make_store():
    backend = (settings.VECTOR_BACKEND or "file").lower()
    if backend == "chroma":
        try:
            return _ChromaMemoryStore(settings.CHROMA_DIR, settings.EMBEDDING_MODEL_NAME)
        except Exception:
            return _FileMemoryStore(settings.MEMORY_FILE)
    if backend == "milvus":
        try:
            return _MilvusMemoryStore()
        except Exception:
            return _FileMemoryStore(settings.MEMORY_FILE)
    return _FileMemoryStore(settings.MEMORY_FILE)


memory_store = _make_store()
