import logging
from assistant.tts import speak
from commands import apps, web, keyboard
from memory.memory_manager import remember_fact, show_all_memory, forget_fact, get_user_name
from data_manager import save_interaction

logger = logging.getLogger(__name__)

def process_command(text: str) -> bool:
    """Zpracuje prikaz. Vraci False pokud ma asistent skoncit."""
    if not text:
        speak("Nerozumel jsem, zkus to znovu.")
        save_interaction(text, "nerozumel", "Nerozumel jsem.", None)
        return True

    response = ""
    error = None

    try:
        # Ukonceni
        if any(k in text for k in ["konec", "vypni se", "skonci", "ukoncit"]):
            speak("Dobra, vypinam se. Na shledanou.")
            save_interaction(text, "vypnuti", "Vypinam se.", None)
            return False

        # Pamet: zapamatuj si
        if "zapamatuj si" in text or "pamatuj si" in text:
            fact = text.replace("zapamatuj si", "").replace("pamatuj si", "").replace("ze", "").strip()
            remember_fact(fact)
            response = f"Zapamatuji si: {fact}"
            speak(response)
            save_interaction(text, "remember", response, None)
            return True

        # Pamet: zapomen
        if "zapomen" in text:
            fact = text.replace("zapomen", "").strip()
            forget_fact(fact)
            response = f"Smazal jsem z pameti: {fact}"
            speak(response)
            save_interaction(text, "forget", response, None)
            return True

        # Pamet: co o mne vis
        if "co o mne vis" in text or "ukaz pamet" in text:
            memory = show_all_memory()
            response = "Vim o tobe: " + "; ".join(memory) if memory else "Zatim o tobe nic nevim."
            speak(response)
            save_interaction(text, "show_memory", response, None)
            return True

        # Jak se jmenuji
        if "jak se jmenuji" in text:
            name = get_user_name()
            response = f"Jmenujes se {name}." if name else "Neznam tvoje jmeno."
            speak(response)
            save_interaction(text, "get_name", response, None)
            return True

        # Napsat text
        if text.startswith("napis "):
            to_type = text[6:].strip()
            keyboard.type_text(to_type)
            response = f"Napsal jsem: {to_type}"
            speak(response)
            save_interaction(text, "type_text", response, None)
            return True

        # Otevrit web
        if "otevri web" in text or "otevri stranku" in text:
            url = text.replace("otevri web", "").replace("otevri stranku", "").strip()
            web.open_url(url)
            response = f"Oteviram: {url}"
            speak(response)
            save_interaction(text, "open_url", response, None)
            return True

        # === APLIKACE - VSE CESKY ===
        if "kalkulacka" in text or "kalkulator" in text:
            apps.open_calculator()
            speak("Oteviram kalkulacku.")
            save_interaction(text, "calc", "Oteviram kalkulacku.", None)
            return True
            
        if "poznamkovy blok" in text or "notepad" in text or "blok" in text:
            apps.open_notepad()
            speak("Oteviram poznamkovy blok.")
            save_interaction(text, "notepad", "Oteviram poznamkovy blok.", None)
            return True
            
        if "pruzkumnik" in text or "soubory" in text:
            apps.open_explorer()
            speak("Oteviram pruzkumnik souboru.")
            save_interaction(text, "explorer", "Oteviram pruzkumnik.", None)
            return True
            
        if "spravce uloh" in text or "task manager" in text:
            apps.open_task_manager()
            speak("Oteviram spravce uloh.")
            save_interaction(text, "taskmgr", "Oteviram spravce uloh.", None)
            return True

        # === WEBY - VSE CESKY ===
        if "jutjub" in text or "youtube" in text:
            web.open_youtube()
            speak("Oteviram YouTube.")
            save_interaction(text, "youtube", "Oteviram YouTube.", None)
            return True
            
        if "gugl" in text or "google" in text:
            web.open_google()
            speak("Oteviram Google.")
            save_interaction(text, "google", "Oteviram Google.", None)
            return True
            
        if "githab" in text or "github" in text:
            web.open_github()
            speak("Oteviram GitHub.")
            save_interaction(text, "github", "Oteviram GitHub.", None)
            return True
            
        if "wikiped" in text or "vikipedie" in text:
            web.open_wikipedia()
            speak("Oteviram Wikipedii.")
            save_interaction(text, "wikipedia", "Oteviram Wikipedii.", None)
            return True

        # Neznamy prikaz
        response = f"Prikaz '{text}' neznam."
        speak(response)
        save_interaction(text, "unknown", response, None)

    except Exception as e:
        error = str(e)
        speak("Nastala chyba, zkontroluj log.")
        logger.error(f"Chyba pri zpracovani prikazu '{text}': {e}")
        save_interaction(text, "error", f"Chyba: {error}", error)

    return True
