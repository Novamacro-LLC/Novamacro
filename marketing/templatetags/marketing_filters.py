from django import template

register = template.Library()


@register.filter
def filter_platform(credentials, platform):
    """Filter credentials by platform"""
    try:
        return credentials.get(platform=platform)
    except:
        return None
