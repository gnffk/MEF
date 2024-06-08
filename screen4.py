from tkinter import *
from assist import *
import json

# 전역 변수 선언
data = None
filtered_data = None
selected_item = None

def LoadopenAPI(search_category=None, search_query=None, bizClsf = None):
    global data, filtered_data
    data = []
    pageNo = 1
    while True:
        host = "apis.data.go.kr"
        endpoint = "/1051000/fclt/list"
        params = {
            "serviceKey": "8gLaHAvMf6cgJYQW75su5MuEjbLGeqjZlnX7mf1wMMhhCAG33jvRpliHV9k5fCqF4uzFPtO9AL8p9VrC2IgERA==",
            "numOfRows": "1000",
            "pageNo": pageNo
        }
        if bizClsf:
            params["bizClsf"] = bizClsf

        response = fetch_data_from_api(host, endpoint, params)
        if response and "result" in response:
            page_data = response["result"]
            if not page_data:
                break
            data.extend(page_data)
            pageNo += 1
        else:
            break

    if data:
        filtered_data = data  # 초기 필터링 데이터 설정
    else:
        data = None
        filtered_data = None
        print("데이터를 불러올 수 없습니다.")
def InitCategoryDropdown(window):
    selected_category = StringVar(window)
    selected_category.set("기관명")  # 기본값 설정
    dropdown_label = Label(window, text="주제 카테고리:", font=(font_name, 15), bg='#efc376')
    dropdown_label.place(x=50, y=150)

    dropdown = OptionMenu(window, selected_category, "기관명")
    dropdown.config(font=(font_name, 12), bg='#efc376')
    dropdown.place(x=200, y=150, width=200, height=30)

    search_label = Label(window, text="검색:", font=(font_name, 15), bg='#efc376')
    search_label.place(x=50, y=200)

    search_entry = Entry(window, font=(font_name, 15), bg='#efc376')
    search_entry.place(x=100, y=200, width=380)

    search_button = Button(window, text="검색", font=(font_name, 12), bg='#efc376',
                           command=lambda: search_data(window, selected_category.get(), search_entry.get()))
    search_button.place(x=500, y=200)


def InitSearch(window):
    search_label = Label(window, text="검색:", font=(font_name, 15), bg='#efc376')
    search_label.place(x=50, y=150)

    search_entry = Entry(window, font=(font_name, 15), bg='#efc376')
    search_entry.place(x=100, y=150, width=380)

    search_button = Button(window, text="검색", font=(font_name, 12), bg='#efc376',
                           command=lambda: search_data(window, search_entry.get()))
    search_button.place(x=500, y=150)


def search_data(window, search_category, search_query):
    LoadopenAPI(search_category, search_query,None)
    if hasattr(window, 'listbox_frame'):
        window.listbox_frame.destroy()

    window.listbox_frame = Frame(window, bg='#efc376')
    window.listbox_frame.place(x=50, y=250, width=500, height=500)

    listbox_scrollbar = Scrollbar(window.listbox_frame, bg='#efc376')
    listbox_scrollbar.pack(side=RIGHT, fill=Y)

    listbox = Listbox(window.listbox_frame, font=(font_name, 10), bg='#efc376', yscrollcommand=listbox_scrollbar.set)
    listbox.pack(side=LEFT, fill=BOTH, expand=True)
    listbox.bind('<<ListboxSelect>>', lambda event: on_select(event, window))

    listbox_scrollbar.config(command=listbox.yview)

    update_listbox(listbox)

def update_listbox(listbox):
    global filtered_data
    listbox.delete(0, END)
    added_names = set()

    if filtered_data:
        for item in filtered_data:
            inst_name = item['instNm']
            if inst_name not in added_names:
                listbox.insert(END, inst_name)
                added_names.add(inst_name)
    else:
        listbox.insert(END, "관련 데이터가 없습니다.")

def on_select(event, window):
    global selected_item, filtered_data
    widget = event.widget
    selection = widget.curselection()
    added_names = []
    if filtered_data:
        for item in filtered_data:
            inst_name = item['instNm']
            if inst_name not in added_names:
                added_names.append(inst_name)

    if selection:
        index = selection[0]
        selected_item = added_names[index]

        # selected_inst_name에 해당하는 item을 찾아 selected_item에 할당합니다.
        for item in filtered_data:
            if item['instNm'] == selected_item:
                selected_item = item
                break
        display_details(window, selected_item)

