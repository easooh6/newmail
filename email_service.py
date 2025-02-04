import smtplib
from config import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Emessage():

    def __init__(self):
        self.server = smtplib.SMTP(EMAIL_HOST,EMAIL_PORT)
        self.server.starttls()
        self.server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)

    def send_message(self,host_add,receive_add,text):
        msg = MIMEMultipart()
        msg['From'] = host_add
        msg['To'] = receive_add
        msg['Subject'] = 'Your code'
        msg.attach(MIMEText(text,'plain'))

        self.server.sendmail(host_add,receive_add,msg.as_string())
    
    def close(self):
        self.server.quit()

