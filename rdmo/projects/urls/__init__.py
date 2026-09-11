from django.urls import re_path

from ..views import (
    IntegrationWebhookView,
    ProjectDetailView,
    ProjectErrorView,
    ProjectInterviewView,
    ProjectJoinView,
    ProjectsView,
)

urlpatterns = [
    re_path(r'^$',
            ProjectsView.as_view(), name='projects'),
    re_path(r'^(?P<pk>[0-9]+)/interview/',
            ProjectInterviewView.as_view(), name='project_interview'),
    re_path(r'^(?P<pk>[0-9]+)/error/',
            ProjectErrorView.as_view(), name='project_error'),
    re_path(r'^join/(?P<token>.+)/$',
            ProjectJoinView.as_view(), name='project_join'),
    re_path(r'^(?P<project_id>[0-9]+)/integrations/(?P<pk>[0-9]+)/webhook/$',
            IntegrationWebhookView.as_view(), name='integration_webhook'),

    # ProjectDetailView needs to come last, since it catches all routes
    re_path(r'^(?P<pk>[0-9]+)/',
            ProjectDetailView.as_view(), name='project'),
]
