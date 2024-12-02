from django.urls import path
from . import views

app_name = 'marketing'  # Added app_name for namespace

urlpatterns = [
    path('dashboard/', views.market_dash, name='market_dash'),
    path('social-credentials/', views.SocialMediaCredentialsView.as_view(), name='social_credentials'),
    path('social-credentials/add/', views.AddSocialMediaCredentialsView.as_view(), name='add_credentials'),
    path('social-credentials/<int:pk>/edit/', views.UpdateSocialMediaCredentialsView.as_view(), name='edit_credentials'),
]