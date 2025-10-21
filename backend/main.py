import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import JSONResponse
from routers import chat, stt, tts, memory
from config import settings

app = FastAPI(title="helloEx Backend", version="0.1.0")

# CORS via settings
allowed_origins = [o.strip() for o in (settings.CORS_ALLOW_ORIGINS or "*").split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(chat.router, prefix="", tags=["chat"])
app.include_router(stt.router, prefix="", tags=["stt"])
app.include_router(tts.router, prefix="", tags=["tts"])
app.include_router(memory.router, prefix="", tags=["memory"])

# Serve static files from storage directory so /static/audio works
app.mount("/static", StaticFiles(directory=settings.DATA_DIR), name="static")


@app.get("/health")
async def health():
    return JSONResponse({"status": "ok"})


# Uvicorn entrypoint helper
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=True)
