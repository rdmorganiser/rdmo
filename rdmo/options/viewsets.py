from django.conf import settings
from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from rdmo.core.exports import XMLResponse
from rdmo.core.permissions import HasModelPermission, HasObjectPermission
from rdmo.core.utils import render_to_format
from rdmo.core.views import ChoicesViewSet
from rdmo.core.viewsets import CopyModelMixin

from .models import Option, OptionSet
from .renderers import OptionRenderer, OptionSetRenderer
from .serializers.export import (OptionExportSerializer,
                                 OptionSetExportSerializer)
from .serializers.v1 import (OptionIndexSerializer, OptionSerializer,
                             OptionSetIndexSerializer, OptionSetListSerializer,
                             OptionSetNestedSerializer, OptionSetSerializer)


class OptionSetViewSet(CopyModelMixin, ModelViewSet):
    permission_classes = (HasModelPermission | HasObjectPermission, )
    queryset = OptionSet.objects.prefetch_related(
        'optionset_options__option',
        'conditions',
        'questions'
    )
    serializer_class = OptionSetSerializer

    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('uri', )
    filterset_fields = (
        'uri',
        'uri_prefix',
        'uri_path',
        'comment'
    )

    def get_serializer_class(self):
        return OptionSetListSerializer if self.action == 'list' else OptionSetSerializer

    @action(detail=False, permission_classes=[HasModelPermission | HasObjectPermission, ])
    def index(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = OptionSetIndexSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, permission_classes=[HasModelPermission | HasObjectPermission, ])
    def nested(self, request, pk):
        serializer = OptionSetNestedSerializer(self.get_object(), context={'request': request})
        return Response(serializer.data)

    @action(detail=False, url_path='export(/(?P<export_format>[a-z]+))?', permission_classes=[HasModelPermission | HasObjectPermission,])
    def export(self, request, export_format='xml'):
        queryset = self.filter_queryset(self.get_queryset())
        if export_format == 'xml':
            serializer = OptionSetExportSerializer(queryset, many=True)
            xml = OptionSetRenderer().render(serializer.data)
            return XMLResponse(xml, name='optionsets')
        else:
            return render_to_format(self.request, export_format, 'optionsets', 'options/export/optionsets.html', {
                'optionsets': queryset
            })

    @action(detail=True, url_path='export(/(?P<export_format>[a-z]+))?', permission_classes=[HasModelPermission | HasObjectPermission,])
    def detail_export(self, request, pk=None, export_format='xml'):
        if export_format == 'xml':
            serializer = OptionSetExportSerializer(self.get_object())
            xml = OptionSetRenderer().render([serializer.data])
            return XMLResponse(xml, name=self.get_object().uri_path)
        else:
            return render_to_format(self.request, export_format, self.get_object().uri_path, 'options/export/optionsets.html', {
                'optionsets': [self.get_object()]
            })


class OptionViewSet(CopyModelMixin, ModelViewSet):
    permission_classes = (HasModelPermission | HasObjectPermission, )
    queryset = Option.objects.annotate(values_count=models.Count('values')) \
                             .annotate(projects_count=models.Count('values__project', distinct=True)) \
                             .prefetch_related('optionsets', 'conditions')
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

    @action(detail=False, permission_classes=[HasModelPermission | HasObjectPermission, ])
    def index(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = OptionIndexSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path='export(/(?P<export_format>[a-z]+))?', permission_classes=[HasModelPermission | HasObjectPermission,])
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

    @action(detail=True, url_path='export(/(?P<export_format>[a-z]+))?', permission_classes=[HasModelPermission | HasObjectPermission,])
    def detail_export(self, request, pk=None, export_format='xml'):
        if export_format == 'xml':
            serializer = OptionExportSerializer(self.get_object())
            xml = OptionRenderer().render([serializer.data])
            return XMLResponse(xml, name=self.get_object().uri_path)
        else:
            return render_to_format(self.request, export_format, self.get_object().uri_path, 'options/export/options.html', {
                'options': [self.get_object()]
            })


class ProviderViewSet(ChoicesViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = settings.OPTIONSET_PROVIDERS
