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

    @swagger_auto_schema(
        operation_description='Send like notification',
        operation_summary='Send like notification',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='user_id'),
                'notification_type': openapi.Schema(type=openapi.TYPE_STRING, description='notification_type'),
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
        self.check_token(request.data.get('token'))

        if request.data['notification_type'] == 'like':
            message = 'liked your post'
        elif request.data['notification_type'] == 'comment':
            message = 'commented your post'
        else:
            message = 'following you'

        serializer = NotificationSerializer(data={"message": message, **request.data})
        if serializer.is_valid():
            obj = serializer.save()
            response = send_message_telegram(obj)
            if response.status_code != 200:
                return Response({'error': 'Could not send message'}, status=status.HTTP_400_BAD_REQUEST)

            return Response(data={'message': 'Sent'}, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
