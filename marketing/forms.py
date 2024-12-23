# content_automation/forms.py
from django import forms
from .models import SocialMediaCredentials, ContentSource, SocialPost


class SocialMediaCredentialsForm(forms.ModelForm):
    api_key = forms.CharField(widget=forms.PasswordInput())
    api_secret = forms.CharField(widget=forms.PasswordInput())
    access_token = forms.CharField(widget=forms.PasswordInput())
    access_token_secret = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = SocialMediaCredentials
        fields = ['platform', 'api_key', 'api_secret', 'access_token', 'access_token_secret']


class ContentSourceForm(forms.ModelForm):
    class Meta:
        model = ContentSource
        fields = ['name', 'url', 'keywords', 'whitelist', 'crawl_depth', 'crawl_frequency']


class SocialPostForm(forms.ModelForm):
    scheduled_time = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        help_text="Leave blank to publish immediately or save as draft"
    )

    class Meta:
        model = SocialPost
        fields = ['platform', 'content', 'scheduled_time']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }


class KeywordSourceDiscoveryForm(forms.ModelForm):
    keywords = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'
        }),
        help_text="Enter keywords or phrases, one per line"
    )
    max_sources = forms.IntegerField(
        initial=5,
        min_value=1,
        max_value=10,
        widget=forms.NumberInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'
        }),
        help_text="Maximum number of sources to add (1-10)"
    )

    class Meta:
        model = ContentSource
        fields = ['keywords', 'max_sources']
