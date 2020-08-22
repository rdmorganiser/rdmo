from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from rdmo.core.exports import XMLResponse
from rdmo.core.permissions import HasModelPermission
from rdmo.core.views import ChoicesViewSet
from rdmo.core.viewsets import CopyModelMixin

from .models import Condition
from .renderers import ConditionRenderer
from .serializers.export import ConditionExportSerializer
from .serializers.v1 import ConditionIndexSerializer, ConditionSerializer


class ConditionViewSet(CopyModelMixin, ModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'uri',
        'key',
        'source',
        'relation',
        'target_text',
        'target_option'
    )

    @action(detail=False)
    def index(self, request):
        queryset = self.get_queryset()
        serializer = ConditionIndexSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, permission_classes=[HasModelPermission])
    def export(self, request):
        serializer = ConditionExportSerializer(self.get_queryset(), many=True)
        xml = ConditionRenderer().render(serializer.data)
        return XMLResponse(xml, name='conditions')

    @action(detail=True, url_path='export', permission_classes=[HasModelPermission])
    def detail_export(self, request, pk=None):
        serializer = ConditionExportSerializer(self.get_object())
        xml = ConditionRenderer().render([serializer.data])
        return XMLResponse(xml, name=self.get_object().key)


class RelationViewSet(ChoicesViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Condition.RELATION_CHOICES
