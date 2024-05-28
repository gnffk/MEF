from tkinter import *
from assist import *
import json

# 전역 변수 선언
data = None
filtered_data = None

def fetch_data_from_api(host, endpoint, params):
    import http.client
    import urllib.parse

    query_string = urllib.parse.urlencode(params)
    conn = http.client.HTTPConnection(host)
    conn.request("GET", f"{endpoint}?{query_string}")
    response = conn.getresponse()

    if response.status == 200:
        data = response.read().decode("utf-8")
        conn.close()
        return json.loads(data)
    else:
        conn.close()
        return None

def LoadopenAPI(search_category=None, search_query=None):
    global data, filtered_data
    host = "apis.data.go.kr"
    endpoint = "/1051000/recruitment/list"
    params = {
        "serviceKey": "GuwRZzKrYZA0iHG1Y+ArdizUhu0a32Kym5AKO4tlpC71aaaCEI6YOzWIEfHyipefqThokj/9YurMG0WibwIfrA==",
        "numOfRows": "700"
    }
    response = fetch_data_from_api(host, endpoint, params)
    if response and "result" in response:
        data = response["result"]
        # 카테고리 및 검색어에 따라 데이터를 필터링합니다.
        if search_category and search_query:
            if search_category == "공시기관":
                filtered_data = [item for item in data if search_query.lower() in item["instNm"].lower()]
            elif search_category == "공시제목":
                filtered_data = [item for item in data if search_query.lower() in item["recrutPbancTtl"].lower()]
        else:
            filtered_data = data
        print("API에서 불러온 데이터:")
        print(json.dumps(filtered_data, indent=4, ensure_ascii=False))
        print(f"불러온 데이터 개수: {len(filtered_data)}")
    else:
        data = None
        filtered_data = None
        print("데이터를 불러올 수 없습니다.")

def InitCategoryDropdown(window):
    selected_category = StringVar(window)
    selected_category.set("공시기관")  # 기본값 설정
    dropdown_label = Label(window, text="주제 카테고리:", font=(font_name, 15), bg='#efc376')
    dropdown_label.place(x=50, y=150)

    dropdown = OptionMenu(window, selected_category, "공시기관", "공시제목")
    dropdown.config(font=(font_name, 12), bg='#efc376')
    dropdown.place(x=200, y=150, width=200, height=30)

    search_label = Label(window, text="검색:", font=(font_name, 15), bg='#efc376')
    search_label.place(x=50, y=200)

    search_entry = Entry(window, font=(font_name, 15), bg='#efc376')
    search_entry.place(x=100, y=200, width=380)

    search_button = Button(window, text="검색", font=(font_name, 12), bg='#efc376',
                           command=lambda: search_data(window, selected_category.get(), search_entry.get()))
    search_button.place(x=500, y=200)

def search_data(window, search_category, search_query):
    LoadopenAPI(search_category, search_query)
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
    if filtered_data:
        for item in filtered_data:
            listbox.insert(END, f"{item['instNm']} - {item['recrutPbancTtl']}")
    else:
        listbox.insert(END, "관련 데이터가 없습니다.")

def on_select(event, window):
    widget = event.widget
    selection = widget.curselection()
    if selection:
        index = selection[0]
        selected_item = filtered_data[index]
        display_details(window, selected_item)

