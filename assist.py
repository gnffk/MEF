from tkinter import *
from tkinter import font
import os

font_name = "충주김생체 TTF"
def clear_window(window):
    for widget in window.winfo_children():
        widget.destroy()

def create_back_button(window, reset_to_start_screen):
    return Button(window, text="뒤로가기", command=lambda: reset_to_start_screen(window))

