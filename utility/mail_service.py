import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utility.settings import settings


def send_bin_alert_mail(
    receiver_email: str,
    category: str,
    location: str = "AutoSortBin",
):
    """
    Sends bin full alert mail.
    """

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
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(
            settings.email_sender,
            settings.email_app_password
        )
        server.sendmail(
            settings.email_sender,
            receiver_email,
            msg.as_string()
        )
        return True

    except Exception as e:
        print("Mail error:", e)
        return False

    finally:
        try:
            server.quit()
        except:
            pass
