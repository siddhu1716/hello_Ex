# helloEx Backend (FastAPI)

Modular FastAPI backend that implements the helloEx pipeline:

- **/chat** – chat with persona with memory context and optional TTS
- **/stt/upload** – Whisper speech-to-text (mock or local)
- **/tts/speak** – ElevenLabs text-to-speech (real if configured, else dummy WAV)
- **/memory/upload** – store text memos and build a simple vector memory
- **/ingest/upload** – upload text/json/audio/image files, clean & ingest into memory (RAG)
- **/finetune/start**, **/finetune/status/{job_id}** – start a finetune job and poll status (mock)
- **/export** – download a zip containing messages and any audio artifacts
- **/health** – heartbeat

## Structure

- `main.py` – app bootstrap, CORS, static mount
- `config.py` – centralized environment/settings
- `routers/` – route modules (`chat.py`, `stt.py`, `tts.py`, `memory.py`)
- `services/` – integrations (`ai_service.py`, `whisper_service.py`, `eleven_service.py`, `embedding_service.py`)
- `utils/` – helpers (`text_utils.py`, `audio_utils.py`)
- `data/storage/` – persisted files: `messages.jsonl`, `memory.jsonl`, `audio/*`, `exports/*`
- Vector store (pluggable): file JSONL (default) or ChromaDB or Milvus

## Quickstart

1. Python 3.11+ recommended.
2. Install deps:

```bash
pip install -r requirements.txt
```

3. Configure env (optional):

Copy `.env.example` to `.env` and set values as needed. Or export env vars directly.

- CORS: `CORS_ALLOW_ORIGINS=*`
- Generic model: `MODEL_BASE_URL`, `MODEL_PATH` (defaults to `/model/infer`)
- Ollama: `OLLAMA_BASE_URL`, `OLLAMA_MODEL`
- vLLM (OpenAI-compatible): `OPENAI_BASE_URL`, `OPENAI_API_KEY`, `OPENAI_MODEL`
- Whisper: `WHISPER_MODE=mock` (default) or `local` (requires `whisper`)
- ElevenLabs: `ELEVEN_API_KEY`, `ELEVEN_VOICE_ID`

- Retrieval & Memory:
  - `RETRIEVAL_ENABLED=true`
  - `VECTOR_BACKEND=file|chroma|milvus`
  - `HISTORY_MESSAGES=6`
  - ChromaDB: `CHROMA_DIR=./backend/data/chroma`, `EMBEDDING_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2`
  - Milvus: `MILVUS_HOST`, `MILVUS_PORT`, optional `MILVUS_USER`, `MILVUS_PASSWORD`, `MILVUS_DB`, `MILVUS_COLLECTION`, `MILVUS_INDEX_TYPE`, `MILVUS_METRIC_TYPE`

4. Run dev server:

```bash
uvicorn main:app --reload --port 8000
```

5. Test endpoints:

- Health: `GET http://localhost:8000/health`
- Chat (TTS optional):

```bash
curl -s http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"I wish I could talk to you again.","persona":"emma","mode":"text","tts":true}' | jq
```

- STT mock:

```bash
curl -s -F file=@/path/to/audio.wav http://localhost:8000/stt/upload | jq
```

- TTS mock:

```bash
curl -s http://localhost:8000/tts/speak \
  -H "Content-Type: application/json" \
  -d '{"text":"It\'s okay to move on."}' | jq
```

- Ingest files (RAG memory):

```bash
curl -s -F files=@/path/to/chats.txt \
         -F files=@/path/to/export.json \
         -F source=whatsapp \
         -F tags="nostalgia,trip" \
         http://localhost:8000/ingest/upload | jq
```

- Finetune (mock):

```bash
JOB=$(curl -s http://localhost:8000/finetune/start -H "Content-Type: application/json" -d '{"dataset_hint":"memory"}' | jq -r .job_id)
curl -s http://localhost:8000/finetune/status/$JOB | jq
```

- Memory upload:

```bash
curl -s http://localhost:8000/memory/upload \
  -H "Content-Type: application/json" \
  -d '{"text":"I remember our first trip to Goa...","tags":["happy","nostalgia"]}' | jq
```

- Export zip:

```bash
curl -s -o helloex_export.zip http://localhost:8000/export
```

## Notes

- If no model is configured, `/chat` returns a sensible mock reply and can still produce TTS (dummy WAV).
- If ElevenLabs is not configured, TTS returns a generated dummy WAV file mounted under `/static/audio/...`.
- Whisper `local` mode requires the `whisper` package and local model; otherwise `mock` mode returns a fixed transcript.
- Retrieval uses the active vector backend configured via `VECTOR_BACKEND`. Ingestion populates that backend and `/chat` performs top-k retrieval (if `RETRIEVAL_ENABLED=true`) and also includes the last `HISTORY_MESSAGES` from `messages.jsonl` as conversational buffer.

## Retrieval Backends

- File (default): simple JSONL at `data/storage/memory.jsonl` with naive cosine similarity over `utils.text_utils.simple_embed()`.
- ChromaDB: embedded persistent vector DB using sentence-transformers. Enable with `VECTOR_BACKEND=chroma`. Install extras from `requirements.txt`.
- Milvus: scalable vector DB. Enable with `VECTOR_BACKEND=milvus` and set connection vars. Collection and index are auto-created on startup.

See `docs/retrieval_memory_flow.md` for an end-to-end diagram and request flow details.
