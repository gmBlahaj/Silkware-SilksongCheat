import tkinter as tk
from pynput import keyboard
import threading
import logging
import sys

from . import config
from . import utils
from . import cheats
from . import config_manager
from .pid_input_window import ask_for_pid
from .key_serializer import key_to_str, str_to_key
from PyMemoryEditor import OpenProcess

class CheatEngine:
    def __init__(self, pid):
        self.root = tk.Tk()
        self.root.withdraw()

        if pid is None:
            pid = ask_for_pid(self.root)
            if not pid:
                self.root.destroy()
                sys.exit(0)
        
        try:
            self.process = OpenProcess(pid=pid)
        except Exception as e:
            logging.error(f"Failed to open process with PID {pid}: {e}")
            self.root.destroy()
            sys.exit(1)

        process_name = utils.get_process_name(self.process.pid)
        logging.info(f"Attached to process: {process_name} (PID: {self.process.pid})")
        
        self.root.geometry("700x350")
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)
        self.root.title("Silkware")

        mono_dll = utils.get_module_base_address(self.process, "mono-2.0-bdwgc.dll")
        unity_dll = utils.get_module_base_address(self.process, "UnityPlayer.dll")

        if not mono_dll or not unity_dll:
            logging.error("Could not find the required modules in the process.")
            sys.exit(1)
        
        config.rosary_base = mono_dll + 0x00A024E8
        config.health_base = mono_dll + 0x00A030B8
        config.shards_base = mono_dll + 0x00A030B8
        config.soul_base = mono_dll + 0x00763240
        config.y_base = unity_dll + 0x01F419A0
        config.x_base = unity_dll + 0x01F41A68
        config.superfly_addr = unity_dll + 0xEBB8AA

        self.superfly_orig_bytes = None
        self.setup_ui()

        self.do_rosary = tk.BooleanVar(value=False)
        self.do_health = tk.BooleanVar(value=False)
        self.do_shards = tk.BooleanVar(value=False)
        self.do_soul = tk.BooleanVar(value=False)
        self.superfly = tk.BooleanVar(value=False)
        self.speed = tk.BooleanVar(value=False)
        self.flight = tk.BooleanVar(value=False)

        self.cheat_vars = {
            "Inf Rosary": self.do_rosary,
            "Inf Shell Shards": self.do_shards,
            "Godmode": self.do_health,
            "Inf Soul": self.do_soul,
            "Super Speed": self.speed,
            "Flight": self.flight,
            "Better Flight": self.superfly
        }
        self.hotkeys = {str_to_key(k): v for k, v in config.HOTKEY_CONFIG.items()}
        self.pressed_keys = set()

        self.superfly.trace_add("write", lambda *args: cheats.toggle_superfly(self))
        self.make_checks()
        self.make_hotkey_frame()
        self.make_settings_frame()
        self.make_draggable()

        self.menu_visible = True
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

    def on_press(self, key):
        if key == keyboard.KeyCode.from_char('.'):
            self.toggle_menu()
        if key in self.hotkeys:
            cheat_name = self.hotkeys[key]
            if cheat_name in self.cheat_vars:
                self.cheat_vars[cheat_name].set(not self.cheat_vars[cheat_name].get())
        self.pressed_keys.add(key)

    def on_release(self, key):
        if key in self.pressed_keys:
            self.pressed_keys.remove(key)

    def set_hotkey(self, cheat_name, btn):
        def capture():
            btn.config(text="Press a key…")
            with keyboard.Listener(on_press=lambda key: set_key(key, cheat_name, btn)) as listener:
                listener.join()

        def set_key(key, cheat_name, btn):
            
            for k, v in list(self.hotkeys.items()):
                if v == cheat_name:
                    del self.hotkeys[k]
            
            self.hotkeys[key] = cheat_name
            key_str = key_to_str(key)
            btn.config(text=f"Hotkey: {key_str}")
            logging.info(f"Hotkey for '{cheat_name}' set to: {key_str}")
            return False

        threading.Thread(target=capture, daemon=True).start()

    def setup_ui(self):
        self.root.configure(bg=config.TITLE_BG)
        main_frame = tk.Frame(self.root, bg=config.TITLE_BG)
        main_frame.pack(fill="both", expand=True, padx=1, pady=1)
        self.title_frame = tk.Frame(main_frame, bg=config.TITLE_BG, height=60)
        self.title_frame.pack(side="top", fill="x")
        self.title_frame.pack_propagate(False)
        self.bg_label = tk.Label(self.title_frame, text=config.ASCII_ART, font=("Consolas",4), fg="#FF914D", bg=config.TITLE_BG, justify="left", anchor="nw")
        self.bg_label.place(relx=0.5, rely=0.5, anchor="center")
        close_btn = tk.Button(self.title_frame, text="✕", font=("Segoe UI",10,"bold"), fg="#EAEAEA",
                              bg=config.TITLE_BG, activebackground="#FF512F", activeforeground="#FFFFFF",
                              bd=0, command=self.safe_close)
        close_btn.pack(side="right", padx=10, pady=5)
        footer_frame = tk.Frame(main_frame, bg=config.DARK_FRAME_BG, height=25)
        footer_frame.pack(side="bottom", fill="x")
        footer_frame.pack_propagate(False)
        footer_label = tk.Label(footer_frame, text="Disclaimer: Use at your own risk. | Press '.' to hide/show menu.",
                                bg=config.DARK_FRAME_BG, fg=config.TEXT_COLOR, font=("Segoe UI", 8))
        footer_label.pack(pady=5)
        main_content_frame = tk.Frame(main_frame, bg=config.CONTENT_BG)
        main_content_frame.pack(side="top", fill="both", expand=True, padx=5, pady=5)
        self.content_frame = tk.Frame(main_content_frame, bg=config.CONTENT_BG)
        self.content_frame.pack(side="left", fill="both", expand=True)
        self.hotkey_frame = tk.Frame(main_content_frame, bg=config.DARK_FRAME_BG)
        self.hotkey_frame.pack(side="left", fill="y", padx=5)
        self.settings_frame = tk.Frame(main_content_frame, bg=config.DARK_FRAME_BG)
        self.settings_frame.pack(side="left", fill="y")

    def make_draggable(self):
        def start_move(event):
            self.root.x = event.x_root
            self.root.y = event.y_root

        def do_move(event):
            dx = event.x_root - self.root.x
            dy = event.y_root - self.root.y
            x = self.root.winfo_x() + dx
            y = self.root.winfo_y() + dy
            self.root.geometry(f"+{x}+{y}")
            self.root.x = event.x_root
            self.root.y = event.y_root

        self.title_frame.bind("<Button-1>", start_move)
        self.title_frame.bind("<B1-Motion>", do_move)
        self.bg_label.bind("<Button-1>", start_move)
        self.bg_label.bind("<B1-Motion>", do_move)

    def make_check(self, text, var, tooltip_text=None, row=0, col=0):
        def log_toggle():
            logging.info(f"{text} {'enabled' if var.get() else 'disabled'}")
        chk = tk.Checkbutton(self.content_frame, text=text, variable=var, bg=config.CONTENT_BG, fg=config.TEXT_COLOR,
                              activebackground=config.CONTENT_BG, activeforeground=config.TEXT_COLOR,
                              selectcolor=config.TITLE_BG, font=("Segoe UI", 11, "bold"), anchor="w", padx=8, command=log_toggle)
        if tooltip_text:
            Tooltip(chk, tooltip_text)
        chk.grid(row=row, column=col, sticky="w", padx=5, pady=5)
        return chk

    def make_checks(self):
        self.make_check("Inf Rosary Beads", self.do_rosary, "Gives you infinite Rosary Beads", 0, 0)
        self.make_check("Inf Shell Shards", self.do_shards, "Gives you infinite Shell Shards", 0, 1)
        self.make_check("Godmode", self.do_health, "Sets your health to max constantly", 1, 0)
        self.make_check("Inf Soul", self.do_soul, "Gives infinite Soul", 1, 1)
        self.make_check("Super Speed", self.speed, "Fast left/right movement", 2, 0)
        self.make_check("Flight", self.flight, "Vertical flight only", 2, 1)
        self.make_check("Better Fly", self.superfly, "Fly + move fast (NOP applied) Sometimes breaks when going through objects", 3, 0)

    def make_hotkey_frame(self):
       
        cheat_to_key = {v: k for k, v in self.hotkeys.items()}

        for i, (cheat_name, var) in enumerate(self.cheat_vars.items()):
            lbl = tk.Label(self.hotkey_frame, text=cheat_name, bg=config.DARK_FRAME_BG, fg=config.TEXT_COLOR, font=("Segoe UI", 10, "bold"))
            lbl.grid(row=i, column=0, sticky="w", pady=2)
            
            key_obj = cheat_to_key.get(cheat_name)
            key_str = key_to_str(key_obj) if key_obj else "Not set"

            btn = tk.Button(self.hotkey_frame, text=f"Hotkey: {key_str}", bg=config.TITLE_BG, fg="#FFFFFF", bd=0)
            btn.grid(row=i, column=1, pady=2, padx=3)
            btn.config(command=lambda c=cheat_name, b=btn: self.set_hotkey(c, b))

    def make_settings_frame(self):
        tk.Label(self.settings_frame, text="Settings", font=("Segoe UI", 12, "bold"), bg=config.DARK_FRAME_BG, fg=config.TEXT_COLOR).pack(pady=5)
        self.fly_speed_var = tk.StringVar(value=str(config.FLY_SPEED))
        self.no_cspd_var = tk.StringVar(value=str(config.NO_CSPD))
        self.x_spd_var = tk.StringVar(value=str(config.X_SPD))
        self.create_setting_entry(self.settings_frame, "Fly Speed:", self.fly_speed_var)
        self.create_setting_entry(self.settings_frame, "No Clip Speed:", self.no_cspd_var)
        self.create_setting_entry(self.settings_frame, "X Speed:", self.x_spd_var)
        save_btn = tk.Button(self.settings_frame, text="Save Settings", command=self.save_settings, bg=config.TITLE_BG, fg="#FFFFFF", bd=0)
        save_btn.pack(pady=10)

    def create_setting_entry(self, parent, text, var):
        frame = tk.Frame(parent, bg=config.DARK_FRAME_BG)
        frame.pack(fill="x", padx=5, pady=5)
        tk.Label(frame, text=text, bg=config.DARK_FRAME_BG, fg=config.TEXT_COLOR, font=("Segoe UI", 10)).pack(side="left")
        entry = tk.Entry(frame, textvariable=var, bg=config.TITLE_BG, fg=config.TEXT_COLOR, width=8, insertbackground=config.TEXT_COLOR)
        entry.pack(side="right")

    def save_settings(self):
        try:
            config.FLY_SPEED = float(self.fly_speed_var.get())
            config.NO_CSPD = float(self.no_cspd_var.get())
            config.X_SPD = float(self.x_spd_var.get())
            
            hotkeys_to_save = {key_to_str(k): v for k, v in self.hotkeys.items()}
            config_manager.save_config(hotkeys_to_save)
            logging.info("Settings and hotkeys saved.")
        except ValueError:
            logging.error("Invalid input for settings. Please enter numbers only.")

    def safe_close(self):
        logging.info("Closing Silkware.")
        self.listener.stop()
        try:
            if self.superfly_orig_bytes:
                self.process.write_process_memory(config.superfly_addr, bytes, 5, self.superfly_orig_bytes)
        except:
            pass
        self.root.destroy()

    def toggle_menu(self):
        if self.root.winfo_viewable():
            self.root.withdraw()
            logging.info("Menu hidden")
        else:
            self.root.deiconify()
            logging.info("Menu shown")

    def run(self):
        logging.info("Starting cheat loop.")
        self.root.deiconify()
        cheats._cheat_loop(self)
        self.root.mainloop()

class Tooltip:
    def __init__(self, widget, text, delay=500):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tipwindow = None
        self.id = None
        widget.bind("<Enter>", self.schedule)
        widget.bind("<Leave>", self.hide)
        widget.bind("<Motion>", self.move)

    def schedule(self, event=None):
        self.unschedule()
        self.id = self.widget.after(self.delay, self.show)

    def unschedule(self):
        if self.id:
            self.widget.after_cancel(self.id)
            self.id = None

    def show(self, event=None):
        if self.tipwindow:
            return
        x = self.widget.winfo_rootx() + 10
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        tw.wm_attributes("-topmost", True)
        frame = tk.Frame(tw, bg="#FF914D", bd=0)
        frame.pack(padx=1, pady=1)
        content = tk.Frame(frame, bg="#3C3C3C")
        content.pack()
        label = tk.Label(content, text=self.text, bg="#3C3C3C", fg="#FF914D", font=("Segoe UI", 10), justify="left", padx=6, pady=4)
        label.pack()

    def hide(self, event=None):
        self.unschedule()
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None

    def move(self, event):
        if self.tipwindow:
            x = event.x_root + 20
            y = event.y_root + 10
            self.tipwindow.wm_geometry(f"+{x}+{y}")