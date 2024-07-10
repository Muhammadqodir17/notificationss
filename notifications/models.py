from django.db import models

TYPE_CHOICES = (
    ('like', 'Like'),
    ('comment', 'Comment'),
    ('follow', 'Follow')
)


class Notification(models.Model):
    user = models.PositiveIntegerField(default=0)
    notification_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    message = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.notification_type
