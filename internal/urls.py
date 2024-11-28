from django.urls import path
from . import views
from .views import SignUpView

urlpatterns = [
    # ... your other URL patterns ...
    path('register/<int:product_id>', SignUpView.as_view(), name='register'),
    path('login', views.auth, name='login'),
    #path('logout', views.logout, name='logout')
]