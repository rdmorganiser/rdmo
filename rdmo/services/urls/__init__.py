from django.urls import path

from ..views import oauth_callback

urlpatterns = [
    path('oauth/<slug:provider_key>/callback/', oauth_callback, name='oauth_callback'),
]
