from django.contrib.auth.models import User
from django.db import models


class SlackProfile(models.Model):
    slack_id = models.CharField(max_length=20, null=False, unique=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, editable=False, related_name="slack_profile"
    )
    name = models.CharField(max_length=50)
    deleted = models.BooleanField(default=False)
    color = models.CharField(max_length=6, null=True, blank=True)
    tz = models.CharField(max_length=50, null=True, blank=True)
    status_text = models.CharField(max_length=255, null=True, blank=True)
    status_emoji = models.CharField(max_length=255, null=True, blank=True)
    status_expiration = models.BigIntegerField(null=True, blank=True)

    image_24 = models.CharField(max_length=255, null=True, blank=True)
    image_32 = models.CharField(max_length=255, null=True, blank=True)
    image_48 = models.CharField(max_length=255, null=True, blank=True)
    image_72 = models.CharField(max_length=255, null=True, blank=True)
    image_192 = models.CharField(max_length=255, null=True, blank=True)
    image_512 = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.slack_id} ({self.user.id})"
