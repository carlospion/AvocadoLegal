"""Conversation and Message models for AvocadoLegal."""
import uuid
from django.db import models


class ConversationStatus(models.TextChoices):
    PENDING = 'pending', 'Pendiente'
    ACTIVE = 'active', 'Activa'
    WAITING_CLIENT = 'waiting_client', 'Esperando Cliente'
    WAITING_LAWYER = 'waiting_lawyer', 'Esperando Abogado'
    RESOLVED = 'resolved', 'Resuelta'
    CLOSED = 'closed', 'Cerrada'


class Conversation(models.Model):
    """Chat conversation between a platform user and a lawyer."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    platform = models.ForeignKey('platforms.Platform', on_delete=models.CASCADE, related_name='conversations')
    platform_user = models.ForeignKey('platforms.PlatformUser', on_delete=models.SET_NULL, null=True, related_name='conversations')
    client = models.ForeignKey('platforms.Client', on_delete=models.SET_NULL, null=True, related_name='conversations')
    loan = models.ForeignKey('loans.Loan', on_delete=models.SET_NULL, null=True, blank=True, related_name='conversations')
    lawyer = models.ForeignKey('lawyers.Lawyer', on_delete=models.SET_NULL, null=True, blank=True, related_name='conversations')
    status = models.CharField(max_length=20, choices=ConversationStatus.choices, default=ConversationStatus.PENDING)
    subject = models.CharField(max_length=255, blank=True, verbose_name='Asunto')
    procedure_requested = models.CharField(max_length=100, blank=True, verbose_name='Procedimiento Solicitado')
    resolution_notes = models.TextField(blank=True, verbose_name='Notas de Resolucion')
    page_url = models.URLField(max_length=500, blank=True, verbose_name='URL de Origen')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Conversacion'
        verbose_name_plural = 'Conversaciones'
        ordering = ['-created_at']

    def __str__(self):
        client_name = self.client.name if self.client else 'Sin cliente'
        return f'{client_name} - {self.platform.name} ({self.status})'

    def close_case(self, notes=''):
        from django.utils import timezone
        self.status = ConversationStatus.CLOSED
        self.resolution_notes = notes
        self.closed_at = timezone.now()
        self.save()
        if self.lawyer:
            self.lawyer.total_cases_handled += 1
            self.lawyer.save(update_fields=['total_cases_handled'])


class SenderType(models.TextChoices):
    PLATFORM_USER = 'platform_user', 'Usuario de Plataforma'
    LAWYER = 'lawyer', 'Abogado'
    SYSTEM = 'system', 'Sistema'


class Message(models.Model):
    """Single message in a conversation."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender_type = models.CharField(max_length=20, choices=SenderType.choices)
    sender_id = models.UUIDField(null=True, blank=True)
    sender_name = models.CharField(max_length=255, blank=True)
    content = models.TextField(verbose_name='Contenido')
    attachments = models.JSONField(default=list, blank=True)
    is_read = models.BooleanField(default=False)
    is_system_message = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Mensaje'
        verbose_name_plural = 'Mensajes'
        ordering = ['sent_at']

    def __str__(self):
        preview = self.content[:50] + '...' if len(self.content) > 50 else self.content
        return f'{self.sender_name}: {preview}'

    @classmethod
    def create_system_message(cls, conversation, content):
        return cls.objects.create(
            conversation=conversation,
            sender_type=SenderType.SYSTEM,
            sender_name='Sistema',
            content=content,
            is_system_message=True
        )

    @classmethod
    def create_welcome_message(cls, conversation):
        content = 'Hola! Ya tenemos los datos basicos del prestamo. Cual es tu consulta y que procedimiento te gustaria iniciar?'
        return cls.create_system_message(conversation, content)