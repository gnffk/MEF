from tkinter import *
from tkinter import font
from assist import clear_window,create_back_button
from screen1 import switch_to_screen_1
from screen2 import switch_to_screen_2
from screen3 import switch_to_screen_3
import os

def create_start_screen(window):
    clear_window(window)


    font_name = "충주김생체 TTF"

    OpenTopic = font.Font(window, size=50, family=font_name)
    MainTopic = font.Font(window, size=20, family=font_name)

    label = Label(window, text="MEF", font=OpenTopic)
    label.place(x=100, y=100)

    button1 = Button(window, text="버튼 1", font=MainTopic,
                     command=lambda: switch_to_screen_1(window, reset_to_start_screen))
    button1.place(x=100, y=300)

    button2 = Button(window, text="버튼 2", font=MainTopic,
                     command=lambda: switch_to_screen_2(window, reset_to_start_screen))
    button2.place(x=100, y=400)

    button3 = Button(window, text="버튼 3", font=MainTopic,
                     command=lambda: switch_to_screen_3(window, reset_to_start_screen))
    button3.place(x=100, y=500)

def reset_to_start_screen(window):
    create_start_screen(window)
