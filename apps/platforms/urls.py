"""URL configuration for platforms app."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlatformRegistrationViewSet, PlatformUserViewSet, ClientViewSet

router = DefaultRouter()
router.register(r'users', PlatformUserViewSet, basename='platformuser')
router.register(r'clients', ClientViewSet, basename='client')

urlpatterns = [
    path('register/', PlatformRegistrationViewSet.as_view({'post': 'create'}), name='platform-register'),
    path('', include(router.urls)),
]