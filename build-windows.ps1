
$ErrorActionPreference = "Stop"

# Debug Shit, just leave it

Write-Host "--- Diagnosing Python environment ---"
Write-Host "Python executable: $(Get-Command python.exe | Select-Object -ExpandProperty Path)"
python.exe -c "import sysconfig; import pprint; pprint.pprint(sysconfig.get_config_vars())"

Write-Host "Searching for distutils.cfg files..."
Get-ChildItem -Path "$env:APPDATA\pip", "$env:APPDATA\Python", "$env:LOCALAPPDATA\pip", "$env:LOCALAPPDATA\Python", "$(Get-Command python.exe | Select-Object -ExpandProperty Path | Split-Path -Parent | Split-Path -Parent)\Lib\distutils" -Filter "distutils.cfg" -Recurse -ErrorAction SilentlyContinue | ForEach-Object { Write-Host "Found: $($_.FullName)" }

Write-Host "--- Cleaning up environment variables for build ---"
$originalPath = $env:Path
$originalInclude = $env:INCLUDE
$originalLib = $env:LIB

$env:Path = ($env:Path -split ';' | Where-Object { $_ -notmatch '(?i)msys64|mingw' }) -join ';'
$env:INCLUDE = ($env:INCLUDE -split ';' | Where-Object { $_ -notmatch '(?i)msys64|mingw' }) -join ';'
$env:LIB = ($env:LIB -split ';' | Where-Object { $_ -notmatch '(?i)msys64|mingw' }) -join ';'

$env:DISTUTILS_USE_SDK = "1"
$env:MSSdk = "1"

Write-Host "--- Upgrading pip and setuptools ---"
python -m pip install --upgrade pip setuptools

Write-Host "--- Installing wheel ---"
pip install wheel

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
  main.py

Write-Host "--- Build complete ---"
Write-Host "Executable is located in the 'dist' directory: dist\Silkware.exe"

# Restore original environment variables
$env:Path = $originalPath
$env:INCLUDE = $originalInclude
$env:LIB = $originalLib