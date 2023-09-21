from django.db import models

from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from django_filters.rest_framework import DjangoFilterBackend

from rdmo.core.exports import XMLResponse
from rdmo.core.permissions import HasModelPermission, HasObjectPermission
from rdmo.core.utils import is_truthy, render_to_format

from .models import Task
from .renderers import TaskRenderer
from .serializers.export import TaskExportSerializer
from .serializers.v1 import TaskIndexSerializer, TaskSerializer


class TaskViewSet(ModelViewSet):
    permission_classes = (HasModelPermission | HasObjectPermission, )
    serializer_class = TaskSerializer
    queryset = Task.objects.select_related('start_attribute', 'end_attribute') \
                           .prefetch_related('catalogs', 'sites', 'editors', 'groups', 'conditions') \
                           .annotate(projects_count=models.Count('projects')) \
                           .order_by('uri')

    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('uri', )
    filterset_fields = (
        'uri',
        'uri_prefix',
        'uri_path',
        'comment',
        'sites',
        'editors'
    )

    @action(detail=False)
    def index(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = TaskIndexSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path='export(/(?P<export_format>[a-z]+))?')
    def export(self, request, export_format='xml'):
        queryset = self.filter_queryset(self.get_queryset())
        if export_format == 'xml':
            serializer = TaskExportSerializer(queryset, many=True)
            xml = TaskRenderer().render(serializer.data, context=self.get_export_renderer_context(request))
            return XMLResponse(xml, name='tasks')
        else:
            return render_to_format(self.request, export_format, 'tasks', 'tasks/export/tasks.html', {
                'tasks': queryset
            })

    @action(detail=True, url_path='export(/(?P<export_format>[a-z]+))?')
    def detail_export(self, request, pk=None, export_format='xml'):
        if export_format == 'xml':
            serializer = TaskExportSerializer(self.get_object())
            xml = TaskRenderer().render([serializer.data], context=self.get_export_renderer_context(request))
            return XMLResponse(xml, name=self.get_object().uri_path)
        else:
            return render_to_format(
                self.request, export_format, self.get_object().uri_path, 'tasks/export/tasks.html', {
                    'tasks': [self.get_object()]
                }
            )

    def get_export_renderer_context(self, request):
        full = is_truthy(request.GET.get('full'))
        return {
            'conditions': full or is_truthy(request.GET.get('conditions')),
            'attributes': full or is_truthy(request.GET.get('attributes')),
            'options': full or is_truthy(request.GET.get('options'))
        }
