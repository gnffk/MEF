from tkinter import *
from assist import *

data = None
filtered_data = None  # 필터링된 데이터를 저장할 변수
search_listbox = None  # 전역 변수로 리스트 박스 참조

def LoadopenAPI():
    global data, filtered_data

    host = "apis.data.go.kr"
    endpoint = "/1051000/public_inst/list"
    params = {
            "serviceKey": "GuwRZzKrYZA0iHG1Y+ArdizUhu0a32Kym5AKO4tlpC71aaaCEI6YOzWIEfHyipefqThokj/9YurMG0WibwIfrA==",
            "numOfRows": "366"
    }
    response = fetch_data_from_api(host, endpoint, params)
    if response and "result" in response:
        data = response["result"]
        filtered_data = data  # 초기 필터링 데이터 설정
    else:
        data = None
        filtered_data = None


def InitScrollBar(window):
    global filtered_data, search_listbox
    listbox_frame = Frame(window)
    listbox_frame.place(x=50, y=300, width=500, height=400)

    ListBoxScrollbar = Scrollbar(listbox_frame, bg='#efc376')
    ListBoxScrollbar.pack(side=RIGHT, fill=Y)

    search_listbox = Listbox(listbox_frame, font=(font_name, 10), bg='#efc376', yscrollcommand=ListBoxScrollbar.set)
    search_listbox.pack(side=LEFT, fill=BOTH, expand=True)

    ListBoxScrollbar.config(command=search_listbox.yview, bg='#efc376')

    update_listbox(search_listbox, filtered_data)


def update_listbox(listbox, data):
    listbox.delete(0, END)
    if data:
        for item in data:
            listbox.insert(END, f"{item['instNm']} - {item['roadNmAddr']}")
    else:
        listbox.insert(END, "없음")


def InitLabel(window):
    label_topic = Label(window, text="공공기관 시설정보", font=(font_name, 30), bg='#efc376')
    label_topic.place(x=50, y=50)


def InitButton(window, reset_to_start_screen):
    back_button = create_back_button(window, reset_to_start_screen)
    back_button.place(x=1100, y=50)


def InitSearch(window):
    search_label = Label(window, text="검색:", font=(font_name, 15), bg='#efc376')
    search_label.place(x=50, y=250)

    search_entry = Entry(window, font=(font_name, 15), bg='#efc376')
    search_entry.place(x=100, y=250, width=380)

    search_button = Button(window, text="검색", font=(font_name, 12), bg='#efc376',
                           command=lambda: search_data(search_entry.get()))
    search_button.place(x=500, y=250)


def search_data(query):
    global data, filtered_data, search_listbox
    LoadopenAPI()  # 데이터 로드 (데이터가 없을 때만 로드)

    if data:
        filtered_data = [item for item in data if query.lower() in item['instNm'].lower()]
    else:
        filtered_data = None
    if search_listbox:
        update_listbox(search_listbox, filtered_data)


def switch_to_screen_1(window, reset_to_start_screen):
    clear_window(window)
    set_background(window)


    InitLabel(window)  # 레이블 초기화
    InitButton(window, reset_to_start_screen)  # 버튼 초기화
    InitSearch(window)  # 검색 초기화
    InitScrollBar(window)  # 스크롤바 초기화

def reset_to_start_screen(window):
    global filtered_data
    filtered_data = data  # 초기 필터링 데이터 설정
    clear_window(window)
    create_start_screen(window)  # 시작 화면을 다시 설정

def create_start_screen(window):
    clear_window(window)
    set_background(window)



