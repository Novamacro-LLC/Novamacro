from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Product, UserProduct


class UserProductInline(admin.TabularInline):
    model = UserProduct
    extra = 1  # Number of empty forms to display


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
    inlines = [UserProductInline]  # Add this line to include products
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'get_products')
    search_fields = ('email', 'first_name', 'last_name', 'city', 'state_abbr', 'zip_code')
    ordering = ('email',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'state_abbr')

    def get_products(self, obj):
        return ", ".join([up.product.name for up in obj.userproduct_set.all()])
    get_products.short_description = 'Assigned Products'


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Product)

