from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from rdmo.core.exports import XMLResponse
from rdmo.core.permissions import HasModelPermission
from rdmo.core.utils import render_to_format
from rdmo.core.views import ChoicesViewSet
from rdmo.core.viewsets import CopyModelMixin

from .models import Condition
from .renderers import ConditionRenderer
from .serializers.export import ConditionExportSerializer
from .serializers.v1 import (ConditionIndexSerializer, ConditionListSerializer,
                             ConditionSerializer)


class ConditionViewSet(CopyModelMixin, ModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = Condition.objects.select_related('source', 'target_option') \
                                .prefetch_related('optionsets', 'pages', 'questionsets', 'questions', 'tasks')

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'uri',
        'key',
        'source',
        'relation',
        'target_text',
        'target_option'
    )

    def get_serializer_class(self):
        return ConditionListSerializer if self.action == 'list' else ConditionSerializer

    @action(detail=False)
    def index(self, request):
        queryset = Condition.objects.select_related('source', 'target_option')
        serializer = ConditionIndexSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path='export(/(?P<export_format>[a-z]+))?', permission_classes=[HasModelPermission])
    def export(self, request, export_format='xml'):
        if export_format == 'xml':
            serializer = ConditionExportSerializer(self.get_queryset(), many=True)
            xml = ConditionRenderer().render(serializer.data)
            return XMLResponse(xml, name='conditions')
        else:
            return render_to_format(self.request, export_format, 'tasks', 'conditions/export/conditions.html', {
                'conditions': self.get_queryset()
            })

    @action(detail=True, url_path='export(/(?P<export_format>[a-z]+))?', permission_classes=[HasModelPermission])
    def detail_export(self, request, pk=None, export_format='xml'):
        if export_format == 'xml':
            serializer = ConditionExportSerializer(self.get_object())
            xml = ConditionRenderer().render([serializer.data])
            return XMLResponse(xml, name=self.get_object().key)
        else:
            return render_to_format(self.request, export_format, self.get_object().key, 'conditions/export/conditions.html', {
                'conditions': [self.get_object()]
            })


class RelationViewSet(ChoicesViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Condition.RELATION_CHOICES
