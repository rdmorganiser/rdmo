from django.conf.urls import url

from .views import interview_create

urlpatterns = [
    # edit own profile
    url(r'^create$', interview_create, name='interview_create'),
]
