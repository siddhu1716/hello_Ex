import json

def test_chat_mock_reply(client):
    payload = {
        "message": "I wish I could talk to you again.",
        "persona": "emma",
        "mode": "text",
        "tts": False,
    }
    r = client.post("/chat", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "reply_text" in data and isinstance(data["reply_text"], str)
    assert data.get("audio_url") in (None, data.get("audio_url"))


def test_chat_with_tts(client):
    payload = {
        "message": "Please say something nice.",
        "tts": True,
    }
    r = client.post("/chat", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "reply_text" in data
    # In mock mode TTS produces a dummy wav path
    if data.get("audio_url"):
        assert data["audio_url"].startswith("/static/audio/")
