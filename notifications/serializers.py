from .models import Notification
from rest_framework import serializers


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('user', 'notification_type', 'message', 'created_at')
