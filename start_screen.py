from tkinter import *
from assist import *
from screen1 import switch_to_screen_1
from screen2 import switch_to_screen_2
from screen3 import switch_to_screen_3
from screen4 import switch_to_screen_4
from PIL import ImageTk, Image
import webbrowser
def create_start_screen(window):
    clear_window(window)

    # 배경화면 설정
    set_background(window)

    # 타이틀 라벨 설정
    label1 = Label(window, text="M\nE\nF", font=(font_name,70), bg='#efc376')
    label1.place(x=150, y=200)
    label2 = Label(window, text="inistry", font=(font_name,20), bg='#efc376')
    label2.place(x=250, y=260)
    label3 = Label(window, text="conomy", font=(font_name,20), bg='#efc376')
    label3.place(x=240, y=370)
    label4 = Label(window, text="inance", font=(font_name,20), bg='#efc376')
    label4.place(x=240, y=470)

    # 공공기관 관련 정보 버튼 설정
    button1 = Button(window, text="공공기관 시설 정보", font=(font_name,20), bg = '#efc376',
                     command=lambda: switch_to_screen_1(window, reset_to_start_screen))
    button1.place(x=750, y=300)

    button2 = Button(window, text="공공기관 진행 사업 정보", font=(font_name,20),bg = '#efc376',
                     command=lambda: switch_to_screen_2(window, reset_to_start_screen))
    button2.place(x=750, y=400)

    button3 = Button(window, text="공공기관 채용 관련 정보", font=(font_name,20),bg = '#efc376',
                     command=lambda: switch_to_screen_3(window, reset_to_start_screen))
    button3.place(x=750, y=500)

    # 오른쪽 상단에 버튼 추가 (이메일, 텔레그램 챗봇, 북마크)


    email_image = Image.open("image/email.png")
    re_email_image = email_image.resize((100,100))
    my_email_img = ImageTk.PhotoImage(re_email_image)
    email_button = Button(window, image=my_email_img, bg='#efc376', command=open_email)
    email_button.image = my_email_img  # 이미지 객체 유지
    email_button.place(x=750, y=50, width=100, height=100)

    telegram_image = Image.open("image/telegram.png")
    re_telegram_image = telegram_image.resize((100, 100))
    my_telegram_image = ImageTk.PhotoImage(re_telegram_image)
    telegram_button = Button(window, image=my_telegram_image, bg='#efc376', command=open_telegram)
    telegram_button.image = my_telegram_image  # 이미지 객체 유지
    telegram_button.place(x=880, y=50, width=100, height=100)

    bookmark_image = Image.open("image/bookmark.png")
    re_bookmark_image = bookmark_image.resize((100, 100))
    my_bookmark_image = ImageTk.PhotoImage(re_bookmark_image)
    bookmark_button = Button(window, image=my_bookmark_image, bg='#efc376', command=lambda: switch_to_screen_4(window, reset_to_start_screen))
    bookmark_button.image = my_bookmark_image  # 이미지 객체 유지
    bookmark_button.place(x=1010, y=50, width=100, height=100)

    # main button 추가
    main_image = Image.open("image/main.png")
    re_main_image = main_image.resize((100, 100))
    my_main_image = ImageTk.PhotoImage(re_main_image)
    main_Label1 = Label(window, image=my_main_image, bg='#efc376')
    main_Label1.image = my_main_image  # 이미지 객체 유지
    main_Label1.place(x=0, y=630, width=200, height=200)

    main_Label2 = Label(window, image=my_main_image, bg='#efc376')
    main_Label2.image = my_main_image  # 이미지 객체 유지
    main_Label2.place(x=200, y=630, width=200, height=200)

    main_Label3 = Label(window, image=my_main_image, bg='#efc376')
    main_Label3.image = my_main_image  # 이미지 객체 유지
    main_Label3.place(x=400, y=630, width=200, height=200)

    main_Label4 = Label(window, image=my_main_image, bg='#efc376')
    main_Label4.image = my_main_image  # 이미지 객체 유지
    main_Label4.place(x=600, y=630, width=200, height=200)

    main_Label5 = Label(window, image=my_main_image, bg='#efc376')
    main_Label5.image = my_main_image  # 이미지 객체 유지
    main_Label5.place(x=800, y=630, width=200, height=200)

    main_Label6 = Label(window, image=my_main_image, bg='#efc376')
    main_Label6.image = my_main_image  # 이미지 객체 유지
    main_Label6.place(x=1000, y=630, width=200, height=200)
def reset_to_start_screen(window):
    create_start_screen(window)

# 버튼 클릭 시 실행될 함수들
def open_email():
    print("이메일 버튼 클릭")

def open_telegram():
    print("텔레그램 버튼 클릭")
    webbrowser.open("tg://resolve?domain=KorMEF_bot")