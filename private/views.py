# private/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class PrivateDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'private/dashboard.html'
