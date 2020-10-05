import logging

from django.conf import settings
from django.shortcuts import redirect
from django.views.generic import DetailView

from rdmo.core.utils import render_to_format
from rdmo.core.views import ObjectPermissionMixin

from ..models import Project, Snapshot
from ..utils import get_answers_tree

logger = logging.getLogger(__name__)


class ProjectAnswersView(ObjectPermissionMixin, DetailView):
    model = Project
    queryset = Project.objects.all()
    permission_required = 'projects.view_project_object'
    template_name = 'projects/project_answers.html'
    no_catalog_error_template = 'projects/project_error_no_catalog.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.catalog is None:
            return redirect('project_error', pk=self.object.pk)
        else:
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(ProjectAnswersView, self).get_context_data(**kwargs)

        try:
            current_snapshot = context['project'].snapshots.get(pk=self.kwargs.get('snapshot_id'))
        except Snapshot.DoesNotExist:
            current_snapshot = None

        context.update({
            'current_snapshot': current_snapshot,
            'snapshots': list(context['project'].snapshots.values('id', 'title')),
            'answers_tree': get_answers_tree(context['project'], current_snapshot),
            'export_formats': settings.EXPORT_FORMATS
        })

        return context


class ProjectAnswersExportView(ObjectPermissionMixin, DetailView):
    model = Project
    queryset = Project.objects.all()
    permission_required = 'projects.view_project_object'

    def get_context_data(self, **kwargs):
        context = super(ProjectAnswersExportView, self).get_context_data(**kwargs)

        try:
            current_snapshot = context['project'].snapshots.get(pk=self.kwargs.get('snapshot_id'))
        except Snapshot.DoesNotExist:
            current_snapshot = None

        context.update({
            'format': self.kwargs.get('format'),
            'title': context['project'].title,
            'answers_tree': get_answers_tree(context['project'], current_snapshot)
        })
        return context

    def render_to_response(self, context, **response_kwargs):
        return render_to_format(self.request, context['format'], context['title'], 'projects/project_answers_export.html', context)
