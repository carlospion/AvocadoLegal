"""Admin configuration for loans app."""
from django.contrib import admin
from .models import Loan


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['client', 'amount', 'balance', 'status', 'days_overdue', 'created_at']
    list_filter = ['status', 'currency', 'created_at']
    search_fields = ['client__name', 'external_id']
    readonly_fields = ['id', 'created_at', 'updated_at']