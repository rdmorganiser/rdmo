from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from rdmo.core.exports import XMLResponse
from rdmo.core.permissions import HasModelPermission
from rdmo.core.utils import render_to_csv, render_to_format
from rdmo.core.viewsets import CopyModelMixin

from .models import Attribute
from .renderers import AttributeRenderer
from .serializers.export import AttributeExportSerializer
from .serializers.v1 import (AttributeIndexSerializer, AttributeListSerializer,
                             AttributeNestedSerializer, AttributeSerializer)


class AttributeViewSet(CopyModelMixin, ModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = Attribute.objects.order_by('path') \
                        .annotate(values_count=models.Count('values')) \
                        .annotate(projects_count=models.Count('values__project', distinct=True)) \
                        .prefetch_related('conditions', 'questionsets', 'questions', 'tasks_as_start', 'tasks_as_end')

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'uri',
        'path',
        'key',
        'parent'
    )

    def get_serializer_class(self):
        return AttributeListSerializer if self.action == 'list' else AttributeSerializer

    @action(detail=False)
    def index(self, request):
        queryset = Attribute.objects.order_by('path')
        serializer = AttributeIndexSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def nested(self, request, pk):
        serializer = AttributeNestedSerializer(self.get_object(), context={'request': request})
        return Response(serializer.data)

    @action(detail=False, url_path='export(/(?P<export_format>[a-z]+))?', permission_classes=[HasModelPermission])
    def export(self, request, export_format='xml'):
        attributes = self.get_queryset()
        if export_format == 'xml':
            serializer = AttributeExportSerializer(attributes, many=True)
            xml = AttributeRenderer().render(serializer.data)
            return XMLResponse(xml, name='attributes')
        elif export_format[:3] == 'csv':
            rows = [(attribute.key, attribute.comment, attribute.uri) for attribute in attributes]
            delimiter = ',' if export_format == 'csvcomma' else ';'
            return render_to_csv('domain', rows, delimiter)
        else:
            return render_to_format(self.request, export_format, 'domain', 'domain/export/attributes.html', {
                'attributes': attributes
            })

    @action(detail=True, url_path='export(/(?P<export_format>[a-z]+))?', permission_classes=[HasModelPermission])
    def detail_export(self, request, pk=None, export_format='xml'):
        attributes = self.get_object().get_descendants(include_self=True)
        if export_format == 'xml':
            serializer = AttributeExportSerializer(attributes, many=True)
            xml = AttributeRenderer().render(serializer.data)
            return XMLResponse(xml, name=self.get_object().key)
        elif export_format[:3] == 'csv':
            rows = [(attribute.key, attribute.comment, attribute.uri) for attribute in attributes]
            delimiter = ',' if export_format == 'csvcomma' else ';'
            return render_to_csv('domain', rows, delimiter)
        else:
            return render_to_format(self.request, export_format, self.get_object().key, 'domain/export/attributes.html', {
                'attributes': attributes
            })
