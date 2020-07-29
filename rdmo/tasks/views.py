import logging

from django.conf import settings
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, TemplateView

from rdmo.core.exports import prettify_xml
from rdmo.core.utils import get_model_field_meta, render_to_format
from rdmo.core.views import CSRFViewMixin, ModelPermissionMixin

from .models import Task
from .renderers import XMLRenderer
from .serializers.export import TaskSerializer as ExportSerializer

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
