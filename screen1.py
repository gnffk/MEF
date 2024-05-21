from tkinter import *
from assist import *


data = None

def LoadopenAPI():
    global data
    host = "apis.data.go.kr"
    endpoint = "/1051000/public_inst/list"
    params = {
            "serviceKey": "GuwRZzKrYZA0iHG1Y%2BArdizUhu0a32Kym5AKO4tlpC71aaaCEI6YOzWIEfHyipefqThokj%2F9YurMG0WibwIfrA%3D%3D",
            "pageNo": "1",
            "numOfRows": "366"
    }
    data = fetch_data_from_api(host, endpoint, params)


def InitScrollBar(window):
    global data
    listbox_frame = Frame(window)
    listbox_frame.place(x=50, y=300, width=500, height=400)

    ListBoxScrollbar = Scrollbar(listbox_frame)
    ListBoxScrollbar.pack(side=RIGHT, fill=Y)

    SearchListBox = Listbox(listbox_frame, yscrollcommand=ListBoxScrollbar.set)
    SearchListBox.pack(side=LEFT, fill=BOTH, expand=True)

    ListBoxScrollbar.config(command=SearchListBox.yview)

    # 데이터 로드
    if data:
        for item in data:
            SearchListBox.insert(END, f"{item['instNm']} - {item['roadNmAddr']}")
    else:
        SearchListBox.insert(END, "데이터를 가져올 수 없습니다.")

def InitLabel(window):
    label_topic = Label(window, text="공공기관 시설정보", font=(font_name, 30), bg='#efc376')
    label_topic.place(x=50, y=50)

def InitButton(window, reset_to_start_screen):
    back_button = create_back_button(window, reset_to_start_screen)
    back_button.place(x=1100, y=50)

def switch_to_screen_1(window, reset_to_start_screen):
    clear_window(window)
    set_background(window)

    LoadopenAPI()  # data 불러오는 함수
    InitLabel(window)  # Label 정리
    InitButton(window, reset_to_start_screen)  # Button 정리
    InitScrollBar(window)  # ScrollBar 정리

