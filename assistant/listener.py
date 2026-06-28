import json
import logging
from assistant.stt import listen_once
from assistant.tts import speak

logger = logging.getLogger(__name__)

def wait_for_wake_word() -> bool:
    with open("config/settings.json", "r", encoding="utf-8") as f:
        settings = json.load(f)
    wake_word = settings.get("wake_word", "asistente").lower()
    print(f"[Cekam na klicove slovo: '{wake_word}']")
    text = listen_once(timeout=4)
    if wake_word in text:
        logger.info("Wake word detekovan.")
        speak("Ano, posloucham.")
        return True
    return False

def listen_command() -> str:
    speak("Co mam udelat?")
    return listen_once(timeout=6)
