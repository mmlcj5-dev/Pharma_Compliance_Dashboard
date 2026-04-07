import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email_alert(to_email: str, subject: str, body: str) -> bool:
    """
    Sends an email alert using Gmail SMTP.
    Requires a Gmail App Password (not your normal Gmail password).
    """

    sender_email = "mmlcj5@gmail.com"
    sender_password = "YOUR_GMAIL_APP_PASSWORD"  # create in Google Account → Security → App passwords

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
        return True
    except Exception as e:
        print("Email error:", e)
        return False