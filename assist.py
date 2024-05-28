from tkinter import *
from tkinter import font
import requests
import os
from io import BytesIO
from PIL import Image, ImageTk
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

def request_geo(road):
    url = 'http://api.vworld.kr/req/address?'
    params = 'service=address&request=getcoord&version=2.0&crs=epsg:4326&refine=true&simple=false&format=json&type='
    road_type = 'ROAD'
    address = '&address='
    keys = '&key='
    primary_key = '4B834672-25F1-3943-972F-98B6E0E5E93A'
    page = requests.get(url+params+road_type+address+road+keys+primary_key)
    json_data = page.json()
    if json_data['response']['status'] == 'OK':
        x = json_data['response']['result']['point']['x']
        y = json_data['response']['result']['point']['y']
        return float(y), float(x)
    else:
        x = 0
        y = 0
        return y, x
# api 들고 오는 함수
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

def get_static_map_image(lat, lng, api_key, zoom=15, size=(400, 400)):
    base_url = "https://maps.googleapis.com/maps/api/staticmap?"
    params = {
        "center": f"{lat},{lng}",
        "zoom": zoom,
        "size": f"{size[0]}x{size[1]}",
        "key": api_key,
        "markers": f"color:red|{lat},{lng}"
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        image_data = response.content
        image = Image.open(BytesIO(image_data))
        return ImageTk.PhotoImage(image)
    else:
        print(f"Error: {response.status_code} - {response.reason}")
        return None