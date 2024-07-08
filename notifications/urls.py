from django.urls import path
from .views import NotificationViewSet

urlpatterns = [
    path('notification/like/', NotificationViewSet.as_view({'post': 'send_like_notification'})),
    path('notification/comment/', NotificationViewSet.as_view({'post': 'send_comment_notification'})),
    path('notification/follow/', NotificationViewSet.as_view({'post': 'send_follow_notification'}))
]