
$ErrorActionPreference = "Stop"

Write-Host "--- Setting up virtual environment ---"
if (-not (Test-Path -Path "venv")) {
    Write-Host "Virtual environment 'venv' not found. Creating it..."
    python.exe -m venv venv
}

if (-not (Test-Path -Path "venv/bin/Activate.ps1")) {
    Write-Error "Error: venv/bin/Activate.ps1 not found. Please ensure your Python installation correctly creates 'Activate.ps1' in the venv/bin/ directory."
    exit 1
}

. "venv/bin/Activate.ps1"

Write-Host "--- Installing/Updating dependencies ---"
pip install -r requirements.txt

Write-Host "--- Installing PyInstaller ---"
pip install pyinstaller

Write-Host "--- Running PyInstaller ---"
if (Test-Path -Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path -Path "dist") { Remove-Item -Recurse -Force "dist" }

pyinstaller `
  --onefile `
  --windowed `
  --name "Silkware" `
  --add-data "silkware/config:config" `
  --hidden-import "pynput.mouse._win32" `
  --hidden-import "pynput.keyboard._win32" `
  --hidden-import "PyMemoryEditor" `
  --hidden-import "PyMemoryEditor.win32" `
  --hidden-import "psutil" `
  main.py

Write-Host "--- Build complete ---"
Write-Host "Executable is located in the 'dist' directory: dist\Silkware.exe"

Deactivate
