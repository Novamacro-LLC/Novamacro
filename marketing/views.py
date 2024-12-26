from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from functools import wraps
from .models import (
    ContentSource,
    DiscoveredContent,
    GeneratedContent,
    SocialPost,
    SocialMediaCredentials,
    SourceAnalysis,
    SourceCategory,
    OAuthState
)
from .forms import (
    SocialMediaCredentialsForm,
    ContentSourceForm,
    KeywordSourceDiscoveryForm,
    SocialPostForm
)
from .services import (
    BedrockService,
    ContentAnalyzer,
    SourceRankingService,
    SocialOAuthService,
    AutomatedSourceManager
)


def market_dash(request):
    return render(request, 'marketing/market_dash.html')


class ContentSourceListView(LoginRequiredMixin, ListView):
    model = ContentSource
    template_name = 'marketing/source_list.html'
    context_object_name = 'sources'

    def get_queryset(self):
        return ContentSource.objects.filter(user=self.request.user)


class AddSocialMediaCredentialsView(LoginRequiredMixin, CreateView):
    model = SocialMediaCredentials
    form_class = SocialMediaCredentialsForm
    template_name = 'marketing/social_credentials_form.html'
    success_url = reverse_lazy('marketing:social_credentials')

    def get_initial(self):
        initial = super().get_initial()
        platform = self.request.GET.get('platform')
        if platform:
            initial['platform'] = platform
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, f"Credentials added successfully. Now you can connect your account.")
        return super().form_valid(form)


# views.py
class AddContentSourceView(LoginRequiredMixin, CreateView):
    model = ContentSource
    form_class = ContentSourceForm
    template_name = 'marketing/source_form.html'
    success_url = reverse_lazy('marketing:source_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Content source added successfully.")
        return super().form_valid(form)

class DiscoveredContentListView(LoginRequiredMixin, ListView):
    model = DiscoveredContent
    template_name = 'marketing/discovered_list.html'
    context_object_name = 'contents'

    def get_queryset(self):
        return DiscoveredContent.objects.filter(
            source__user=self.request.user
        ).order_by('-discovered_at')


class SocialMediaCredentialsView(LoginRequiredMixin, ListView):
    model = SocialMediaCredentials
    template_name = 'marketing/social_credentials.html'
    context_object_name = 'credentials'

    def get_queryset(self):
        return SocialMediaCredentials.objects.filter(user=self.request.user)


class AddSocialMediaCredentialsView(LoginRequiredMixin, CreateView):
    model = SocialMediaCredentials
    form_class = SocialMediaCredentialsForm
    template_name = 'marketing/social_credentials_form.html'
    success_url = reverse_lazy('marketing:social_credentials')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UpdateSocialMediaCredentialsView(LoginRequiredMixin, UpdateView):
    model = SocialMediaCredentials
    form_class = SocialMediaCredentialsForm
    template_name = 'marketing/social_credentials_form.html'
    success_url = reverse_lazy('marketing:social_credentials')

    def get_queryset(self):
        return SocialMediaCredentials.objects.filter(user=self.request.user)


class UpdateContentSourceView(LoginRequiredMixin, UpdateView):
    model = ContentSource
    form_class = ContentSourceForm
    template_name = 'marketing/source_form.html'
    success_url = reverse_lazy('marketing:source_list')

    def get_queryset(self):
        return ContentSource.objects.filter(user=self.request.user)


class DeleteContentSourceView(LoginRequiredMixin, DeleteView):
    model = ContentSource
    success_url = reverse_lazy('marketing:source_list')
    template_name = 'marketing/source_confirm_delete.html'

    def get_queryset(self):
        return ContentSource.objects.filter(user=self.request.user)


class GeneratedContentListView(LoginRequiredMixin, ListView):
    model = GeneratedContent
    template_name = 'marketing/generated_content_list.html'
    context_object_name = 'generated_contents'

    def get_queryset(self):
        return GeneratedContent.objects.filter(
            discovered_content__source__user=self.request.user
        ).order_by('-created_at')


class SocialPostListView(LoginRequiredMixin, ListView):
    model = SocialPost
    template_name = 'marketing/social_post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return SocialPost.objects.filter(
            generated_content__discovered_content__source__user=self.request.user
        ).order_by('-scheduled_time', '-created_at')


