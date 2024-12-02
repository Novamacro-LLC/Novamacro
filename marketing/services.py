import boto3
from botocore.config import Config
import json
from .models import SocialMediaCredentials  # Fixed the model name


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
