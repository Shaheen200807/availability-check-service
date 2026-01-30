from django.urls import path
from . import views

urlpatterns = [
    path('check/', views.check_availability, name='check_availability'),
    path('health/', views.health_check, name='health_check'),
]