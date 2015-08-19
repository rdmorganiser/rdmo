from django.conf import settings as django_settings

def settings(request):

    return {
        'site_title': django_settings.SITE_TITLE,
        'site_url': django_settings.SITE_URL
    }
