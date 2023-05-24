import hmac
import logging

from django.conf import settings as django_settings
from django.http import HttpResponse

logger = logging.getLogger(__name__)

ENCODING = "ascii"
SLACK_SIGNING_SECRET = django_settings.SLACK.get("SIGNING_SECRET", None)


def __verify_signature(signature, timestamp, message_body):
    message = ":".join(["v0", timestamp, message_body])
    digest = (
        "v0="
        + hmac.digest(
            bytearray(SLACK_SIGNING_SECRET, ENCODING),
            bytearray(message, ENCODING),
            "sha256",
        ).hex()
    )
    return hmac.compare_digest(
        bytearray(signature, ENCODING), bytearray(digest, ENCODING)
    )


def verify_slack_request(request):
    if request.method != "POST":
        return HttpResponse(content="Method Not Allowed", status=405), None

    if SLACK_SIGNING_SECRET is None:
        logger.warning(
            "Slack signatures are disabled. Please make sure you config SLACK_SIGNING_SECRET"
        )
        return None

    try:
        message_body = request.body.decode("utf-8")
        signature = request.headers.get("x-slack-signature")
        timestamp = request.headers.get("x-slack-request-timestamp")
        verified = __verify_signature(signature, timestamp, message_body)
    except Exception:
        logger.exception("Failed to verify Slack message signature")
        return HttpResponse(content="Unauthorized", status=401), None

    if not verified:
        return HttpResponse(content="Unauthorized", status=401), None

    return None
