from tkinter import *
from tkinter import font


def switch_to_screen_1(window):
    clear_window(window)
    label = Label(window, text="첫 번째 화면", font=("Helvetica", 20))
    label.pack(pady=20)

    # 여기에 첫 번째 화면의 다른 위젯을 추가하세요.
    back_button = Button(window, text="뒤로가기", command=lambda: reset_to_start_screen(window))
    back_button.pack()


def switch_to_screen_2(window):
    clear_window(window)
    label = Label(window, text="두 번째 화면", font=("Helvetica", 20))
    label.pack(pady=20)

    # 여기에 두 번째 화면의 다른 위젯을 추가하세요.
    back_button = Button(window, text="뒤로가기", command=lambda: reset_to_start_screen(window))
    back_button.pack()


def switch_to_screen_3(window):
    clear_window(window)
    label = Label(window, text="세 번째 화면", font=("Helvetica", 20))
    label.pack(pady=20)

    # 여기에 세 번째 화면의 다른 위젯을 추가하세요.
    back_button = Button(window, text="뒤로가기", command=lambda: reset_to_start_screen(window))
    back_button.pack()


def create_start_screen(window):
    clear_window(window)
    OpenTopic = font.Font(window, size=50, family='ChungjuKimSaeng')
    MainTopic = font.Font(family="Helvetica", size=10, weight="bold")

    label = Label(window, text="MEF", font=OpenTopic)
    label.place(x=100, y=100)

    button1 = Button(window, text="버튼 1", font=MainTopic, command=lambda: switch_to_screen_1(window))
    button1.place(x=100, y=300)

    button2 = Button(window, text="버튼 2", font=MainTopic, command=lambda: switch_to_screen_2(window))
    button2.place(x=100, y=400)

    button3 = Button(window, text="버튼 3", font=MainTopic, command=lambda: switch_to_screen_3(window))
    button3.place(x=100, y=500)


def clear_window(window):
    for widget in window.winfo_children():
        widget.destroy()


def reset_to_start_screen(window):
    create_start_screen(window)
