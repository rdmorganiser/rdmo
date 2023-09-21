import logging

from django.conf import settings
from django.http import Http404
from django.template import TemplateSyntaxError
from django.views.generic import DetailView

from rdmo.core.constants import VALUE_TYPE_FILE
from rdmo.core.utils import render_to_format
from rdmo.core.views import ObjectPermissionMixin
from rdmo.views.models import View

from ..models import Project, Snapshot
from ..utils import get_value_path

logger = logging.getLogger(__name__)


class ProjectViewView(ObjectPermissionMixin, DetailView):
    model = Project
    queryset = Project.objects.all()
    permission_required = 'projects.view_project_object'
    template_name = 'projects/project_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # prefetch most elements of the catalog
        context['project'].catalog.prefetch_elements()

        try:
            context['current_snapshot'] = context['project'].snapshots.get(pk=self.kwargs.get('snapshot_id'))
        except Snapshot.DoesNotExist:
            context['current_snapshot'] = None

        try:
            context['view'] = context['project'].views.get(pk=self.kwargs.get('view_id'))
        except View.DoesNotExist as e:
            raise Http404 from e

        try:
            context['rendered_view'] = context['view'].render(context['project'],
                                                              snapshot=context['current_snapshot'])
        except TemplateSyntaxError:
            context['rendered_view'] = None

        # collect values with files, remove double files and order them.
        context['attachments'] = context['project'].values.filter(snapshot=context['current_snapshot']) \
                                                          .filter(value_type=VALUE_TYPE_FILE) \
                                                          .order_by('file')

        context.update({
            'snapshots': list(context['project'].snapshots.values('id', 'title')),
            'export_formats': settings.EXPORT_FORMATS
        })

        return context


class ProjectViewExportView(ObjectPermissionMixin, DetailView):
    model = Project
    queryset = Project.objects.all()
    permission_required = 'projects.view_project_object'

    def get_context_data(self, **kwargs):
        export_format = self.kwargs.get('format')

        context = super().get_context_data(**kwargs)

        # prefetch most elements of the catalog
        context['project'].catalog.prefetch_elements()

        try:
            context['current_snapshot'] = context['project'].snapshots.get(pk=self.kwargs.get('snapshot_id'))
        except Snapshot.DoesNotExist:
            context['current_snapshot'] = None

        try:
            context['view'] = context['project'].views.get(pk=self.kwargs.get('view_id'))
        except View.DoesNotExist as e:
            raise Http404 from e

        try:
            context['rendered_view'] = context['view'].render(context['project'],
                                                              snapshot=context['current_snapshot'],
                                                              export_format=export_format)
        except TemplateSyntaxError:
            context['rendered_view'] = None

        context.update({
            'title': context['project'].title,
            'format': export_format,
            'resource_path': get_value_path(context['project'], context['current_snapshot'])
        })

        return context

    def render_to_response(self, context, **response_kwargs):
        return render_to_format(self.request, context['format'], context['title'],
                                'projects/project_view_export.html', context)
