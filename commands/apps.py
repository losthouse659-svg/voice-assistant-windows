import subprocess
import json
import logging

logger = logging.getLogger(__name__)

def _check_whitelist(app_name: str) -> bool:
    try:
        with open("config/whitelist.json", "r", encoding="utf-8") as f:
            whitelist = json.load(f)
        return app_name.lower() in [a.lower() for a in whitelist.get("allowed_apps", [])]
    except Exception:
        return False

def _run(cmd: str):
    app = cmd.split()[0]
    if not _check_whitelist(app):
        logger.warning(f"Aplikace '{app}' neni na whitelistu.")
        raise PermissionError(f"Aplikace '{app}' neni povolena.")
    subprocess.Popen(cmd, shell=True)
    logger.info(f"Spusteno: {cmd}")

def open_calculator():
    _run("calc")

def open_notepad():
    _run("notepad")

def open_explorer():
    _run("explorer")

def open_task_manager():
    _run("taskmgr")

def open_paint():
    _run("mspaint")

def open_cmd():
    _run("cmd")

def gaming_mode():
    """Spustí herí ní mód - Discord, Steam a CS2."""
    logger.info("Spouštím herí ní mód...")
    
    # Spusť Discord
    try:
        _run("discord")
        logger.info("Discord spuštěn")
    except Exception as e:
        logger.error(f"Chyba při spuštění Discord: {e}")
    
    # Spusť Steam
    try:
        _run("steam")
        logger.info("Steam spuštěn")
    except Exception as e:
        logger.error(f"Chyba při spuštění Steam: {e}")
    
    # Spusť CS2 (Counter-Strike 2)
    try:
        # CS2 se spouští přes Steam URL
        subprocess.Popen(["start", "steam://rungameid/730"], shell=True)
        logger.info("CS2 spuštěno")
    except Exception as e:
        logger.error(f"Chyba při spuštění CS2: {e}")
    
    return True

def open_app(app_name: str):
    """Univerzální funkce pro otevření aplikace."""
    return _run(app_name)
