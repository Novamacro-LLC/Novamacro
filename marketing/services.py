import boto3
from botocore.config import Config
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urlencode
import whois
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
import secrets
import hashlib
import base64
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


class OAuthError(Exception):
    """Base class for OAuth errors"""
    pass


class TokenExpiredError(OAuthError):
    """Raised when token is expired and cannot be refreshed"""
    pass


class TokenRefreshError(OAuthError):
    """Raised when token refresh fails"""
    pass


class BedrockService:
    def __init__(self):
        self.client = boto3.client('bedrock-runtime', config=Config(
            region_name='us-east-1'
        ))

    def generate_summary(self, content, max_length=500):
        prompt = f"""Please summarize the following content in a clear and engaging way, 
        keeping the summary under {max_length} characters:

        {content}"""

        response = self.client.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": [{"role": "user", "content": prompt}]
            })
        )

        return json.loads(response['body'].read())['content'][0]['text']

    def generate_social_post(self, summary, platform, tone):
        char_limits = {
            'twitter': 280,
            'facebook': 2000,
            'linkedin': 3000
        }

        prompt = f"""Create a {tone} social media post for {platform} about:

        {summary}

        Keep it under {char_limits[platform]} characters and include relevant hashtags."""

        response = self.client.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": [{"role": "user", "content": prompt}]
            })
        )

        return json.loads(response['body'].read())['content'][0]['text']


class SocialMediaService:
    @staticmethod
    def get_credentials(user, platform):
        try:
            return SocialMediaCredentials.objects.get(user=user, platform=platform)
        except SocialMediaCredentials.DoesNotExist:
            return None

    def post_to_twitter(self, credentials, content):
        # Implement X (Twitter) API integration
        import tweepy

        auth = tweepy.OAuthHandler(credentials.api_key, credentials.api_secret)
        auth.set_access_token(credentials.access_token, credentials.access_token_secret)
        api = tweepy.API(auth)

        try:
            api.update_status(content)
            return True
        except Exception as e:
            print(f"Error posting to Twitter: {str(e)}")
            return False

    def post_to_facebook(self, credentials, content):
        # Implement Facebook API integration
        import facebook

        try:
            graph = facebook.GraphAPI(credentials.access_token)
            graph.put_object("me", "feed", message=content)
            return True
        except Exception as e:
            print(f"Error posting to Facebook: {str(e)}")
            return False

    def post_to_linkedin(self, credentials, content):
        # Implement LinkedIn API integration
        from linkedin import linkedin

        try:
            authentication = linkedin.LinkedInAuthentication(
                credentials.api_key,
                credentials.api_secret,
                credentials.access_token
            )
            application = linkedin.LinkedInApplication(authentication)
            application.submit_share(content)
            return True
        except Exception as e:
            print(f"Error posting to LinkedIn: {str(e)}")
            return False


