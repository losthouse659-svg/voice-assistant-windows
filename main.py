import logging
import os
import sys
from assistant.listener import wait_for_wake_word, listen_command
from assistant.dispatcher import process_command
from assistant.tts import speak
from assistant.stt import load_model

def setup_logging():
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler("logs/assistant.log", encoding="utf-8"),
            logging.StreamHandler(sys.stdout)
        ]
    )

def main():
    setup_logging()
    logger = logging.getLogger("main")
    logger.info("Spoustim hlasoveho asistenta...")

    print("="*50)
    print(" HLASOVY ASISTENT - Windows")
    print(" Klicove slovo: 'asistente'")
    print(" Pro ukonceni rekni: 'konec' nebo 'vypni se'")
    print("="*50)

    try:
        speak("Nahravam model rozpoznavani hlasu, chvilku strpeni.")
        load_model()
        speak("Asistent je pripraveny. Rekni 'asistente' pro aktivaci.")
    except FileNotFoundError as e:
        print(f"CHYBA: {e}")
        logger.error(f"Nelze spustit asistenta: {e}")
        sys.exit(1)

    running = True
    while running:
        try:
            if wait_for_wake_word():
                command = listen_command()
                logger.info(f"Prikaz: '{command}'")
                running = process_command(command)
        except KeyboardInterrupt:
            speak("Preruseni. Na shledanou.")
            break
        except Exception as e:
            logger.error(f"Nezachycena chyba: {e}")
            speak("Nastala neocekavana chyba.")

    logger.info("Asistent ukoncen.")
    print("Asistent ukoncen.")

if __name__ == "__main__":
    main()
