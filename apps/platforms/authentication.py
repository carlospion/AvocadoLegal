"""
Custom API Key authentication for AvocadoLegal.
Platforms authenticate using their unique API key.
"""
from rest_framework import authentication, exceptions, permissions
from apps.platforms.models import Platform


class APIKeyAuthentication(authentication.BaseAuthentication):
    """
    Custom authentication using API Key.
    The API key should be passed in the header as: Authorization: Api-Key <key>
    """

    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')

        if not auth_header:
            return None

        try:
            auth_type, api_key = auth_header.split(' ', 1)
        except ValueError:
            return None

        if auth_type.lower() != 'api-key':
            return None

        try:
            platform = Platform.objects.get(api_key=api_key, is_active=True)
        except Platform.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid API Key')

        request.platform = platform
        return (None, platform)

    def authenticate_header(self, request):
        return 'Api-Key'


class PlatformPermission(permissions.BasePermission):
    """Permission class that checks if request has a valid platform."""

    def has_permission(self, request, view):
        return hasattr(request, 'platform') and request.platform is not None

    def has_object_permission(self, request, view, obj):
        # Check if the object belongs to the requesting platform
        if hasattr(obj, 'platform'):
            return obj.platform == request.platform
        if hasattr(obj, 'client') and hasattr(obj.client, 'platform'):
            return obj.client.platform == request.platform
        return True