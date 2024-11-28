# internal/views.py
from django.shortcuts import render, redirect
from django.urls import reverse_lazy  # Add this import
from django.views.generic.edit import CreateView
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'public/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Register'
        context['description'] = 'Sign Up for Novamacro services'  # Customize this as needed
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, 'Account created successfully!')
        return response

