# private/urls.py
from django.urls import path
from .views import PrivateDashboardView

app_name = 'private'  # Add namespace

urlpatterns = [
    path('dashboard/', PrivateDashboardView.as_view(), name='dashboard'),
]