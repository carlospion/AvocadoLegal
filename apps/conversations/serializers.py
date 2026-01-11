"""Serializers for conversations app."""
from rest_framework import serializers
from .models import Conversation, Message, ConversationStatus, SenderType


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model."""
    class Meta:
        model = Message
        fields = [
            'id', 'sender_type', 'sender_id', 'sender_name',
            'content', 'attachments', 'is_read', 'sent_at'
        ]
        read_only_fields = ['id', 'sent_at']


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for Conversation model."""
    platform_name = serializers.CharField(source='platform.name', read_only=True)
    client_name = serializers.SerializerMethodField()
    lawyer_name = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'id', 'platform', 'platform_name', 'platform_user',
            'client', 'client_name', 'loan', 'lawyer', 'lawyer_name',
            'status', 'status_display', 'subject', 'procedure_requested',
            'resolution_notes', 'messages', 'message_count',
            'created_at', 'closed_at'
        ]
        read_only_fields = ['id', 'created_at', 'closed_at']

    def get_client_name(self, obj):
        return obj.client.name if obj.client else None
    
    def get_lawyer_name(self, obj):
        return obj.lawyer.name if obj.lawyer else None

    def get_message_count(self, obj):
        return obj.messages.count()


class ConversationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a Conversation."""
    class Meta:
        model = Conversation
        fields = ['platform_user', 'client', 'loan', 'subject', 'procedure_requested']
        extra_kwargs = {
            'platform_user': {'required': False, 'allow_null': True},
            'client': {'required': False, 'allow_null': True},
            'loan': {'required': False, 'allow_null': True},
            'subject': {'required': False, 'allow_blank': True},
            'procedure_requested': {'required': False, 'allow_blank': True},
        }


class MessageCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a Message."""
    class Meta:
        model = Message
        fields = ['sender_type', 'sender_id', 'sender_name', 'content', 'attachments']
        extra_kwargs = {
            'sender_id': {'required': False, 'allow_null': True},
            'sender_name': {'required': False, 'allow_blank': True},
            'attachments': {'required': False},
        }