def display_details(window, item):
    if hasattr(window, 'details_frame'):
        window.details_frame.destroy()

    details_frame = Frame(window, bg='#efc376')
    details_frame.place(x=575, y=50, width=500, height=300)

    details_text = Text(details_frame, font=(font_name, 12), bg='#efc376', wrap=WORD)
    details_text.pack(side=LEFT, fill=BOTH, expand=True)

    details_scrollbar = Scrollbar(details_frame, command=details_text.yview)
    details_scrollbar.pack(side=RIGHT, fill=Y)

    details_text.config(yscrollcommand=details_scrollbar.set)

    details_text.delete(1.0, END)
    num = 0
    if selected_item:
        details_text.insert(END, f"-하위시설명-\n")  # '하위시설명' 문구를 한 번만 출력
        for item in filtered_data:
            if item['instNm'] == selected_item['instNm']:
                details_text.insert(END, f"{item['fcltNm']}\n")  # 들여쓰기하여 하위시설명 출력
                num += 1
        if num == 0:
            details_text.insert(END, "하위 기관이 없습니다.")
    else:
        details_text.insert(END, "관련 데이터가 없습니다.")

    if hasattr(window, 'bar_chart_canvas'):
        window.bar_chart_canvas.destroy()

    bar_chart_canvas = Canvas(window, bg='#efc376')
    bar_chart_canvas.place(x=575, y=370, width=600, height=380)

    # 막대 그래프 데이터 준비
    fclt_type_counts = {}  # fcltTypeNm 값의 개수를 저장할 딕셔너리
    for sub_item in filtered_data:
        if sub_item['instNm'] == selected_item['instNm']:
            fclt_type = sub_item['fcltTypeNm']
            fclt_type_counts[fclt_type] = fclt_type_counts.get(fclt_type, 0) + 1

    # 막대 그래프를 그리기 위한 변수들 설정
    bar_width = 30
    space_between_bars = 10
    starting_x = 50
    starting_y = 300  # 높이 조정
    max_value = max(fclt_type_counts.values())

    # 막대 그래프 그리기
    for i, (fclt_type, count) in enumerate(fclt_type_counts.items()):
        bar_height = (count / max_value) * 200  # 높이 조정
        x0 = starting_x + i * (bar_width + space_between_bars)
        y0 = starting_y - bar_height
        x1 = x0 + bar_width
        y1 = starting_y
        bar_chart_canvas.create_rectangle(x0, y0, x1, y1, fill='blue')
        bar_chart_canvas.create_text(x0 + 15, y0 - 30, text=fclt_type, fill='black', font=(font_name, 10),
                                     angle=90)  # fclt_type를 세로로 작성
        bar_chart_canvas.create_text((x0 + x1) // 2, y1 + 10, text=str(count), fill='black', font=(font_name, 10))

    # x축 레이블
    bar_chart_canvas.create_text(300, 360, text="Facility Type", fill='black', font=(font_name, 12))  # 위치 조정
    # y축 레이블
    bar_chart_canvas.create_text(30, 260, text="Count", fill='black', font=(font_name, 8))  # 위치 조정
def InitLabel(window):
    label_topic = Label(window, text="기관 내 시설", font=(font_name, 30), bg='#efc376')
    label_topic.place(x=50, y=50)

def InitButton(window, reset_to_start_screen):
    back_button = create_back_button(window, reset_to_start_screen)
    back_button.place(x=1100, y=50)

def InitEmptyFrames(window):
    # 기본 빈 프레임들을 초기화
    window.listbox_frame = Frame(window, bg='#efc376')
    window.listbox_frame.place(x=50, y=250, width=500, height=500)

    window.listbox_scrollbar = Scrollbar(window.listbox_frame, bg='#efc376')
    window.listbox_scrollbar.pack(side=RIGHT, fill=Y)

    window.listbox = Listbox(window.listbox_frame, font=(font_name, 10), bg='#efc376', yscrollcommand=window.listbox_scrollbar.set)
    window.listbox.pack(side=LEFT, fill=BOTH, expand=True)
    window.listbox.bind('<<ListboxSelect>>', lambda event: on_select(event, window))

    window.listbox_scrollbar.config(command=window.listbox.yview)

    # 상세 정보 프레임
    window.details_frame = Frame(window, bg='#efc376')
    window.details_frame.place(x=575, y=50, width=500, height=300)

    window.details_text = Text(window.details_frame, font=(font_name, 12), bg='#efc376', wrap=WORD)
    window.details_text.pack(side=LEFT, fill=BOTH, expand=True)

    window.details_scrollbar = Scrollbar(window.details_frame, command=window.details_text.yview)
    window.details_scrollbar.pack(side=RIGHT, fill=Y)

    window.details_text.config(yscrollcommand=window.details_scrollbar.set)

    window.procedure_frame = Frame(window, bg='#efc376')
    window.procedure_frame.place(x=575, y=370, width=600, height=380)

    window.procedure_text = Text(window.procedure_frame, font=(font_name, 12), bg='#efc376', wrap=WORD)
    window.procedure_text.pack(side=LEFT, fill=BOTH, expand=True)

    window.procedure_scrollbar = Scrollbar(window.procedure_frame, command=window.procedure_text.yview)
    window.procedure_scrollbar.pack(side=RIGHT, fill=Y)

    window.procedure_text.config(yscrollcommand=window.procedure_scrollbar.set)

def switch_to_screen_4(window, reset_to_start_screen):
    clear_window(window)
    set_background(window)

    InitLabel(window)  # Label 초기화
    InitButton(window, reset_to_start_screen)  # Button 초기화
    InitCategoryDropdown(window)  # 카테고리 드롭다운 및 검색 초기화
    InitEmptyFrames(window)  # 빈 프레임 초기화