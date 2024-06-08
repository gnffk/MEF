import os
from tkinter import *
from assist import *
from PIL import Image, ImageTk

data = None
filtered_data = None  # 필터링된 데이터를 저장할 변수
search_listbox = None  # 전역 변수로 리스트 박스 참조
infobox_text = None  # InfoBox의 텍스트 위젯 참조
map_label = None  # Map Label 참조
google_maps_api_key = 'AIzaSyDbSUl8RcidvuEFE9r9KER3hU-j2yA0OSw'  # 여기에 Google Maps API 키를 입력하세요
current_lat = None
current_lng = None
current_zoom = 15  # 기본 줌 레벨

def LoadopenAPI():
    global data, filtered_data
    host = "apis.data.go.kr"
    endpoint = "/1051000/public_inst/list"
    params = {
        "serviceKey": "GuwRZzKrYZA0iHG1Y+ArdizUhu0a32Kym5AKO4tlpC71aaaCEI6YOzWIEfHyipefqThokj/9YurMG0WibwIfrA==",
        "numOfRows": "366"
    }
    response = fetch_data_from_api(host, endpoint, params)
    print(response)
    if response and "result" in response:
        data = response["result"]
        print(data)
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
    global map_label, name_label
    map_label = Label(window, bg='#efc376')
    map_label.place(x=600, y=310, width=500, height=390)
    name_label = Label(window, font=(font_name, 15), bg='#efc376')
    name_label.place(x=600, y=700, width=500, height=30)

    zoom_in_button = Button(window, text="+", font=(font_name, 12), bg='#efc376', command=zoom_in)
    zoom_in_button.place(x=1050, y=310, width=50, height=30)

    zoom_out_button = Button(window, text="-", font=(font_name, 12), bg='#efc376', command=zoom_out)
    zoom_out_button.place(x=1050, y=350, width=50, height=30)

def update_map(lat, lng, name, zoom):
    global map_label, name_label, google_maps_api_key
    map_image = get_static_map_image(lat, lng, google_maps_api_key, zoom=zoom)
    if map_image:
        map_label.config(image=map_image)
        map_label.image = map_image  # 이미지 객체를 유지
        name_label.config(text=name)

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
    global filtered_data, search_listbox, infobox_text, current_lat, current_lng, current_zoom
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
        current_lat, current_lng = request_geo(selected_item['roadNmAddr'])
        current_zoom = 15  # 기본 줌 레벨로 초기화
        update_map(current_lat, current_lng, selected_item['instNm'], current_zoom)

        infobox_text.config(state=NORMAL)
        infobox_text.delete(1.0, END)
        infobox_text.insert(END, info)
        infobox_text.config(state=DISABLED)

def zoom_in():
    global current_zoom
    if current_zoom < 21:  # 최대 줌 레벨
        current_zoom += 1
        update_map(current_lat, current_lng, name_label.cget("text"), current_zoom)

def zoom_out():
    global current_zoom
    if current_zoom > 0:  # 최소 줌 레벨
        current_zoom -= 1
        update_map(current_lat, current_lng, name_label.cget("text"), current_zoom)

def reset_to_start_screen(window):
    global filtered_data
    filtered_data = data  # 초기 필터링 데이터 설정
    clear_window(window)
    create_start_screen(window)  # 시작 화면을 다시 설정

def create_start_screen(window):
    clear_window(window)
    set_background(window)

def switch_to_screen_1(window, reset_to_start_screen):
    clear_window(window)
    set_background(window)

    InitLabel(window)  # 레이블 초기화
    InitButton(window, reset_to_start_screen)  # 버튼 초기화
    InitSearch(window)  # 검색 초기화
    InitScrollBar(window)  # 스크롤바 초기화
    InitInfo(window)  # InfoBox 초기화
    InitMap(window) # map 초기화