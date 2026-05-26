from django.db import models

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from django_filters.rest_framework import DjangoFilterBackend

from rdmo.core.exports import XMLResponse
from rdmo.core.filters import SearchFilter
from rdmo.core.permissions import HasModelPermission, HasObjectPermission
from rdmo.core.utils import is_truthy, render_to_format
from rdmo.core.views import ChoicesViewSet
from rdmo.domain.models import Attribute

from ..config.constants import PLUGIN_TYPES
from ..config.models import Plugin
from .models import Option, OptionSet
from .renderers import OptionRenderer, OptionSetRenderer
from .serializers.export import OptionExportSerializer, OptionSetExportSerializer
from .serializers.v1 import (
    OptionIndexSerializer,
    OptionSerializer,
    OptionSetIndexSerializer,
    OptionSetNestedSerializer,
    OptionSetSerializer,
)


class OptionSetViewSet(ModelViewSet):
    permission_classes = (HasModelPermission | HasObjectPermission, )
    serializer_class = OptionSetSerializer

    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('uri', )
    filterset_fields = (
        'uri',
        'uri_prefix',
        'uri_path',
        'comment'
    )

    def get_queryset(self):
        queryset = OptionSet.objects.all()
        if self.action in ['index']:
            return queryset
        elif self.action in ['nested', 'export', 'detail_export']:
            return queryset.prefetch_related(
                'optionset_options__option',
                'conditions',
            )
        else:
            return queryset.prefetch_related(
                'optionset_options__option',
                'conditions',
                'questions',
                'plugins',
                'editors',
            )

    @action(detail=False)
    def index(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = OptionSetIndexSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def nested(self, request, pk):
        serializer = OptionSetNestedSerializer(self.get_object(), context={'request': request})
        return Response(serializer.data)

    @action(detail=False, url_path='export(?:/(?P<export_format>[a-z]+))?')
    def export(self, request, export_format='xml'):
        queryset = self.filter_queryset(self.get_queryset())
        if export_format == 'xml':
            serializer = OptionSetExportSerializer(
                queryset,
                many=True,
                context=self.get_export_serializer_context(queryset),
            )
            xml = OptionSetRenderer().render(serializer.data, context=self.get_export_flags())
            return XMLResponse(xml, name='optionsets')
        else:
            return render_to_format(self.request, export_format, 'optionsets', 'options/export/optionsets.html', {
                'optionsets': queryset
            })

    @action(detail=True, url_path='export(?:/(?P<export_format>[a-z]+))?')
    def detail_export(self, request, pk=None, export_format='xml'):
        instance = self.get_object()
        if export_format == 'xml':
            serializer = OptionSetExportSerializer(
                instance,
                context=self.get_export_serializer_context([instance]),
            )
            xml = OptionSetRenderer().render([serializer.data], context=self.get_export_flags())
            return XMLResponse(xml, name=instance.uri_path)
        else:
            return render_to_format(
                self.request, export_format, instance.uri_path, 'options/export/optionsets.html', {
                    'optionsets': [instance]
                }
            )

    def get_export_flags(self):
        full = is_truthy(self.request.GET.get('full'))
        return {
            'attributes': full or is_truthy(self.request.GET.get('attributes')),
            'conditions': full or is_truthy(self.request.GET.get('conditions')),
            'options': full or is_truthy(self.request.GET.get('options')),
            'plugins': full or is_truthy(request.GET.get('plugins')),
        }

    def get_export_serializer_context(self, optionsets):
        return {
            'attribute_map': Attribute.objects.get_queryset_ancestors(
                Attribute.objects.filter(id__in={
                    condition.source_id
                    for optionset in optionsets
                    for condition in optionset.conditions.all()
                }),
                include_self=True
            ).in_bulk()
        }


class OptionViewSet(ModelViewSet):
    permission_classes = (HasModelPermission | HasObjectPermission, )
    serializer_class = OptionSerializer

    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('uri', 'text')
    filterset_fields = (
        'uri',
        'uri_prefix',
        'uri_path',
        'optionsets',
        'optionsets__uri',
        'optionsets__uri_path',
        'comment'
    )

    def get_queryset(self):
        queryset = Option.objects.all()
        if self.action in ['index']:
            return queryset
        else:
            return queryset.annotate(
                values_count=models.Count('values')
            ).annotate(
                projects_count=models.Count('values__project', distinct=True)
            ).prefetch_related(
                'optionsets',
                'conditions',
                'editors'
            )

    @action(detail=False)
    def index(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = OptionIndexSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path='export(?:/(?P<export_format>[a-z]+))?')
    def export(self, request, export_format='xml'):
        queryset = self.filter_queryset(self.get_queryset())
        if export_format == 'xml':
            serializer = OptionExportSerializer(queryset, many=True)
            xml = OptionRenderer().render(serializer.data)
            return XMLResponse(xml, name='options')
        else:
            return render_to_format(self.request, export_format, 'options', 'options/export/options.html', {
                'options': queryset
            })

    @action(detail=True, url_path='export(?:/(?P<export_format>[a-z]+))?')
    def detail_export(self, request, pk=None, export_format='xml'):
        instance = self.get_object()
        if export_format == 'xml':
            serializer = OptionExportSerializer(instance)
            xml = OptionRenderer().render([serializer.data])
            return XMLResponse(xml, name=instance.uri_path)
        else:
            return render_to_format(
                self.request, export_format, instance.uri_path, 'options/export/options.html', {
                    'options': [instance]
                }
            )


class AdditionalInputsViewSet(ChoicesViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Option.ADDITIONAL_INPUT_CHOICES


class ProviderViewSet(ChoicesViewSet):
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        providers = {}

        plugins = Plugin.objects.filter_plugins_for_project(
            plugin_type=PLUGIN_TYPES.OPTIONSET_PROVIDER,
            user=self.request.user
        )
        for plugin in plugins:
            key = plugin.url_name or plugin.uri_path
            if key:
                providers[key] = plugin.title
        return list(providers.items())
