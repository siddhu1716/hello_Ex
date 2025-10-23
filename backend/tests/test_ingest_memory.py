import io
import os


def test_ingest_text_writes_embeddings(client):
    content = b"Hello there. This is a small chat export.\nSecond line of memory."
    # upload one text file
    files = {"files": ("chats.txt", io.BytesIO(content), "text/plain")}
    r = client.post("/ingest/upload", files=files)
    assert r.status_code == 200
    data = r.json()
    assert data["total_files"] == 1
    assert data["total_embeddings"] >= 1
    # memory.jsonl should exist and contain at least one line
    from config import settings
    assert os.path.exists(settings.MEMORY_FILE)
    with open(settings.MEMORY_FILE, "r", encoding="utf-8") as f:
        lines = [ln for ln in f.readlines() if ln.strip()]
    assert len(lines) >= 1
