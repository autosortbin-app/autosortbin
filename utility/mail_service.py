import smtplib
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utility.settings import settings


def send_bin_alert_mail(
    receiver_email: str,
    category: str,
    location: str = "AutoSortBin",
):
    print("📨 Mail task started")
    print("Receiver:", receiver_email)
    print("Category:", category)

    subject = f"Bin Full Alert: {category.capitalize()} Bin"
    body = (
        f"The {category} bin is full and requires emptying.\n\n"
        f"Location: {location}"
    )

    msg = MIMEMultipart()
    msg["From"] = settings.email_sender
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        # 🔥 Explicit network check
        socket.create_connection(("smtp.gmail.com", 465), timeout=10)

        # ✅ SSL SMTP (works on Render)
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=20)
        server.login(
            settings.email_sender,
            settings.email_app_password
        )
        server.sendmail(
            settings.email_sender,
            receiver_email,
            msg.as_string()
        )
        server.quit()

        print("✅ Mail sent successfully")
        return True

    except Exception as e:
        print("❌ Mail error:", repr(e))
        return False
