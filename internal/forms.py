from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

# Create state choices
STATE_CHOICES = [
    ('', 'Select one...'),
    ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'),
    ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'),
    ('CT', 'Connecticut'), ('DE', 'Delaware'), ('FL', 'Florida'),
    ('GA', 'Georgia'), ('HI', 'Hawaii'), ('IA', 'Idaho'),
    ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'),
    ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'),
    ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'),
    ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'),
    ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'),
    ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'),
    ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'),
    ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'),
    ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'),
    ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'), ('WY', 'Wyoming')
]


class CustomUserCreationForm(UserCreationForm):

    # Redefine password fields to match your naming convention
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input medium w-input',
            'placeholder': 'Password',
            'id': 'password-form-5',
            'name': 'password-form-5',
            'maxlength': '256',
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input medium w-input',
            'placeholder': 'Repeat Password',
            'id': 'password-2-form-5',
            'name': 'password-2-form-5',
            'maxlength': '256',
        })
    )


    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'phone_number',
                 'address', 'city', 'state_abbr', 'zip_code')
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'input medium w-input',
                'placeholder': 'Email Address',
                'id': 'email-form-6',
                'maxlength': '256',
                'name': 'email-form-5',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'input medium w-node-cdcb9418-85d6-ebcd-6e81-b284e0864eb0-8e490223 w-input',
                'placeholder': 'First Name',
                'id': 'firstname-form',
                'maxlength': '256',
                'name': 'firstname-form-5',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'input medium w-node-_92375030-ea2c-6355-7837-fa68df8cfbd3-8e490223 w-input',
                'placeholder': 'Last Name',
                'id': 'lastname-form',
                'maxlength': '256',
                'name': 'lastname-form-5',
            }),
            'address': forms.TextInput(attrs={
                'class': 'input medium w-input',
                'placeholder': 'Address',
                'id': 'address-form',
                'maxlength': '256',
                'name': 'address-form-5',
            }),
            'city': forms.TextInput(attrs={
                'class': 'input medium w-input',
                'placeholder': 'City',
                'id': 'city-form',
                'maxlength': '256',
                'name': 'city-form-5',
            }),
            'state_abbr': forms.Select(
                choices=STATE_CHOICES,
                attrs={
                    'class': 'select medium w-select',
                    'id': 'state',
                    'name': 'state-1',
                }
            ),
            'zip_code': forms.TextInput(attrs={
                'class': 'input medium w-node-_77b1ac9a-530a-7b0b-086f-1f7418716e2d-8e490223 w-input',
                'placeholder': 'Zip',
                'id': 'zip-form',
                'maxlength': '256',
                'name': 'zip-form-5',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'input medium w-node-_8ed50714-d68b-982a-f4bf-b9b30ec39723-8e490223 w-input',
                'placeholder': 'Phone Number',
                'id': 'phone-form',
                'maxlength': '256',
                'name': 'phone-form-5',
                'type': 'tel',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['phone_number'].required = True