def display_details(window, item):
    details_frame = Frame(window, bg='#efc376')
    details_frame.place(x=575, y=50, width=500, height=300)

    details_text = Text(details_frame, font=(font_name, 12), bg='#efc376', wrap=WORD)
    details_text.pack(side=LEFT, fill=BOTH, expand=True)

    details_scrollbar = Scrollbar(details_frame, command=details_text.yview)
    details_scrollbar.pack(side=RIGHT, fill=Y)

    details_text.config(yscrollcommand=details_scrollbar.set)

    details_text.delete(1.0, END)

    details = f"""
기관명: {item['instNm']}
공시제목: {item['recrutPbancTtl']}
NCS 코드명: {item.get('ncsCdNmLst', '없음')}
고용형태: {item.get('hireTypeNmLst', '없음')}
근무지역: {item.get('workRgnNmLst', '없음')}
채용구분: {item.get('recrutSeNm', '없음')}
우대조건: {item.get('prefCondCn', '없음')}
공고시작일: {item.get('pbancBgngYmd', '없음')}
공고종료일: {item.get('pbancEndYmd', '없음')}
홈페이지: {item.get('srcUrl', '없음')}
채용정보 URL: {item.get('srcUrl', '없음')}
신입/경력: {item.get('recrutSeNm', '없음')}
응시 자격: {item.get('aplyQlfcCn', '없음')}
학력조건: {item.get('acbgCondNmLst', '없음')}
모집여부: {item.get('ongoingYn', '없음')}
    """
    details_text.insert(END, details)

    # 전형절차 및 방법 프레임
    procedure_frame = Frame(window, bg='#efc376')
    procedure_frame.place(x=575, y=370, width=500, height=200)

    procedure_text = Text(procedure_frame, font=(font_name, 12), bg='#efc376', wrap=WORD)
    procedure_text.pack(side=LEFT, fill=BOTH, expand=True)

    procedure_scrollbar = Scrollbar(procedure_frame, command=procedure_text.yview)
    procedure_scrollbar.pack(side=RIGHT, fill=Y)

    procedure_text.config(yscrollcommand=procedure_scrollbar.set)

    procedure_text.delete(1.0, END)
    procedure_text.insert(END, f"전형절차 및 방법: \n{item.get('scrnprcdrMthdExpln', '없음')}")

    # 결격사유 프레임
    disqualification_frame = Frame(window, bg='#efc376')
    disqualification_frame.place(x=575, y=600, width=500, height=100)

    disqualification_text = Text(disqualification_frame, font=(font_name, 12), bg='#efc376', wrap=WORD)
    disqualification_text.pack(side=LEFT, fill=BOTH, expand=True)

    disqualification_scrollbar = Scrollbar(disqualification_frame, command=disqualification_text.yview)
    disqualification_scrollbar.pack(side=RIGHT, fill=Y)

    disqualification_text.config(yscrollcommand=disqualification_scrollbar.set)

    disqualification_text.delete(1.0, END)
    disqualification_text.insert(END, f"결격사유: \n{item.get('disqlfcRsn', '없음')}")

def InitLabel(window):
    label_topic = Label(window, text="공공기관 공시 정보", font=(font_name, 30), bg='#efc376')
    label_topic.place(x=50, y=50)

def InitButton(window, reset_to_start_screen):
    back_button = create_back_button(window, reset_to_start_screen)
    back_button.place(x=1100, y=50)

def InitEmptyFrames(window):
    # 기본 빈 프레임들을 초기화
    details_frame = Frame(window, bg='#efc376')
    details_frame.place(x=575, y=50, width=500, height=300)

    details_text = Text(details_frame, font=(font_name, 12), bg='#efc376', wrap=WORD)
    details_text.pack(side=LEFT, fill=BOTH, expand=True)

    details_scrollbar = Scrollbar(details_frame, command=details_text.yview)
    details_scrollbar.pack(side=RIGHT, fill=Y)

    details_text.config(yscrollcommand=details_scrollbar.set)


    # 전형절차 및 방법 프레임
    procedure_frame = Frame(window, bg='#efc376')
    procedure_frame.place(x=575, y=370, width=500, height=200)

    procedure_text = Text(procedure_frame, font=(font_name, 12), bg='#efc376', wrap=WORD)
    procedure_text.pack(side=LEFT, fill=BOTH, expand=True)

    procedure_scrollbar = Scrollbar(procedure_frame, command=procedure_text.yview)
    procedure_scrollbar.pack(side=RIGHT, fill=Y)

    procedure_text.config(yscrollcommand=procedure_scrollbar.set)


    # 결격사유 프레임
    disqualification_frame = Frame(window, bg='#efc376')
    disqualification_frame.place(x=575, y=600, width=500, height=100)

    disqualification_text = Text(disqualification_frame, font=(font_name, 12), bg='#efc376', wrap=WORD)
    disqualification_text.pack(side=LEFT, fill=BOTH, expand=True)

    disqualification_scrollbar = Scrollbar(disqualification_frame, command=disqualification_text.yview)
    disqualification_scrollbar.pack(side=RIGHT, fill=Y)

    disqualification_text.config(yscrollcommand=disqualification_scrollbar.set)


def switch_to_screen_3(window, reset_to_start_screen):
    clear_window(window)
    set_background(window)

    InitLabel(window)  # Label 초기화
    InitButton(window, reset_to_start_screen)  # Button 초기화
    InitCategoryDropdown(window)  # 카테고리 드롭다운 및 검색 초기화
    InitEmptyFrames(window)  # 빈 프레임 초기화

