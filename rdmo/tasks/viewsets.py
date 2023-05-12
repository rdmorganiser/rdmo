from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from rdmo.core.exports import XMLResponse
from rdmo.core.permissions import HasModelPermission
from rdmo.core.utils import render_to_format
from rdmo.core.viewsets import CopyModelMixin

from .models import Task
from .renderers import TaskRenderer
from .serializers.export import TaskExportSerializer
from .serializers.v1 import (TaskIndexSerializer, TaskListSerializer,
                             TaskSerializer)


class TaskViewSet(CopyModelMixin, ModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = Task.objects.select_related('start_attribute', 'end_attribute') \
                           .prefetch_related('catalogs', 'sites', 'groups', 'conditions') \
                           .annotate(projects_count=models.Count('projects'))
    serializer_class = TaskSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'uri',
        'key',
        'comment'
    )

    def get_serializer_class(self):
        return TaskListSerializer if self.action == 'list' else TaskSerializer

    @action(detail=False)
    def index(self, request):
        queryset = Task.objects.select_related('start_attribute', 'end_attribute')
        serializer = TaskIndexSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path='export(/(?P<export_format>[a-z]+))?', permission_classes=[HasModelPermission])
    def export(self, request, export_format='xml'):
        if export_format == 'xml':
            serializer = TaskExportSerializer(self.get_queryset(), many=True)
            xml = TaskRenderer().render(serializer.data)
            return XMLResponse(xml, name='tasks')
        else:
            return render_to_format(self.request, export_format, 'tasks', 'tasks/export/tasks.html', {
                'tasks': self.get_queryset()
            })

    @action(detail=True, url_path='export(/(?P<export_format>[a-z]+))?', permission_classes=[HasModelPermission])
    def detail_export(self, request, pk=None, export_format='xml'):
        if export_format == 'xml':
            serializer = TaskExportSerializer(self.get_object())
            xml = TaskRenderer().render([serializer.data])
            return XMLResponse(xml, name=self.get_object().key)
        else:
            return render_to_format(self.request, export_format, self.get_object().key, 'tasks/export/tasks.html', {
                'tasks': [self.get_object()]
            })
