from assist import *


from PIL import Image, ImageTk
from tkinterweb import HtmlFrame
import folium


data = None
filtered_data = None  # 필터링된 데이터를 저장할 변수
search_listbox = None  # 전역 변수로 리스트 박스 참조
infobox_text = None  # InfoBox의 텍스트 위젯 참조

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
    listbox_frame.place(x=50, y=200, width=500, height=500)

    ListBoxScrollbar = Scrollbar(listbox_frame)
    ListBoxScrollbar.pack(side=RIGHT, fill=Y)

    search_listbox = Listbox(listbox_frame, font=(font_name, 10), bg='#efc376', yscrollcommand=ListBoxScrollbar.set)
    search_listbox.pack(side=LEFT, fill=BOTH, expand=True)

    ListBoxScrollbar.config(command=search_listbox.yview, bg='#efc376')

    search_listbox.bind("<<ListboxSelect>>", display_info)  # 리스트박스 선택 이벤트 바인딩

    update_listbox(search_listbox, filtered_data)

def InitInfo(window):
    global infobox_text
    InfoBox_frame = Frame(window)
    InfoBox_frame.place(x=600, y=200, width=500, height=100)

    InfoBox_Scrollbar = Scrollbar(InfoBox_frame, bg='#efc376')
    InfoBox_Scrollbar.pack(side=RIGHT, fill=Y)

    infobox_text = Text(InfoBox_frame, font=(font_name, 10), bg='#efc376', yscrollcommand=InfoBox_Scrollbar.set)
    infobox_text.pack(side=LEFT, fill=BOTH, expand=True)

    InfoBox_Scrollbar.config(command=infobox_text.yview, bg='#efc376')
def InitMap(window):
    global map_frame
    map_frame = HtmlFrame(window, horizontal_scrollbar="auto")
    map_frame.place(x=600, y=320, width=500, height=380)
def update_map(x, y):
    map = folium.Map(location=[x,y], zoom_start=15)
    marker = folium.Marker([x, y])
    marker.add_to(map)
    map.save("map/map.html")
def update_listbox(listbox, data):
    listbox.delete(0, END)
    if data:
        for item in data:
            listbox.insert(END, f"{item['instNm']} - {item['sprvsnInstNm']}")
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
    search_label.place(x=50, y=150)

    search_entry = Entry(window, font=(font_name, 15), bg='#efc376')
    search_entry.place(x=100, y=150, width=380)

    search_button = Button(window, text="검색", font=(font_name, 12), bg='#efc376',
                           command=lambda: search_data(search_entry.get()))
    search_button.place(x=500, y=150)

def search_data(query):
    global data, filtered_data, search_listbox
    LoadopenAPI()  # 데이터 로드 (데이터가 없을 때만 로드)

    if data:
        filtered_data = [item for item in data if query.lower() in item['instNm'].lower()]
    else:
        filtered_data = None
    if search_listbox:
        update_listbox(search_listbox, filtered_data)

def display_info(event):
    global filtered_data, search_listbox, infobox_text
    selection = search_listbox.curselection()
    if selection:
        index = selection[0]
        selected_item = filtered_data[index]
        info = f"기관명: {selected_item['instNm']}\n" \
               f"부서: {selected_item['sprvsnInstNm']}\n" \
               f"홈페이지: {selected_item['siteUrl']}\n" \
               f"전화번호: {selected_item['rprsTelno']}\n" \
               f"도로명 주소: {selected_item['roadNmAddr']}\n" \
               f"지번 주소: {selected_item['lotnoAddr']}"
        x, y = request_geo(selected_item['roadNmAddr'])
        update_map(x,y)
        infobox_text.config(state=NORMAL)
        infobox_text.delete(1.0, END)
        infobox_text.insert(END, info)
        infobox_text.config(state=DISABLED)


def switch_to_screen_1(window, reset_to_start_screen):
    clear_window(window)
    set_background(window)

    InitLabel(window)  # 레이블 초기화
    InitButton(window, reset_to_start_screen)  # 버튼 초기화
    InitSearch(window)  # 검색 초기화
    InitScrollBar(window)  # 스크롤바 초기화
    InitInfo(window)  # InfoBox 초기화
    InitMap(window) # map 초기화
def reset_to_start_screen(window):
    global filtered_data
    filtered_data = data  # 초기 필터링 데이터 설정
    clear_window(window)
    create_start_screen(window)  # 시작 화면을 다시 설정

def create_start_screen(window):
    clear_window(window)
    set_background(window)
