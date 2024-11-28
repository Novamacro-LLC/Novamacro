from django.urls import path

from internal.urls import urlpatterns
from . import views

urlpatterns = [
    path('dashboard/', views.market_dash, name='market_dash'),
]