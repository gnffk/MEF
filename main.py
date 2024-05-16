import json
from tkinter import *
from start_screen import create_start_screen  # 스크린 설정 함수를 임포트

window = Tk()
window.title("MEF")
window.geometry("1000x800+100+100")
window.resizable(False, False)

def main():
    create_start_screen(window)
    window.mainloop()

if __name__ == '__main__':
    main()
else:
    print("main launcher imported\n")
