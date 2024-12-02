from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Social Media Manager
class ContentSource(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    url = models.URLField()
    keywords = models.TextField()
    whitelist = models.BooleanField(default=True)
    crawl_depth = models.IntegerField(default=2)
    crawl_frequency = models.IntegerField(default=24)  # hours
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DiscoveredContent(models.Model):
    source = models.ForeignKey(ContentSource, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    content = models.TextField()
    url = models.URLField()
    discovered_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)


class GeneratedContent(models.Model):
    TONE_CHOICES = [
        ('professional', 'Professional'),
        ('casual', 'Casual'),
        ('witty', 'Witty'),
        ('informative', 'Informative'),
    ]

    discovered_content = models.ForeignKey(DiscoveredContent, on_delete=models.CASCADE)
    summary = models.TextField()
    tone = models.CharField(max_length=20, choices=TONE_CHOICES)
    hashtags = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class SocialPost(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('published', 'Published'),
        ('failed', 'Failed'),
    ]

    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('linkedin', 'LinkedIn'),
    ]

    generated_content = models.ForeignKey(GeneratedContent, on_delete=models.CASCADE)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    scheduled_time = models.DateTimeField(null=True, blank=True)
    published_time = models.DateTimeField(null=True, blank=True)
    engagement_metrics = models.JSONField(default=dict)


class SocialMediaCredentials(models.Model):
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('twitter', 'X (Twitter)'),
        ('linkedin', 'LinkedIn'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    api_key = models.CharField(max_length=255)
    api_secret = models.CharField(max_length=255)
    access_token = models.CharField(max_length=255)
    access_token_secret = models.CharField(max_length=255, null=True, blank=True)  # For X (Twitter)
    refresh_token = models.CharField(max_length=255, null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'platform']