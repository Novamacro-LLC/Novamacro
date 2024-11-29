# internal/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import Product, UserProduct
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from django.shortcuts import redirect
import logging

logger = logging.getLogger(__name__)


from .forms import CustomUserCreationForm
from .models import Product, UserProduct
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from django.shortcuts import redirect
import logging

logger = logging.getLogger(__name__)


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('internal:login')
    template_name = 'public/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Register'
        context['description'] = 'Sign Up for Novamacro services'

        # Get product_id directly from kwargs
        product_id = self.kwargs['product_id']
        logger.info(f"Product ID: {product_id}")

        if product_id:
            try:
                product = Product.objects.get(id=product_id)
                context['product'] = product
                context['payment_link'] = product.payment_link
                logger.info(f"Found product: {product.name}")
            except Product.DoesNotExist:
                logger.error(f"Product with ID {product_id} not found")
                messages.error(self.request, 'Invalid product selected.')
        return context

    def form_valid(self, form):
        # First save the form to create the user
        response = super().form_valid(form)

        # Get product_id from URL path
        product_id = self.kwargs['product_id']
        logger.info(f"Product ID in form_valid: {product_id}")

        try:
            # Get the product
            product = Product.objects.get(id=product_id)
            logger.info(f"Creating UserProduct for user {self.object.email} and product {product.name}")

            # Create the UserProduct relationship
            UserProduct.objects.create(
                user=self.object,  # self.object is the newly created user
                product=product
            )

            messages.success(self.request,
                             'Account created successfully! Please complete your payment to activate your subscription.')
            logger.info("UserProduct created successfully")
        except Product.DoesNotExist:
            logger.error(f"Product with ID {product_id} not found during form_valid")
            messages.error(self.request, 'Product could not be assigned.')
        except Exception as e:
            logger.error(f"Error creating UserProduct: {str(e)}")
            messages.error(self.request, 'There was an error assigning the product.')

        return response


class StaffDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'internal/dashboard.html'

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('private_dashboard')


class PrivateDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'private/dashboard.html'


# Custom login redirect view
def login_redirect_view(request):
    if request.user.is_staff:
        return redirect('internal:dashboard')
    return redirect('private:dashboard')



class StaffDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'internal/dashboard.html'

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('private_dashboard')


class PrivateDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'private/dashboard.html'


# Custom login redirect view
def login_redirect_view(request):
    if request.user.is_staff:
        return redirect('internal:dashboard')
    return redirect('private:dashboard')
