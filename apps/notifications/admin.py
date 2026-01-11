"""Admin configuration for notifications app."""
from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'lawyer', 'notification_type', 'is_read', 'is_sent', 'created_at']
    list_filter = ['notification_type', 'channel', 'is_read', 'is_sent']
    search_fields = ['title', 'message', 'lawyer__name']
    readonly_fields = ['id', 'created_at', 'sent_at', 'read_at']