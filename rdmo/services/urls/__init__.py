from django.urls import path

from ..views import oauth_callback

urlpatterns = [
    path('oauth/<slug:url_name>/callback/', oauth_callback, name='oauth_callback'),
]
