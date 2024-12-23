from django.urls import path
from . import views

app_name = 'marketing'

urlpatterns = [
    path('dashboard/', views.market_dash, name='market_dash'),
    # Content Sources
    path('content/sources/', views.ContentSourceListView.as_view(), name='source_list'),
    path('content/sources/add/', views.AddContentSourceView.as_view(), name='add_source'),
    path('content/sources/<int:pk>/edit/', views.UpdateContentSourceView.as_view(), name='edit_source'),
    path('content/sources/<int:pk>/delete/', views.DeleteContentSourceView.as_view(), name='delete_source'),
    # Discovered Content
    path('content/discovered/', views.DiscoveredContentListView.as_view(), name='discovered_list'),
    # Generated Content
    path('content/generated/', views.GeneratedContentListView.as_view(), name='generated_list'),
    # Social Posts
    path('content/posts/', views.SocialPostListView.as_view(), name='social_post_list'),
    path('content/posts/create/', views.CreateSocialPostView.as_view(), name='create_post'),
    path('content/posts/<int:pk>/edit/', views.UpdateSocialPostView.as_view(), name='edit_post'),
    path('content/posts/<int:pk>/delete/', views.DeleteSocialPostView.as_view(), name='delete_post'),
    # Social Media Credentials
    path('social-credentials/', views.SocialMediaCredentialsView.as_view(), name='social_credentials'),
    path('social-credentials/add/', views.AddSocialMediaCredentialsView.as_view(), name='add_credentials'),
    path('social-credentials/<int:pk>/edit/', views.UpdateSocialMediaCredentialsView.as_view(), name='edit_credentials'),
    path('content/sources/<int:pk>/analysis/', views.SourceAnalysisView.as_view(), name='source_analysis'),
    path('content/sources/rankings/', views.SourceRankingView.as_view(), name='source_rankings'),
    path('content/sources/discover/', views.AutoDiscoverSourcesView.as_view(), name='auto_discover_sources'),
    path('oauth/<str:platform>/start/', views.InitiateOAuthView.as_view(), name='oauth_start'),
    path('oauth/<str:platform>/callback/', views.OAuthCallbackView.as_view(), name='oauth_callback'),
]
