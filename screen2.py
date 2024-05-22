from assist import *

def InitScrollBar(window):
    global data
    listbox_frame = Frame(window)
    listbox_frame.place(x=50, y=220, width=500, height=180)

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

def InitGraph(window):
    listbox_frame1 = Frame(window)
    listbox_frame1.place(x=50, y=450, width=500, height=300)

    ListBoxScrollbar1 = Scrollbar(listbox_frame1)
    ListBoxScrollbar1.pack(side=RIGHT, fill=Y)

    SearchListBox = Listbox(listbox_frame1, yscrollcommand=ListBoxScrollbar1.set)
    SearchListBox.pack(side=LEFT, fill=BOTH, expand=True)

    ListBoxScrollbar1.config(command=SearchListBox.yview)

def InitInform(window):
    listbox_frame2 = Frame(window)
    listbox_frame2.place(x=600, y=120, width=500, height=630)

    ListBoxScrollbar2 = Scrollbar(listbox_frame2)
    ListBoxScrollbar2.pack(side=RIGHT, fill=Y)

    SearchListBox = Listbox(listbox_frame2, yscrollcommand=ListBoxScrollbar2.set)
    SearchListBox.pack(side=LEFT, fill=BOTH, expand=True)

    ListBoxScrollbar2.config(command=SearchListBox.yview)

def search(window):
    StringVar = Frame(window)
    StringVar.place(x=50,y=120,width = 500,height=50)
    str = StringVar
    Entry(StringVar,textvariable=str,font=(font_name,30),justify=LEFT,width=500).pack(side=LEFT)

def InitLabel(window):
    label_topic = Label(window, text="공공기관 진행 사업 정보", font=(font_name, 30), bg='#efc376')
    label_topic.place(x=50, y=50)

def InitButton(window, reset_to_start_screen):
    back_button = create_back_button(window, reset_to_start_screen)
    back_button.place(x=1100, y=50)

def switch_to_screen_2(window, reset_to_start_screen):
    clear_window(window)
    set_background(window)

    InitLabel(window)  # Label 정리
    search(window)
    InitGraph(window)
    InitInform(window)
    InitButton(window, reset_to_start_screen)  # Button 정리
    InitScrollBar(window)  # ScrollBar 정리