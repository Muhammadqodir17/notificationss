from django.conf import settings
import requests

TOKEN = settings.TOKEN
CHAT_ID = settings.CHAT_ID
TELEGRAM_API_URL = settings.TELEGRAM_API_URL


def send_message_telegram(obj):
    message = (
        f"Microservice: Notification\n"
        f"message:{obj.user} {obj.message}"
    )
    return requests.get(TELEGRAM_API_URL.format(TOKEN, message, CHAT_ID))
