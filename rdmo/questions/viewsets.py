from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from rdmo.core.constants import VALUE_TYPE_CHOICES
from rdmo.core.exports import XMLResponse
from rdmo.core.permissions import HasModelPermission
from rdmo.core.views import ChoicesViewSet
from rdmo.core.viewsets import CopyModelMixin

from .models import Catalog, Question, QuestionSet, Section
from .renderers import (CatalogRenderer, QuestionRenderer, QuestionSetRenderer,
                        SectionRenderer)
from .serializers.export import (CatalogExportSerializer,
                                 QuestionExportSerializer,
                                 QuestionSetExportSerializer,
                                 SectionExportSerializer)
from .serializers.v1 import (CatalogIndexSerializer, CatalogNestedSerializer,
                             CatalogSerializer, QuestionIndexSerializer,
                             QuestionNestedSerializer, QuestionSerializer,
                             QuestionSetIndexSerializer,
                             QuestionSetNestedSerializer,
                             QuestionSetSerializer, SectionIndexSerializer,
                             SectionNestedSerializer, SectionSerializer)


class CatalogViewSet(CopyModelMixin, ModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'uri',
        'key',
        'comment'
    )

    @action(detail=True)
    def nested(self, request, pk):
        queryset = get_object_or_404(Catalog, pk=pk)
        serializer = CatalogNestedSerializer(queryset)
        return Response(serializer.data)

    @action(detail=False)
    def index(self, request):
        serializer = CatalogIndexSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    @action(detail=False, permission_classes=[HasModelPermission])
    def export(self, request):
        serializer = CatalogExportSerializer(self.get_queryset(), many=True)
        xml = CatalogRenderer().render(serializer.data)
        return XMLResponse(xml, name='catalogs')

    @action(detail=True, url_path='export', permission_classes=[HasModelPermission])
    def detail_export(self, request, pk=None):
        serializer = CatalogExportSerializer(self.get_object())
        xml = CatalogRenderer().render([serializer.data])
        return XMLResponse(xml, name=self.get_object().key)


class SectionViewSet(CopyModelMixin, ModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'uri',
        'path',
        'key',
        'catalog',
        'comment'
    )

    @action(detail=True)
    def nested(self, request, pk):
        queryset = get_object_or_404(Section, pk=pk)
        serializer = SectionNestedSerializer(queryset)
        return Response(serializer.data)

    @action(detail=False)
    def index(self, request):
        serializer = SectionIndexSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    @action(detail=False, permission_classes=[HasModelPermission])
    def export(self, request):
        serializer = SectionExportSerializer(self.get_queryset(), many=True)
        xml = SectionRenderer().render(serializer.data)
        return XMLResponse(xml, name='sections')

    @action(detail=True, url_path='export', permission_classes=[HasModelPermission])
    def detail_export(self, request, pk=None):
        serializer = SectionExportSerializer(self.get_object())
        xml = SectionRenderer().render([serializer.data])
        return XMLResponse(xml, name=self.get_object().path)


class QuestionSetViewSet(CopyModelMixin, ModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = QuestionSet.objects.all()
    serializer_class = QuestionSetSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'attribute',
        'uri',
        'path',
        'key',
        'section',
        'comment',
        'is_collection'
    )

    @action(detail=True)
    def nested(self, request, pk):
        queryset = get_object_or_404(QuestionSet, pk=pk)
        serializer = QuestionSetNestedSerializer(queryset)
        return Response(serializer.data)

    @action(detail=False)
    def index(self, request):
        serializer = QuestionSetIndexSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    @action(detail=False, permission_classes=[HasModelPermission])
    def export(self, request):
        serializer = QuestionSetExportSerializer(self.get_queryset(), many=True)
        xml = QuestionSetRenderer().render(serializer.data)
        return XMLResponse(xml, name='questionsets')

    @action(detail=True, url_path='export', permission_classes=[HasModelPermission])
    def detail_export(self, request, pk=None):
        serializer = QuestionSetExportSerializer(self.get_object())
        xml = QuestionSetRenderer().render([serializer.data])
        return XMLResponse(xml, name=self.get_object().path)


class QuestionViewSet(CopyModelMixin, ModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'attribute',
        'uri',
        'path',
        'key',
        'questionset',
        'is_collection',
        'value_type',
        'widget_type',
        'unit',
        'comment'
    )

    @action(detail=True)
    def nested(self, request, pk):
        queryset = get_object_or_404(Question, pk=pk)
        serializer = QuestionNestedSerializer(queryset)
        return Response(serializer.data)

    @action(detail=False)
    def index(self, request):
        serializer = QuestionIndexSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    @action(detail=False, permission_classes=[HasModelPermission])
    def export(self, request):
        serializer = QuestionExportSerializer(self.get_queryset(), many=True)
        xml = QuestionRenderer().render(serializer.data)
        return XMLResponse(xml, name='questions')

    @action(detail=True, url_path='export', permission_classes=[HasModelPermission])
    def detail_export(self, request, pk=None):
        serializer = QuestionExportSerializer(self.get_object())
        xml = QuestionRenderer().render([serializer.data])
        return XMLResponse(xml, name=self.get_object().path)


class WidgetTypeViewSet(ChoicesViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Question.WIDGET_TYPE_CHOICES


class ValueTypeViewSet(ChoicesViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = VALUE_TYPE_CHOICES
