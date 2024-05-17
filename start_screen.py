from tkinter import *
from tkinter import font
from assist import *
from screen1 import switch_to_screen_1
from screen2 import switch_to_screen_2
from screen3 import switch_to_screen_3
import os

def create_start_screen(window):
    clear_window(window)

    OpenTopic = font.Font(window, size=70, family=font_name)
    MainTopic = font.Font(window, size=20, family=font_name)

    label = Label(window, text="M\nE\nF", font=OpenTopic)
    label.place(x=150, y=200)
    label = Label(window, text="inistry", font=MainTopic)
    label.place(x=250, y=260)
    label = Label(window, text="conomy", font=MainTopic)
    label.place(x=240, y=370)
    label = Label(window, text="inance", font=MainTopic)
    label.place(x=240, y=470)


    button1 = Button(window, text="버튼 1", font=MainTopic,
                     command=lambda: switch_to_screen_1(window, reset_to_start_screen))
    button1.place(x=1000, y=300)

    button2 = Button(window, text="버튼 2", font=MainTopic,
                     command=lambda: switch_to_screen_2(window, reset_to_start_screen))
    button2.place(x=1000, y=400)

    button3 = Button(window, text="버튼 3", font=MainTopic,
                     command=lambda: switch_to_screen_3(window, reset_to_start_screen))
    button3.place(x=1000, y=500)

def reset_to_start_screen(window):
    create_start_screen(window)
