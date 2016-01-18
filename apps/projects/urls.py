from django.conf.urls import url

from .views import projects, project, ProjectCreateView, ProjectUpdateView, ProjectDeleteView

urlpatterns = [
    url(r'^$', projects, name='projects'),
    url(r'^(?P<pk>[0-9]+)$', project, name='project'),
    url(r'^create$', ProjectCreateView.as_view(), name='project_create'),
    url(r'^(?P<pk>[0-9]+)/update$', ProjectUpdateView.as_view(), name='project_update'),
    url(r'^(?P<pk>[0-9]+)/delete$', ProjectDeleteView.as_view(), name='project_delete'),
]
