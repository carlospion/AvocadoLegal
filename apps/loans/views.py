"""API views for loans app."""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.platforms.authentication import APIKeyAuthentication, PlatformPermission
from .models import Loan
from .serializers import LoanSerializer, LoanCreateSerializer


class LoanViewSet(viewsets.ModelViewSet):
    """ViewSet for Loan CRUD operations."""
    authentication_classes = [APIKeyAuthentication]
    permission_classes = [PlatformPermission]

    def get_serializer_class(self):
        if self.action == 'create':
            return LoanCreateSerializer
        return LoanSerializer

    def get_queryset(self):
        return Loan.objects.filter(client__platform=self.request.platform)

    @action(detail=False, methods=['get'])
    def irregular(self, request):
        """Get all irregular loans."""
        irregular_loans = self.get_queryset().filter(
            status__in=['retraso', 'mora', 'vencido', 'cobranza', 'legal']
        )
        serializer = LoanSerializer(irregular_loans, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def analyze(self, request, pk=None):
        """Analyze a loan and return its status."""
        loan = self.get_object()
        return Response({
            'loan_id': str(loan.id),
            'client_name': loan.client.name,
            'status': loan.status,
            'is_irregular': loan.is_irregular,
            'days_overdue': loan.days_overdue,
            'recommendation': self._get_recommendation(loan)
        })

    def _get_recommendation(self, loan):
        if loan.days_overdue > 90:
            return 'Accion legal recomendada'
        elif loan.days_overdue > 60:
            return 'Iniciar proceso de cobranza formal'
        elif loan.days_overdue > 30:
            return 'Contactar cliente para acuerdo de pago'
        else:
            return 'Monitorear situacion'