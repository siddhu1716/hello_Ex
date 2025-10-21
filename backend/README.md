# helloEx Backend (FastAPI)

Modular FastAPI backend that implements the helloEx pipeline:

- **/chat** – chat with persona with memory context and optional TTS
- **/stt/upload** – Whisper speech-to-text (mock or local)
- **/tts/speak** – ElevenLabs text-to-speech (real if configured, else dummy WAV)
- **/memory/upload** – store text memos and build a simple vector memory
- **/export** – download a zip containing messages and any audio artifacts
- **/health** – heartbeat

## Structure

- `main.py` – app bootstrap, CORS, static mount
- `config.py` – centralized environment/settings
- `routers/` – route modules (`chat.py`, `stt.py`, `tts.py`, `memory.py`)
- `services/` – integrations (`ai_service.py`, `whisper_service.py`, `eleven_service.py`, `embedding_service.py`)
- `utils/` – helpers (`text_utils.py`, `audio_utils.py`)
- `data/storage/` – persisted files: `messages.jsonl`, `memory.jsonl`, `audio/*`, `exports/*`

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
