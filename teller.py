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

import noti


def send_welcome_message(chat_id):
    welcome_message = ("안녕하세요 MEF 챗봇입니다. 원하시는 정보를 입력해주세요\n"
                       "1. 기업 정보\n"
                       "2. 채용 정보\n"
                       "3. 사업 정보")
    noti.sendMessage(chat_id, welcome_message)


def send_company_categories(chat_id):
    categories_message = ("원하시는 기업 정보를 선택해주세요\n"
                          "1. 공기업\n"
                          "2. 준정부기관\n"
                          "3. 기타공공기관")
    noti.sendMessage(chat_id, categories_message)

def send_busy_categories(chat_id):
    categories_message = ("원하시는 사업 정보를 선택해주세요\n"
                          "1. 건강\n"
                          "2. 공공안전\n"
                          "3. 교육연구\n"
                          "4. 국가인프라\n"
                          "5. 문화생활\n"
                          "6. 사회복지\n"
                          "7. 산업진흥\n"
                          "8. 생활환경\n"
                          "9. 취업직업\n"
                          "10. 해외남북교류\n"
                          "11. 기타\n"
                          "12. 분류안됨")
    noti.sendMessage(chat_id, categories_message)

def send_categories(chat_id):
    categories_message = ("원하시는 기업 정보를 선택해주세요\n"
                          "1. 정규직\n"
                          "2. 무기계약직\n"
                          "3. 비정규직\n"
                          "4. 청년인턴\n")
    noti.sendMessage(chat_id, categories_message)

def handle_company_details(chat_id, category):
    inst_type_map = {
        '공기업': '공기업',
        '준정부기관': '준정부기관',
        '기타공공기관': '기타공공기관'
    }
    inst_type = inst_type_map.get(category)
    if inst_type:
        res_list = noti.getData1(inst_type)
        if res_list:
            details_message = '\n'.join(res_list)
        else:
            details_message = f'{inst_type}에 대한 정보를 찾을 수 없습니다.'
    else:
        details_message = "잘못된 선택입니다. 다시 시도해주세요."

    noti.sendMessage(chat_id, details_message)
    send_welcome_message(chat_id)  # 정보를 출력한 후 다시 초기 화면으로 돌아갑니다.

def handle_busy_details(chat_id, category):
    res_list = noti.getData2(category)
    if res_list:
        details_message = '\n'.join([f"{item['bizNm']}" for item in res_list])
    else:
        details_message = f'{category}에 대한 정보를 찾을 수 없습니다.'

    noti.sendMessage(chat_id, details_message)
    send_welcome_message(chat_id)  # 정보를 출력한 후 다시 초기 화면으로 돌아갑니다.

def handle_details(chat_id, inst_type):

    if inst_type:
        res_list = noti.getData3(inst_type)

        if res_list:
            details_message = '\n'.join(res_list)
        else:
            details_message = f'{inst_type}에 대한 정보를 찾을 수 없습니다.'
    else:
        details_message = "잘못된 선택입니다. 다시 시도해주세요."

    noti.sendMessage(chat_id, details_message)
    send_welcome_message(chat_id)  # 정보를 출력한 후 다시 초기 화면으로 돌아갑니다.
def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        noti.sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return

    text = msg['text']
    args = text.split(' ')

    if text.startswith('안녕') or text.startswith('/start'):
        send_welcome_message(chat_id)
    elif text.startswith('기업'):
        send_company_categories(chat_id)
    elif text in ['공기업', '준정부기관', '기타공공기관']:
        handle_company_details(chat_id, text)
    elif text.startswith('사업'):
        send_busy_categories(chat_id)
    elif text in ['건강', '공공안전', '교육연구', '국가인프라', '문화생활', '사회복지', '산업진흥','생활환경','취업직업','해외남북교류','기타','분류안됨']:
        handle_busy_details(chat_id, text)
    elif text.startswith('채용'):
        send_categories(chat_id)
    elif text in ['정규직', '무기계약직', '비정규직', '청년인턴']:
        handle_details(chat_id, text)
    else:
        noti.sendMessage(chat_id, '모르는 명령어입니다.\n')


def start_telegram_bot():
    bot = telepot.Bot(noti.TOKEN)
    bot.message_loop(handle)
    while True:
        time.sleep(10)

# 이 부분은 메인 프로그램에서 직접 실행하지 않도록 주석 처리합니다.
# if __name__ == '__main__'
#    start_telegram_bot()
