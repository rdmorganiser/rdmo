from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import TemplateView

from .views import *

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', interview, name='interview'),

    url(_(r'^(?P<interview_id>[0-9]+)/start/$'), interview_start, name='interview_start'),
    url(_(r'^(?P<interview_id>[0-9]+)/resume/$'), interview_resume, name='interview_resume'),
    url(_(r'^(?P<interview_id>[0-9]+)/group/(?P<group_id>[0-9]+)$'), interview_group, name='interview_group'),
    url(_(r'^(?P<interview_id>[0-9]+)/done$'), interview_done, name='interview_done'),

    url(_(r'^create/project/(?P<project_id>[0-9]+)/$'), interview_create, name='interview_create'),
    url(_(r'^(?P<pk>[0-9]+)/update$'), InterviewUpdateView.as_view(), name='interview_update'),
    url(_(r'^(?P<pk>[0-9]+)/delete$'), InterviewDeleteView.as_view(), name='interview_delete'),
]
