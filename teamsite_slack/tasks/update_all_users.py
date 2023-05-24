from __future__ import absolute_import, unicode_literals

import logging

import requests
from django.conf import settings as django_settings
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q

from ..models import SlackProfile

logger = logging.getLogger(__name__)


def get_page(cursor=None):
    logger.info(f"Making request with cursor: {cursor}")

    headers = {"Authorization": f"Bearer {django_settings.SLACK['API_TOKEN']}"}
    data = {}
    if cursor is not None:
        data["cursor"] = cursor

    x = requests.post("https://slack.com/api/users.list", headers=headers, json=data)
    x.raise_for_status()

    response = x.json()

    members = response.get("members")
    if members is None:
        logger.error(f"No members found in response: {response}")

    try:
        cursor = response["response_metadata"]["next_cursor"]
    except:
        cursor = None
    return members, cursor


@transaction.atomic
def _update_slack_profile(user: dict, django_user: User, save=True):
    try:
        slack_profile = SlackProfile.objects.get(slack_id=user["id"])
    except SlackProfile.DoesNotExist:
        slack_profile = SlackProfile(slack_id=user["id"], user=django_user)

    slack_profile.name = user.get("name")
    slack_profile.deleted = user.get("deleted", False)
    slack_profile.color = user.get("color")
    slack_profile.tz = user.get("tz)")

    profile = user["profile"]
    slack_profile.status_text = profile.get("status_text")
    slack_profile.status_emoji = profile.get("status_emoji")
    slack_profile.status_expiration = profile.get("status_expiration")

    slack_profile.image_24 = profile.get("image_24")
    slack_profile.image_32 = profile.get("image_32")
    slack_profile.image_48 = profile.get("image_48")
    slack_profile.image_72 = profile.get("image_72")
    slack_profile.image_192 = profile.get("image_192")
    slack_profile.image_512 = profile.get("image_512")

    if save:
        try:
            slack_profile.save()
        except:
            logger.exception(f"Failed to update Slack Profile for {user.get('email')}")

    return slack_profile


def update_all_users():
    logger.debug("Updating all users")
    members, cursor = get_page()
    all_members = members
    while cursor is not None and cursor != "":
        members, cursor = get_page(cursor=cursor)
        all_members += members

    for user in members:
        email = user["profile"].get("email")

        if email is None:
            continue

        if user.get("deleted", False):
            continue

        if user.get("is_restricted", False) or user.get("is_ultra_restricted", False):
            continue

        email = email.lower()
        logger.debug(f"Processing change for {email}")

        django_user = User.objects.filter(
            Q(email=email) | Q(additional_emails__email=email)
        ).first()
        if django_user is None:
            logger.debug(f"User not found: {email}")
            continue

        _update_slack_profile(user, django_user, save=True)
