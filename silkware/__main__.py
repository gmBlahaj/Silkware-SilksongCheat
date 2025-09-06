import argparse
import logging
import sys
from PyMemoryEditor.process.errors import ProcessNotFoundError

from . import config
from .gui import CheatEngine
from .error_window import show_error
from . import config_manager

# --- logging setup ---
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%H:%M:%S')

def main():
    config_manager.load_config()
    try:
        import psutil
    except ImportError:
        print("The 'psutil' library is required. Please install it by running: pip install psutil")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Silkware - A Silksong cheat tool.")
    parser.add_argument("--pid", type=int, help="The process ID of the Silksong process.")
    parser.add_argument("--process-name", type=str, default=config.PROCESS_NAME, help="The name of the Silksong process.")
    args = parser.parse_args()

    pid = args.pid

    if not pid:
        if sys.platform == "win32":
            logging.info(f"Searching for process: '{args.process_name}'")
            for proc in psutil.process_iter(['pid', 'name']):
                if args.process_name.lower() in proc.info.get('name', '').lower():
                    pid = proc.info['pid']
                    logging.info(f"Found process. PID: {pid}, Name: {proc.info.get('name')}")
                    break
        else:  
            pid = None

    if not pid and sys.platform == 'win32':
        error_title = "Process Not Found"
        error_message = f"""Process '{args.process_name}' not found.\n\nMake sure Silksong is running."""
        show_error(error_title, error_message)
        logging.error("Process not found.")
        sys.exit(1)

    try:
        engine = CheatEngine(pid)
        engine.run()
    except ProcessNotFoundError as e:
        show_error("Process Not Found", f"Process with PID {pid} not found. Make sure Silksong is running.")
        logging.error(f"Process with PID {pid} not found: {e}")
        sys.exit(1)
    except Exception as e:
        # Catching other potential errors
        show_error("Error", f"An unexpected error occurred: {e}")
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()