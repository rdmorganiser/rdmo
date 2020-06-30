from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import include, re_path

from ..views import profile_update, remove_user, terms_of_use

urlpatterns = [
    # edit own profile
    re_path(r'^$', profile_update, name='profile_update'),
    re_path('^remove', remove_user, name='profile_remove'),
]

if settings.ACCOUNT_TERMS_OF_USE is True:
    urlpatterns += [
        re_path('^terms-of-use/', terms_of_use, name='terms_of_use')
    ]

if settings.ACCOUNT or settings.SOCIALACCOUNT:
    # include django-allauth urls
    urlpatterns += [
        re_path(r'^', include('allauth.urls'))
    ]
else:
    urlpatterns += [
        re_path('^login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='account_login'),
        re_path('^logout/', auth_views.LogoutView.as_view(next_page=settings.LOGIN_REDIRECT_URL), name='account_logout'),
    ]
