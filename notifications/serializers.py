from .models import Notification
from rest_framework import serializers


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('user_id', 'post_id', 'notification_type', 'message', 'created_at')


class FollowNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('user_id', 'notification_type', 'message', 'created_at')