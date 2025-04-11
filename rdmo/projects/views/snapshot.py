import logging

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView

from rdmo.core.plugins import get_plugin
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

    def get_export_plugin(self):
        export_plugin = get_plugin('PROJECT_SNAPSHOT_EXPORTS', self.kwargs.get('format'))
        if export_plugin is None:
            raise Http404

        export_plugin.request = self.request
        export_plugin.snapshot = self.object

        return export_plugin

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.get_export_plugin().render()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.get_export_plugin().submit()
