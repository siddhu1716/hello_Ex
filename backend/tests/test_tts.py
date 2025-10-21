def test_tts_speak_mock(client):
    payload = {"text": "This is a test."}
    r = client.post("/tts/speak", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "audio_url" in data
    assert data["audio_url"].startswith("/static/audio/")
