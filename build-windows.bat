@echo off
setlocal

echo --- Setting up virtual environment ---
IF NOT EXIST venv (
    echo Virtual environment 'venv' not found. Creating it...
    python -m venv venv
)

call venv\Scripts\activate

echo --- Installing/Updating dependencies ---
pip install -r requirements.txt

echo --- Installing PyInstaller ---
pip install pyinstaller

echo --- Running PyInstaller ---
IF EXIST build rmdir /s /q build
IF EXIST dist rmdir /s /q dist

pyinstaller ^
  --onefile ^
  --windowed ^
  --name "Silkware" ^
  --add-data "silkware/config;config" ^
  main.py

echo --- Build complete ---
echo Executable is located in the 'dist' directory: dist\Silkware.exe

call venv\Scripts\deactivate
endlocal
