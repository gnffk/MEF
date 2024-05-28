import json
from tkinter import *
from assist import *
import urllib.parse
import http.client

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
        print("관련 데이터가 없습니다.")


def fetch_data_from_api(host, endpoint, params):
    query_string = urllib.parse.urlencode(params)
    conn = http.client.HTTPConnection(host)
    conn.request("GET", f"{endpoint}?{query_string}")
    response = conn.getresponse()

    data = response.read().decode("utf-8")
    conn.close()
    if response.status == 200:
        try:
            json_data = json.loads(data)
            return json_data
        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}")
            return None
    else:
        print(f"HTTP Error: {response.status} {response.reason}")
        return None


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
        listbox.insert(END, "관련 데이터가 없습니다.")


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
    if data:
        filtered_data = [item for item in data if query.lower() in item['bizNm'].lower()]
    else:
        filtered_data = None
    if hasattr(window, 'listbox_frame'):
        window.listbox_frame.destroy()

    window.listbox_frame = Frame(window, bg='#efc376')
    window.listbox_frame.place(x=50, y=300, width=500, height=400)

    listbox_scrollbar = Scrollbar(window.listbox_frame, bg='#efc376')
    listbox_scrollbar.pack(side=RIGHT, fill=Y)

    listbox = Listbox(window.listbox_frame, font=(font_name, 10), bg='#efc376', yscrollcommand=listbox_scrollbar.set)
    listbox.pack(side=LEFT, fill=BOTH, expand=True)

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
        listbox.insert(END, "관련 데이터가 없습니다.")


def InitButton(window, reset_to_start_screen):
    back_button = create_back_button(window, reset_to_start_screen)
    back_button.place(x=1100, y=50)


def switch_to_screen_2(window, reset_to_start_screen):
    clear_window(window)
    set_background(window)

    InitLabel(window)  # Label 초기화
    InitButton(window, reset_to_start_screen)  # Button 초기화
    InitCategoryDropdown(window)  # 사업 분야 드롭다운 초기화
    InitSearch(window)  # 검색 초기화
