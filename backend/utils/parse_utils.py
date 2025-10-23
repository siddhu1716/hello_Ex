import re
from typing import List, Dict

# Pattern to match WhatsApp-style exports like:
# 12/24/24, 10:05 pm - Alex: Message text
WHATSAPP_PATTERN = re.compile(r"^\d{1,2}/\d{1,2}/\d{2,4},?\s+\d{1,2}:\d{2}\s?(?:AM|PM|am|pm)?\s?-\s(.*?):\s(.*)$")


def parse_whatsapp_pairs(text: str, user_of_interest: str) -> List[Dict[str, str]]:
    pairs: List[Dict[str, str]] = []
    lines = text.splitlines()
    convo: List[Dict[str, str]] = []
    for line in lines:
        m = WHATSAPP_PATTERN.match(line.strip())
        if not m:
            if convo:
                convo[-1]["text"] += " " + line.strip()
            continue
        speaker, msg = m.groups()
        convo.append({"speaker": speaker.strip(), "text": msg.strip()})

    for i in range(1, len(convo)):
        if convo[i]["speaker"] == user_of_interest:
            prev = convo[i - 1]["text"]
            reply = convo[i]["text"]
            if prev and reply:
                pairs.append({"instruction": prev, "response": reply})
    return pairs