class CreateSocialPostView(LoginRequiredMixin, CreateView):
    model = SocialPost
    form_class = SocialPostForm
    template_name = 'marketing/social_post_form.html'
    success_url = reverse_lazy('marketing:social_post_list')

    def form_valid(self, form):
        # Get the action from the submit button (draft, schedule, or publish)
        action = self.request.POST.get('action', 'draft')

        post = form.save(commit=False)

        # Set the status based on the action
        if action == 'publish':
            post.status = 'published'
            post.published_time = timezone.now()
        elif action == 'schedule' and post.scheduled_time:
            post.status = 'scheduled'
        else:
            post.status = 'draft'

        return super().form_valid(form)


class UpdateSocialPostView(LoginRequiredMixin, UpdateView):
    model = SocialPost
    form_class = SocialPostForm
    template_name = 'marketing/social_post_form.html'
    success_url = reverse_lazy('marketing:social_post_list')

    def get_queryset(self):
        return SocialPost.objects.filter(
            generated_content__discovered_content__source__user=self.request.user
        )

    def form_valid(self, form):
        action = self.request.POST.get('action', 'draft')
        post = form.save(commit=False)

        if action == 'publish':
            post.status = 'published'
            post.published_time = timezone.now()
        elif action == 'schedule' and post.scheduled_time:
            post.status = 'scheduled'
        else:
            post.status = 'draft'

        return super().form_valid(form)


class DeleteSocialPostView(LoginRequiredMixin, DeleteView):
    model = SocialPost
    template_name = 'marketing/social_post_confirm_delete.html'
    success_url = reverse_lazy('marketing:social_post_list')

    def get_queryset(self):
        return SocialPost.objects.filter(
            generated_content__discovered_content__source__user=self.request.user
        )


