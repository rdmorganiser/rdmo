import logging

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, ListView
from django.urls import reverse_lazy

from rdmo.core.exports import prettify_xml
from rdmo.core.imports import handle_uploaded_file, read_xml_file
from rdmo.core.views import ModelPermissionMixin, CSRFViewMixin
from rdmo.core.utils import get_model_field_meta, render_to_format

from .imports import import_tasks
from .models import Task
from .serializers.export import TaskSerializer as ExportSerializer
from .renderers import XMLRenderer

log = logging.getLogger(__name__)


class TasksView(ModelPermissionMixin, CSRFViewMixin, TemplateView):
    template_name = 'tasks/tasks.html'
    permission_required = 'tasks.view_task'

    def get_context_data(self, **kwargs):
        context = super(TasksView, self).get_context_data(**kwargs)
        context['export_formats'] = settings.EXPORT_FORMATS
        context['meta'] = {
            'Task': get_model_field_meta(Task)
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
            xmldata = XMLRenderer().render(serializer.data)
            response = HttpResponse(prettify_xml(xmldata), content_type="application/xml")
            response['Content-Disposition'] = 'filename="tasks.xml"'
            return response
        else:
            return render_to_format(self.request, format, _('Tasks'), 'tasks/tasks_export.html', context)


class TasksImportXMLView(ModelPermissionMixin, ListView):
    permission_required = ('tasks.add_task', 'tasks.change_task', 'tasks.delete_task')
    success_url = reverse_lazy('tasks')
    parsing_error_template = 'core/import_parsing_error.html'

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.success_url)

    def post(self, request, *args, **kwargs):
        # context = self.get_context_data(**kwargs)
        try:
            request.FILES['uploaded_file']
        except KeyError:
            return HttpResponseRedirect(self.success_url)
        else:
            tempfilename = handle_uploaded_file(request.FILES['uploaded_file'])

        tree = read_xml_file(tempfilename)
        if tree is None:
            log.info('Xml parsing error. Import failed.')
            return render(request, self.parsing_error_template, status=400)
        else:
            import_tasks(tree)
            return HttpResponseRedirect(self.success_url)
