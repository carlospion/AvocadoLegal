"""Views for lawyers dashboard panel."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, TemplateView
from django.http import JsonResponse, HttpResponseForbidden
from django.utils import timezone
from django.db.models import Count, Q
from .models import Lawyer, LawyerSchedule
from apps.conversations.models import Conversation, Message, ConversationStatus, SenderType


class LawyerRequiredMixin(LoginRequiredMixin):
    """Mixin that requires the user to be a lawyer."""
    login_url = '/admin/login/'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not hasattr(request.user, 'lawyer_profile'):
            return render(request, 'lawyers/no_access.html', {
                'message': 'Tu usuario no tiene un perfil de abogado asociado. Contacta al administrador.'
            })
        return super().dispatch(request, *args, **kwargs)
    
    def get_lawyer(self):
        return self.request.user.lawyer_profile


class DashboardView(LawyerRequiredMixin, TemplateView):
    """Main dashboard for lawyers."""
    template_name = 'lawyers/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lawyer = self.get_lawyer()
        
        context['lawyer'] = lawyer
        context['active_cases'] = Conversation.objects.filter(
            lawyer=lawyer, 
            status__in=[ConversationStatus.ACTIVE, ConversationStatus.PENDING, ConversationStatus.WAITING_CLIENT]
        ).count()
        context['pending_cases'] = Conversation.objects.filter(
            lawyer=lawyer, 
            status=ConversationStatus.PENDING
        ).count()
        context['resolved_today'] = Conversation.objects.filter(
            lawyer=lawyer,
            status=ConversationStatus.CLOSED,
            closed_at__date=timezone.now().date()
        ).count()
        context['total_resolved'] = lawyer.total_cases_handled
        context['recent_conversations'] = Conversation.objects.filter(
            lawyer=lawyer
        ).order_by('-updated_at')[:5]
        context['unassigned_cases'] = Conversation.objects.filter(
            lawyer__isnull=True,
            status=ConversationStatus.PENDING
        ).order_by('-created_at')[:10]
        
        return context


class ConversationListView(LawyerRequiredMixin, ListView):
    """List of conversations for the lawyer."""
    template_name = 'lawyers/conversation_list.html'
    context_object_name = 'conversations'
    paginate_by = 20
    
    def get_queryset(self):
        lawyer = self.get_lawyer()
        status = self.request.GET.get('status', 'active')
        qs = Conversation.objects.filter(lawyer=lawyer)
        if status == 'active':
            qs = qs.filter(status__in=[
                ConversationStatus.ACTIVE, 
                ConversationStatus.PENDING,
                ConversationStatus.WAITING_CLIENT
            ])
        elif status == 'closed':
            qs = qs.filter(status=ConversationStatus.CLOSED)
        return qs.order_by('-updated_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_status'] = self.request.GET.get('status', 'active')
        context['lawyer'] = self.get_lawyer()
        return context


class ConversationDetailView(LawyerRequiredMixin, DetailView):
    """Detail view for a conversation with chat."""
    template_name = 'lawyers/conversation_detail.html'
    context_object_name = 'conversation'
    
    def get_queryset(self):
        return Conversation.objects.filter(lawyer=self.get_lawyer())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = self.object.messages.all().order_by('sent_at')
        context['lawyer'] = self.get_lawyer()
        return context


class QueueView(LawyerRequiredMixin, ListView):
    """View unassigned cases queue."""
    template_name = 'lawyers/queue.html'
    context_object_name = 'cases'
    
    def get_queryset(self):
        return Conversation.objects.filter(
            lawyer__isnull=True,
            status=ConversationStatus.PENDING
        ).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lawyer'] = self.get_lawyer()
        return context


@login_required(login_url='/admin/login/')
def assign_case(request, pk):
    """Assign a case to the current lawyer."""
    if not hasattr(request.user, 'lawyer_profile'):
        return JsonResponse({'error': 'Not a lawyer'}, status=403)
    
    lawyer = request.user.lawyer_profile
    conversation = get_object_or_404(Conversation, pk=pk, lawyer__isnull=True)
    
    if not lawyer.can_accept_new_case:
        return JsonResponse({'error': 'Cannot accept more cases'}, status=400)
    
    conversation.lawyer = lawyer
    conversation.status = ConversationStatus.ACTIVE
    conversation.save()
    
    Message.create_system_message(conversation, f'El abogado {lawyer.name} ha tomado este caso.')
    
    return JsonResponse({'success': True, 'conversation_id': str(conversation.id)})


@login_required(login_url='/admin/login/')
def send_message(request, pk):
    """Send a message in a conversation."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    if not hasattr(request.user, 'lawyer_profile'):
        return JsonResponse({'error': 'Not a lawyer'}, status=403)
    
    lawyer = request.user.lawyer_profile
    conversation = get_object_or_404(Conversation, pk=pk, lawyer=lawyer)
    content = request.POST.get('content', '').strip()
    if not content:
        return JsonResponse({'error': 'Content is required'}, status=400)
    
    message = Message.objects.create(
        conversation=conversation,
        sender_type=SenderType.LAWYER,
        sender_id=lawyer.id,
        sender_name=lawyer.name,
        content=content
    )
    conversation.status = ConversationStatus.WAITING_CLIENT
    conversation.save()
    
    return JsonResponse({
        'success': True,
        'message': {
            'id': str(message.id),
            'content': message.content,
            'sender_name': message.sender_name,
            'sent_at': message.sent_at.isoformat()
        }
    })


@login_required(login_url='/admin/login/')
def close_case(request, pk):
    """Close a case."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    if not hasattr(request.user, 'lawyer_profile'):
        return JsonResponse({'error': 'Not a lawyer'}, status=403)
    
    lawyer = request.user.lawyer_profile
    conversation = get_object_or_404(Conversation, pk=pk, lawyer=lawyer)
    notes = request.POST.get('notes', '')
    conversation.close_case(notes)
    
    return JsonResponse({'success': True})


@login_required(login_url='/admin/login/')
def toggle_availability(request):
    """Toggle lawyer availability."""
    if not hasattr(request.user, 'lawyer_profile'):
        return JsonResponse({'error': 'Not a lawyer'}, status=403)
    
    lawyer = request.user.lawyer_profile
    lawyer.is_available = not lawyer.is_available
    lawyer.save(update_fields=['is_available'])
    
    return JsonResponse({'success': True, 'is_available': lawyer.is_available})


@login_required(login_url='/admin/login/')
def toggle_shift(request):
    """Toggle lawyer shift status."""
    if not hasattr(request.user, 'lawyer_profile'):
        return JsonResponse({'error': 'Not a lawyer'}, status=403)
    
    lawyer = request.user.lawyer_profile
    lawyer.is_on_shift = not lawyer.is_on_shift
    lawyer.save(update_fields=['is_on_shift'])
    
    return JsonResponse({'success': True, 'is_on_shift': lawyer.is_on_shift})