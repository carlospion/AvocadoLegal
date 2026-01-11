"""URL configuration for AvocadoLegal project."""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView, RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/lawyers/', permanent=False), name='home'),
    path('admin/', admin.site.urls),
    path('api/v1/platforms/', include('apps.platforms.urls')),
    path('api/v1/loans/', include('apps.loans.urls')),
    path('api/v1/conversations/', include('apps.conversations.urls')),
    path('lawyers/', include('apps.lawyers.urls')),
    path('demo/', TemplateView.as_view(template_name='demo.html'), name='demo'),
    path('platforms/register/', TemplateView.as_view(template_name='platforms/register.html'), name='platform_register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)