from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from app import views

urlpatterns = [
    path('', views.index, name='home'),
    path('disclaimer/', views.disclaimer, name='disclaimer'),
    path('privacy-policy/', views.privacy_policy, name='privacy-policy')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)