from fastapi import FastAPI
from app.voice_stream import router as voice_stream_router

app = FastAPI(
    title="RTC Voice Microservice",
    version="0.2.0",
    description="Microservicio de voz en tiempo real (WebSocket /voice-stream)"
)

@app.get("/health")
async def health():
    return {"status": "ok"}

app.include_router(voice_stream_router)   