class SourceAnalysisView(LoginRequiredMixin, DetailView):
    model = SourceAnalysis
    template_name = 'marketing/source_analysis.html'
    context_object_name = 'analysis'

    def get_queryset(self):
        return SourceAnalysis.objects.filter(
            source__user=self.request.user
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['source'] = self.object.source
        return context


class SourceRankingView(LoginRequiredMixin, ListView):
    model = SourceAnalysis
    template_name = 'marketing/source_ranking.html'
    context_object_name = 'rankings'

    def get_queryset(self):
        return SourceAnalysis.objects.filter(
            source__user=self.request.user
        ).order_by('-overall_rank')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = SourceCategory.objects.all()
        return context


class AutoDiscoverSourcesView(LoginRequiredMixin, FormView):
    template_name = 'marketing/auto_discover_sources.html'
    form_class = KeywordSourceDiscoveryForm
    success_url = reverse_lazy('marketing:source_list')

    def form_valid(self, form):
        keywords = [k.strip() for k in form.cleaned_data['keywords'].split('\n') if k.strip()]
        max_sources = form.cleaned_data['max_sources']

        source_manager = AutomatedSourceManager()
        try:
            added_sources = source_manager.find_and_add_sources(
                user=self.request.user,
                keywords=keywords,
                max_sources=max_sources
            )

            messages.success(
                self.request,
                f"Successfully added {len(added_sources)} new content sources based on your keywords."
            )
        except Exception as e:
            messages.error(
                self.request,
                f"Error discovering sources: {str(e)}"
            )

        return super().form_valid(form)


class InitiateOAuthView(LoginRequiredMixin, View):
    def get(self, request, platform):
        oauth_service = SocialOAuthService()
        try:
            auth_url = oauth_service.get_authorization_url(platform, request.user)
            return redirect(auth_url)
        except Exception as e:
            messages.error(request, f"Error initiating {platform} authentication: {str(e)}")
            return redirect('marketing:social_credentials')


class OAuthCallbackView(LoginRequiredMixin, View):
    def get(self, request, platform):
        code = request.GET.get('code')
        state = request.GET.get('state')

        if not code or not state:
            messages.error(request, "Invalid OAuth callback parameters")
            return redirect('marketing:social_credentials')

        oauth_service = SocialOAuthService()
        try:
            tokens = oauth_service.handle_oauth_callback(platform, code, state)

            # Save credentials
            SocialMediaCredentials.objects.update_or_create(
                user=request.user,
                platform=platform,
                defaults={
                    'access_token': tokens.get('access_token'),
                    'refresh_token': tokens.get('refresh_token'),
                    'expires_at': timezone.now() + timedelta(seconds=tokens.get('expires_in', 3600))
                }
            )

            messages.success(request, f"Successfully connected {platform} account!")
        except Exception as e:
            messages.error(request, f"Error completing {platform} authentication: {str(e)}")

        return redirect('marketing:social_credentials')


def requires_fresh_token(view_func):
    """Decorator to mark views that require fresh tokens"""
    view_func.requires_fresh_token = True
    return view_func


class OAuthCallbackView(LoginRequiredMixin, View):
    def get(self, request, platform):
        code = request.GET.get('code')
        state = request.GET.get('state')
        error = request.GET.get('error')
        error_description = request.GET.get('error_description')

        if error:
            messages.error(request, f"Authentication error: {error_description or error}")
            return redirect('marketing:social_credentials')

        if not code or not state:
            messages.error(request, "Invalid OAuth callback parameters")
            return redirect('marketing:social_credentials')

        oauth_service = SocialOAuthService()
        try:
            # Verify state first
            try:
                oauth_state = OAuthState.objects.get(
                    state=state,
                    user=request.user
                )
                if oauth_state.platform != platform:
                    raise ValidationError("Invalid platform in OAuth state")
            except OAuthState.DoesNotExist:
                raise ValidationError("Invalid or expired OAuth state")

            # Get tokens
            tokens = oauth_service.handle_oauth_callback(platform, code, state)

            # Verify token validity
            test_credentials = SocialMediaCredentials(
                user=request.user,
                platform=platform,
                access_token=tokens.get('access_token')
            )
            is_valid, error = oauth_service.verify_token_validity(test_credentials)

            if not is_valid:
                raise ValidationError(f"Token validation failed: {error}")

            # Save credentials
            credentials, created = SocialMediaCredentials.objects.update_or_create(
                user=request.user,
                platform=platform,
                defaults={
                    'access_token': tokens.get('access_token'),
                    'refresh_token': tokens.get('refresh_token'),
                    'expires_at': timezone.now() + timedelta(seconds=tokens.get('expires_in', 3600))
                }
            )

            messages.success(request, f"Successfully connected {platform} account!")

        except ValidationError as e:
            messages.error(request, str(e))
        except OAuthError as e:
            messages.error(request, f"OAuth error: {str(e)}")
        except Exception as e:
            messages.error(request, f"Unexpected error: {str(e)}")

        return redirect('marketing:social_credentials')


@requires_fresh_token
class CreateSocialPostView(LoginRequiredMixin, CreateView):
    """Example view requiring fresh tokens"""
    model = SocialPost
    form_class = SocialPostForm
    template_name = 'marketing/social_post_form.html'

    def form_valid(self, form):
        platform = form.cleaned_data.get('platform')
        credentials = SocialMediaCredentials.objects.get(
            user=self.request.user,
            platform=platform
        )

        # Token will be automatically refreshed by middleware if needed
        # Proceed with posting...
        return super().form_valid(form)


class DeleteSocialMediaCredentialsView(LoginRequiredMixin, DeleteView):
    model = SocialMediaCredentials
    success_url = reverse_lazy('marketing:social_credentials')
    template_name = 'marketing/social_credentials_confirm_delete.html'

    def get_queryset(self):
        return SocialMediaCredentials.objects.filter(user=self.request.user)


def privacy_policy(request):
    return render(request, 'privacy_policy.html')


def terms_of_service(request):
    return render(request, 'terms_of_service.html')
