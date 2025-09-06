set -e
echo "--- Setting up virtual environment ---"
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Virtual environment 'venv' not found. Please create it and install dependencies first."
    echo "Example: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

echo "--- Installing PyInstaller ---"
pip install pyinstaller

echo "--- Running PyInstaller ---"

rm -rf build dist
pyinstaller \
  --onefile \
  --windowed \
  --name "Silkware" \
  --add-data "silkware/config:config" \
  --hidden-import "Xlib.display" \
  --hidden-import "Xlib.X" \
  --hidden-import "Xlib.protocol" \
  --hidden-import "Xlib.error" \
  --hidden-import "Xlib.xobject" \
  --hidden-import "Xlib.ext" \
  --hidden-import "Xlib.keysymdef" \
  --hidden-import "Xlib.threaded" \
  --hidden-import "Xlib.Xatom" \
  --hidden-import "Xlib.Xcursorfont" \
  --hidden-import "Xlib.XK" \
  --hidden-import "Xlib.Xutil" \
  --hidden-import "Xlib.xauth" \
  main.py

echo "--- Build complete ---"
echo "Executable is located in the 'dist' directory: dist/Silkware"


deactivate
