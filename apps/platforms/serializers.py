"""Serializers for platforms app."""
from rest_framework import serializers
from .models import Platform, PlatformUser, Client


class PlatformSerializer(serializers.ModelSerializer):
    """Serializer for Platform model."""
    class Meta:
        model = Platform
        fields = ['id', 'name', 'domain', 'contact_name', 'contact_email', 'contact_phone', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class PlatformRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for registering a new platform."""
    class Meta:
        model = Platform
        fields = ['name', 'domain', 'contact_name', 'contact_email', 'contact_phone']


class PlatformUserSerializer(serializers.ModelSerializer):
    """Serializer for PlatformUser model."""
    class Meta:
        model = PlatformUser
        fields = ['id', 'external_id', 'name', 'email', 'role', 'created_at']
        read_only_fields = ['id', 'created_at']


class ClientSerializer(serializers.ModelSerializer):
    """Serializer for Client model."""
    class Meta:
        model = Client
        fields = ['id', 'external_id', 'name', 'cedula', 'phone', 'email', 'address', 'additional_data', 'created_at']
        read_only_fields = ['id', 'created_at']


class ClientCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a Client."""
    class Meta:
        model = Client
        fields = ['external_id', 'name', 'cedula', 'phone', 'email', 'address', 'additional_data']
        extra_kwargs = {
            'external_id': {'required': False, 'allow_blank': True},
            'cedula': {'required': False, 'allow_blank': True},
            'phone': {'required': False, 'allow_blank': True},
            'email': {'required': False, 'allow_blank': True},
            'address': {'required': False, 'allow_blank': True},
            'additional_data': {'required': False},
        }