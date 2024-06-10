import smtplib
from email.mime.text import MIMEText
from tkinter import *
from assist import *
def open_email_window():
    email_window = Toplevel()
    email_window.title("이메일 보내 버려엇")
    email_window.geometry("400x300")
    set_background(email_window)

    Label(email_window, text="누구에게:",font=(font_name,10), bg = '#efc376').grid(row=0, column=0, padx=10, pady=10)
    receiver_entry = Entry(email_window, width=30, bg = '#efc376')
    receiver_entry.grid(row=0, column=1, padx=10, pady=10,)

    Label(email_window, text="주제:",font=(font_name,10), bg = '#efc376').grid(row=1, column=0, padx=10, pady=10)
    subject_entry = Entry(email_window, width=30, bg = '#efc376')
    subject_entry.grid(row=1, column=1, padx=10, pady=10)

    Label(email_window, text="목적:",font=(font_name,10), bg = '#efc376').grid(row=2, column=0, padx=10, pady=10)
    body_entry = Text(email_window, width=30, height=10, bg = '#efc376')
    body_entry.grid(row=2, column=1, padx=10, pady=10)

    def send_email():
        sender = "cnc4934@gmail.com"  # 고정된 보내는 사람 이메일 주소
        password = "rdoihmdlhthfdazu"  # 생성한 앱 비밀번호

        receiver = receiver_entry.get()
        subject = subject_entry.get()
        body = body_entry.get("1.0", END)

        # Gmail SMTP 서버에 연결 설정
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        # 이메일 메시지 생성
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = receiver

        try:
            # SMTP 서버에 연결
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, receiver, msg.as_string())
            server.quit()
            print("이메일이 성공적으로 전송되었습니다.")
        except Exception as e:
            print(f"이메일 전송 중 오류 발생: {e}")

    send_button = Button(email_window, text="Send",font=(font_name,10), command=send_email, bg = '#efc376')
    send_button.grid(row=3, column=1, pady=10)