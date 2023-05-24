from __future__ import absolute_import, unicode_literals

import logging

from ..tasks.user_change import dnd_updated_user, user_change

logger = logging.getLogger(__name__)


def on_webhook_received(message):
    type = message["event"]["type"]
    if type == "user_change":
        user_change(message)
    elif type == "dnd_updated_user":
        dnd_updated_user(message)
    else:
        logger.error(f"No handler for Slack message of type {type} ")
        return
