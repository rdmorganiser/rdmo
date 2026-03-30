from django.urls import re_path

from ..views import ProjectDetailView, ProjectErrorView, ProjectInterviewView, ProjectJoinView, ProjectsView

urlpatterns = [
    re_path(r'^$',
            ProjectsView.as_view(), name='projects'),
    re_path(r'^(?P<pk>[0-9]+)/',
            ProjectDetailView.as_view(), name='project'),
    re_path(r'^join/(?P<token>.+)/$',
            ProjectJoinView.as_view(), name='project_join'),
    re_path(r'^(?P<pk>[0-9]+)/interview/',
            ProjectInterviewView.as_view(), name='project_interview'),
    re_path(r'^(?P<pk>[0-9]+)/error/',
            ProjectErrorView.as_view(), name='project_error'),
]
