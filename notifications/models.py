from django.db import models

TYPE_CHOICES = (
    (1, 'Like'),
    (2, 'Comment'),
    (3, 'Follow')
)


class Notification(models.Model):
    user = models.PositiveIntegerField(default=0)
    notification_type = models.IntegerField(default=1,choices=TYPE_CHOICES)
    message = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.notification_type
