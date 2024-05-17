from tkinter import *
from assist import *


def switch_to_screen_1(window, reset_to_start_screen):
    clear_window(window)

    # 배경화면 설정
    set_background(window)

    host = "apis.data.go.kr"
    endpoint = "/1051000/public_inst/list"
    params = {
        "serviceKey": "GuwRZzKrYZA0iHG1Y%2BArdizUhu0a32Kym5AKO4tlpC71aaaCEI6YOzWIEfHyipefqThokj%2F9YurMG0WibwIfrA%3D%3D",
        "pageNo": "1",
        "numOfRows": "10",
        "type": "json",
    }
    data = fetch_data_from_api(host, endpoint, params)

    print(type(data))

    label_topic = Label(window, text="공공기관 시설정보", font=(font_name, 30), bg='#efc376')
    label_topic.place(x=50, y=50)


    back_button = create_back_button(window, reset_to_start_screen)
    back_button.place(x=1100, y=50)
