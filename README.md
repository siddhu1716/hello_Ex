# helloEx — AI Closure Companion

Chat with a compassionate simulation of someone from your past by uploading real chat history. helloEx builds a persona from your memories and lets you have thoughtful, empathetic conversations for reflection and closure.

## 🧠 Concept

Upload chat exports (e.g., WhatsApp, iMessage, Telegram) and talk to an AI that mimics tone, style, and common phrases from selected memories. Choose modes (Nostalgia, Cold, Honest, etc.) and optionally hear the AI reply with voice.

## 🌟 MVP Features

- **Chat upload + parsing** (planned): support `.txt`/`.json` exports and extract speakers, timestamps, tone
- **AI persona simulation**: prompt-built persona with simple memory retrieval
- **Live chat**: send messages and get instant replies
- **Voice options**: STT (speech-to-text) and TTS (text-to-speech) paths

## 🎯 Full Vision (Selected Highlights)

- **Chat Modes**: Nostalgia, Cold, Honest, Ideal Future, Therapist
- **Timeline Conversations**: pick a relationship era to simulate tone
- **Mood/Persona Sliders**: Emotional ↔ Logical, Realism ↔ Fantasy, Intimacy ↔ Distant
- **Voice Integration**: ElevenLabs (or fallback) for persona voice
- **Memory Scrapbook**: milestones and notable messages
- **What-If Scenarios**: alternate branches of conversations

## ⚙️ Architecture

- **Frontend**: React + Vite app in `helloEx_frontend/`
- **Backend**: FastAPI app in `backend/`
  - Endpoints: `/chat`, `/stt/upload`, `/tts/speak`, `/memory/upload`, `/export`, `/health`
  - Integrations:
    - Model via REST: vLLM (OpenAI-compatible), Ollama, or generic endpoint (with mock fallback)
    - Whisper STT: local or mock
    - ElevenLabs TTS: real if configured, else dummy WAV
  - Storage: `backend/data/storage/` for messages (`messages.jsonl`), memories (`memory.jsonl`), audio (`audio/`)

## 🚀 Quickstart

### Backend (FastAPI)

1) Install dependencies:

```bash
cd backend
pip install -r requirements.txt
```

2) Configure environment (optional):

```bash
cp .env.example .env
# edit .env with your model/TTS settings if available
```

3) Run dev server:

```bash
uvicorn main:app --reload --port 8000
```

4) Try the API:

```bash
# Health
curl -s http://localhost:8000/health

# Chat (with optional TTS)
curl -s http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"I wish I could talk to you again.","persona":"emma","mode":"text","tts":true}' | jq

# STT (mock by default)
curl -s -F file=@/path/to/audio.wav http://localhost:8000/stt/upload | jq

# TTS (dummy WAV without ElevenLabs)
curl -s http://localhost:8000/tts/speak \
  -H "Content-Type: application/json" \
  -d '{"text":"It\'s okay to move on."}' | jq
```

### Frontend (Vite React)

```bash
cd helloEx_frontend
npm install
npm run dev
```

Configure the frontend to call your backend at `http://localhost:8000` (e.g., via environment or API client).

## 🔌 Model & Voice Configuration

Set these in `backend/.env` (see `.env.example`):

- vLLM (OpenAI-compatible): `OPENAI_BASE_URL`, `OPENAI_API_KEY`, `OPENAI_MODEL`
- Ollama: `OLLAMA_BASE_URL`, `OLLAMA_MODEL`
- Generic model: `MODEL_BASE_URL`, `MODEL_PATH` (default `/model/infer`)
- Whisper: `WHISPER_MODE=mock` or `local` (requires `whisper`)
- ElevenLabs: `ELEVEN_API_KEY`, `ELEVEN_VOICE_ID`

If nothing is configured, the backend uses safe mock fallbacks so you can test end-to-end immediately.

## 🔐 Ethics & Boundaries

- Only upload conversations you have the right to use
- No impersonation without consent
- Not a replacement for therapy; use responsibly

## 📂 Project Layout

- `helloEx_frontend/` — React app (UI)
- `backend/` — FastAPI app
  - `routers/` — HTTP routes (`chat.py`, `stt.py`, `tts.py`, `memory.py`)
  - `services/` — integrations (model proxy, Whisper, ElevenLabs, memory)
  - `utils/` — helpers (prompt building, embeddings, audio)
  - `data/storage/` — messages, memories, audio artifacts

## 🛣️ Roadmap (MVP → Full)

- **MVP**: chat, STT, TTS, memory upload, export, basic persona prompt
- **Next**: chat upload + parser, richer retrieval, mode sliders, timeline simulation, UI polish
- **Later**: advanced memory scrapbook, what-if branching, privacy controls, deploy

