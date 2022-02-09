from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from rdmo.core.exports import XMLResponse
from rdmo.core.permissions import HasModelPermission
from rdmo.core.viewsets import CopyModelMixin

from .models import Attribute
from .renderers import AttributeRenderer
from .serializers.export import AttributeExportSerializer
from .serializers.v1 import (AttributeIndexSerializer,
                             AttributeNestedSerializer, AttributeSerializer)


class AttributeViewSet(CopyModelMixin, ModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = Attribute.objects.order_by('path') \
                        .annotate(values_count=models.Count('values')) \
                        .annotate(projects_count=models.Count('values__project', distinct=True)) \
                        .prefetch_related('conditions', 'questionsets', 'questions', 'tasks_as_start', 'tasks_as_end')

    serializer_class = AttributeSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'uri',
        'path',
        'key',
        'parent'
    )

    @action(detail=False)
    def nested(self, request):
        queryset = Attribute.objects.get_cached_trees()
        serializer = AttributeNestedSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def index(self, request):
        queryset = Attribute.objects.order_by('path')
        serializer = AttributeIndexSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, permission_classes=[HasModelPermission])
    def export(self, request):
        serializer = AttributeExportSerializer(self.get_queryset(), many=True)
        xml = AttributeRenderer().render(serializer.data)
        return XMLResponse(xml, name='attributes')

    @action(detail=True, url_path='export', permission_classes=[HasModelPermission])
    def detail_export(self, request, pk=None):
        queryset = self.get_object().get_descendants(include_self=True)
        serializer = AttributeExportSerializer(queryset, many=True)
        xml = AttributeRenderer().render(serializer.data)
        return XMLResponse(xml, name=self.get_object().key)
