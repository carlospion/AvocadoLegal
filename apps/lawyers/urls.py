"""URL configuration for lawyers app."""
from django.urls import path
from . import views

app_name = 'lawyers'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('conversations/', views.ConversationListView.as_view(), name='conversation_list'),
    path('conversations/<uuid:pk>/', views.ConversationDetailView.as_view(), name='conversation_detail'),
    path('queue/', views.QueueView.as_view(), name='queue'),
    path('assign/<uuid:pk>/', views.assign_case, name='assign_case'),
    path('send-message/<uuid:pk>/', views.send_message, name='send_message'),
    path('close-case/<uuid:pk>/', views.close_case, name='close_case'),
    path('toggle-availability/', views.toggle_availability, name='toggle_availability'),
    path('toggle-shift/', views.toggle_shift, name='toggle_shift'),
]