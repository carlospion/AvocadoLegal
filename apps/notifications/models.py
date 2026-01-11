"""Notification model for AvocadoLegal."""
import uuid
from django.db import models


class NotificationType(models.TextChoices):
    NEW_CASE = 'new_case', 'Nuevo Caso'
    NEW_MESSAGE = 'new_message', 'Nuevo Mensaje'
    CASE_ASSIGNED = 'case_assigned', 'Caso Asignado'
    CASE_CLOSED = 'case_closed', 'Caso Cerrado'
    REMINDER = 'reminder', 'Recordatorio'


class NotificationChannel(models.TextChoices):
    EMAIL = 'email', 'Email'
    PUSH = 'push', 'Push'
    BOTH = 'both', 'Ambos'


class Notification(models.Model):
    """Notification sent to a lawyer."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lawyer = models.ForeignKey('lawyers.Lawyer', on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NotificationType.choices)
    channel = models.CharField(max_length=10, choices=NotificationChannel.choices, default=NotificationChannel.BOTH)
    title = models.CharField(max_length=255, verbose_name='Titulo')
    message = models.TextField(verbose_name='Mensaje')
    conversation = models.ForeignKey('conversations.Conversation', on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications')
    is_read = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Notificacion'
        verbose_name_plural = 'Notificaciones'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} - {self.lawyer.name}'

    def mark_as_read(self):
        from django.utils import timezone
        self.is_read = True
        self.read_at = timezone.now()
        self.save(update_fields=['is_read', 'read_at'])