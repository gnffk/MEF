from tkinter import *
from tkinter import font
from screen1 import switch_to_screen_1
from screen2 import switch_to_screen_2
from screen3 import switch_to_screen_3


def create_start_screen(window):
    clear_window(window)
    OpenTopic = font.Font(window, size=50, family='ChungjuKimSaeng')
    MainTopic = font.Font(family="Helvetica", size=10, weight="bold")

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


def clear_window(window):
    for widget in window.winfo_children():
        widget.destroy()


def reset_to_start_screen(window):
    create_start_screen(window)
