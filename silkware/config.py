import sys

# --- constants ---
PROCESS_NAME = "Hollow Knight Silksong.exe" if sys.platform == "win32" else "Hollow Knight Silksong"

# --- movement settings ---
FLY_SPEED = 2.5
NO_CSPD = 1.5
X_SPD = 0.4

# --- colors ---
TITLE_BG = "#2A2A2A"
CONTENT_BG = "#3C3C3C"
DARK_FRAME_BG = "#252525"
TEXT_COLOR = "#FF914D"

# --- ascii art ---
ASCII_ART = r"""
           /$$ /$$ /$$
          |__/| $$| $$
  /$$$$$$$ /$$| $$| $$   /$$ /$$  /$$  /$$  /$$$$$$   /$$$$$$   /$$$$$$ 
 /$$_____/| $$| $$| $$  /$$/| $$ | $$ | $$ |____  $$ /$$__  $$ /$$__  $$
|  $$$$$$ | $$| $$| $$$$$$/ | $$ | $$ | $$  /$$$$$$$| $$  \__/| $$$$$$$$
 \____  $$| $$| $$| $$_  $$ | $$ | $$ | $$ /$$__  $$| $$      | $$_____/
 /$$$$$$$/| $$| $$| $$ \  $$|  $$$$$/$$$$/|  $$$$$$$| $$      |  $$$$$$$
|_______/ |__/|__/|__/  \__/ \_____/\___/  \_______/|__/       \_______/
"""

# --- addresses ---
rosary_base = None
rosary_offsets = [0x350, 0x10, 0x60, 0x0, 0xD8, 0xB8, 0x23C]
health_base = None
health_offsets = [0x138, 0x1A8, 0x10, 0x60, 0x0, 0x110, 0x21C]
shards_base = None
shards_offsets = [0x138, 0x1A8, 0x10, 0x60, 0x0, 0x110, 0x908]
soul_base = None
soul_offsets = [0x298, 0xB80, 0x308, 0x20, 0x78, 0x250, 0x240]
y_base = None
y_offsets = [0xA90,0x608,0x18,0x48,0x60,0x330]
x_base = None
x_offsets = [0x118, 0x80,0x620,0x0,0x380,0x10,0x42C]
superfly_addr = None

# --- keybinds ---
HOTKEY_CONFIG = {}
