from django.urls import re_path

from ..views import (MembershipCreateView, MembershipDeleteView,
                     MembershipUpdateView, ProjectAnswersExportView,
                     ProjectAnswersView, ProjectCreateImportView,
                     ProjectCreateUploadView, ProjectCreateView,
                     ProjectDeleteView, ProjectDetailView, ProjectErrorView,
                     ProjectExportView, ProjectQuestionsView, ProjectsView,
                     ProjectUpdateImportView, ProjectUpdateTasksView,
                     ProjectUpdateUploadView, ProjectUpdateView,
                     ProjectUpdateViewsView, ProjectViewExportView,
                     ProjectViewView, SiteProjectsView, SnapshotCreateView,
                     SnapshotRollbackView, SnapshotUpdateView)

urlpatterns = [
    re_path(r'^$', ProjectsView.as_view(), name='projects'),
    re_path(r'^all/$', SiteProjectsView.as_view(), name='site_projects'),

    re_path(r'^create/$', ProjectCreateView.as_view(), name='project_create'),
    re_path(r'^upload/$', ProjectCreateUploadView.as_view(), name='project_create_upload'),
    re_path(r'^import/$', ProjectCreateImportView.as_view(), name='project_create_import'),
    re_path(r'^(?P<pk>[0-9]+)/$', ProjectDetailView.as_view(), name='project'),
    re_path(r'^(?P<pk>[0-9]+)/update/$', ProjectUpdateView.as_view(), name='project_update'),
    re_path(r'^(?P<pk>[0-9]+)/update/tasks/$', ProjectUpdateTasksView.as_view(), name='project_update_tasks'),
    re_path(r'^(?P<pk>[0-9]+)/update/views/$', ProjectUpdateViewsView.as_view(), name='project_update_views'),
    re_path(r'^(?P<pk>[0-9]+)/delete/$', ProjectDeleteView.as_view(), name='project_delete'),
    re_path(r'^(?P<pk>[0-9]+)/export/(?P<format>[a-z]+)/$', ProjectExportView.as_view(), name='project_export'),
    re_path(r'^(?P<pk>[0-9]+)/upload/$', ProjectUpdateUploadView.as_view(), name='project_update_upload'),
    re_path(r'^(?P<pk>[0-9]+)/import/$', ProjectUpdateImportView.as_view(), name='project_update_import'),

    re_path(r'^(?P<project_id>[0-9]+)/memberships/create$', MembershipCreateView.as_view(), name='membership_create'),
    re_path(r'^(?P<project_id>[0-9]+)/memberships/(?P<pk>[0-9]+)/update/$', MembershipUpdateView.as_view(), name='membership_update'),
    re_path(r'^(?P<project_id>[0-9]+)/memberships/(?P<pk>[0-9]+)/delete/$', MembershipDeleteView.as_view(), name='membership_delete'),

    re_path(r'^(?P<project_id>[0-9]+)/snapshots/create/$', SnapshotCreateView.as_view(), name='snapshot_create'),
    re_path(r'^(?P<project_id>[0-9]+)/snapshots/(?P<pk>[0-9]+)/update/$', SnapshotUpdateView.as_view(), name='snapshot_update'),
    re_path(r'^(?P<project_id>[0-9]+)/snapshots/(?P<pk>[0-9]+)/rollback/$', SnapshotRollbackView.as_view(), name='snapshot_rollback'),

    re_path(r'^(?P<pk>[0-9]+)/answers/$', ProjectAnswersView.as_view(), name='project_answers'),
    re_path(r'^(?P<pk>[0-9]+)/answers/export/(?P<format>[a-z]+)/$', ProjectAnswersExportView.as_view(), name='project_answers_export'),

    re_path(r'^(?P<pk>[0-9]+)/snapshots/(?P<snapshot_id>[0-9]+)/answers/$', ProjectAnswersView.as_view(), name='project_answers'),
    re_path(r'^(?P<pk>[0-9]+)/snapshots/(?P<snapshot_id>[0-9]+)/answers/export/(?P<format>[a-z]+)/$', ProjectAnswersExportView.as_view(), name='project_answers_export'),

    re_path(r'^(?P<pk>[0-9]+)/views/(?P<view_id>[0-9]+)/$', ProjectViewView.as_view(), name='project_view'),
    re_path(r'^(?P<pk>[0-9]+)/views/(?P<view_id>[0-9]+)/export/(?P<format>[a-z]+)/$', ProjectViewExportView.as_view(), name='project_view_export'),

    re_path(r'^(?P<pk>[0-9]+)/snapshots/(?P<snapshot_id>[0-9]+)/views/(?P<view_id>[0-9]+)/$', ProjectViewView.as_view(), name='project_view'),
    re_path(r'^(?P<pk>[0-9]+)/snapshots/(?P<snapshot_id>[0-9]+)/views/(?P<view_id>[0-9]+)/export/(?P<format>[a-z]+)/$', ProjectViewExportView.as_view(), name='project_view_export'),

    re_path(r'^(?P<pk>[0-9]+)/questions/', ProjectQuestionsView.as_view(), name='project_questions'),
    re_path(r'^(?P<pk>[0-9]+)/error/', ProjectErrorView.as_view(), name='project_error'),
]
