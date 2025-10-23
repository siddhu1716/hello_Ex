import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# load .env if present
load_dotenv()


class Settings(BaseSettings):
    # CORS
    CORS_ALLOW_ORIGINS: str = os.getenv("CORS_ALLOW_ORIGINS", "*")

    # Model backends
    MODEL_BASE_URL: str | None = os.getenv("MODEL_BASE_URL")  # generic /infer style
    MODEL_PATH: str | None = os.getenv("MODEL_PATH", "/model/infer")

    # Ollama
    OLLAMA_BASE_URL: str | None = os.getenv("OLLAMA_BASE_URL")  # e.g., http://localhost:11434
    OLLAMA_MODEL: str | None = os.getenv("OLLAMA_MODEL")

    # vLLM (OpenAI compatible)
    OPENAI_BASE_URL: str | None = os.getenv("OPENAI_BASE_URL")  # e.g., http://localhost:8000/v1
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str | None = os.getenv("OPENAI_MODEL")

    # Whisper
    WHISPER_MODE: str = os.getenv("WHISPER_MODE", "mock")  # mock | local

    # ElevenLabs
    ELEVEN_API_KEY: str | None = os.getenv("ELEVEN_API_KEY")
    ELEVEN_VOICE_ID: str | None = os.getenv("ELEVEN_VOICE_ID")
    ELEVEN_BASE_URL: str = os.getenv("ELEVEN_BASE_URL", "https://api.elevenlabs.io/v1")

    # Storage
    DATA_DIR: str = os.path.join(os.path.dirname(__file__), "data", "storage")
    AUDIO_DIR: str = os.path.join(DATA_DIR, "audio")
    EXPORT_DIR: str = os.path.join(DATA_DIR, "exports")
    MEMORY_FILE: str = os.path.join(DATA_DIR, "memory.jsonl")
    MESSAGES_FILE: str = os.path.join(DATA_DIR, "messages.jsonl")

    # Retrieval and Vector Store
    RETRIEVAL_ENABLED: bool = os.getenv("RETRIEVAL_ENABLED", "true").lower() in {"1", "true", "yes", "on"}
    VECTOR_BACKEND: str = os.getenv("VECTOR_BACKEND", "file")  # file | chroma | milvus
    CHROMA_DIR: str = os.getenv("CHROMA_DIR", os.path.join(os.path.dirname(__file__), "data", "chroma"))
    EMBEDDING_MODEL_NAME: str = os.getenv("EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
    HISTORY_MESSAGES: int = int(os.getenv("HISTORY_MESSAGES", "6"))

    # Milvus
    MILVUS_HOST: str = os.getenv("MILVUS_HOST", "localhost")
    MILVUS_PORT: str = os.getenv("MILVUS_PORT", "19530")
    MILVUS_USER: str | None = os.getenv("MILVUS_USER")
    MILVUS_PASSWORD: str | None = os.getenv("MILVUS_PASSWORD")
    MILVUS_DB: str | None = os.getenv("MILVUS_DB")
    MILVUS_COLLECTION: str = os.getenv("MILVUS_COLLECTION", "memories")
    MILVUS_INDEX_TYPE: str = os.getenv("MILVUS_INDEX_TYPE", "HNSW")
    MILVUS_METRIC_TYPE: str = os.getenv("MILVUS_METRIC_TYPE", "IP")


settings = Settings()

# ensure dirs
os.makedirs(settings.DATA_DIR, exist_ok=True)
os.makedirs(settings.AUDIO_DIR, exist_ok=True)
os.makedirs(settings.EXPORT_DIR, exist_ok=True)
os.makedirs(getattr(settings, "CHROMA_DIR", os.path.join(os.path.dirname(__file__), "data", "chroma")), exist_ok=True)
