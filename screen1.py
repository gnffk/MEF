from tkinter import *
from assist import *
def switch_to_screen_1(window, reset_to_start_screen):
    clear_window(window)
    set_background(window, 'image/korean_book_background.png')

    label = Label(window, text="첫 번째 화면", font=(font_name, 20))
    label.pack(pady=20)

    # 여기에 첫 번째 화면의 다른 위젯을 추가하세요.
    back_button = Button(window, text="뒤로가기", command=lambda: reset_to_start_screen(window))
    back_button.pack()

