import smtplib
from config import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from celery import Celery

app = Celery('letters',broker=CELERY_BROKER_URL)


@app.task
def send_message(host_add,receive_add,text):
    try:
        server = smtplib.SMTP(EMAIL_HOST,EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)

        msg = MIMEMultipart()
        msg['From'] = host_add
        msg['To'] = receive_add
        msg['Subject'] = 'Your code'
        msg.attach(MIMEText(text,'plain'))

        server.sendmail(host_add,receive_add,msg.as_string())
        server.quit()
    except Exception:
        print("Error sending email", Exception)

