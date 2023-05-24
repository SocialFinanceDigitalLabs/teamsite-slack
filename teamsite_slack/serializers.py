import time

from rest_framework import serializers
from sf_slack.models import SlackProfile


class SlackProfileSerializer(serializers.HyperlinkedModelSerializer):
    status_expired = serializers.SerializerMethodField()

    def get_status_expired(self, obj):
        if obj.status_expiration == 0:
            return False
        return obj.status_expiration < time.time()

    class Meta:
        model = SlackProfile
        fields = [
            "slack_id",
            "name",
            "deleted",
            "color",
            "tz",
            "status_text",
            "status_expiration",
            "status_expired",
            "image_24",
            "image_32",
            "image_48",
            "image_72",
            "image_192",
            "image_512",
        ]
