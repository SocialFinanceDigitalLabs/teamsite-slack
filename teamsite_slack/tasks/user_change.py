import logging

from .update_all_users import _update_slack_profile

logger = logging.getLogger(__name__)


def user_change(message):
    user = message["event"]["user"]
    email = user["profile"].get("email")
    logger.info(f"Processing slack profile change for {email}")
    if email is None:
        logger.warning("No email found in Slack event.")
        return

    _update_slack_profile(user, django_user, save=True)


def dnd_updated_user(message):
    """
    Processes a `dnd_updated_user` message. We currently ignore these.
    :param message:
    :return:
    """
    pass
