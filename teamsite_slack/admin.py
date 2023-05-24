from django.contrib import admin

from .models import SlackProfile


@admin.register(SlackProfile)
class ZoomProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user_name",
        "name",
        "status_text",
        "status_emoji",
        "has_pic",
        "deleted",
    )
    search_fields = ("user__username",)

    def user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    user_name.admin_order_field = "user__first_name"

    def has_pic(self, obj):
        return obj.image_192 is not None

    has_pic.boolean = True


class InlineSlackProfile(admin.TabularInline):
    model = SlackProfile
    fields = ["slack_id", "name", "deleted", "status_text", "status_emoji", "image_192"]
