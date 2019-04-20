from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import list_route
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from rdmo.core.permissions import HasModelPermission

from .models import Task
from .serializers.v1 import TaskSerializer, TaskIndexSerializer


class TaskViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = (
        'uri',
        'key'
    )

    @list_route()
    def index(self, request):
        serializer = TaskIndexSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)
