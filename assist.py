from tkinter import *
from tkinter import font
import os

def clear_window(window):
    for widget in window.winfo_children():
        widget.destroy()

def load_custom_font(size):
    font_path = os.path.join(os.path.dirname(__file__), 'font', 'ChungjuKimSaeng.ttf')
    return font.Font(window=Tk(), file=font_path, size=size)

def create_back_button(window, reset_to_start_screen):
    return Button(window, text="뒤로가기", command=lambda: reset_to_start_screen(window))
