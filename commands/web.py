import webbrowser
import json
import logging

logger = logging.getLogger(__name__)

def _check_whitelist(domain: str) -> bool:
    try:
        with open("config/whitelist.json", "r", encoding="utf-8") as f:
            whitelist = json.load(f)
        allowed = whitelist.get("allowed_websites", [])
        return any(d in domain for d in allowed)
    except Exception:
        return False

def open_url(url: str):
    if not url.startswith("http"):
        url = "https://" + url
    if not _check_whitelist(url):
        logger.warning(f"Web '{url}' neni na whitelistu.")
        raise PermissionError(f"Web '{url}' neni povolen.")
    webbrowser.open(url)
    logger.info(f"Otevren web: {url}")

def open_youtube():
    webbrowser.open("https://www.youtube.com")

def open_google():
    webbrowser.open("https://www.google.com")

def open_wikipedia():
    webbrowser.open("https://cs.wikipedia.org")

def open_github():
    webbrowser.open("https://www.github.com")
