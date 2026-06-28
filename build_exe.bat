@echo off
echo ============================================
echo  BUILD: Hlasovy asistent -> .EXE
echo ============================================

REM Zkontroluj Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo CHYBA: Python nenalezen v PATH!
    pause
    exit /b 1
)

REM Nainstaluj PyInstaller pokud chybi
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo Instaluji PyInstaller...
    pip install pyinstaller
)

REM Build
echo Spoustim build...
pyinstaller --onefile --noconsole --name VoiceAssistant ^  
    --add-data "config;config" ^  
    --add-data "models;models" ^  
    --add-data "data;data" ^  
    main.py

echo.
echo ============================================
if exist dist\VoiceAssistant.exe (
    echo  BUILD USPESNY!
    echo  EXE je v: dist\VoiceAssistant.exe
) else (
    echo  BUILD SELHAL - zkontroluj chyby vyse
)
echo ============================================
pause
