from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name='home'),
    path('disclaimer/', views.disclaimer, name='disclaimer'),
    path('privacy-policy/', views.privacy_policy, name='privacy-policy')
]