from rest_framework.viewsets import ViewSet
from .models import Notification
import requests

TELEGRAM_BOT_TOKEN = '6617362077:AAEtf2XpYMWLVtAg3kiUNCFvNvcenHfQt9M'


class NotificationViewSet(ViewSet):

    def send_notification(self, request):
        pass

    def send_liked_notification(self, chat_id, tg_token, post):
        notification = Notification.objects.filter(post=post).first()
        if notification and notification.notification_type == 'like':
            message = notification.message
            requests.get(f"""http://api.telegram.org/bot{tg_token}sendMessage
                        ?chat_id={chat_id}&text={message}""")

    def send_commented_notification(self, chat_id, tg_token, post):
        notification = Notification.objects.filter(post=post).first()
        if notification and notification.notification_type == 'comment':
            message = notification.message
            requests.get(f"""http://api.telegram.org/bot{tg_token}sendMessage
                            ?chat_id={chat_id}&text={message}""")

