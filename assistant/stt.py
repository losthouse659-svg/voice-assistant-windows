import json
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import logging
import os
import time

logger = logging.getLogger(__name__)

_model = None
_recognizer = None

def load_model():
    global _model, _recognizer
    with open("config/settings.json", "r", encoding="utf-8") as f:
        settings = json.load(f)
    model_path = settings.get("vosk_model_path", "models/vosk-model-small-cs-0.4-rhasspy")
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Vosk model nenalezen: {model_path}\n"
            "Stahni model z https://alphacephei.com/vosk/models a rozbal ho do slozky models/"
        )
    _model = Model(model_path)
    _recognizer = KaldiRecognizer(_model, 16000)
    logger.info("Vosk model nacten.")

def listen_once(timeout: int = 5) -> str:
    global _recognizer
    if _recognizer is None:
        load_model()
    q = queue.Queue()
    def callback(indata, frames, time_info, status):
        if status:
            logger.warning(f"Mikrofon status: {status}")
        q.put(bytes(indata))
    result_text = ""
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype="int16",
                           channels=1, callback=callback):
        logger.info("Posloucham...")
        start = time.time()
        while time.time() - start < timeout:
            try:
                data = q.get(timeout=0.5)
            except queue.Empty:
                continue
            if _recognizer.AcceptWaveform(data):
                res = json.loads(_recognizer.Result())
                result_text = res.get("text", "")
                if result_text:
                    break
        if not result_text:
            partial = json.loads(_recognizer.PartialResult())
            result_text = partial.get("partial", "")
    logger.info(f"STT vysledek: '{result_text}'")
    return result_text.strip().lower()