class ContentAnalyzer:
    def __init__(self):
        self.bedrock_client = boto3.client('bedrock-runtime')

    def analyze_content_quality(self, content: str, url: str) -> dict:
        """
        Detailed content quality analysis using AWS Bedrock
        """
        prompt = f"""Analyze this content for quality metrics. Consider:

        1. Content Quality:
           - Writing quality and clarity
           - Depth of analysis
           - Factual accuracy
           - Original insights
           - Use of sources/citations

        2. Authority:
           - Author expertise
           - Domain reputation
           - Citation patterns
           - Professional presentation

        3. Technical Aspects:
           - Content structure
           - Readability
           - Mobile optimization
           - Loading speed
           - User experience

        URL: {url}
        Content Sample: {content[:2000]}...

        Provide detailed scores (0-100) and explanations for each category.
        Include specific examples from the content to support your analysis.
        """

        response = self.bedrock_client.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": [{"role": "user", "content": prompt}]
            })
        )

        analysis = json.loads(response['body'].read())['content'][0]['text']

        # Parse the analysis into structured data
        return self._parse_quality_analysis(analysis)

    def categorize_content(self, content: str, url: str) -> list:
        """
        Categorize content into predefined categories
        """
        prompt = f"""Analyze this content and categorize it into relevant categories. Consider:

        1. Main Topic Areas:
           - Technology
           - Business
           - Science
           - Health
           - etc.

        2. Content Type:
           - News
           - Analysis
           - Tutorial
           - Opinion
           - Research

        3. Audience Level:
           - Beginner
           - Intermediate
           - Advanced
           - Expert

        URL: {url}
        Content: {content[:2000]}...

        Provide:
        1. Primary category
        2. Secondary categories
        3. Content type
        4. Audience level
        5. Confidence score for each categorization
        """

        response = self.bedrock_client.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": [{"role": "user", "content": prompt}]
            })
        )

        return self._parse_categorization(response)

    def analyze_source_authority(self, url: str) -> dict:
        """
        Analyze source authority and reputation
        """
        try:
            domain = urlparse(url).netloc

            # Check domain age
            whois_info = whois.whois(domain)
            domain_age = datetime.now() - whois_info.creation_date[0]

            # Check for SSL
            has_ssl = url.startswith('https')

            # Check for social presence
            social_presence = self._check_social_presence(domain)

            # Use Bedrock for reputation analysis
            prompt = f"""Analyze the authority and reputation of this website:

            Domain: {domain}
            Age: {domain_age.days} days
            SSL: {has_ssl}
            Social Presence: {social_presence}

            Consider:
            1. Industry recognition
            2. Content quality
            3. Professional presentation
            4. Technical implementation

            Provide an authority score (0-100) and detailed explanation.
            """

            response = self.bedrock_client.invoke_model(
                modelId='anthropic.claude-3-haiku-20240307',
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 500,
                    "messages": [{"role": "user", "content": prompt}]
                })
            )

            return self._parse_authority_analysis(response)

        except Exception as e:
            return {
                'authority_score': 0,
                'error': str(e)
            }

    def calculate_freshness_score(self, source: ContentSource) -> int:
        """
        Calculate content freshness score based on update frequency
        """
        try:
            # Get recent content
            recent_content = DiscoveredContent.objects.filter(
                source=source
            ).order_by('-discovered_at')[:10]

            if not recent_content:
                return 0

            # Calculate average time between updates
            update_times = [c.discovered_at for c in recent_content]
            time_diffs = []
            for i in range(len(update_times) - 1):
                diff = update_times[i] - update_times[i + 1]
                time_diffs.append(diff.total_seconds())

            avg_update_time = sum(time_diffs) / len(time_diffs)

            # Score based on update frequency
            if avg_update_time <= 3600:  # Hourly
                return 100
            elif avg_update_time <= 86400:  # Daily
                return 80
            elif avg_update_time <= 604800:  # Weekly
                return 60
            elif avg_update_time <= 2592000:  # Monthly
                return 40
            else:
                return 20

        except Exception as e:
            print(f"Error calculating freshness score: {str(e)}")
            return 0

    def calculate_engagement_score(self, source: ContentSource) -> int:
        """
        Calculate engagement score based on social media metrics
        """
        try:
            # Get recent posts
            recent_posts = SocialPost.objects.filter(
                generated_content__discovered_content__source=source
            ).order_by('-created_at')[:20]

            if not recent_posts:
                return 0

            # Calculate average engagement
            total_engagement = 0
            for post in recent_posts:
                metrics = post.engagement_metrics
                engagement = (
                        metrics.get('likes', 0) * 1 +
                        metrics.get('shares', 0) * 3 +
                        metrics.get('comments', 0) * 5
                )
                total_engagement += engagement

            avg_engagement = total_engagement / len(recent_posts)

            # Normalize to 0-100 scale
            normalized_score = min(100, (avg_engagement / 100) * 100)

            return round(normalized_score)

        except Exception as e:
            print(f"Error calculating engagement score: {str(e)}")
            return 0


