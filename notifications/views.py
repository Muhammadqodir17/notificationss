from rest_framework.viewsets import ViewSet
from .serializers import NotificationSerializer
import requests
from .utils import send_message_telegram
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError


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
        response = requests.post('http://134.122.76.27:8118/api/v1/get/user/id/',
                                 json={'user_id': pk,
                                       'token': str(self.get_token().json().get('token'))})
        return response

    @swagger_auto_schema(
        operation_description='Send like notification',
        operation_summary='Send like notification',
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
            200: NotificationSerializer()
        },
        tags=['Notification']
    )
    def send_notifications(self, request, *args, **kwargs):
        data = request.data
        # self.check_token(request.data.get('token'))
        user = self.get_user(request.data.get('user_id'))
        print(user.json().get("first_name"))
        if user.json().get("first_name") is not None or user.json().get("last_name") is not None:
            if int(data.get('notification_type')) == 1:
                message = f'{user.json().get("first_name")} {user.json().get("last_name")} liked your post'
            elif int(data.get('notification_type')) == 2:
                message = f'{user.json().get("first_name")} {user.json().get("last_name")} commented your post'
            elif int(data.get('notification_type')) == 3:
                message = f'{user.json().get("first_name")} {user.json().get("last_name")} following you'
            else:
                return Response(data={'error': 'notification_type not found'})

            serializer = NotificationSerializer(data={"message": message, **data, 'user_id': data.get('user_id')})
            if serializer.is_valid():
                obj = serializer.save()
                response = send_message_telegram(obj)
                if response.status_code != 200:
                    return Response({'error': 'Could not send message'}, status=status.HTTP_400_BAD_REQUEST)

                return Response(data={'message': 'Sent'}, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data={'error': 'User not found'})
