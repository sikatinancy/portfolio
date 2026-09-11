
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    Conversation,
    Message,
    Notification,
    User,
)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = (
        "email",
        "username",
        "is_staff",
        "is_active",
    )

    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
    )

    search_fields = (
        "email",
        "username",
    )

    ordering = (
        "email",
    )


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = (
        "visitor_name",
        "visitor_email",
        "visitor_phone",
        "subject",
        "created_at",
        "updated_at",
        "is_archived",
    )

    list_filter = (
        "is_archived",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "visitor_name",
        "visitor_email",
        "visitor_phone",
        "subject",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-updated_at",
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "conversation",
        "sender",
        "message_type",
        "is_read",
        "created_at",
    )

    list_filter = (
        "message_type",
        "is_read",
        "created_at",
    )

    search_fields = (
        "content",
        "original_filename",
        "conversation__visitor_name",
        "conversation__visitor_email",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "message",
        "is_read",
        "created_at",
    )

    list_filter = (
        "is_read",
        "created_at",
    )

    search_fields = (
        "user__email",
        "message__content",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )