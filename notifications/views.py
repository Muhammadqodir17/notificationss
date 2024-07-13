from rest_framework.viewsets import ViewSet
from .serializers import NotificationSerializer, FollowNotificationSerializer
import requests
from .utils import send_message_telegram
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .models import Notification


class NotificationViewSet(ViewSet):

    def check_token(self, token):
        response = requests.post('http://134.122.76.27:8114/api/v1/check/', data={'token': token})
        if response.status_code != 200:
            raise ValidationError({'error': 'Invalid token'})

    def get_token(self):
        response = requests.post('http://134.122.76.27:8114/api/v1/login/', json={
            "service_id": 4,
            "service_name": "Notification",
            "secret_key": "1f79d048-058d-4919-9661-a75f095c6ad2"
        })
        return response

    def get_user(self, pk):
        response = requests.post(f'http://134.122.76.27:8118/api/v1/get/user/{pk}/',
                                 json={'token': str(self.get_token().json().get('token'))})
        return response

    def get_post(self, pk):
        response = requests.post(f'http://134.122.76.27:8111/api/v1/post/detail-delete/{pk}/',
                                 json={'token': str(self.get_token().json().get('token'))})
        return response

    @swagger_auto_schema(
        operation_description='Send notification',
        operation_summary='Send notification',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='user_id'),
                'post_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='post_id'),
                'notification_type': openapi.Schema(type=openapi.TYPE_INTEGER, description='notification_type'),
                'token': openapi.Schema(type=openapi.TYPE_STRING, description='token'),
            },
            required=['user_id', 'post_id' 'notification_type', 'token']
        ),
        responses={
            400: 'Bad request',
            200: NotificationSerializer()
        },
        tags=['Notification']
    )
    def send_notifications(self, request, *args, **kwargs):

        data = request.data

        self.check_token(request.data.get('token'))

        post = self.get_post(request.data.get('post_id'))

        user = self.get_user(request.data.get('user_id'))

        if post.status_code == 404:
            return Response(data={'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        if user.json().get("first_name") is not None or user.json().get(
                "last_name") is not None:

            if int(data.get('notification_type')) == 1:
                message = (f'{user.json().get("first_name")} {user.json().get("last_name")} liked your post: '
                           f'{request.data.get('post_id')}')

            elif int(data.get('notification_type')) == 2:
                message = (f'{user.json().get("first_name")} {user.json().get("last_name")}'
                           f' commented {request.data.get('message')}'
                           f' post: {request.data.get('post_id')}')
            else:
                return Response(data={'error': 'Invalid notification_type'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = NotificationSerializer(data={"message": message, **data,
                                                      'user_id': data.get('user_id')})

            if serializer.is_valid():
                serializer.save()
                response = send_message_telegram(message)
                if response.status_code != 200:
                    return Response({'error': 'Could not send message'}, status=status.HTTP_400_BAD_REQUEST)

                return Response(data={'message': 'Sent'}, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data={'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description='Get Notifications by id',
        operation_summary='Get Notifications by id',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'token': openapi.Schema(type=openapi.TYPE_STRING, description='token'),
            },
            required=['token']
        ),
        responses={
            400: 'Bad request',
            200: NotificationSerializer()
        },
        tags=['Notification']
    )
    def get_by_id(self, request, *args, **kwargs):
        self.check_token(request.data.get('token'))
        user = self.get_user(kwargs['pk'])

        if user.status_code != 200:
            return Response(data={'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        notifications = Notification.objects.filter(user_id=kwargs['pk'])

        return Response(data=NotificationSerializer(notifications, many=True).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description='Get all Notifications',
        operation_summary='Get all Notifications',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'token': openapi.Schema(type=openapi.TYPE_STRING, description='token'),
            },
            required=['token']
        ),
        responses={
            400: 'Bad request',
            200: NotificationSerializer()
        },
        tags=['Notification']
    )
    def get_all(self, request, *args, **kwargs):
        self.check_token(request.data.get('token'))

        notifications = Notification.objects.all()

        return Response(data=NotificationSerializer(notifications, many=True), status=status.HTTP_200_OK)


class NotificationForFollowViewSet(ViewSet):

    def check_token(self, token):
        response = requests.post('http://134.122.76.27:8114/api/v1/check/', data={'token': token})
        if response.status_code != 200:
            raise ValidationError({'error': 'Invalid token'})

    def get_token(self):
        response = requests.post('http://134.122.76.27:8114/api/v1/login/', json={
            "service_id": 4,
            "service_name": "Notification",
            "secret_key": "1f79d048-058d-4919-9661-a75f095c6ad2"
        })
        return response

    def get_user(self, pk):
        response = requests.post(f'http://134.122.76.27:8118/api/v1/get/user/{pk}/',
                                 json={'token': str(self.get_token().json().get('token'))})
        return response

    @swagger_auto_schema(
        operation_description='Send follow notification',
        operation_summary='Send follow notification',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='user_id'),
                'notification_type': openapi.Schema(type=openapi.TYPE_INTEGER, description='notification_type'),
                'token': openapi.Schema(type=openapi.TYPE_STRING, description='token'),
            },
            required=['user_id', 'notification_type', 'token']
        ),
        responses={
            400: 'Bad request',
            200: FollowNotificationSerializer()
        },
        tags=['Notification']
    )
    def send_follow_notification(self, request, *args, **kwargs):
        data = request.data
        self.check_token(request.data.get('token'))
        user = self.get_user(request.data.get('user_id'))
        if user.json().get("first_name") is not None or user.json().get("last_name") is not None:
            if int(data.get('notification_type')) == 3:
                message = f'{user.json().get("first_name")} {user.json().get("last_name")} following you'
            else:
                return Response(data={'error': 'Invalid notification_type'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = FollowNotificationSerializer(data={"message": message, **data, 'user_id': data.get('user_id')})
            if serializer.is_valid():
                serializer.save()
                response = send_message_telegram(message)
                if response.status_code != 200:
                    return Response({'error': 'Could not send message'}, status=status.HTTP_400_BAD_REQUEST)

                return Response(data={'message': 'Sent'}, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
