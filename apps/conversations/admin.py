"""Admin configuration for conversations app."""
from django.contrib import admin
from .models import Conversation, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ['id', 'sender_type', 'sender_name', 'content', 'sent_at']
    can_delete = False


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['client', 'platform', 'lawyer', 'status', 'created_at']
    list_filter = ['status', 'platform', 'created_at']
    search_fields = ['client__name', 'subject']
    readonly_fields = ['id', 'created_at', 'updated_at', 'closed_at']
    inlines = [MessageInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'sender_name', 'sender_type', 'is_read', 'sent_at']
    list_filter = ['sender_type', 'is_read', 'sent_at']
    search_fields = ['content', 'sender_name']
    readonly_fields = ['id', 'sent_at']