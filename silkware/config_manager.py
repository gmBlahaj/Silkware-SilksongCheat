import json
import os
import logging
from . import config

CONFIG_DIR = os.path.join(os.path.dirname(__file__), "config")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                user_config = json.load(f)
                config.FLY_SPEED = user_config.get("FLY_SPEED", config.FLY_SPEED)
                config.NO_CSPD = user_config.get("NO_CSPD", config.NO_CSPD)
                config.X_SPD = user_config.get("X_SPD", config.X_SPD)
                config.HOTKEY_CONFIG = user_config.get("HOTKEYS", config.HOTKEY_CONFIG)
                logging.info(f"Loaded settings from {CONFIG_FILE}")
        except (json.JSONDecodeError, IOError) as e:
            logging.error(f"Could not load {CONFIG_FILE}: {e}. Using default settings.")
    else:
        logging.info("No config file found. Using default settings.")

def save_config(hotkeys):
    if not os.path.exists(CONFIG_DIR):
        try:
            os.makedirs(CONFIG_DIR)
        except OSError as e:
            logging.error(f"Could not create config directory {CONFIG_DIR}: {e}")
            return

    settings = {
        "FLY_SPEED": config.FLY_SPEED,
        "NO_CSPD": config.NO_CSPD,
        "X_SPD": config.X_SPD,
        "HOTKEYS": hotkeys
    }

    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(settings, f, indent=4)
        logging.info(f"Saved settings to {CONFIG_FILE}")
    except IOError as e:
        logging.error(f"Could not save settings to {CONFIG_FILE}: {e}")