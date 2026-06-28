import logging
import os
import sys

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
    logger.info("Spoustim hlasoveho asistenta s GUI...")
    
    # Import GUI
    from gui import VoiceAssistantGUI
    
    # Spust GUI
    app = VoiceAssistantGUI()
    app.run()

if __name__ == "__main__":
    main()
