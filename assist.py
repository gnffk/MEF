from tkinter import *
from tkinter import font
import os

#font 종류--------------------
font_name = "충주김생체 TTF"

#화면 종류 ---------------------------------

def set_background(window, image_path):
    backGroundImage = PhotoImage(file=image_path)
    background_label = Label(window, image=backGroundImage)
    background_label.image = backGroundImage  # 이미지 객체 유지
    background_label.place(x=0, y=0)
    return background_label

#window 함수 -------------------------------------
def clear_window(window):
    for widget in window.winfo_children():
        widget.destroy()

#버튼 함수 ---------------------------------------------
def create_back_button(window, reset_to_start_screen):
    return Button(window, text="뒤로가기", command=lambda: reset_to_start_screen(window))

