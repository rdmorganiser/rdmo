from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from django_filters.rest_framework import DjangoFilterBackend

from rdmo.core.exports import XMLResponse
from rdmo.core.filters import SearchFilter
from rdmo.core.permissions import HasModelPermission, HasObjectPermission
from rdmo.core.utils import render_to_format
from rdmo.management.viewsets import ElementToggleCurrentSiteViewSetMixin

from .models import Plugin
from .renderers import PluginRenderer
from .serializers.export import PluginExportSerializer
from .serializers.v1 import PluginIndexSerializer, PluginSerializer


class PluginViewSet(ElementToggleCurrentSiteViewSetMixin, ModelViewSet):
    permission_classes = (HasModelPermission | HasObjectPermission, )
    serializer_class = PluginSerializer
    queryset = (
        Plugin
            .objects
            .prefetch_related('catalogs', 'sites', 'editors', 'groups')
            .order_by('uri')
    )

    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('uri', 'title')
    filterset_fields = (
        'uri',
        'uri_prefix',
        'uri_path',
        'comment',
        'plugin_type',
        'sites',
        'editors'
    )

    @action(detail=False)
    def index(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = PluginIndexSerializer(queryset, many=True)
        return Response(serializer.data)
    @action(detail=False, url_path='export(?:/(?P<export_format>[a-z]+))?')
    def export(self, request, export_format='xml'):
        queryset = self.filter_queryset(self.get_queryset())
        if export_format == 'xml':
            serializer = PluginExportSerializer(queryset, many=True)
            xml = PluginRenderer().render(serializer.data)
            return XMLResponse(xml, name='plugins')
        return render_to_format(self.request, export_format, 'plugins', 'config/export/plugins.html', {
            'plugins': queryset
        })

    @action(detail=True, url_path='export(?:/(?P<export_format>[a-z]+))?')
    def detail_export(self, request, pk=None, export_format='xml'):
        plugin = self.get_object()

        if export_format == 'xml':
            serializer = PluginExportSerializer(plugin)
            xml = PluginRenderer().render([serializer.data])
            return XMLResponse(xml, name=plugin.uri_path)
        return render_to_format(self.request, export_format, plugin.uri_path,
                                'config/export/plugins.html', {
                                    'plugins': [plugin]
                                })
