from django.conf.urls import url, include

from rest_framework import routers

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
from .viewsets import (
    ProjectViewSet,
    ValueViewSet,
    QuestionEntityViewSet,
    CatalogViewSet,
    ProjectApiViewSet,
    SnapshotApiViewSet,
    ValueApiViewSet
)

# regular views

projects_patterns = [
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

# internal AJAX API

internal_router = routers.DefaultRouter()
internal_router.register(r'projects', ProjectViewSet, base_name='project')
internal_router.register(r'values', ValueViewSet, base_name='value')
internal_router.register(r'entities', QuestionEntityViewSet, base_name='entity')
internal_router.register(r'catalogs', CatalogViewSet, base_name='catalog')

projects_patterns_internal = [
    url(r'^', include(internal_router.urls)),
]

# programmable API

api_router = routers.DefaultRouter()
api_router.register(r'projects', ProjectApiViewSet, base_name='project')
api_router.register(r'snapshots', SnapshotApiViewSet, base_name='snapshot')
api_router.register(r'values', ValueApiViewSet, base_name='value')

projects_patterns_api = [
    url(r'^', include(api_router.urls)),
]
