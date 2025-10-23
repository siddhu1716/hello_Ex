import os
from utils.text_utils import append_message, get_recent_messages
from config import settings


def test_get_recent_messages_returns_last_n(tmp_path):
    # isolate messages file to temp dir
    settings.DATA_DIR = str(tmp_path)
    settings.MESSAGES_FILE = os.path.join(settings.DATA_DIR, "messages.jsonl")
    os.makedirs(settings.DATA_DIR, exist_ok=True)

    # write messages via append_message
    for i in range(10):
        append_message("user" if i % 2 == 0 else "assistant", f"m{i}")

    # fetch last 4
    msgs = get_recent_messages(4)
    assert len(msgs) == 4
    assert msgs[0]["content"] == "m6"
    assert msgs[1]["content"] == "m7"
    assert msgs[2]["content"] == "m8"
    assert msgs[3]["content"] == "m9"
