from django.urls import path
from .views import NotificationViewSet, NotificationForFollowViewSet

urlpatterns = [
    path('notification/', NotificationViewSet.as_view({'post': 'send_notifications'})),
    path('notification/follow/', NotificationForFollowViewSet.as_view({'post': 'send_follow_notification'})),
    path('notification/<int:pk>/', NotificationViewSet.as_view({'post': 'get_by_id'})),
    path('notification/get/', NotificationViewSet.as_view({'post': 'get_all'}))
]
