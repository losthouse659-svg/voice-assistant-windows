@echo off
echo Spoustim hlasoveho asistenta...
cd /d "%~dp0"
python main.py
if %errorlevel% neq 0 (
    echo.
    echo CHYBA pri spusteni! Zkontroluj:
    echo 1. Jsi ve spravne slozce?
    echo 2. Jsou nainstalovane balicky? (pip install -r requirements.txt)
    echo 3. Je Vosk model v models/ slozce?
    pause
)
pause
