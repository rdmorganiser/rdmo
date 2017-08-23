from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.filters import DjangoFilterBackend
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from rdmo.core.permissions import HasModelPermission
from rdmo.conditions.models import Condition
from rdmo.domain.models import Attribute

from .models import Task, TimeFrame
from .serializers import (
    TaskSerializer,
    TimeFrameSerializer,
    TaskIndexSerializer,
    AttributeSerializer,
    ConditionSerializer
)
from .serializers.api import TaskSerializer as TaskApiSerializer


class TaskViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @list_route()
    def index(self, request):
        queryset = Task.objects.all()
        serializer = TaskIndexSerializer(queryset, many=True)
        return Response(serializer.data)


class TimeFrameViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = TimeFrame.objects.all()
    serializer_class = TimeFrameSerializer

    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('task', )


class AttributeViewSet(ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = Attribute.objects.filter(value_type='datetime')
    serializer_class = AttributeSerializer


class ConditionViewSet(ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer


class TaskApiViewSet(ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission, )
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    queryset = Task.objects.all()
    serializer_class = TaskApiSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = (
        'uri',
        'key'
    )
