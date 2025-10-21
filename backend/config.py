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


settings = Settings()

# ensure dirs
os.makedirs(settings.DATA_DIR, exist_ok=True)
os.makedirs(settings.AUDIO_DIR, exist_ok=True)
os.makedirs(settings.EXPORT_DIR, exist_ok=True)
