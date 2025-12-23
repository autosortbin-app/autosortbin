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
    """
    Robust, non-blocking SMTP mail sender (Render-safe)
    """

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

    server = None

    try:
        # ⏱️ hard timeout → prevents hanging forever
        server = smtplib.SMTP(
            host="smtp.gmail.com",
            port=587,
            timeout=10
        )

        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login(
            settings.email_sender,
            settings.email_app_password
        )

        server.sendmail(
            settings.email_sender,
            receiver_email,
            msg.as_string()
        )

        print("✅ Mail sent successfully")
        return True

    except (smtplib.SMTPException, socket.timeout) as e:
        print("❌ Mail failed:", repr(e))
        return False

    except Exception as e:
        print("🔥 Unexpected mail error:", repr(e))
        return False

    finally:
        if server:
            try:
                server.quit()
            except Exception:
                pass

