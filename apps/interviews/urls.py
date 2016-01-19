from django.conf.urls import url

from .views import interview, interview_create, interview_update, interview_delete

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)$', interview, name='interview'),
    url(r'^create$', interview_create, name='interview_create'),
    url(r'^(?P<pk>[0-9]+)/update$', interview_update, name='interview_update'),
    url(r'^(?P<pk>[0-9]+)/delete$', interview_delete, name='interview_delete'),
]
