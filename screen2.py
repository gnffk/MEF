import json
from tkinter import *
from assist import *

# 사업 분야(대)와 중분류 목록
categories = {
    "건강": ["전체 - B01", "식의약품안전 - B0101", "의료지원 - B0102", "질병치료 - B0103", "환경위생 - B0104", "기타 - B0105"],
    "공공안전": ["전체 - B02", "공공기능 - B0201", "국방 - B0202", "사업안전 - B0203", "시설안전 - B0204", "기타 - B0205"],
    "교육연구": ["전체 - B03", "교육 - B0301", "교육지원 - B0302", "연구개발 - B0303", "기타 - B0304"],
    "국가인프라": ["전체 - B04", "교통 - B0401", "물류 - B0402", "에너지 - B0403", "자원 - B0404", "기타 - B0405"],
    "문화생활": ["전체 - B05", "문화예술 - B0501", "여가활동 - B0502", "체육활동 - B0503", "기타 - B0504"],
    "사회복지": ["전체 - B06", "일반복지 - B0601", "취약계층복지 - B0602", "기타 - B0603"],
    "산업진흥": ["전체 - B07", "산업금융 - B0701", "산업발전 - B0702", "산업지원 - B0703", "기타 - B0704"],
    "생활환경": ["전체 - B08", "기상기후 - B0801", "소비자지원 - B0802", "자연환경 - B0803", "주거환경 - B0804", "주택토지 - B0805", "기타 - B0806"],
    "취업직업": ["전체 - B09", "노동연구 - B0901", "취업/직장생활 - B0902", "기타 - B0903"],
    "해외남북교류": ["전체 - B10", "남북교류 - B1001", "해외교류 - B1002", "기타 - B1003"],
    "기타": ["전체 - B11", "기타 - B1101"],
    "분류안됨": ["전체 - NULL"]
}

data = None
filtered_data = None
selected_item = None  # 전역 변수로 선택한 아이템 저장

