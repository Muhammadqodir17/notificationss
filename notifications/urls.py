from django.urls import path
from .views import NotificationViewSet

urlpatterns = [
    path('notification/', NotificationViewSet.as_view({'post': 'send_notifications'}))
]
