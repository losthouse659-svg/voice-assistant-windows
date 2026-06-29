import customtkinter as ctk
import threading
import logging
from assistant.listener import wait_for_wake_word, listen_command
from assistant.dispatcher import process_command
from assistant.stt import load_model
from assistant.tts import speak

logger = logging.getLogger(__name__)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class VoiceAssistantGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Voice Assistant")
        self.root.geometry("700x750")
        self.root.resizable(False, False)
        
        self.running = False
        self.thread = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Header
        header = ctk.CTkLabel(
            self.root,
            text="VOICE ASSISTANT",
            font=("Arial", 32, "bold"),
            text_color="#00d4ff"
        )
        header.pack(pady=15)
        
        # Tabview - Zalozky
        self.tabview = ctk.CTkTabview(self.root, width=650, height=580)
        self.tabview.pack(pady=10)
        
        # Pridat zalozky
        self.tabview.add("Asistent")
        self.tabview.add("Prikazy")
        
        # === ZALOZKA: Asistent ===
        self.setup_assistant_tab()
        
        # === ZALOZKA: Prikazy ===
        self.setup_commands_tab()
        
        # Wake word info (spodni)
        info_label = ctk.CTkLabel(
            self.root,
            text='Klicove slovo: "asistente"',
            font=("Arial", 12),
            text_color="#888888"
        )
        info_label.pack(pady=5)
        
    def setup_assistant_tab(self):
        """Nastaveni zalozky Asistent"""
        tab = self.tabview.tab("Asistent")
        
        # Status indicator
        self.status_frame = ctk.CTkFrame(tab, fg_color="transparent")
        self.status_frame.pack(pady=10)
        
        self.status_dot = ctk.CTkLabel(
            self.status_frame,
            text="\u25cf",
            font=("Arial", 40),
            text_color="#ff3333"
        )
        self.status_dot.pack(side="left", padx=10)
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Vypnuto",
            font=("Arial", 18)
        )
        self.status_label.pack(side="left")
        
        # Log area
        log_label = ctk.CTkLabel(
            tab,
            text="Aktivita:",
            font=("Arial", 14, "bold")
        )
        log_label.pack(pady=(10, 5))
        
        self.log_text = ctk.CTkTextbox(
            tab,
            width=600,
            height=300,
            font=("Consolas", 11),
            fg_color="#1a1a1a",
            text_color="#00ff00"
        )
        self.log_text.pack(pady=10)
        
        # Control buttons
        button_frame = ctk.CTkFrame(tab, fg_color="transparent")
        button_frame.pack(pady=15)
        
        self.start_btn = ctk.CTkButton(
            button_frame,
            text="START",
            width=150,
            height=50,
            font=("Arial", 16, "bold"),
            fg_color="#00aa00",
            hover_color="#00cc00",
            command=self.start_assistant
        )
        self.start_btn.pack(side="left", padx=10)
        
        self.stop_btn = ctk.CTkButton(
            button_frame,
            text="STOP",
            width=150,
            height=50,
            font=("Arial", 16, "bold"),
            fg_color="#aa0000",
            hover_color="#cc0000",
            command=self.stop_assistant,
            state="disabled"
        )
        self.stop_btn.pack(side="left", padx=10)
        
    def setup_commands_tab(self):
        """Nastaveni zalozky Prikazy"""
        tab = self.tabview.tab("Prikazy")
        
        # Nadpis
        title = ctk.CTkLabel(
            tab,
            text="Vsechny dostupne prikazy:",
            font=("Arial", 16, "bold"),
            text_color="#00d4ff"
        )
        title.pack(pady=10)
        
        # Seznam prikazu
        commands_text = ctk.CTkTextbox(
            tab,
            width=600,
            height=450,
            font=("Consolas", 12),
            fg_color="#1a1a1a",
            text_color="#ffffff"
        )
        commands_text.pack(pady=10)
        
        # Obsah prikazu
        commands_list = """
=== APLIKACE ===
kalkulacka / kalkulator           -> Otevre kalkulacku
poznamkovy blok / notepad / blok  -> Otevre Notepad
pruzkumnik / soubory              -> Otevre Pruzkumnik souboru
spravce uloh / task manager       -> Otevre Task Manager

=== WEBY ===
jutjub / youtube                  -> Otevre YouTube
gugl / google                     -> Otevre Google
githab / github                   -> Otevre GitHub
wikiped / vikipedie               -> Otevre Wikipedii
otevri web [url]                  -> Otevre zadany web

=== PSANI TEXTU ===
napis [text]                      -> Napise text do aktivniho okna

=== PAMET ===
zapamatuj si [info]               -> Ulozi informaci
pamatuj si [info]                 -> Ulozi informaci
co o mne vis                      -> Vypise celou pamet
ukaz pamet                        -> Vypise celou pamet
zapomen [info]                    -> Smaze z pameti
jak se jmenuji                    -> Rekne ulozene jmeno

=== UKONCENI ===
konec / vypni se / skonci         -> Vypne asistenta

=== JAK POUZIVAT ===
1. Klikni START
2. Rekni "asistente"
3. Pocka na "Co mam udelat?"
4. Rekni prikaz (napr. "kalkulacka")
        """
        
        commands_text.insert("0.0", commands_list)
        commands_text.configure(state="disabled")
        
    def log(self, message: str, color="#00ff00"):
        """Prida zpravu do log okna"""
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"{message}\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")
        
    def set_status(self, text: str, color: str):
        """Nastavi status asistenta"""
        self.status_label.configure(text=text)
        self.status_dot.configure(text_color=color)
        
    def start_assistant(self):
        if self.running:
            return
            
        self.running = True
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.set_status("Spoustim...", "#ffaa00")
        self.log("[SYSTEM] Nahravam Vosk model...")
        
        self.thread = threading.Thread(target=self.assistant_loop, daemon=True)
        self.thread.start()
        
    def stop_assistant(self):
        self.running = False
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.set_status("Vypnuto", "#ff3333")
        self.log("[SYSTEM] Asistent vypnut.")
        
    def assistant_loop(self):
        try:
            load_model()
            self.log("[SYSTEM] Model nahran.")
            self.set_status("Continuous Listening - Posloucham prikazy", "#00ff00")
            speak("Posloucham. Rekni 'ztlum se' pro pauzu nebo 'konec' pro ukonceni.")
            self.log("[SYSTEM] Continuous listening aktivni - zadny wake word potreba.")
            
            while self.running:
                command = listen_command()
                self.log(f"[USER] Prikaz: '{command}'")
                
                if command:
                    continue_running = process_command(command)
                    self.log(f"[ASSISTANT] Zpracovano: '{command}'")
                    
                    if not continue_running:
                        self.running = False
                        self.root.after(0, self.stop_assistant)
                        break                    
        except FileNotFoundError as e:
            self.log(f"[ERROR] {e}")
            self.log("[ERROR] Spust install_model.bat")
            self.running = False
            self.root.after(0, self.stop_assistant)
        except Exception as e:
            self.log(f"[ERROR] {e}")
            logger.error(f"Chyba v assistant_loop: {e}")
            self.running = False
            self.root.after(0, self.stop_assistant)
            
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = VoiceAssistantGUI()
    app.run()
