"""API views for conversations app."""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from apps.platforms.authentication import APIKeyAuthentication, PlatformPermission
from apps.platforms.models import Client
from apps.lawyers.models import Lawyer
from .models import Conversation, Message, ConversationStatus, SenderType
from .serializers import (
    ConversationSerializer, ConversationCreateSerializer,
    MessageSerializer, MessageCreateSerializer
)


class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for Conversation CRUD operations."""
    authentication_classes = [APIKeyAuthentication]
    permission_classes = [PlatformPermission]

    def get_serializer_class(self):
        if self.action == 'create':
            return ConversationCreateSerializer
        return ConversationSerializer

    def get_queryset(self):
        return Conversation.objects.filter(platform=self.request.platform)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create client from scraped data if provided
        client = None
        client_data = request.data.get('client_data', {})
        if client_data and (client_data.get('name') or client_data.get('cedula')):
            client, created = Client.objects.get_or_create(
                platform=request.platform,
                cedula=client_data.get('cedula', ''),
                defaults={
                    'name': client_data.get('name', 'Cliente Web'),
                    'phone': client_data.get('phone', ''),
                    'email': client_data.get('email', ''),
                    'external_id': f"web_{timezone.now().timestamp()}"
                }
            )
            if not created and client_data.get('name'):
                # Update existing client with new data
                client.name = client_data.get('name', client.name)
                client.phone = client_data.get('phone', client.phone)
                client.email = client_data.get('email', client.email)
                client.save()
        
        conversation = serializer.save(platform=request.platform, client=client)
        
        # Create welcome message
        Message.create_welcome_message(conversation)
        
        # Try to auto-assign to available lawyer
        self._assign_lawyer(conversation)
        
        return Response({
            'id': str(conversation.id),
            'status': conversation.status,
            'subject': conversation.subject,
            'client_id': str(client.id) if client else None,
            'created_at': conversation.created_at.isoformat(),
            'message': 'Conversation created successfully'
        }, status=status.HTTP_201_CREATED)

    def _assign_lawyer(self, conversation):
        """Auto-assign conversation to available lawyer."""
        available_lawyer = Lawyer.objects.filter(
            is_available=True,
            is_on_shift=True
        ).first()
        if available_lawyer and available_lawyer.can_accept_new_case:
            conversation.lawyer = available_lawyer
            conversation.status = ConversationStatus.ACTIVE
            conversation.save()
            # Notify about assignment
            Message.create_system_message(
                conversation,
                f'El abogado {available_lawyer.name} ha tomado este caso.'
            )

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        """Send a message in the conversation."""
        conversation = self.get_object()
        serializer = MessageCreateSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.save(conversation=conversation)
            conversation.updated_at = timezone.now()
            conversation.save()
            return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """Get all messages in the conversation."""
        conversation = self.get_object()
        messages = conversation.messages.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        """Close the conversation/case."""
        conversation = self.get_object()
        notes = request.data.get('notes', '')
        conversation.close_case(notes)
        return Response({
            'message': 'Conversation closed',
            'closed_at': conversation.closed_at.isoformat()
        })