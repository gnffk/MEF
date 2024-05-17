from tkinter import *
from assist import *


def switch_to_screen_2(window, reset_to_start_screen):
    clear_window(window)

    # 배경화면 설정
    set_background(window)

    label = Label(window, text="두 번째 화면", font=(font_name, 20), bg='#efc376')
    label.pack(pady=20)


    back_button = create_back_button(window, reset_to_start_screen)
    back_button.pack()
