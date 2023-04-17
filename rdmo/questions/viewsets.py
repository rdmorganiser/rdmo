from django.db import models
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

from .models import Catalog, Page, Question, QuestionSet, Section
from .renderers import (CatalogRenderer, PageRenderer, QuestionRenderer,
                        QuestionSetRenderer, SectionRenderer)
from .serializers.export import (CatalogExportSerializer, PageExportSerializer,
                                 QuestionExportSerializer,
                                 QuestionSetExportSerializer,
                                 SectionExportSerializer)
from .serializers.v1 import (CatalogIndexSerializer, CatalogListSerializer,
                             CatalogNestedSerializer, CatalogSerializer,
                             PageIndexSerializer, PageListSerializer,
                             PageNestedSerializer, PageSerializer,
                             QuestionIndexSerializer, QuestionListSerializer,
                             QuestionSerializer, QuestionSetIndexSerializer,
                             QuestionSetListSerializer,
                             QuestionSetNestedSerializer,
                             QuestionSetSerializer, SectionIndexSerializer,
                             SectionListSerializer, SectionNestedSerializer,
                             SectionSerializer)
from .utils import get_widget_type_choices


class CatalogViewSet(CopyModelMixin, ModelViewSet):
    permission_classes = (HasModelPermission, )

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'uri',
        'uri_prefix',
        'uri_path',
        'comment',
        'sites'
    )

    def get_queryset(self):
        queryset = Catalog.objects.annotate(projects_count=models.Count('projects'))
        if self.action in ('nested', 'export', 'detail_export'):
            return queryset.prefetch_elements()
        else:
            return queryset.prefetch_related('sites', 'groups', 'catalog_sections__section')

    def get_serializer_class(self):
        return CatalogListSerializer if self.action == 'list' else CatalogSerializer

    @action(detail=True)
    def nested(self, request, pk):
        serializer = CatalogNestedSerializer(self.get_object(), context={'request': request})
        return Response(serializer.data)

    @action(detail=False)
    def index(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = CatalogIndexSerializer(queryset, many=True)
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
        return XMLResponse(xml, name=self.get_object().uri_path)


class SectionViewSet(CopyModelMixin, ModelViewSet):
    permission_classes = (HasModelPermission, )

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'uri',
        'uri_prefix',
        'uri_path',
        'comment'
    )

    def get_queryset(self):
        queryset = Section.objects.all()
        if self.action in ('nested', 'export', 'detail_export'):
            return queryset.prefetch_elements()
        else:
            return queryset.prefetch_related('catalogs', 'section_pages__page')

    def get_serializer_class(self):
        return SectionListSerializer if self.action == 'list' else SectionSerializer

    @action(detail=True)
    def nested(self, request, pk):
        serializer = SectionNestedSerializer(self.get_object(), context={'request': request})
        return Response(serializer.data)

    @action(detail=False)
    def index(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = SectionIndexSerializer(queryset, many=True)
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
        return XMLResponse(xml, name=self.get_object().uri_path)


class PageViewSet(CopyModelMixin, ModelViewSet):
    permission_classes = (HasModelPermission, )

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'attribute',
        'uri',
        'uri_prefix',
        'uri_path',
        'comment',
        'is_collection'
    )

    def get_queryset(self):
        queryset = Page.objects.all()
        if self.action in ['nested', 'export', 'detail_export']:
            return queryset.prefetch_elements().select_related('attribute')
        else:
            return queryset.prefetch_related(
                'conditions',
                'sections',
                'page_questionsets__questionset',
                'page_questions__question'
            ).select_related('attribute')

    def get_serializer_class(self):
        return PageListSerializer if self.action == 'list' else PageSerializer

    @action(detail=True)
    def nested(self, request, pk):
        serializer = PageNestedSerializer(self.get_object(), context={'request': request})
        return Response(serializer.data)

    @action(detail=False)
    def index(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = PageIndexSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, permission_classes=[HasModelPermission])
    def export(self, request):
        serializer = PageExportSerializer(self.get_queryset(), many=True)
        xml = PageRenderer().render(serializer.data)
        return XMLResponse(xml, name='pages')

    @action(detail=True, url_path='export', permission_classes=[HasModelPermission])
    def detail_export(self, request, pk=None):
        serializer = PageExportSerializer(self.get_object())
        xml = PageRenderer().render([serializer.data])
        return XMLResponse(xml, name=self.get_object().uri_path)


class QuestionSetViewSet(CopyModelMixin, ModelViewSet):
    permission_classes = (HasModelPermission, )

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'attribute',
        'uri',
        'uri_prefix',
        'uri_path',
        'comment',
        'is_collection'
    )

    def get_serializer_class(self):
        return QuestionSetListSerializer if self.action == 'list' else QuestionSetSerializer

    def get_queryset(self):
        queryset = QuestionSet.objects.all()
        if self.action in ('nested', 'export', 'detail_export'):
            return queryset.prefetch_elements().select_related('attribute')
        else:
            return queryset.prefetch_related(
                'conditions',
                'pages',
                'parents',
                'questionset_questionsets__questionset',
                'questionset_questions__question'
            ).select_related('attribute')

    @action(detail=True)
    def nested(self, request, pk):
        serializer = QuestionSetNestedSerializer(self.get_object(), context={'request': request})
        return Response(serializer.data)

    @action(detail=False)
    def index(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = QuestionSetIndexSerializer(queryset, many=True)
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
        return XMLResponse(xml, name=self.get_object().uri_path)


class QuestionViewSet(CopyModelMixin, ModelViewSet):
    permission_classes = (HasModelPermission, )

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'attribute',
        'uri',
        'uri_prefix',
        'uri_path',
        'is_collection',
        'value_type',
        'widget_type',
        'unit',
        'comment'
    )

    def get_serializer_class(self):
        return QuestionListSerializer if self.action == 'list' else QuestionSerializer

    def get_queryset(self):
        queryset = Question.objects.all()
        if self.action in ('nested', 'export', 'detail_export'):
            return queryset.prefetch_elements().select_related('attribute')
        else:
            return queryset.prefetch_related(
                'conditions',
                'optionsets',
                'pages',
                'questionsets'
            ).select_related('attribute')

    @action(detail=False)
    def index(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = QuestionIndexSerializer(queryset, many=True)
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
        return XMLResponse(xml, name=self.get_object().uri_path)


class WidgetTypeViewSet(ChoicesViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = get_widget_type_choices()


class ValueTypeViewSet(ChoicesViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = VALUE_TYPE_CHOICES
