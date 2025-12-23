import requests
from utility.settings import settings


def send_bin_alert_mail(
    receiver_email: str,
    category: str,
    location: str = "AutoSortBin",
) -> bool:
    """
    Send bin-full alert email using Brevo (Sendinblue) HTTP API.
    Works on Render (no SMTP).
    """

    print("📨 Mail task started")
    print("Receiver:", receiver_email)
    print("Category:", category)

    url = "https://api.brevo.com/v3/smtp/email"

    payload = {
        "sender": {
            "email": settings.email_sender,
            "name": "AutoSortBin"
        },
        "to": [
            {"email": receiver_email}
        ],
        "subject": f"Bin Full Alert: {category.capitalize()} Bin",
        "textContent": (
            f"The {category} bin is full and requires emptying.\n\n"
            f"Location: {location}"
        )
    }

    headers = {
        "accept": "application/json",
        "api-key": settings.brevo_api_key,
        "content-type": "application/json"
    }

    try:
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=10
        )

        print("📡 Brevo response code:", response.status_code)
        print("📨 Brevo response:", response.text)

        # Brevo returns 201 for success
        return response.status_code == 201

    except Exception as e:
        print("❌ Mail API error:", repr(e))
        return False
