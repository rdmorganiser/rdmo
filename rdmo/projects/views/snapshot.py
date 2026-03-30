import logging

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView

from rdmo.config.constants import PLUGIN_TYPES
from rdmo.config.models import Plugin
from rdmo.core.views import ObjectPermissionMixin, RedirectViewMixin

from ..forms import SnapshotCreateForm
from ..models import Project, Snapshot

logger = logging.getLogger(__name__)


class SnapshotCreateView(ObjectPermissionMixin, RedirectViewMixin, CreateView):
    model = Snapshot
    form_class = SnapshotCreateForm
    permission_required = 'projects.add_snapshot_object'

    def dispatch(self, *args, **kwargs):
        self.project = get_object_or_404(Project.objects.all(), pk=self.kwargs['project_id'])
        return super().dispatch(*args, **kwargs)

    def get_permission_object(self):
        return self.project

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.project
        return kwargs


class SnapshotUpdateView(ObjectPermissionMixin, RedirectViewMixin, UpdateView):
    model = Snapshot
    queryset = Snapshot.objects.all()
    fields = ['title', 'description']
    permission_required = 'projects.change_snapshot_object'

    def get_queryset(self):
        return Snapshot.objects.filter(project_id=self.kwargs['project_id'])

    def get_permission_object(self):
        return self.get_object().project


class SnapshotRollbackView(ObjectPermissionMixin, RedirectViewMixin, DetailView):
    model = Snapshot
    queryset = Snapshot.objects.all()
    permission_required = 'projects.rollback_snapshot_object'
    template_name = 'projects/snapshot_rollback.html'

    def get_queryset(self):
        return Snapshot.objects.filter(project_id=self.kwargs['project_id'])

    def get_permission_object(self):
        return self.get_object().project

    def post(self, request, *args, **kwargs):
        snapshot = self.get_object()

        if 'cancel' not in request.POST:
            snapshot.rollback()

        return HttpResponseRedirect(reverse('project', args=[snapshot.project.id]))


class SnapshotExportView(ObjectPermissionMixin, DetailView):
    model = Snapshot
    queryset = Snapshot.objects.all()
    permission_required = 'projects.export_snapshot_object'

    def get_queryset(self):
        return Snapshot.objects.filter(project_id=self.kwargs['project_id'])

    def get_permission_object(self):
        return self.get_object().project

    def get_plugin_by_url_name(self, url_name, project=None):
        for plugin in Plugin.objects.for_context(
            plugin_type=PLUGIN_TYPES.PROJECT_SNAPSHOT_EXPORT,
            project=project,
            user=self.request.user,
        ):
            if plugin.url_name == url_name:
                return plugin

    def get_export_plugin(self):
        plugin = self.get_plugin_by_url_name(self.kwargs.get('url_name'), self.object.project)
        if plugin:
            import_plugin = plugin.initialize_class()
            import_plugin.request = self.request
            import_plugin.snapshot = self.object

            return import_plugin

        # no plugin for this url_name found
        raise Http404

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.get_export_plugin().render()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.get_export_plugin().submit()
