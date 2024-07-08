from rest_framework.viewsets import ViewSet
from .models import Notification
import requests
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class NotificationViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description='Send like notification',
        operation_summary='Send like notification',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='user_id'),
                'post_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='user_id'),
            },
            required=['user_id', 'post_id']
        ),
        responses={
            400: 'Bad request',
            200: 'Ok'
        },
        tags=['like']
    )
    def send_like_notification(self, request, *args, **kwargs):
        obj = Notification.objects.create(user=request.data['user'], post=request.data['post'],
                                          notification_type='like', message='like')
        obj.save()

        notification = Notification.objects.filter(user=request.data['user'], post=request.data['post'],
                                                   notification_type='like').first()

        requests.get(
            f"""http://api.telegram.org/bot{settings.tg_token}
            sendMessage?chat_id={settings.chat_id}
            &text=Notification\nMessage: {request.data['user']} {notification.message}"""
        )

    @swagger_auto_schema(
        operation_description='Send comment notification',
        operation_summary='Send comment notification',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='user_id'),
                'post_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='user_id'),
            },
            required=['user_id', 'post_id']
        ),
        responses={
            400: 'Bad request',
            200: 'Ok'
        },
        tags=['comment']
    )
    def send_comment_notification(self, request, *args, **kwargs):
        obj = Notification.objects.create(user=request.data['user'], post=request.data['post'],
                                          notification_type='comment', message='comment')
        obj.save()

        notification = Notification.objects.filter(user=request.data['user'], post=request.data['post'],
                                                   notification_type='comment').first()

        requests.get(
            f"""http://api.telegram.org/bot{settings.tg_token}
                sendMessage?chat_id={settings.chat_id}
                &text=Notification\nMessage: {request.data['user']} {notification.message}"""
        )

    @swagger_auto_schema(
        operation_description='Send follow notification',
        operation_summary='Send follow notification',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='user_id'),
                'post_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='user_id'),
            },
            required=['user_id', 'post_id']
        ),
        responses={
            400: 'Bad request',
            200: 'Ok'
        },
        tags=['follow']
    )
    def send_follow_notification(self, request, *args, **kwargs):
        obj = Notification.objects.create(user=request.data['user'], post=request.data['post'],
                                          notification_type='follow', message='follow')
        obj.save()

        notification = Notification.objects.filter(user=request.data['user'], post=request.data['post'],
                                                   notification_type='follow').first()

        requests.get(
            f"""http://api.telegram.org/bot{settings.tg_token}
            sendMessage?chat_id={settings.chat_id}
            &text=Notification\nMessage: {request.data['user']} {notification.message}"""
        )
