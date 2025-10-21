import io

def test_stt_upload_mock(client):
    # 1 second of silence wav header (not necessary since mock ignores content)
    buf = io.BytesIO(b"fake-audio")
    files = {"file": ("sample.wav", buf, "audio/wav")}
    r = client.post("/stt/upload", files=files)
    assert r.status_code == 200
    data = r.json()
    assert "transcript" in data
    assert data.get("language") in (None, "en")
