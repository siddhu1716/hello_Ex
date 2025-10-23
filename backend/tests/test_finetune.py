import io

def test_finetune_whatsapp_endpoint_queues_job(client):
    text = (
        "12/24/24, 10:05 pm - Alex: Hey Sam, are you free tomorrow?\n"
        "12/24/24, 10:07 pm - Sam: Yes, let's catch up in the afternoon.\n"
        "12/24/24, 10:08 pm - Alex: Great, see you then!\n"
    ).encode("utf-8")
    files = {"file": ("whatsapp.txt", io.BytesIO(text), "text/plain")}
    data = {"user_of_interest": "Sam"}
    r = client.post("/finetune/whatsapp", files=files, data=data)
    assert r.status_code == 200
    job = r.json()
    assert "job_id" in job
    # check status endpoint
    r2 = client.get(f"/finetune/status/{job['job_id']}")
    assert r2.status_code == 200
    st = r2.json()
    assert st["job_id"] == job["job_id"]
    assert st["status"] in ("queued", "running", "completed")
