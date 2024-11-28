from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    """Define admin model for custom User model with no username field."""
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {
            'fields': (
                'first_name',
                'last_name',
                'phone_number',
                'date_of_birth',
                'address',
                'city',
                'state_abbr',
                'zip_code'
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            )
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'city', 'state_abbr', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name', 'city', 'state_abbr', 'zip_code')
    ordering = ('email',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'state_abbr')


admin.site.register(CustomUser, CustomUserAdmin)