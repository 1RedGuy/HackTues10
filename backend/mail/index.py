import smtplib, ssl, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

smtp_server = os.getenv("SMTP_SERVER")
sender_email = os.getenv("SENDER_EMAIL")
port = 587
password = os.getenv("SMTP_PASSWORD")

context = ssl.create_default_context()

class Email_Service():
    def __init__(self):
        server = smtplib.SMTP(smtp_server,port)
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, password)
        self.server = server

    def send_email(self, receiver_email, message, subject):
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg.attach(MIMEText(message))
        self.server.sendmail(sender_email, receiver_email, msg.as_string())
    
    def send_password(self, receiver_email, password):
        message = (f"Your password is {password}")
        self.send_email(receiver_email, message, "EduNova: Your first password!")
        
