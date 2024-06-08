#!/usr/bin/python
# coding=utf-8

import sys
import time
import sqlite3
import telepot
from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
import traceback
from assist import fetch_data_from_api

TOKEN = '7435221852:AAFp7IvK36o1albxCVj8GP9DT1MUyCXNhi8'
MAX_MSG_LENGTH = 4096  # 텔레그램 메시지 최대 길이
bot = telepot.Bot(TOKEN)

def getData1(inst_type):
    global filtered_datas

    res_list = []
    host = "apis.data.go.kr"
    endpoint = "/1051000/public_inst/list"
    params = {
        "serviceKey": "GuwRZzKrYZA0iHG1Y+ArdizUhu0a32Kym5AKO4tlpC71aaaCEI6YOzWIEfHyipefqThokj/9YurMG0WibwIfrA==",
        "numOfRows": "366"
    }
    response = fetch_data_from_api(host, endpoint, params)
    if response and "result" in response:
        data = response["result"]

        filtered_datas = data

    for key in filtered_datas:
        instTypeNm = key.get('instTypeNm')
        if inst_type == '공기업':
            if instTypeNm == '공기업(준시장형)' or instTypeNm == '공기업(시장형)':
                instName = key.get('instNm')
                instDesc = key.get('sprvsnInstNm')
                instType = key.get('instTypeNm')
                row = f'{instName}: {instDesc} / {instType}'
                print(row)
                res_list.append(row.strip())

        elif inst_type == '준정부기관':
            if instTypeNm == '준정부기관(기금관리형)' or instTypeNm == '준정부기관(위탁집행형)':
                instName = key.get('instNm')
                instDesc = key.get('sprvsnInstNm')
                instType = key.get('instTypeNm')
                row = f'{instName}: {instDesc} / {instType}'
                print(row)
                res_list.append(row.strip())

        elif instTypeNm == '기타공공기관':
            if instTypeNm == '기타공공기관':
                instName = key.get('instNm')
                instDesc = key.get('sprvsnInstNm')
                instType = key.get('instTypeNm')
                row = f'{instName}: {instDesc} / {instType}'
                print(row)
                res_list.append(row.strip())

    # 결과 리스트 출력
    print("Result list:")
    print(res_list)

    return res_list

def sendMessage(user, msg):
    try:
        if len(msg) > MAX_MSG_LENGTH:
            for i in range(0, len(msg), MAX_MSG_LENGTH):
                bot.sendMessage(user, msg[i:i+MAX_MSG_LENGTH])
        else:
            bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)

if __name__ == '__main__':
    print('Received token:', TOKEN)
    pprint(bot.getMe())
