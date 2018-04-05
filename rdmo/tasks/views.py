import logging

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, ListView

from rdmo.core.imports import handle_uploaded_file, validate_xml
from rdmo.core.views import ModelPermissionMixin
from rdmo.core.utils import get_model_field_meta, render_to_format

from .imports import import_tasks
from .models import Task, TimeFrame
from .serializers.export import TaskSerializer as ExportSerializer
from .renderers import XMLRenderer

log = logging.getLogger(__name__)


class TasksView(ModelPermissionMixin, TemplateView):
    template_name = 'tasks/tasks.html'
    permission_required = 'tasks.view_task'

    def get_context_data(self, **kwargs):
        context = super(TasksView, self).get_context_data(**kwargs)
        context['export_formats'] = settings.EXPORT_FORMATS
        context['meta'] = {
            'Task': get_model_field_meta(Task),
            'TimeFrame': get_model_field_meta(TimeFrame)
        }
        return context


class TasksExportView(ModelPermissionMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    permission_required = 'tasks.view_task'

    def render_to_response(self, context, **response_kwargs):
        format = self.kwargs.get('format')
        if format == 'xml':
            serializer = ExportSerializer(context['tasks'], many=True)
            response = HttpResponse(XMLRenderer().render(serializer.data), content_type="application/xml")
            response['Content-Disposition'] = 'filename="tasks.xml"'
            return response
        else:
            return render_to_format(self.request, format, _('Tasks'), 'tasks/tasks_export.html', context)


class TasksImportXMLView(ModelPermissionMixin, ListView):
    permission_required = 'projects.export_project_object'
    success_url = '/tasks'
    parsing_error_url = 'core/import_parsing_error.html'
    template_name = 'tasks/file_upload.html'

    def post(self, request, *args, **kwargs):
        # context = self.get_context_data(**kwargs)
        tempfilename = handle_uploaded_file(request.FILES['uploaded_file'])
        roottag, xmltree = validate_xml(tempfilename)
        if roottag == 'tasks':
            import_tasks(xmltree)
            return HttpResponseRedirect(self.success_url)
        else:
            log.info('Xml parsing error. Import failed.')
            return render(request, self.parsing_error_url, status=400)
