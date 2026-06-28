import pyautogui
import time
import logging

logger = logging.getLogger(__name__)

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1

def type_text(text: str):
    """Napise text do aktivniho okna."""
    if not text:
        return
    logger.info(f"Pisu text: {text}")
    time.sleep(0.5)
    pyautogui.write(text, interval=0.05)

def press_key(key: str):
    """Stiskne klavesu."""
    logger.info(f"Stiskam klavesu: {key}")
    pyautogui.press(key)

def hotkey(*keys):
    """Stiskne kombinaci klaves."""
    logger.info(f"Kombinace klaves: {keys}")
    pyautogui.hotkey(*keys)

def copy_text():
    hotkey('ctrl', 'c')

def paste_text():
    hotkey('ctrl', 'v')

def select_all():
    hotkey('ctrl', 'a')
