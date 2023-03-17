from django.conf import settings
from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from rdmo.core.exports import XMLResponse
from rdmo.core.permissions import HasModelPermission
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
    permission_classes = (HasModelPermission, )
    queryset = OptionSet.objects.prefetch_related(
        'optionset_options__option',
        'conditions',
        'questions'
    )
    serializer_class = OptionSetSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'uri',
        'uri_prefix',
        'uri_path',
        'comment'
    )

    def get_serializer_class(self):
        return OptionSetListSerializer if self.action == 'list' else OptionSetSerializer

    @action(detail=False)
    def index(self, request):
        queryset = OptionSet.objects.prefetch_related('options')
        serializer = OptionSetIndexSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def nested(self, request, pk):
        serializer = OptionSetNestedSerializer(self.get_object(), context={'request': request})
        return Response(serializer.data)

    @action(detail=False, permission_classes=[HasModelPermission])
    def export(self, request):
        serializer = OptionSetExportSerializer(self.get_queryset(), many=True)
        xml = OptionSetRenderer().render(serializer.data)
        return XMLResponse(xml, name='optionsets')

    @action(detail=True, url_path='export', permission_classes=[HasModelPermission])
    def detail_export(self, request, pk=None):
        serializer = OptionSetExportSerializer(self.get_object())
        xml = OptionSetRenderer().render([serializer.data])
        return XMLResponse(xml, name=self.get_object().uri_path)


class OptionViewSet(CopyModelMixin, ModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = Option.objects.annotate(values_count=models.Count('values')) \
                             .annotate(projects_count=models.Count('values__project', distinct=True)) \
                             .prefetch_related('option_optionsets__optionset')
    serializer_class = OptionSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'uri',
        'uri_prefix',
        'uri_path',
        'optionsets',
        'optionsets__uri',
        'optionsets__uri_path',
        'comment'
    )

    @action(detail=False)
    def index(self, request):
        queryset = Option.objects.prefetch_related('optionsets')
        serializer = OptionIndexSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, permission_classes=[HasModelPermission])
    def export(self, request):
        serializer = OptionExportSerializer(self.get_queryset(), many=True)
        xml = OptionRenderer().render(serializer.data)
        return XMLResponse(xml, name='options')

    @action(detail=True, url_path='export', permission_classes=[HasModelPermission])
    def detail_export(self, request, pk=None):
        serializer = OptionExportSerializer(self.get_object())
        xml = OptionRenderer().render([serializer.data])
        return XMLResponse(xml, name=self.get_object().uri_path)


class ProviderViewSet(ChoicesViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = settings.OPTIONSET_PROVIDERS
