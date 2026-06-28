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
