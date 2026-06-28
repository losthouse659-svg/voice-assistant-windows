# Voice Assistant Windows

Offline hlasovy asistent pro Windows. Zdarma, bez internetu, ovlada PC hlasem.

## Co umi
- Poslouchá mikrofon a rozpoznává hlas offline (Vosk)
- Mluví zpět hlasem (pyttsx3)
- Otvírá aplikace: kalkulačka, notepad, průzkumník, správce úloh
- Otvírá weby: YouTube, Google, GitHub, Wikipedia
- Píše diktovaný text do aktivního okna
- Pamatuje si informace o uživateli (SQLite)
- Ukládá historii příkazů (SQLite)
- Jde spustit jako .exe přes PyInstaller

## Struktura projektu
```
voice-assistant-windows/
├── main.py                  # Hlavní spouštěč
├── requirements.txt         # Python závislosti
├── build_exe.bat            # Build do .exe
├── launcher.bat             # Rychlé spuštění
├── README.md
├── .gitignore
├── assistant/
│   ├── tts.py               # Text-to-speech
│   ├── stt.py               # Speech-to-text (Vosk)
│   ├── listener.py          # Mikrofon + wake word
│   └── dispatcher.py        # Zpracování příkazů
├── commands/
│   ├── apps.py              # Spouštění aplikací
│   ├── web.py               # Otevírání webů
│   └── keyboard.py          # Psaní textu
├── config/
│   ├── settings.json        # Nastavení
│   └── whitelist.json       # Povolené příkazy
├── memory/
│   └── memory_manager.py    # Paměť uživatele
├── data_manager.py          # Historie
├── models/                  # Vosk model (nestahovat z GitHubu)
├── data/                    # SQLite databáze (generuje se automaticky)
└── logs/                    # Logy
```

## Instalace

### 1. Stáhnout projekt
```
git clone https://github.com/losthouse659-svg/voice-assistant-windows.git
cd voice-assistant-windows
```

### 2. Nainstalovat balíčky
```
pip install -r requirements.txt
```

### 3. Stáhnout Vosk model
1. Jdi na https://alphacephei.com/vosk/models
2. Stáhni **vosk-model-small-cs-0.4-rhasspy** (český model)
3. Rozbal ho do složky `models/`
4. Výsledek: `models/vosk-model-small-cs-0.4-rhasspy/`

## Spuštění

### Přes Python:
```
python main.py
```

### Přes launcher.bat:
Dvakrát klikni na `launcher.bat`

## Build do .EXE

```
build_exe.bat
```

Nebo ručně:
```
pip install pyinstaller
pyinstaller --onefile --noconsole --name VoiceAssistant --add-data "config;config" --add-data "models;models" --add-data "data;data" main.py
```

Výsledný .exe je v: `dist/VoiceAssistant.exe`

**Pozor:** Složky `models/`, `config/` a `data/` musí být vedle .exe souboru při spuštění!

## Hlasové příkazy

Nejdřív řekni klíčové slovo: **"asistente"**

Pak řekni příkaz:

| Příkaz | Akce |
|--------|------|
| kalkulačka / kalkulator | Otevře kalkulačku |
| notepad / poznámkový blok | Otevře Notepad |
| průzkumník | Otevře Průzkumník souborů |
| správce úloh | Otevře Task Manager |
| youtube | Otevře YouTube |
| google | Otevře Google |
| github | Otevře GitHub |
| wikipedia | Otevře Wikipedii |
| napiš [text] | Napíše text do aktivního okna |
| otevři web [url] | Otevře zadaný web |
| zapamatuj si [fakt] | Uloží informaci |
| co o mně víš | Vypíše paměť |
| zapomeň [fakt] | Smaže z paměti |
| jak se jmenuji | Řekne uložené jméno |
| konec / vypni se | Ukončí asistenta |

## Přidání nového příkazu

Otevři `assistant/dispatcher.py` a přidej nový blok:
```python
if "muj_prikaz" in text:
    # co ma udelat
    speak("Hotovo.")
    save_interaction(text, "muj_prikaz", "Hotovo.", None)
    return True
```

## Historie a paměť

Oboje je uloženo v: `data/assistant.db`

- **Historie**: tabulka `history` - čas, příkaz, akce, odpověď, chyba
- **Paměť**: tabulka `memory` - uložené fakty o uživateli

## Řešení problémů

**Mikrofon nejde:**
- Zkontroluj Nastavení Windows > Soukromí > Mikrofon
- Spusť jako administrátor
- Zkus `python -c "import sounddevice; print(sounddevice.query_devices())"`

**Vosk model nenalezen:**
- Zkontroluj cestu v `config/settings.json` → `vosk_model_path`
- Složka musí existovat: `models/vosk-model-small-cs-0.4-rhasspy/`

**pyttsx3 nemluví:**
- Zkontroluj hlasové balíčky Windows: Nastavení > Čas a jazyk > Řeč
- Zkus změnit `tts_voice_index` v settings.json na 1 nebo 2

**EXE nenajde data:**
- Zkopíruj složky `config/`, `models/`, `data/` vedle `VoiceAssistant.exe`

## Omezení
- Vosk model pro češtinu je menší = nižší přesnost než Google Speech
- pyautogui.write() nefunguje správně s diakritikou
- EXE build může být velký (100-500 MB kvůli Vosk modelu)
- Asistent musí být aktivní okno při psaní textu