class SourceRankingService:
    def __init__(self):
        self.analyzer = ContentAnalyzer()

    def analyze_and_rank_source(self, source: ContentSource) -> SourceAnalysis:
        """
        Perform comprehensive source analysis and ranking
        """
        try:
            # Get latest content
            latest_content = DiscoveredContent.objects.filter(
                source=source
            ).order_by('-discovered_at').first()

            if not latest_content:
                return None

            # Perform analysis
            quality_analysis = self.analyzer.analyze_content_quality(
                latest_content.content,
                latest_content.url
            )

            categories = self.analyzer.categorize_content(
                latest_content.content,
                latest_content.url
            )

            authority_analysis = self.analyzer.analyze_source_authority(
                source.url
            )

            freshness_score = self.analyzer.calculate_freshness_score(source)
            engagement_score = self.analyzer.calculate_engagement_score(source)

            # Create or update analysis
            analysis, created = SourceAnalysis.objects.update_or_create(
                source=source,
                defaults={
                    'quality_score': quality_analysis['quality_score'],
                    'relevance_score': quality_analysis['relevance_score'],
                    'authority_score': authority_analysis['authority_score'],
                    'freshness_score': freshness_score,
                    'engagement_score': engagement_score,
                    'analysis_notes': {
                        'quality': quality_analysis,
                        'authority': authority_analysis,
                        'categories': categories
                    }
                }
            )

            # Update categories
            analysis.categories.clear()
            for category in categories:
                cat_obj, _ = SourceCategory.objects.get_or_create(
                    name=category['name'],
                    defaults={'description': category['description']}
                )
                analysis.categories.add(cat_obj)

            # Calculate overall rank
            analysis.overall_rank = analysis.calculate_overall_rank()
            analysis.save()

            return analysis

        except Exception as e:
            print(f"Error analyzing source {source.name}: {str(e)}")
            return None

    def _analyze_domain(self, url: str) -> Dict:
        """Analyze domain age and reputation"""
        try:
            domain = urlparse(url).netloc
            whois_info = whois.whois(domain)

            # Calculate domain age
            creation_date = whois_info.creation_date
            if isinstance(creation_date, list):
                creation_date = creation_date[0]

            domain_age = datetime.now() - creation_date

            return {
                'domain': domain,
                'age_days': domain_age.days,
                'has_ssl': url.startswith('https'),
                'registrar': whois_info.registrar
            }
        except Exception as e:
            print(f"Error analyzing domain {url}: {str(e)}")
            return None

    def _check_content_quality(self, url: str) -> Dict:
        """Check content quality of the website"""
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Get main content
            # Remove scripts, styles, and navigation elements
            for element in soup(['script', 'style', 'nav', 'header', 'footer']):
                element.decompose()

            text = soup.get_text()

            # Analyze with Bedrock
            prompt = f"""Analyze this website's content quality. Consider:
            1. Writing quality and professionalism
            2. Content depth and expertise
            3. Content organization
            4. Update frequency
            5. Overall authority

            Content sample:
            {text[:2000]}...

            Provide a score from 0-100 and brief explanation."""

            response = self.bedrock_client.invoke_model(
                modelId='anthropic.claude-3-haiku-20240307',
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 500,
                    "messages": [{"role": "user", "content": prompt}]
                })
            )

            result = json.loads(response['body'].read())
            text_response = result['content'][0]['text']

            # Parse score from response
            import re
            score_match = re.search(r'(\d{1,3})', text_response)
            score = int(score_match.group(1)) if score_match else 50

            return {
                'score': score,
                'analysis': text_response
            }

        except Exception as e:
            print(f"Error checking content quality for {url}: {str(e)}")
            return None

    def find_and_add_sources(self, user, keywords: List[str], max_sources: int = 5) -> List[ContentSource]:
        """Find and add new content sources based on keywords"""
        try:
            discovered_sources = []

            # Use Bedrock to generate search queries
            search_prompt = f"""Generate 3 specific search queries to find high-quality content sources about:
            {', '.join(keywords)}

            Focus on finding authoritative and regularly updated sources."""

            response = self.bedrock_client.invoke_model(
                modelId='anthropic.claude-3-haiku-20240307',
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 300,
                    "messages": [{"role": "user", "content": search_prompt}]
                })
            )

            queries = [q.strip() for q in response['content'][0]['text'].split('\n') if q.strip()]

            # Search for each query using a search engine API
            for query in queries:
                # Here you would integrate with a search API (Google Custom Search, Bing, etc.)
                # For demonstration, we'll use a placeholder search function
                results = self._search_sources(query)

                for result in results:
                    if len(discovered_sources) >= max_sources:
                        break

                    domain_analysis = self._analyze_domain(result['url'])
                    if not domain_analysis:
                        continue

                    content_analysis = self._check_content_quality(result['url'])
                    if not content_analysis:
                        continue

                    if content_analysis['score'] >= 70 and domain_analysis['age_days'] > 90:
                        source = ContentSource.objects.create(
                            user=user,
                            name=result['title'],
                            url=result['url'],
                            keywords=','.join(keywords),
                            whitelist=True,
                            crawl_depth=2,
                            crawl_frequency=24
                        )
                        discovered_sources.append(source)

            return discovered_sources

        except Exception as e:
            print(f"Error in find_and_add_sources: {str(e)}")
            raise

    def _search_sources(self, query: str) -> List[Dict]:
        """
        Placeholder for search engine integration.
        In production, integrate with Google Custom Search API or similar.
        """
        # This is a mock implementation
        # In production, integrate with an actual search API
        return [
            {
                'title': 'Example Source 1',
                'url': 'https://example1.com',
                'description': 'Example description 1'
            },
            {
                'title': 'Example Source 2',
                'url': 'https://example2.com',
                'description': 'Example description 2'
            }
        ]


