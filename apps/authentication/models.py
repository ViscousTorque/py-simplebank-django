import uuid
from django.db import models
from apps.accounts.models import User


class Session(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    refresh_token = models.CharField(max_length=512)
    user_agent = models.CharField(max_length=255)
    client_ip = models.GenericIPAddressField()
    is_blocked = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session {self.id} - {self.username}"
