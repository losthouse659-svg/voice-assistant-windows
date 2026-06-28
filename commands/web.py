import webbrowser
import subprocess
import logging

logger = logging.getLogger(__name__)

# Whitelist povolených domén
WHITELIST = [
    "youtube.com",
    "google.com",
    "google.cz",
    "wikipedia.org",
    "github.com",
    "stackoverflow.com",
    "reddit.com",
    "facebook.com",
    "twitter.com",
    "instagram.com",
    "twitch.tv",
    "discord.com"
]

def open_website(query: str):
    """Otevře webovou stránku na základě dotazu."""
    query = query.lower().strip()
    
    # Zkratky pro populární weby
    shortcuts = {
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "wikipedi": "https://www.wikipedia.org",
        "github": "https://github.com",
        "stackoverflow": "https://stackoverflow.com",
        "reddit": "https://www.reddit.com",
        "facebook": "https://www.facebook.com",
        "twitter": "https://twitter.com",
        "instagram": "https://www.instagram.com",
        "twitch": "https://www.twitch.tv",
        "discord": "https://discord.com"
    }
    
    # Zkontroluj zkratky
    for key, url in shortcuts.items():
        if key in query:
            logger.info(f"Otevírám {url}")
            webbrowser.open(url)
            return True
    
    # Pokud obsahuje .cz, .com atd., otevři přímo
    if "." in query:
        url = query if query.startswith("http") else f"https://{query}"
        logger.info(f"Otevírám URL: {url}")
        webbrowser.open(url)
        return True
import webbrowser
import subprocess
import os
import logging    # Jinak vyhledej na Googlu
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    logger.info(f"Vyhledávám na Googlu: {query}")
    webbrowser.open(search_url)
    return True

def open_comet():
    """Otevře prohlížeč Comet."""
    try:
        # Zkus najít Comet v běžných umístěních
        paths = [
            r"C:\\Program Files\\Comet\\Comet.exe",
            r"C:\\Program Files (x86)\\Comet\\Comet.exe",
            r"C:\\Users\\{}\\AppData\\Local\\Comet\\Comet.exe".format(os.getenv('USERNAME'))
        ]
        
        for path in paths:
            if os.path.exists(path):
                subprocess.Popen([path])
                logger.info(f"Otevírám Comet: {path}")
                return True
        
        # Pokud není nalezen, zkus otevřít přes start
        subprocess.Popen(["start", "comet"], shell=True)
        logger.info("Otevírám Comet přes start menu")
        return True
        
    except Exception as e:
        logger.error(f"Chyba při otevírání Comet: {e}")
        return False
