from django.db import models
from django.conf import settings
import uuid


class Room(models.Model):
    room_code = models.CharField(max_length=10, unique=True, editable=False)
    room_name = models.CharField(max_length=100)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.room_code:
            self.room_code = str(uuid.uuid4()).replace("-", "")[:6].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.room_name} ({self.room_code})"