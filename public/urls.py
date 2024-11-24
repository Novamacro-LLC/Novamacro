from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('products', views.products, name='products'),
    path('consulting', views.consulting, name='consulting'),
    path('connect', views.connect, name='connect'),

]
