import pyttsx3
import json
import logging

logger = logging.getLogger(__name__)

def get_engine():
    with open("config/settings.json", "r", encoding="utf-8") as f:
        settings = json.load(f)
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    voice_index = settings.get("tts_voice_index", 0)
    if voices and voice_index < len(voices):
        engine.setProperty("voice", voices[voice_index].id)
    engine.setProperty("rate", settings.get("tts_rate", 160))
    engine.setProperty("volume", settings.get("tts_volume", 1.0))
    return engine

_engine = None

def speak(text: str):
    global _engine
    if _engine is None:
        _engine = get_engine()
    logger.info(f"TTS: {text}")
    print(f"[Asistent]: {text}")
    _engine.say(text)
    _engine.runAndWait()
