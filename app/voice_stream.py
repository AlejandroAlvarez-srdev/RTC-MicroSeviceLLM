from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import uuid
import tempfile
import os
import subprocess
import numpy as np
import whisper
import soundfile as sf

router = APIRouter()

# ⚠️ Whisper model (puedes cambiar a "small", "medium", etc)
model = whisper.load_model("tiny")


@router.websocket("/voice-stream")
async def voice_stream(ws: WebSocket):
    await ws.accept()
    session_id = str(uuid.uuid4())
    print(f"🔵 Nueva conexión WebSocket: {session_id}")

    audio_buffer = bytearray()

    try:
        while True:
            data = await ws.receive_bytes()
            audio_buffer.extend(data)

            # Procesar cada ~1 segundo (ajustable)
            if len(audio_buffer) > 16000 * 2 * 2:  # 1 segundo approx
                text = transcribe_chunk(audio_buffer)
                await ws.send_text(f"ASR: {text}")
                audio_buffer = bytearray()

            await ws.send_text("ok")

    except WebSocketDisconnect:
        print(f"🔴 Cliente desconectado: {session_id}")


# ============================================
# 🔥 FUNCIÓN COMPLETA PARA TRANSCRIBIR CHUNKS
# ============================================
def transcribe_chunk(chunk_bytes: bytes) -> str:
    """
    Convierte los bytes webm → wav → numpy array → whisper.
    Soluciona errores de Windows, EBML y ffmpeg.
    """

    # 1️⃣ Guardar chunk webm temporal
    fd_webm, path_webm = tempfile.mkstemp(suffix=".webm")
    with os.fdopen(fd_webm, "wb") as f:
        f.write(chunk_bytes)

    # 2️⃣ Convertir a wav (mono, 16kHz)
    fd_wav, path_wav = tempfile.mkstemp(suffix=".wav")
    os.close(fd_wav)

    cmd = [
        "ffmpeg",
        "-y",
        "-i", path_webm,
        "-ac", "1",
        "-ar", "16000",
        "-f", "wav",
        path_wav,
    ]

    try:
        subprocess.run(cmd, capture_output=True, check=True)
    except Exception as e:
        print("❌ FFmpeg ERROR:", e)
        cleanup([path_webm, path_wav])
        return "(ffmpeg error)"

    # 3️⃣ Leer WAV como numpy array
    try:
        audio, sr = sf.read(path_wav)
    except Exception as e:
        print("❌ Error leyendo WAV:", e)
        cleanup([path_webm, path_wav])
        return "(audio error)"

    # 4️⃣ Pasar a Whisper
    try:
        result = model.transcribe(audio, fp16=False)
        text = (result.get("text") or "").strip()
    except Exception as e:
        print("❌ Whisper ERROR:", e)
        cleanup([path_webm, path_wav])
        return "(whisper error)"

    # 5️⃣ Limpiar temporales
    cleanup([path_webm, path_wav])

    print("📝 Transcripción:", text)
    return text


def cleanup(paths):
    """Borra archivos temporales sin generar errores."""
    for p in paths:
        try:
            os.remove(p)
        except:
            pass
