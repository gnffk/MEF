from tkinter import *
from tkinter import font

import os

import urllib.parse
import http.client
import json

# 전역 변수로 이미지와 폰트를 로드
background_image = None
font_name = "충주김생체 TTF"



def preload_assets(window):
    global background_image
    # 배경 이미지 로드
    background_image = PhotoImage(file='image/korean_book_background.png')

# 배경 설정 함수
def set_background(window):
    global background_image
    background_label = Label(window, image=background_image, bg = '#efc376')
    background_label.image = background_image  # 이미지 객체 유지
    background_label.place(x=0, y=0)
    return background_label


# 창의 모든 위젯을 제거하는 함수
def clear_window(window):
    for widget in window.winfo_children():
        widget.destroy()


# 뒤로가기 버튼 생성 함수
def create_back_button(window, reset_to_start_screen):
    return Button(window, text="뒤로가기",bg = '#efc376', command=lambda: reset_to_start_screen(window))

# api 들고 오는 함수
def fetch_data_from_api(host, endpoint, params):
    query_string = urllib.parse.urlencode(params)

    # 연결을 만듭니다.
    conn = http.client.HTTPConnection(host)

    # 요청을 보냅니다.
    conn.request("GET", f"{endpoint}?{query_string}")

    # 응답을 받습니다.
    response = conn.getresponse()

    # 상태와 이유를 출력합니다.
    print(response.status, response.reason)

    # 응답 본문을 읽고 디코딩합니다.
    data = response.read().decode('utf-8')
    conn.close()

    # JSON 데이터로 변환하여 반환합니다.
    try:
        json_data = json.loads(data)

        # 원하는 데이터 필터링
        filtered_data = []
        if endpoint == "/1051000/public_inst/list":
            items = json_data["result"]

            for item in items:
                filtered_data.append({
                    "instCd": item.get("instCd"),
                    "instNm": item.get("instNm"),
                    "sprvsnInstCd": item.get("sprvsnInstCd"),
                    "sprvsnInstNm": item.get("sprvsnInstNm"),
                    "instType": item.get("instType"),
                    "roadNmAddr": item.get("roadNmAddr"),
                    "daddr": item.get("daddr"),
                    "rprsTelno": item.get("rprsTelno"),
                    "rprsEml": item.get("rprsEml"),
                    "siteUrl": item.get("siteUrl"),
                    "ctpvNm": item.get("ctpvNm"),
                    "lotnoAddr": item.get("lotnoAddr")
                })
        return filtered_data
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        return None

