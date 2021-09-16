import smtplib

def send_mail(subject,body):
    sender = "major.plays96@gmail.com"
    receiver = "major.plays96@gmail.com"
    password = "oqnltyqhugtacydj"

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