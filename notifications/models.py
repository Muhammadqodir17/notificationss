from django.db import models
from rest_framework.authtoken.admin import User

TYPE_CHOICES = (
    ('like', 'Like'),
    ('comment', 'Comment'),
)

MESSAGE_CHOICE = (
    ('like', 'Your post liked'),
    ('comment', 'Your post commented')
)


class Post(models.Model):
    pass


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    message = models.CharField(max_length=100, choices=MESSAGE_CHOICE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.notification_type
