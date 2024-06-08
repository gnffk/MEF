#!/usr/bin/python
# coding=utf-8

import sys
import traceback
from pprint import pprint

import telepot
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

def getData2(inst_type):
    global data, filtered_data, bizClsf

    bizClsf = ""
    if inst_type == '건강':
        bizClsf = "B01"
    elif inst_type == '공공안전':
        bizClsf = 'B02'
    elif inst_type == '교육연구':
        bizClsf = 'B03'
    elif inst_type == '국가인프라':
        bizClsf = 'B04'
    elif inst_type == '생활환경':
        bizClsf = 'B05'
    elif inst_type == '취업직업':
        bizClsf = 'B06'
    elif inst_type == '해외남북교류':
        bizClsf = 'B07'
    elif inst_type == '기타':
        bizClsf = 'B08'
    elif inst_type == '분류안됨':
        bizClsf = 'NULL'

    print(bizClsf)

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
        print(bizClsf)
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

    return filtered_data

def getData3(inst_type):
    global data, filtered_data
    res_list = []
    host = "apis.data.go.kr"
    endpoint = "/1051000/recruitment/list"
    params = {
        "serviceKey": "GuwRZzKrYZA0iHG1Y+ArdizUhu0a32Kym5AKO4tlpC71aaaCEI6YOzWIEfHyipefqThokj/9YurMG0WibwIfrA==",
        "numOfRows": "500"
    }
    response = fetch_data_from_api(host, endpoint, params)
    if response and "result" in response:
        data = response["result"]

        filtered_data = data
        print("API에서 불러온 데이터:")
        print(f"불러온 데이터 개수: {len(filtered_data)}")
    else:
        data = None
        filtered_data = None
        print("데이터를 불러올 수 없습니다.")

    for key in filtered_data:
        instTypeNm = key.get('hireTypeNmLst')
        if inst_type == instTypeNm:
            instName = key.get('instNm')
            instDesc = key.get('recrutPbancTtl')
            row = f'{instName}: {instDesc}'
            print(row)
            res_list.append(row.strip())

        elif instTypeNm == '청년인턴':
            if instTypeNm == '청년인턴(체험형)' or instTypeNm == '청년인턴(채용형)':
                instName = key.get('instNm')
                instDesc = key.get('recrutPbancTtl')
                row = f'{instName}: {instDesc}'
                print(row)
                res_list.append(row.strip())



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
