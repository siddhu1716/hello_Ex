import os
import pytest
from fastapi.testclient import TestClient

from config import settings
from main import app


@pytest.fixture(scope="function")
def client(tmp_path):
    # Redirect storage to a temp directory for isolation
    settings.DATA_DIR = str(tmp_path)
    settings.AUDIO_DIR = os.path.join(settings.DATA_DIR, "audio")
    settings.EXPORT_DIR = os.path.join(settings.DATA_DIR, "exports")
    settings.MEMORY_FILE = os.path.join(settings.DATA_DIR, "memory.jsonl")
    settings.MESSAGES_FILE = os.path.join(settings.DATA_DIR, "messages.jsonl")

    os.makedirs(settings.DATA_DIR, exist_ok=True)
    os.makedirs(settings.AUDIO_DIR, exist_ok=True)
    os.makedirs(settings.EXPORT_DIR, exist_ok=True)

    # Force mock modes to avoid external dependencies
    os.environ["WHISPER_MODE"] = "mock"
    settings.WHISPER_MODE = "mock"
    # Use file backend memory store pointing to temp path and disable retrieval
    os.environ["VECTOR_BACKEND"] = "file"
    settings.VECTOR_BACKEND = "file"
    os.environ["RETRIEVAL_ENABLED"] = "false"
    settings.RETRIEVAL_ENABLED = False
    # Rebind memory_store to point at the temp file
    try:
        from services import embedding_service
        embedding_service.memory_store = embedding_service._FileMemoryStore(settings.MEMORY_FILE)
    except Exception:
        pass
    os.environ.pop("ELEVEN_API_KEY", None)

    return TestClient(app)
