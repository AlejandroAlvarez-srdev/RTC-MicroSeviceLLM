from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import uuid

router = APIRouter()

@router.websocket("/voice-stream")
async def voice_stream(ws: WebSocket):
    await ws.accept()
    session_id = str(uuid.uuid4())
    
    print(f"🔵 New Web Socket Connection: {session_id}")

    try:
        while True:
            
            data = await ws.receive_bytes()

            print(f"🎧 Audio recibido conversacional ({len(data)} bytes)")

            await ws.send_text("ok")

    except WebSocketDisconnect:
        print(f"🔴 Disconnected: {session_id}")
