from tkinter import *
from assist import *
from screen1 import switch_to_screen_1
from screen2 import switch_to_screen_2
from screen3 import switch_to_screen_3

def create_start_screen(window):
    clear_window(window)

    # 배경화면 설정
    set_background(window)

    label1 = Label(window, text="M\nE\nF", font=(font_name,70), bg='white')
    label1.place(x=150, y=200)
    label2 = Label(window, text="inistry", font=(font_name,20), bg='white')
    label2.place(x=250, y=260)
    label3 = Label(window, text="conomy", font=(font_name,20), bg='white')
    label3.place(x=240, y=370)
    label4 = Label(window, text="inance", font=(font_name,20), bg='white')
    label4.place(x=240, y=470)

    button1 = Button(window, text="버튼 1", font=(font_name,20),
                     command=lambda: switch_to_screen_1(window, reset_to_start_screen))
    button1.place(x=1000, y=300)

    button2 = Button(window, text="버튼 2", font=(font_name,20),
                     command=lambda: switch_to_screen_2(window, reset_to_start_screen))
    button2.place(x=1000, y=400)

    button3 = Button(window, text="버튼 3", font=(font_name,20),
                     command=lambda: switch_to_screen_3(window, reset_to_start_screen))
    button3.place(x=1000, y=500)

def reset_to_start_screen(window):
    create_start_screen(window)
