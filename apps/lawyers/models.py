"""Lawyer model for AvocadoLegal."""
import uuid
from django.db import models
from django.contrib.auth.models import User


class LawyerSpecialty(models.TextChoices):
    COBRANZAS = 'cobranzas', 'Cobros de Peso'
    EMBARGOS = 'embargos', 'Embargos'
    INTIMACIONES = 'intimaciones', 'Intimaciones'
    GENERAL = 'general', 'Asuntos Generales'


class Lawyer(models.Model):
    """Represents a lawyer from JCJ Consultings."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='lawyer_profile')
    name = models.CharField(max_length=255, verbose_name='Nombre Completo')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Telefono')
    specialty = models.CharField(max_length=20, choices=LawyerSpecialty.choices, default=LawyerSpecialty.GENERAL)
    is_available = models.BooleanField(default=True, verbose_name='Disponible')
    is_on_shift = models.BooleanField(default=False, verbose_name='En Turno')
    max_concurrent_cases = models.PositiveIntegerField(default=5, verbose_name='Max Casos Simultaneos')
    total_cases_handled = models.PositiveIntegerField(default=0, verbose_name='Casos Atendidos')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Abogado'
        verbose_name_plural = 'Abogados'
        ordering = ['-is_on_shift', '-is_available', 'name']

    def __str__(self):
        status = 'ON' if self.is_available else 'OFF'
        return f'[{status}] {self.name} - {self.get_specialty_display()}'

    @property
    def active_cases_count(self):
        return self.conversations.filter(status__in=['active', 'pending']).count()

    @property
    def can_accept_new_case(self):
        return self.is_available and self.is_on_shift and self.active_cases_count < self.max_concurrent_cases


class LawyerSchedule(models.Model):
    """Lawyer schedule/shift."""
    DAYS_OF_WEEK = [
        (0, 'Lunes'), (1, 'Martes'), (2, 'Miercoles'), (3, 'Jueves'),
        (4, 'Viernes'), (5, 'Sabado'), (6, 'Domingo'),
    ]
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE, related_name='schedules')
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK, verbose_name='Dia')
    start_time = models.TimeField(verbose_name='Hora Inicio')
    end_time = models.TimeField(verbose_name='Hora Fin')

    class Meta:
        verbose_name = 'Horario'
        verbose_name_plural = 'Horarios'
        unique_together = ['lawyer', 'day_of_week']
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return f'{self.lawyer.name} - {self.get_day_of_week_display()}: {self.start_time}-{self.end_time}'