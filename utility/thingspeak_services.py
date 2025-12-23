import requests
from utility.settings import settings

def write_bintoopen(value: int) -> bool:
    url = (
        f"https://api.thingspeak.com/update"
        f"?api_key={settings.thingspeak_write_api_key}"
        f"&field1={value}"
    )
    r = requests.get(url, timeout=10)
    return r.status_code == 200 and r.text != "0"


def write_binfull(value: int) -> bool:
    url = (
        f"https://api.thingspeak.com/update"
        f"?api_key={settings.thingspeak_write_api_key}"
        f"&field2={value}"
    )
    r = requests.get(url, timeout=10)
    return r.status_code == 200 and r.text != "0"


def read_bintoopen() -> int | None:
    url = (
        f"https://api.thingspeak.com/channels/"
        f"{settings.thingspeak_channel_id}/fields/1/last.json"
        f"?api_key={settings.thingspeak_read_api_key}"
    )
    r = requests.get(url, timeout=10)
    data = r.json()
    return int(data["field1"]) if data.get("field1") else None


def read_binfull() -> int | None:
    url = (
        f"https://api.thingspeak.com/channels/"
        f"{settings.thingspeak_channel_id}/fields/2/last.json"
        f"?api_key={settings.thingspeak_read_api_key}"
    )
    r = requests.get(url, timeout=10)
    data = r.json()
    return int(data["field2"]) if data.get("field2") else None
