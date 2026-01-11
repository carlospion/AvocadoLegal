"""Serializers for loans app."""
from rest_framework import serializers
from .models import Loan, LoanStatus


class LoanSerializer(serializers.ModelSerializer):
    """Serializer for Loan model."""
    client_name = serializers.CharField(source='client.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Loan
        fields = [
            'id', 'external_id', 'client', 'client_name',
            'amount', 'balance', 'currency', 'status', 'status_display',
            'days_overdue', 'loan_date', 'due_date', 'is_irregular',
            'payment_history', 'full_data', 'created_at'
        ]
        read_only_fields = ['id', 'is_irregular', 'created_at']


class LoanCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a Loan."""
    class Meta:
        model = Loan
        fields = [
            'external_id', 'client', 'amount', 'balance', 'currency',
            'status', 'days_overdue', 'loan_date', 'due_date',
            'payment_history', 'full_data'
        ]