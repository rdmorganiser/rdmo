from django.conf.urls import url

from .views import (
    ProjectsView,
    ProjectExportXMLView,
    ProjectCreateView,
    ProjectDetailView,
    ProjectUpdateView,
    ProjectDeleteView,
    MembershipCreateView,
    MembershipUpdateView,
    MembershipDeleteView,
    SnapshotCreateView,
    SnapshotUpdateView,
    SnapshotRollbackView,
    ProjectAnswersView,
    ProjectAnswersExportView,
    ProjectViewView,
    ProjectViewExportView,
    ProjectQuestionsView
)

urlpatterns = [
    url(r'^$', ProjectsView.as_view(), name='projects'),
    url(r'^(?P<pk>[0-9]+)/export/xml/$', ProjectExportXMLView.as_view(), name='project_export_xml'),

    url(r'^create/$', ProjectCreateView.as_view(), name='project_create'),
    url(r'^(?P<pk>[0-9]+)/$', ProjectDetailView.as_view(), name='project'),
    url(r'^(?P<pk>[0-9]+)/update/$', ProjectUpdateView.as_view(), name='project_update'),
    url(r'^(?P<pk>[0-9]+)/delete/$', ProjectDeleteView.as_view(), name='project_delete'),

    url(r'^(?P<project_id>[0-9]+)/memberships/create$', MembershipCreateView.as_view(), name='membership_create'),
    url(r'^(?P<project_id>[0-9]+)/memberships/(?P<pk>[0-9]+)/update/$', MembershipUpdateView.as_view(), name='membership_update'),
    url(r'^(?P<project_id>[0-9]+)/memberships/(?P<pk>[0-9]+)/delete/$', MembershipDeleteView.as_view(), name='membership_delete'),

    url(r'^(?P<project_id>[0-9]+)/snapshots/create/$', SnapshotCreateView.as_view(), name='snapshot_create'),
    url(r'^(?P<project_id>[0-9]+)/snapshots/(?P<pk>[0-9]+)/update/$', SnapshotUpdateView.as_view(), name='snapshot_update'),
    url(r'^(?P<project_id>[0-9]+)/snapshots/(?P<pk>[0-9]+)/rollback/$', SnapshotRollbackView.as_view(), name='snapshot_rollback'),

    url(r'^(?P<pk>[0-9]+)/answers/$', ProjectAnswersView.as_view(), name='project_answers'),
    url(r'^(?P<pk>[0-9]+)/answers/export/(?P<format>[a-z]+)/$', ProjectAnswersExportView.as_view(), name='project_answers_export'),

    url(r'^(?P<pk>[0-9]+)/snapshots/(?P<snapshot_id>[0-9]+)/answers/$', ProjectAnswersView.as_view(), name='project_answers'),
    url(r'^(?P<pk>[0-9]+)/snapshots/(?P<snapshot_id>[0-9]+)/answers/export/(?P<format>[a-z]+)/$', ProjectAnswersExportView.as_view(), name='project_answers_export'),

    url(r'^(?P<pk>[0-9]+)/views/(?P<view_id>[0-9]+)/$', ProjectViewView.as_view(), name='project_view'),
    url(r'^(?P<pk>[0-9]+)/views/(?P<view_id>[0-9]+)/export/(?P<format>[a-z]+)/$', ProjectViewExportView.as_view(), name='project_view_export'),

    url(r'^(?P<pk>[0-9]+)/snapshots/(?P<snapshot_id>[0-9]+)/views/(?P<view_id>[0-9]+)/$', ProjectViewView.as_view(), name='project_view'),
    url(r'^(?P<pk>[0-9]+)/snapshots/(?P<snapshot_id>[0-9]+)/views/(?P<view_id>[0-9]+)/export/(?P<format>[a-z]+)/$', ProjectViewExportView.as_view(), name='project_view_export'),

    url(r'^(?P<pk>[0-9]+)/questions/', ProjectQuestionsView.as_view(), name='project_questions'),
]
