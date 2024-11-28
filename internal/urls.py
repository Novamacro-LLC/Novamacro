from django.urls import path
from .views import SignUpView

urlpatterns = [
    # ... your other URL patterns ...
    path('register/', SignUpView.as_view(), name='register'),
]