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