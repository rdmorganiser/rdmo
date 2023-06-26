from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter

from rdmo.core.exports import XMLResponse
from rdmo.core.permissions import HasModelPermission, HasObjectPermission
from rdmo.core.utils import render_to_format
from rdmo.core.viewsets import CopyModelMixin

from .models import View
from .renderers import ViewRenderer
from .serializers.export import ViewExportSerializer
from .serializers.v1 import (ViewIndexSerializer, ViewListSerializer,
                             ViewSerializer)


class ViewViewSet(CopyModelMixin, ModelViewSet):
    permission_classes = (HasModelPermission | HasObjectPermission, )
    queryset = View.objects.prefetch_related('catalogs', 'sites', 'editors', 'groups') \
                           .annotate(projects_count=models.Count('projects'))

    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('uri', )
    filterset_fields = (
        'uri',
        'uri_prefix',
        'key',
        'comment',
        'sites',
        'editors'
    )

    def get_serializer_class(self):
        return ViewListSerializer if self.action == 'list' else ViewSerializer

    @action(detail=False)
    def index(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = ViewIndexSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path='export(/(?P<export_format>[a-z]+))?')
    def export(self, request, export_format='xml'):
        queryset = self.filter_queryset(self.get_queryset())
        if export_format == 'xml':
            serializer = ViewExportSerializer(queryset, many=True)
            xml = ViewRenderer().render(serializer.data)
            return XMLResponse(xml, name='views')
        else:
            return render_to_format(self.request, export_format, 'views', 'views/export/views.html', {
                'views': queryset
            })

    @action(detail=True, url_path='export(/(?P<export_format>[a-z]+))?')
    def detail_export(self, request, pk=None, export_format='xml'):
        if export_format == 'xml':
            serializer = ViewExportSerializer(self.get_object())
            xml = ViewRenderer().render([serializer.data])
            return XMLResponse(xml, name=self.get_object().key)
        else:
            return render_to_format(self.request, export_format, self.get_object().key, 'views/export/views.html', {
                'views': [self.get_object()]
            })
