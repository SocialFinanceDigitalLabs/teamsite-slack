import json
import logging

from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from sf_slack.util import crypto

from .tasks import on_command_received, on_interaction_received, on_webhook_received

User = get_user_model()

logger = logging.getLogger(__name__)


@csrf_exempt
def webhook(request):
    error = crypto.verify_slack_request(request)
    if error is not None:
        return error

    body = request.body.decode("utf-8")

    try:
        message_data = json.loads(body)
    except ValueError as e:
        logger.exception("Failed to parse Slack message body")
        return HttpResponse(content="Bad Request", status=400)

    challenge = message_data.get("challenge")
    if challenge is not None:
        return JsonResponse(dict(challenge=challenge))

    on_webhook_received.delay(message_data)

    return HttpResponse("OK")


@csrf_exempt
def command(request):
    error = crypto.verify_slack_request(request)
    if error is not None:
        return error

    on_command_received.delay(request.POST)

    return HttpResponse()


@csrf_exempt
def interaction(request):
    error = crypto.verify_slack_request(request)
    if error is not None:
        return error

    message = json.loads(request.POST["payload"])
    on_interaction_received.delay(message)

    return HttpResponse("OK")
