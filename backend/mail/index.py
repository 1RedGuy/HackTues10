import smtplib, ssl, os
from email.mime.multipart import MIMEMultipart

smtp_server = os.getenv("SMTP_SERVER")
sender_email = os.getenv("SENDER_EMAIL")
port = 465
password = os.getenv("PASSWORD")

context = ssl.create_default_context()

class Email_Service():
    def __init__(self):
        server = smtplib.SMTP_SSL(smtp_server,port)
        server.ehlo()
        server.login(sender_email, password)
        print("Email server connected")
        self.server = server
    def send_email(self, receiver_email, message, subject):
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = receiver_email
        self.server.sendmail(sender_email, receiver_email, message.as_string())
