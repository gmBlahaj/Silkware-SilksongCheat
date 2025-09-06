import tkinter as tk
from tkinter import simpledialog

def ask_for_pid(parent):
    # Linux shenanigans. 10x easier than finding out the PID automatically
    pid_str = simpledialog.askstring("Process ID", "Please enter the Process ID (PID) of the game:", parent=parent)
    
    if pid_str and pid_str.isdigit():
        return int(pid_str)
    return None
