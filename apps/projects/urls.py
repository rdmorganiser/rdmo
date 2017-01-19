from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^$', projects, name='projects'),
    url(r'^export/xml/$', project_answers_export_xml, name='project_answers_export_xml'),
    url(r'^(?P<pk>[0-9]+)/$', project, name='project'),

    url(r'^create/$', ProjectCreateView.as_view(), name='project_create'),
    url(r'^(?P<pk>[0-9]+)/update/$', ProjectUpdateView.as_view(), name='project_update'),
    url(r'^(?P<pk>[0-9]+)/delete/$', ProjectDeleteView.as_view(), name='project_delete'),

    url(r'^(?P<project_id>[0-9]+)/snapshots/create/$', SnapshotCreateView.as_view(), name='snapshot_create'),
    url(r'^(?P<project_id>[0-9]+)/snapshots/(?P<pk>[0-9]+)/update/$', SnapshotUpdateView.as_view(), name='snapshot_update'),
    url(r'^(?P<project_id>[0-9]+)/snapshots/(?P<snapshot_id>[0-9]+)/rollback/$', snapshot_rollback, name='snapshot_rollback'),

    url(r'^(?P<project_id>[0-9]+)/answers/$', project_answers, name='project_answers'),
    url(r'^(?P<project_id>[0-9]+)/snapshot/(?P<snapshot_id>[0-9]+)/answers/$', project_answers, name='project_answers'),
    url(r'^(?P<project_id>[0-9]+)/answers/export/(?P<format>[a-z]+)/$', project_answers_export, name='project_answers_export'),
    url(r'^(?P<project_id>[0-9]+)/snapshot/(?P<snapshot_id>[0-9]+)/answers/export/(?P<format>[a-z]+)/$', project_answers_export, name='project_answers_export'),

    url(r'^(?P<project_id>[0-9]+)/view/(?P<view_id>[0-9]+)/$', project_view, name='project_view'),
    url(r'^(?P<project_id>[0-9]+)/snapshot/(?P<snapshot_id>[0-9]+)/view/(?P<view_id>[0-9]+)/$', project_view, name='project_view'),
    url(r'^(?P<project_id>[0-9]+)/view/(?P<view_id>[0-9]+)/export/(?P<format>[a-z]+)/$', project_view_export, name='project_view_export'),
    url(r'^(?P<project_id>[0-9]+)/snapshot/(?P<snapshot_id>[0-9]+)/view/(?P<view_id>[0-9]+)/export/(?P<format>[a-z]+)/$', project_view_export, name='project_view_export'),

    url(r'^(?P<project_id>[0-9]+)/questions/', project_questions, name='project_questions'),
]
