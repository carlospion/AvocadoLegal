"""
Platform model for AvocadoLegal.
Represents external SaaS platforms that integrate with the API.
"""
import uuid
import secrets
from django.db import models


class Platform(models.Model):
    """
    Represents an external platform (SaaS) that uses the AvocadoLegal API.
    Each platform has a unique API key for authentication.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name='Nombre de la Plataforma')
    api_key = models.CharField(max_length=64, unique=True, editable=False)
    domain = models.CharField(max_length=255, verbose_name='Dominio')
    contact_name = models.CharField(max_length=255, blank=True, verbose_name='Nombre de Contacto')
    contact_email = models.EmailField(blank=True, verbose_name='Email de Contacto')
    contact_phone = models.CharField(max_length=20, blank=True, verbose_name='Telefono')
    settings = models.JSONField(default=dict, blank=True, verbose_name='Configuracion')
    is_active = models.BooleanField(default=True, verbose_name='Activa')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creacion')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ultima Actualizacion')

    class Meta:
        verbose_name = 'Plataforma'
        verbose_name_plural = 'Plataformas'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.api_key:
            self.api_key = self.generate_api_key()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_api_key():
        return f'avl_{secrets.token_urlsafe(32)}'

    def regenerate_api_key(self):
        self.api_key = self.generate_api_key()
        self.save(update_fields=['api_key', 'updated_at'])
        return self.api_key


class PlatformUser(models.Model):
    """User from an external platform (gestor de prestamos)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, related_name='users')
    external_id = models.CharField(max_length=255, verbose_name='ID Externo')
    name = models.CharField(max_length=255, verbose_name='Nombre')
    email = models.EmailField(blank=True, verbose_name='Email')
    role = models.CharField(max_length=100, blank=True, verbose_name='Rol')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Usuario de Plataforma'
        verbose_name_plural = 'Usuarios de Plataformas'
        unique_together = ['platform', 'external_id']
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} ({self.platform.name})'


class Client(models.Model):
    """Loan client from an external platform."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, related_name='clients')
    external_id = models.CharField(max_length=255, blank=True, verbose_name='ID Externo')
    name = models.CharField(max_length=255, verbose_name='Nombre Completo')
    cedula = models.CharField(max_length=20, blank=True, verbose_name='Cedula')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Telefono')
    email = models.EmailField(blank=True, verbose_name='Email')
    address = models.TextField(blank=True, verbose_name='Direccion')
    additional_data = models.JSONField(default=dict, blank=True, verbose_name='Datos Adicionales')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.cedula}'