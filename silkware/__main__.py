import argparse
import logging
import sys
from PyMemoryEditor.process.errors import ProcessNotFoundError

from . import config
from .gui import CheatEngine
from .error_window import show_error
from . import config_manager
from .utils import get_process_name, get_pid_by_name

# --- logging setup ---
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%H:%M:%S')

def main():
    config_manager.load_config()

    parser = argparse.ArgumentParser(description="Silkware - A Silksong cheat tool.")
    parser.add_argument("--pid", type=int, help="The process ID of the Silksong process.")
    parser.add_argument("--process-name", type=str, default=config.PROCESS_NAME, help="The name of the Silksong process.")
    args = parser.parse_args()

    pid = args.pid

    if not pid:
        logging.info(f"Searching for process: '{args.process_name}'")
        pid = get_pid_by_name(args.process_name)
        if pid:
            logging.info(f"Found process. PID: {pid}, Name: {get_process_name(pid)}")

    if not pid:
        if sys.platform.startswith("linux"):
            from .pid_input_window import ask_for_pid
            import tkinter as tk
            root = tk.Tk()
            root.withdraw()
            pid = ask_for_pid(root)
            root.destroy()
        else:
            error_title = "Process Not Found"
            error_message = f"""Process '{args.process_name}' not found.\n\nMake sure Silksong is running."""
            show_error(error_title, error_message)
            logging.error("Process not found.")
            sys.exit(1)

    if not pid:
        logging.error("No PID provided or found. Exiting.")
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
