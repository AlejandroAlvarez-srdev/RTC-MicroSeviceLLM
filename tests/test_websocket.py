import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_websocket_connection():
    with client.websocket_connect("/voice-stream") as websocket:
        websocket.send_bytes(b"\x00\x01\x02")
        msg = websocket.receive_text()
        assert msg == "ok"
