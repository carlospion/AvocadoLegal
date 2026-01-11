"""Admin configuration for lawyers app."""
from django.contrib import admin
from .models import Lawyer, LawyerSchedule


class LawyerScheduleInline(admin.TabularInline):
    model = LawyerSchedule
    extra = 1


@admin.register(Lawyer)
class LawyerAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialty', 'is_available', 'is_on_shift', 'active_cases_count', 'total_cases_handled']
    list_filter = ['specialty', 'is_available', 'is_on_shift']
    search_fields = ['name', 'email']
    readonly_fields = ['id', 'created_at', 'updated_at', 'active_cases_count']
    inlines = [LawyerScheduleInline]