from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .models import ContentSource, DiscoveredContent, GeneratedContent, SocialPost, SocialMediaCredentials
from .forms import SocialMediaCredentialsForm
from .services import BedrockService


def market_dash(request):
    return render(request, 'marketing/market_dash.html')


class SocialMediaCredentialsView(LoginRequiredMixin, ListView):
    model = SocialMediaCredentials
    template_name = 'marketing/social_credentials.html'  # Updated template path
    context_object_name = 'credentials'

    def get_queryset(self):
        return SocialMediaCredentials.objects.filter(user=self.request.user)


class AddSocialMediaCredentialsView(LoginRequiredMixin, CreateView):
    model = SocialMediaCredentials
    form_class = SocialMediaCredentialsForm
    template_name = 'marketing/social_credentials_form.html'  # Updated template path
    success_url = reverse_lazy('marketing:social_credentials')  # Changed namespace

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UpdateSocialMediaCredentialsView(LoginRequiredMixin, UpdateView):  # Added missing view
    model = SocialMediaCredentials
    form_class = SocialMediaCredentialsForm
    template_name = 'marketing/social_credentials_form.html'  # Updated template path
    success_url = reverse_lazy('marketing:social_credentials')  # Changed namespace

    def get_queryset(self):
        return SocialMediaCredentials.objects.filter(user=self.request.user)



