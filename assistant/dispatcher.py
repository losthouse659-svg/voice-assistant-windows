import logging
from assistant.tts import speak
from commands import apps, web, keyboard
from memory.memory_manager import remember_fact, show_all_memory, forget_fact, get_user_name
from data_manager import save_interaction

logger = logging.getLogger(__name__)

# Globální stav pro pause/resume
listening_paused = False
def process_command(text: str) -> bool:
    """Zpracuje příkaz. Vrací False pokud má asistent skončit."""
    if not text:
        speak("Nerozuměl jsem, zkus to znovu.")
        save_interaction(text, "nerozuměl", "Nerozuměl jsem.", None)
        return True
    
    response = ""
    error = None
    
    try:
        global listening_paused
        
        # Pokud je poslouchání pozastaveno, kontroluj jen příkazy na probuzení
        if listening_paused:
            if any(k in text for k in ["probuď se", "probuď", "zapni poslouchání", "zapni", "začni poslouchat"]):
                listening_paused = False
                speak("Poslouchám znovu.")
                save_interaction(text, "resume_listening", "Poslouchání obnoveno.", None)
                return True
            else:
                # Ignoruj všechny ostatní příkazy když je paused
                return True
        
        # Pause listening
        if any(k in text for k in ["ztlum se", "přestaň poslouchat", "vypni poslouchání", "vypni se na chvíli", "pausa"]):
            listening_paused = True
            speak("Ztišuji se. Řekni 'probuď se' pro pokračování.")
            save_interaction(text, "pause_listening", "Poslouchání pozastaveno.", None)
            return True
        
        # Ukončení        # Ukončení
        if any(k in text for k in ["konec", "vypni se", "skonči", "ukončit"]):
            speak("Dobrá, vypínám se. Na shledanou.")
            save_interaction(text, "vypnutí", "Vypínám se.", None)
            return False
        
        # Paměť: zapamatuj si
        if "zapamatuj si" in text or "pamatuj si" in text:
            fact = text.replace("zapamatuj si", "").replace("pamatuj si", "").replace("že", "").strip()
            remember_fact(fact)
            response = f"Zapamatuji si: {fact}"
            speak(response)
            save_interaction(text, "remember", response, None)
            return True
        
        # Paměť: zapomeň
        if "zapomeň" in text:
            fact = text.replace("zapomeň", "").strip()
            forget_fact(fact)
            response = f"Smazal jsem z paměti: {fact}"
            speak(response)
            save_interaction(text, "forget", response, None)
            return True
        
        # Paměť: co o mně víš
        if "co o mně víš" in text or "ukaž paměť" in text:
            memory = show_all_memory()
            response = "Vím o tobě: " + "; ".join(memory) if memory else "Zatím o tobě nic nevím."
            speak(response)
            save_interaction(text, "show_memory", response, None)
            return True
        
        # Jak se jmenuji
        if "jak se jmenuji" in text:
            name = get_user_name()
            response = f"Jmenuješ se {name}." if name else "Neznám tvoje jméno."
            speak(response)
            save_interaction(text, "get_name", response, None)
            return True
        
        # Napsat text
        if text.startswith("napiš "):
            to_type = text[6:].strip()
            keyboard.type_text(to_type)
            response = f"Píšu: {to_type}"
            speak(response)
            save_interaction(text, "type", response, None)
            return True
        
        # Herní mód
        if "herní mód" in text or "herní" in text and "mód" in text or "gaming mode" in text:
            apps.gaming_mode()
            response = "Spouštím herní mód - Discord, Steam a CS2"
            speak(response)
            save_interaction(text, "gaming_mode", response, None)
            return True
        
        # Comet prohlížeč
        if "comet" in text:
            web.open_comet()
            response = "Otevírám Comet prohlížeč"
            speak(response)
            save_interaction(text, "open_comet", response, None)
            return True
        
        # Otevřít aplikaci        if "otevři" in text or "spusť" in text or "spusti" in text:
            app_name = text.replace("otevři", "").replace("spusť", "").replace("spusti", "").strip()
            success = apps.open_app(app_name)
            if success:
                response = f"Otevírám {app_name}"
                speak(response)
                save_interaction(text, "open_app", response, None)
                return True
            else:
                response = f"Nepodařilo se otevřít {app_name}"
                speak(response)
                save_interaction(text, "open_app_failed", response, None)
                return True
        
        # Otevřít webovou stránku
        if "web" in text or "stránku" in text or "stranku" in text:
            url = text.replace("otevři", "").replace("web", "").replace("stránku", "").replace("stranku", "").strip()
            web.open_website(url)
            response = f"Otevírám web: {url}"
            speak(response)
            save_interaction(text, "open_web", response, None)
            return True
        
        # Kalkulačka
        if "kalkulačka" in text or "kalkulacka" in text:
            apps.open_calculator()
            response = "Otevírám kalkulačku"
            speak(response)
            save_interaction(text, "calculator", response, None)
            return True
        
        # Poznámkový blok
        if "poznámkový blok" in text or "poznamkovy blok" in text or "notepad" in text:
            apps.open_notepad()
            response = "Otevírám poznámkový blok"
            speak(response)
            save_interaction(text, "notepad", response, None)
            return True
        
        # Průzkumník
        if "průzkumník" in text or "pruzkumnik" in text or "explorer" in text or "složky" in text or "slozky" in text:
            apps.open_explorer()
            response = "Otevírám průzkumníka"
            speak(response)
            save_interaction(text, "explorer", response, None)
            return True
        
        # Příkaz nebyl rozpoznán
        speak("Nerozuměl jsem tvému příkazu. Zkus to jinak.")
        save_interaction(text, "unknown", "Nerozpoznaný příkaz.", None)
        return True
        
    except Exception as e:
        logger.error(f"Chyba při zpracování příkazu: {e}")
        speak("Nastala chyba při zpracování příkazu.")
        save_interaction(text, "error", str(e), str(e))
        return True
