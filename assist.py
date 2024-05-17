from tkinter import *
from tkinter import font
import os

# 전역 변수로 이미지와 폰트를 로드
background_image = None
font_name = "충주김생체 TTF"



def preload_assets(window):
    global background_image
    # 배경 이미지 로드
    background_image = PhotoImage(file='image/korean_book_background.png')

# 배경 설정 함수
def set_background(window):
    global background_image
    background_label = Label(window, image=background_image, bg = '#efc376')
    background_label.image = background_image  # 이미지 객체 유지
    background_label.place(x=0, y=0)
    return background_label


# 창의 모든 위젯을 제거하는 함수
def clear_window(window):
    for widget in window.winfo_children():
        widget.destroy()


# 뒤로가기 버튼 생성 함수
def create_back_button(window, reset_to_start_screen):
    return Button(window, text="뒤로가기",bg = '#efc376', command=lambda: reset_to_start_screen(window))
