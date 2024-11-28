# internal/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy  # Add this import
from django.views.generic.edit import CreateView
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import Product, UserProduct


def auth(request):
    return render(request, 'public/login.html', {'title': 'Login', 'description': 'Login to your account'})


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'public/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Register'
        context['description'] = 'Sign Up for Novamacro services'  # Customize this as needed
        product_id = self.kwargs.get('product_id')
        if product_id:
            product = get_object_or_404(Product, pk=product_id)
            context['payment_link'] = product.payment_link
            context['product_name'] = product.name
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        # Get the product_id from URL parameters
        product_id = self.request.GET.get('product_id')
        if product_id:
            # Get the product
            product = get_object_or_404(Product, id=product_id)
            # Create the UserProduct relationship
            UserProduct.objects.create(
                user=self.object,  # self.object is the newly created user
                product=product
            )

        messages.success(self.request,
                         'Account created successfully! Please complete your payment to activate your subscription.')
        return response


