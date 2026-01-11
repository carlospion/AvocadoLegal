"""Loan model for AvocadoLegal."""
import uuid
from django.db import models


class LoanStatus(models.TextChoices):
    AL_DIA = 'al_dia', 'Al Dia'
    RETRASO = 'retraso', 'Retraso'
    MORA = 'mora', 'Mora'
    VENCIDO = 'vencido', 'Vencido'
    COBRANZA = 'cobranza', 'Cobranza'
    LEGAL = 'legal', 'Legal'
    REESTRUCTURADO = 'reestructurado', 'Reestructurado'
    SALDADO = 'saldado', 'Saldado'


class Loan(models.Model):
    """Represents a loan from an external platform."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey('platforms.Client', on_delete=models.CASCADE, related_name='loans')
    external_id = models.CharField(max_length=255, blank=True, verbose_name='ID Externo del Prestamo')
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Monto del Prestamo')
    balance = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Balance Pendiente')
    currency = models.CharField(max_length=3, default='DOP', verbose_name='Moneda')
    status = models.CharField(max_length=20, choices=LoanStatus.choices, default=LoanStatus.RETRASO)
    days_overdue = models.PositiveIntegerField(default=0, verbose_name='Dias en Atraso')
    payment_history = models.JSONField(default=list, blank=True, verbose_name='Historial de Pagos')
    full_data = models.JSONField(default=dict, blank=True, verbose_name='Datos Completos')
    loan_date = models.DateField(null=True, blank=True, verbose_name='Fecha del Prestamo')
    due_date = models.DateField(null=True, blank=True, verbose_name='Fecha de Vencimiento')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Prestamo'
        verbose_name_plural = 'Prestamos'
        ordering = ['-days_overdue', '-created_at']

    def __str__(self):
        return f'{self.client.name} - ${self.amount} ({self.status})'

    @property
    def is_irregular(self):
        irregular_statuses = [LoanStatus.RETRASO, LoanStatus.MORA, LoanStatus.VENCIDO, LoanStatus.COBRANZA, LoanStatus.LEGAL]
        return self.status in irregular_statuses