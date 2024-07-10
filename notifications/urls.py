from django.urls import path
from .views import NotificationViewSet

urlpatterns = [
    path('notification/', NotificationViewSet.as_view({'post': 'send_notifications'})),
    # path('notification/comment/', NotificationViewSet.as_view({'post': 'send_comment_notification'})),
    # path('notification/follow/', NotificationViewSet.as_view({'post': 'send_follow_notification'}))
]