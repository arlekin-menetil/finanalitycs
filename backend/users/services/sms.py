import requests
from django.conf import settings

TOKEN = None


def get_token():
    global TOKEN

    if TOKEN:
        return TOKEN

    try:
        res = requests.post(
            "https://notify.eskiz.uz/api/auth/login",
            data={
                "email": settings.ESKIZ_EMAIL,
                "password": settings.ESKIZ_PASSWORD
            },
            timeout=10
        )

        data = res.json()

        if "data" not in data:
            print("❌ Eskiz auth error:", data)
            return None

        TOKEN = data["data"]["token"]
        return TOKEN

    except Exception as e:
        print("❌ TOKEN ERROR:", e)
        return None


def send_sms(phone, code):
    token = get_token()

    if not token:
        return False

    message = "This is test from Eskiz"

    try:
        res = requests.post(
            "https://notify.eskiz.uz/api/message/sms/send",
            headers={
                "Authorization": f"Bearer {token}"
            },
            data={
                "mobile_phone": phone,
                "message": message,
                "from": "4546"
            },
            timeout=10
        )

        try:
            data = res.json()
            print("📩 Eskiz response:", data)
        except:
            print("❌ Eskiz raw:", res.text)

        return res.status_code == 200

    except Exception as e:
        print("❌ SMS ERROR:", e)
        return False