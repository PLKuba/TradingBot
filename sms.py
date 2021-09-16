import smtplib
from config import MAIL,MAIL_PASSWORD

def send_mail(subject,body):
    sender = MAIL
    receiver = MAIL
    password = MAIL_PASSWORD

    # header
    message = f"""\
Subject: {subject}

{body}"""

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(sender,password)
        server.sendmail(sender, receiver, message)
        print("Email has been sent!")
    except smtplib.SMTPAuthenticationError:
        print("unable to sign in")
