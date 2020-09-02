from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from rdmo.core.exports import XMLResponse
from rdmo.core.permissions import HasModelPermission
from rdmo.core.viewsets import CopyModelMixin

from .models import Task
from .renderers import TaskRenderer
from .serializers.export import TaskExportSerializer
from .serializers.v1 import TaskIndexSerializer, TaskSerializer


class TaskViewSet(CopyModelMixin, ModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'uri',
        'key',
        'comment'
    )

    @action(detail=False)
    def index(self, request):
        serializer = TaskIndexSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    @action(detail=False, permission_classes=[HasModelPermission])
    def export(self, request):
        serializer = TaskExportSerializer(self.get_queryset(), many=True)
        xml = TaskRenderer().render(serializer.data)
        return XMLResponse(xml, name='tasks')

    @action(detail=True, url_path='export', permission_classes=[HasModelPermission])
    def detail_export(self, request, pk=None):
        serializer = TaskExportSerializer(self.get_object())
        xml = TaskRenderer().render([serializer.data])
        return XMLResponse(xml, name=self.get_object().key)
