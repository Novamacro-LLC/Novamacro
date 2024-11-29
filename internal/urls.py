from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUpView,StaffDashboardView, PrivateDashboardView, login_redirect_view

app_name = 'internal'

urlpatterns = [
    path('register/<int:product_id>', SignUpView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='public/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='public/password_reset.html',
             email_template_name='public/password_reset_email.html',
             subject_template_name='public/password_reset_subject.txt',
             success_url='/internal/password-reset/done/'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='public/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='public/password_reset_confirm.html',
             success_url='/internal/reset/complete/'
         ),
         name='password_reset_confirm'),
    path('reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='public/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    path('login-redirect/', login_redirect_view, name='login_redirect'),
    path('dashboard/staff/', StaffDashboardView.as_view(), name='dashboard'),
]
