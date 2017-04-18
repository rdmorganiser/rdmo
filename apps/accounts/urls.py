from django.conf import settings
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from .views import profile_update

accounts_patterns = [
    # edit own profile
    url(r'^$', profile_update, name='profile_update'),
]

if settings.ACCOUNT or settings.SOCIALACCOUNT:
    # include django-allauth urls
    accounts_patterns += [
        url(r'^', include('allauth.urls')),
    ]
else:
    accounts_patterns += [
        url('^login/', auth_views.login, {'template_name': 'account/login.html'}, name='account_login'),
        url('^logout/', auth_views.logout, {'next_page': settings.LOGIN_REDIRECT_URL}, name='account_logout'),
    ]
