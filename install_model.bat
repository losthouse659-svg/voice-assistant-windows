@echo off
echo ============================================
echo  AUTOMATICKE STAZENI VOSK MODELU (cestina)
echo ============================================
echo.

REM Zkontroluj Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo CHYBA: Python neni nainstalovany!
    echo Stahni Python z https://python.org
    pause
    exit /b 1
)

REM Zkontroluj jestli model uz existuje
if exist "models\vosk-model-small-cs-0.4-rhasspy\" (
    echo Model uz existuje v models\vosk-model-small-cs-0.4-rhasspy\
    echo Neni potreba stahnout znovu.
    pause
    exit /b 0
)

REM Vytvor slozku models
if not exist "models" mkdir models

echo Stahuji Vosk model pro cestinu...
echo (velikost cca 40 MB, muze to chvili trvat)
echo.

python -c "
import urllib.request, zipfile, os, sys
url = 'https://alphacephei.com/vosk/models/vosk-model-small-cs-0.4-rhasspy.zip'
zip_path = 'models/vosk-model-small-cs-0.4-rhasspy.zip'
print('Stahuji:', url)
try:
    urllib.request.urlretrieve(url, zip_path, reporthook=lambda b,bs,ts: print(f'  {min(100,int(b*bs*100/ts))}%%', end='\\r') if ts>0 else None)
    print('\\nRozbaluji...')
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall('models/')
    os.remove(zip_path)
    print('HOTOVO! Model je v models/vosk-model-small-cs-0.4-rhasspy/')
except Exception as e:
    print('CHYBA:', e)
    sys.exit(1)
"

if %errorlevel% neq 0 (
    echo.
    echo CHYBA pri stazeni. Zkus model stahnout rucne:
    echo 1. Jdi na https://alphacephei.com/vosk/models
    echo 2. Stahni vosk-model-small-cs-0.4-rhasspy.zip
    echo 3. Rozbal do slozky models/
    pause
    exit /b 1
)

echo.
echo ============================================
echo  Model uspesne stazen!
echo  Spust asistenta: python main.py
echo ============================================
pause
