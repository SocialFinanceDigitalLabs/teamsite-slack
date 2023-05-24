import emoji
import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from .models import SlackProfile


class SlackProfileNode(DjangoObjectType):
    status_emoji_unicode = graphene.String()

    @staticmethod
    def resolve_status_emoji_unicode(profile, info):
        try:
            uni_version = emoji.emojize(profile.status_emoji, use_aliases=True)
            if ":" in uni_version:
                return ""
            else:
                return uni_version
        except:
            return ""

    class Meta:
        model = SlackProfile
        filter_fields = ["status_text"]
        interfaces = (graphene.relay.Node,)
        fields = "__all__"


class Query(object):
    slack_profile = graphene.relay.Node.Field(SlackProfileNode)
    all_slack_profiles = DjangoFilterConnectionField(SlackProfileNode)