def LoadopenAPI(bizClsf=None):
    global data, filtered_data
    data = []
    pageNo = 1
    while True:
        host = "apis.data.go.kr"
        endpoint = "/1051000/biz/list"
        params = {
            "serviceKey": "GuwRZzKrYZA0iHG1Y+ArdizUhu0a32Kym5AKO4tlpC71aaaCEI6YOzWIEfHyipefqThokj/9YurMG0WibwIfrA==",
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
        print("API에서 불러온 데이터:")
        print(json.dumps(data, indent=4, ensure_ascii=False))
        print(f"불러온 데이터 개수: {len(data)}")
    else:
        data = None
        filtered_data = None
        print("데이터를 불러올 수 없습니다.")

def InitLabel(window):
    label_topic = Label(window, text="공공기관 진행 사업 정보", font=(font_name, 30), bg='#efc376')
    label_topic.place(x=50, y=50)

def InitCategoryDropdown(window):
    selected_category = StringVar(window)
    selected_category.set("건강")  # 기본값 설정
    dropdown_label = Label(window, text="사업 분야(대):", font=(font_name, 15), bg='#efc376')
    dropdown_label.place(x=50, y=150)

    dropdown = OptionMenu(window, selected_category, *categories.keys(),
                          command=lambda _: update_subcategories(window, selected_category.get()))
    dropdown.config(font=(font_name, 12), bg='#efc376')
    dropdown.place(x=200, y=150, width=200, height=30)

    InitSubCategoryDropdown(window, "건강")  # 초기 하위 카테고리 설정

def InitSubCategoryDropdown(window, category):
    subcategories = categories[category]
    selected_subcategory = StringVar(window)
    selected_subcategory.set(subcategories[0])  # 기본값 설정

    if hasattr(window, 'sub_dropdown_label'):
        window.sub_dropdown_label.destroy()
    if hasattr(window, 'sub_dropdown'):
        window.sub_dropdown.destroy()
    if hasattr(window, 'select_button'):
        window.select_button.destroy()

    window.sub_dropdown_label = Label(window, text="사업 분야(중):", font=(font_name, 15), bg='#efc376')
    window.sub_dropdown_label.place(x=50, y=200)

    window.sub_dropdown = OptionMenu(window, selected_subcategory, *subcategories)
    window.sub_dropdown.config(font=(font_name, 12), bg='#efc376')
    window.sub_dropdown.place(x=200, y=200, width=200, height=30)

    window.select_button = Button(window, text="선택", font=(font_name, 12), bg='#efc376',
                                  command=lambda: select_subcategory(window, selected_subcategory.get()))
    window.select_button.place(x=410, y=200, width=60, height=30)

def update_subcategories(window, category):
    InitSubCategoryDropdown(window, category)

def select_subcategory(window, subcategory):
    bizClsf = None if subcategory == "전체 - NULL" else subcategory.split(" - ")[1]
    LoadopenAPI(bizClsf=bizClsf)  # 선택한 후에 데이터를 다시 로드합니다
    print(f"Selected subcategory: {subcategory}")
    if hasattr(window, 'listbox_frame'):
        window.listbox_frame.destroy()

    window.listbox_frame = Frame(window, bg='#efc376')
    window.listbox_frame.place(x=50, y=300, width=500, height=400)

    listbox_scrollbar = Scrollbar(window.listbox_frame, bg='#efc376')
    listbox_scrollbar.pack(side=RIGHT, fill=Y)

    listbox = Listbox(window.listbox_frame, font=(font_name, 10), bg='#efc376', yscrollcommand=listbox_scrollbar.set)
    listbox.pack(side=LEFT, fill=BOTH, expand=True)
    listbox.bind('<<ListboxSelect>>', lambda event: on_select(event, window))

    listbox_scrollbar.config(command=listbox.yview)

    update_listbox(listbox, bizClsf)

def update_listbox(listbox, subcategory_code):
    global filtered_data
    listbox.delete(0, END)
    if filtered_data:
        if subcategory_code is None:
            filtered_items = [item for item in filtered_data if item.get('bizClsf') is None]
        else:
            filtered_items = [item for item in filtered_data if subcategory_code == "B0" or (
                        item.get('bizClsf') and item['bizClsf'].startswith(subcategory_code))]
        if filtered_items:
            for item in filtered_items:
                listbox.insert(END, f"{item['bizNm']}")
        else:
            listbox.insert(END, "관련 데이터가 없습니다.")
    else:
        listbox.insert(END, "데이터를 불러올 수 없습니다.")

def InitSearch(window):
    search_label = Label(window, text="검색:", font=(font_name, 15), bg='#efc376')
    search_label.place(x=50, y=250)

    search_entry = Entry(window, font=(font_name, 15), bg='#efc376')
    search_entry.place(x=100, y=250, width=380)

    search_button = Button(window, text="검색", font=(font_name, 12), bg='#efc376',
                           command=lambda: search_data(window, search_entry.get()))
    search_button.place(x=500, y=250)

def search_data(window, query):
    global filtered_data
    if filtered_data:
        filtered_items = [item for item in filtered_data if query.lower() in item['bizNm'].lower()]
    else:
        filtered_items = []

    if hasattr(window, 'listbox_frame'):
        window.listbox_frame.destroy()

    window.listbox_frame = Frame(window, bg='#efc376')
    window.listbox_frame.place(x=50, y=300, width=500, height=400)

    listbox_scrollbar = Scrollbar(window.listbox_frame, bg='#efc376')
    listbox_scrollbar.pack(side=RIGHT, fill=Y)

    listbox = Listbox(window.listbox_frame, font=(font_name, 10), bg='#efc376', yscrollcommand=listbox_scrollbar.set)
    listbox.pack(side=LEFT, fill=BOTH, expand=True)
    listbox.bind('<<ListboxSelect>>', lambda event: on_select(event, window))

    listbox_scrollbar.config(command=listbox.yview)

    update_listbox_search(listbox, query)

def update_listbox_search(listbox, query):
    global filtered_data
    listbox.delete(0, END)
    if filtered_data:
        filtered_items = [item for item in filtered_data if query.lower() in item['bizNm'].lower()]
        if filtered_items:
            for item in filtered_items:
                listbox.insert(END, f"{item['bizNm']}")
        else:
            listbox.insert(END, "관련 데이터가 없습니다.")
    else:
        listbox.insert(END, "데이터를 불러올 수 없습니다.")

def on_select(event, window):
    global selected_item
    widget = event.widget
    selection = widget.curselection()
    if selection:
        index = selection[0]
        selected_item = filtered_data[index]
        display_details(window)

def display_details(window):
    global selected_item
    if selected_item:
        # 상세 정보 프레임
        details_frame = Frame(window, bg='#efc376')
        details_frame.place(x=600, y=100, width=500, height=300)

        details_text = Text(details_frame, font=(font_name, 12), bg='#efc376', wrap=WORD)
        details_text.pack(side=LEFT, fill=BOTH, expand=True)

        details_scrollbar = Scrollbar(details_frame, command=details_text.yview)
        details_scrollbar.pack(side=RIGHT, fill=Y)

        details_text.config(yscrollcommand=details_scrollbar.set)

        details_text.delete(1.0, END)  # 기존 내용을 지우고 새로운 내용을 추가합니다.

        details = f"""
사업명: {selected_item['bizNm']}
기관명: {selected_item['instNm']}
사업분류: {selected_item['bizClsfNm']}
사업기간: {selected_item['bizPeriodSeNm']}
문의정보: {selected_item['utztnInqInfo']}
홈페이지: {selected_item['siteUrl'] if selected_item['siteUrl'] else '없음'}
생애주기: {selected_item['lifecyclNmLst'] if selected_item['lifecyclNmLst'] else '없음'}
        """
        details_text.insert(END, details)

        # 사업 설명 프레임
        biz_expln_frame = Frame(window, bg='#efc376')
        biz_expln_frame.place(x=600, y=400, width=500, height=150)

        biz_expln_text = Text(biz_expln_frame, font=(font_name, 12), bg='#efc376', wrap=WORD)
        biz_expln_text.pack(side=LEFT, fill=BOTH, expand=True)

        biz_expln_scrollbar = Scrollbar(biz_expln_frame, command=biz_expln_text.yview)
        biz_expln_scrollbar.pack(side=RIGHT, fill=Y)

        biz_expln_text.config(yscrollcommand=biz_expln_scrollbar.set)

        biz_expln_text.delete(1.0, END)
        biz_expln_text.insert(END, f"사업설명: \n{selected_item['bizExpln']}")

        # 대상자 설명 프레임
        target_expln_frame = Frame(window, bg='#efc376')
        target_expln_frame.place(x=600, y=550, width=500, height=150)

        target_expln_text = Text(target_expln_frame, font=(font_name, 12), bg='#efc376', wrap=WORD)
        target_expln_text.pack(side=LEFT, fill=BOTH, expand=True)

        target_expln_scrollbar = Scrollbar(target_expln_frame, command=target_expln_text.yview)
        target_expln_scrollbar.pack(side=RIGHT, fill=Y)

        target_expln_text.config(yscrollcommand=target_expln_scrollbar.set)

        target_expln_text.delete(1.0, END)
        target_expln_text.insert(END, f"대상자설명: \n{selected_item['utztnTrgtExpln']}")

def InitButton(window, reset_to_start_screen):
    back_button = create_back_button(window, reset_to_start_screen)
    back_button.place(x=1100, y=50)

def InitEmptyFrames(window):
    # 기본 빈 프레임들을 초기화
    details_frame = Frame(window, bg='#efc376')
    details_frame.place(x=600, y=100, width=500, height=300)

    details_text = Text(details_frame, font=(font_name, 12), bg='#efc376', wrap=WORD)
    details_text.pack(side=LEFT, fill=BOTH, expand=True)

    details_scrollbar = Scrollbar(details_frame, command=details_text.yview)
    details_scrollbar.pack(side=RIGHT, fill=Y)

    details_text.config(yscrollcommand=details_scrollbar.set)


    # 사업 설명 프레임
    biz_expln_frame = Frame(window, bg='#efc376')
    biz_expln_frame.place(x=600, y=400, width=500, height=150)

    biz_expln_text = Text(biz_expln_frame, font=(font_name, 12), bg='#efc376', wrap=WORD)
    biz_expln_text.pack(side=LEFT, fill=BOTH, expand=True)

    biz_expln_scrollbar = Scrollbar(biz_expln_frame, command=biz_expln_text.yview)
    biz_expln_scrollbar.pack(side=RIGHT, fill=Y)

    biz_expln_text.config(yscrollcommand=biz_expln_scrollbar.set)

    # 대상자 설명 프레임
    target_expln_frame = Frame(window, bg='#efc376')
    target_expln_frame.place(x=600, y=550, width=500, height=150)

    target_expln_text = Text(target_expln_frame, font=(font_name, 12), bg='#efc376', wrap=WORD)
    target_expln_text.pack(side=LEFT, fill=BOTH, expand=True)

    target_expln_scrollbar = Scrollbar(target_expln_frame, command=target_expln_text.yview)
    target_expln_scrollbar.pack(side=RIGHT, fill=Y)

    target_expln_text.config(yscrollcommand=target_expln_scrollbar.set)


def switch_to_screen_2(window, reset_to_start_screen):
    clear_window(window)
    set_background(window)

    InitLabel(window)  # Label 초기화
    InitButton(window, reset_to_start_screen)  # Button 초기화
    InitCategoryDropdown(window)  # 사업 분야 드롭다운 초기화
    InitSearch(window)  # 검색 초기화
    InitEmptyFrames(window)  # 빈 프레임 초기화


