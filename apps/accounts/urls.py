from django.conf.urls import url, include

from .views import profile_update


urlpatterns = [
    # edit own profile
    url(r'^$', profile_update, name='profile_update'),

    # include django-allauth urls
    url(r'^', include('allauth.urls')),
]