class AutomatedSourceManager:
    def __init__(self):
        # Configure the Bedrock client with a specific region
        self.bedrock_client = boto3.client(
            'bedrock-runtime',
            region_name='us-east-1',  # Specify your AWS region
            config=Config(
                region_name='us-east-1'  # Ensure region is set in config too
            )
        )

    def find_and_add_sources(self, user, keywords: List[str], max_sources: int = 5) -> List[ContentSource]:
        """Find and add new content sources based on keywords"""
        try:
            discovered_sources = []

            # For now, let's add a simple source as a test
            source = ContentSource.objects.create(
                user=user,
                name="Test Source",
                url="https://example.com",
                keywords=','.join(keywords),
                whitelist=True,
                crawl_depth=2,
                crawl_frequency=24
            )
            discovered_sources.append(source)

            return discovered_sources

        except Exception as e:
            print(f"Error in find_and_add_sources: {str(e)}")
            raise


class SocialOAuthService:
    def __init__(self):
        self.oauth_settings = {
            'twitter': {
                'auth_url': 'https://twitter.com/i/oauth2/authorize',
                'token_url': 'https://api.twitter.com/2/oauth2/token',
                'scope': 'tweet.read tweet.write users.read',
            },
            'facebook': {
                'auth_url': 'https://www.facebook.com/v18.0/dialog/oauth',
                'token_url': 'https://graph.facebook.com/v18.0/oauth/access_token',
                'scope': 'public_profile'
            },
            'linkedin': {
                'auth_url': 'https://www.linkedin.com/oauth/v2/authorization',
                'token_url': 'https://www.linkedin.com/oauth/v2/accessToken',
                'scope': 'w_member_social',
            }
        }
        self.code_verifiers = {}

    def get_authorization_url(self, platform, user):
        """Generate OAuth authorization URL for the specified platform"""
        if platform not in self.oauth_settings:
            raise ValueError(f"Unsupported platform: {platform}")

        print(f"\nOAuth Debug for {platform}:")
        try:
            credentials = SocialMediaCredentials.objects.get(
                user=user,
                platform=platform
            )
            print(f"Found credentials for user {user.id}")
            print(f"Client ID format: {credentials.client_id[:5]}...")

            settings = self.oauth_settings[platform]
            state = secrets.token_urlsafe(32)

            if platform == 'twitter':
                code_verifier = secrets.token_urlsafe(32)
                # Create OAuth state with code_verifier
                OAuthState.objects.create(
                    user=user,
                    state=state,
                    platform=platform,
                    code_verifier=code_verifier  # Store the code_verifier
                )
                params = {
                    'client_id': credentials.client_id,
                    'redirect_uri': f"http://localhost:8000/marketing/oauth/{platform}/callback/",
                    'state': state,
                    'scope': 'tweet.read tweet.write users.read',
                    'response_type': 'code',
                    'code_challenge': code_verifier,
                    'code_challenge_method': 'plain'
                }
            else:
                # Create OAuth state without code_verifier for other platforms
                OAuthState.objects.create(
                    user=user,
                    state=state,
                    platform=platform
                )
                params = {
                    'client_id': credentials.client_id,
                    'redirect_uri': f"http://localhost:8000/marketing/oauth/{platform}/callback/",
                    'scope': settings['scope'],
                    'state': state,
                    'response_type': 'code'
                }

                if platform == 'facebook':
                    params['auth_type'] = 'rerequest'

            print("OAuth Parameters:")
            for key, value in params.items():
                print(f"{key}: {value}")

            auth_url = f"{settings['auth_url']}?{urlencode(params)}"
            print(f"Final URL: {auth_url}")

            return auth_url

        except Exception as e:
            print(f"Error generating auth URL: {str(e)}")
            raise

    def handle_oauth_callback(self, platform, code, state):
        """Handle OAuth callback and get tokens"""
        try:
            oauth_state = OAuthState.objects.get(state=state)
            if oauth_state.platform != platform:
                raise ValueError("Invalid platform in OAuth state")

            settings = self.oauth_settings.get(platform)
            if not settings:
                raise ValueError(f"Unsupported platform: {platform}")

            credentials = oauth_state.user.social_credentials.get(platform=platform)

            if platform == 'twitter':
                code_verifier = oauth_state.code_verifier  # Changed this line
                if not code_verifier:
                    raise ValueError("Missing code verifier")

                params = {
                    'code': code,
                    'grant_type': 'authorization_code',
                    'client_id': credentials.client_id,
                    'redirect_uri': f"http://localhost:8000/marketing/oauth/{platform}/callback/",
                    'code_verifier': code_verifier
                }
            else:
                params = {
                    'client_id': credentials.client_id,
                    'client_secret': credentials.client_secret,
                    'code': code,
                    'redirect_uri': f"http://localhost:8000/marketing/oauth/{platform}/callback/",
                    'grant_type': 'authorization_code'
                }

            response = requests.post(settings['token_url'], data=params)

            if response.status_code != 200:
                raise ValueError(f"Token exchange failed: {response.text}")

            return response.json()

        except OAuthState.DoesNotExist:
            raise ValueError("Invalid OAuth state")
        except Exception as e:
            raise ValueError(f"OAuth callback failed: {str(e)}")

    def verify_token_validity(self, credentials):
        """Verify if the token is valid"""
        try:
            if credentials.platform == 'facebook':
                response = requests.get(
                    'https://graph.facebook.com/v18.0/me',
                    params={'access_token': credentials.access_token}
                )
            elif credentials.platform == 'twitter':
                response = requests.get(
                    'https://api.twitter.com/2/users/me',
                    headers={'Authorization': f'Bearer {credentials.access_token}'}
                )
            elif credentials.platform == 'linkedin':
                # Use LinkedIn's token introspection
                response = requests.get(
                    'https://api.linkedin.com/v2/me',
                    headers={
                        'Authorization': f'Bearer {credentials.access_token}',
                        'X-Restli-Protocol-Version': '2.0.0'
                    }
                )
                # For LinkedIn, we'll consider it valid even if we get a 403
                # as long as we get a response
                if response.status_code == 403:
                    return True, None
            else:
                return False, "Unsupported platform"

            response.raise_for_status()
            return True, None

        except requests.exceptions.RequestException as e:
            if credentials.platform == 'linkedin' and '403' in str(e):
                return True, None
            return False, str(e)

    def check_and_refresh_token(self, credentials):
        """Check token validity and refresh if needed"""
        try:
            if not self._needs_refresh(credentials):
                return True, None

            new_tokens = self._refresh_token(credentials)

            credentials.access_token = new_tokens['access_token']
            credentials.refresh_token = new_tokens.get('refresh_token', credentials.refresh_token)
            credentials.expires_at = timezone.now() + timedelta(seconds=new_tokens.get('expires_in', 3600))
            credentials.save()

            return True, None

        except TokenExpiredError:
            return False, "Token has expired and cannot be refreshed. Please reconnect your account."
        except TokenRefreshError as e:
            return False, f"Failed to refresh token: {str(e)}"
        except Exception as e:
            return False, f"Unexpected error during token refresh: {str(e)}"

    def _needs_refresh(self, credentials):
        """Check if token needs refresh"""
        if not credentials.expires_at:
            return True
        return credentials.expires_at - timezone.now() < timedelta(hours=1)

    def _refresh_token(self, credentials):
        """Refresh OAuth tokens"""
        if credentials.platform not in self.oauth_settings:
            raise ValueError(f"Unsupported platform: {credentials.platform}")

        settings = self.oauth_settings[credentials.platform]

        data = {
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': credentials.refresh_token,
        }

        if credentials.platform == 'facebook':
            data['redirect_uri'] = "http://localhost:8000/marketing/oauth/facebook/callback/"

        try:
            response = requests.post(settings['token_url'], data=data)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            raise TokenRefreshError(f"Token refresh request failed: {str(e)}")
        except Exception as e:
            raise TokenRefreshError(f"Token refresh failed: {str(e)}")


class TokenRefreshMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.oauth_service = SocialOAuthService()

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if not hasattr(view_func, 'requires_fresh_token'):
            return None

        if not request.user.is_authenticated:
            return None

        # Get credentials for the relevant platform
        platform = view_kwargs.get('platform')
        if not platform:
            return None

        try:
            from .models import SocialMediaCredentials
            credentials = SocialMediaCredentials.objects.get(
                user=request.user,
                platform=platform
            )

            success, error = self.oauth_service.check_and_refresh_token(credentials)
            if not success:
                messages.error(request, error)
                return redirect('marketing:social_credentials')

        except SocialMediaCredentials.DoesNotExist:
            messages.error(request, f"No credentials found for {platform}")
            return redirect('marketing:social_credentials')
        except Exception as e:
            messages.error(request, f"Error checking credentials: {str(e)}")
            return redirect('marketing:social_credentials')

        return None
