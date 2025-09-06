import tkinter as tk
from tkinter import messagebox

def show_error(title, message):
   # Simple error window, good enough.
    root = tk.Tk()
    root.withdraw()  
    messagebox.showerror(title, message)
    root.destroy()
