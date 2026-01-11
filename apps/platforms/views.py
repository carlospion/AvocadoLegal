"""API views for platforms app."""
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Platform, PlatformUser, Client
from .serializers import (
    PlatformSerializer, PlatformRegistrationSerializer,
    PlatformUserSerializer, ClientSerializer, ClientCreateSerializer
)
from .authentication import APIKeyAuthentication, PlatformPermission


class PlatformRegistrationViewSet(viewsets.ViewSet):
    """ViewSet for platform registration (public endpoint)."""
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        """Register a new platform and get API key."""
        serializer = PlatformRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            platform = serializer.save()
            return Response({
                'id': str(platform.id),
                'name': platform.name,
                'api_key': platform.api_key,
                'message': 'Platform registered successfully. Save your API key securely.'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlatformUserViewSet(viewsets.ModelViewSet):
    """ViewSet for PlatformUser CRUD operations."""
    serializer_class = PlatformUserSerializer
    authentication_classes = [APIKeyAuthentication]
    permission_classes = [PlatformPermission]

    def get_queryset(self):
        return PlatformUser.objects.filter(platform=self.request.platform)

    def perform_create(self, serializer):
        serializer.save(platform=self.request.platform)


class ClientViewSet(viewsets.ModelViewSet):
    """ViewSet for Client CRUD operations."""
    authentication_classes = [APIKeyAuthentication]
    permission_classes = [PlatformPermission]

    def get_serializer_class(self):
        if self.action == 'create':
            return ClientCreateSerializer
        return ClientSerializer

    def get_queryset(self):
        return Client.objects.filter(platform=self.request.platform)

    def perform_create(self, serializer):
        serializer.save(platform=self.request.platform)

    @action(detail=True, methods=['get'])
    def loans(self, request, pk=None):
        """Get all loans for a specific client."""
        client = self.get_object()
        from apps.loans.serializers import LoanSerializer
        loans = client.loans.all()
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)