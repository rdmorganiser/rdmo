from django.conf import settings
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, ListView

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import list_route
from rest_framework.response import Response

from apps.core.views import ModelPermissionMixin
from apps.core.utils import render_to_format
from apps.core.permissions import HasModelPermission
from apps.conditions.models import Condition
from apps.domain.models import Attribute

from .models import Task
from .serializers import (
    TaskSerializer,
    TaskIndexSerializer,
    AttributeSerializer,
    ConditionSerializer,
    ExportSerializer
)
from .renderers import XMLRenderer


class TasksView(ModelPermissionMixin, TemplateView):
    template_name = 'tasks/tasks.html'
    permission_required = 'tasks.view_task'

    def get_context_data(self, **kwargs):
        context = super(TasksView, self).get_context_data(**kwargs)
        context['export_formats'] = settings.EXPORT_FORMATS
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


class TaskViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @list_route()
    def index(self, request):
        queryset = Task.objects.all()
        serializer = TaskIndexSerializer(queryset, many=True)
        return Response(serializer.data)


class AttributeViewSet(ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = Attribute.objects.filter(value_type='datetime')
    serializer_class = AttributeSerializer


class ConditionViewSet(ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer
