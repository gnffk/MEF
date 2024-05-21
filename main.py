import json
from tkinter import *
from assist import preload_assets  # 어시스트의 자산을 미리 로드
from start_screen import create_start_screen  # 스크린 설정 함수를 임포트

window = Tk()
window.title("MEF")
window.geometry("1200x800+100+100")
window.resizable(False, False)

def main():
    preload_assets(window)  # 애플리케이션 시작 전에 자산을 미리 로드
    create_start_screen(window)
    window.mainloop()

if __name__ == '__main__':
    main()
else:
    print("main launcher imported\n")
    
