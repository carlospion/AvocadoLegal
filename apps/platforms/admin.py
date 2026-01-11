"""Admin configuration for platforms app."""
from django.contrib import admin
from .models import Platform, PlatformUser, Client


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ['name', 'domain', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'domain', 'contact_email']
    readonly_fields = ['id', 'api_key', 'created_at', 'updated_at']


@admin.register(PlatformUser)
class PlatformUserAdmin(admin.ModelAdmin):
    list_display = ['name', 'platform', 'email', 'role', 'created_at']
    list_filter = ['platform', 'created_at']
    search_fields = ['name', 'email', 'external_id']


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'cedula', 'platform', 'phone', 'created_at']
    list_filter = ['platform', 'created_at']
    search_fields = ['name', 'cedula', 'email', 'phone']