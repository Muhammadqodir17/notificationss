from django.db import models

TYPE_CHOICES = (
    ('like', 'Like'),
    ('comment', 'Comment'),
    ('follow', 'Follow')
)

MESSAGE_CHOICE = (
    ('like', 'liked your post'),
    ('comment', 'commented:'),
    ('follow', 'started following you')
)


class Notification(models.Model):
    user = models.PositiveIntegerField(default=0)
    post = models.PositiveIntegerField(default=0)
    notification_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    message = models.CharField(max_length=100, choices=MESSAGE_CHOICE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.notification_type
