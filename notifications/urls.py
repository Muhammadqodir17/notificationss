from django.urls import path
from .views import NotificationViewSet

urlpatterns = [
    path('notification/like/', NotificationViewSet.as_view({'get': 'send_liked_notification'})),
    path('notification/comment/', NotificationViewSet.as_view({'get': 'send_commented_notification'}))
]