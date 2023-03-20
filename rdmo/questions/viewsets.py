from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from rdmo.core.constants import VALUE_TYPE_CHOICES
from rdmo.core.exports import XMLResponse
from rdmo.core.permissions import HasModelPermission, HasObjectPermission
from rdmo.core.utils import render_to_format
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
    permission_classes = (HasModelPermission | HasObjectPermission,)
    serializer_class = CatalogSerializer

    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('uri', 'title')
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

    @action(detail=True, permission_classes=[HasModelPermission | HasObjectPermission, ])
    def nested(self, request, pk):
        serializer = CatalogNestedSerializer(self.get_object(), context={'request': request})
        return Response(serializer.data)

    @action(detail=False, permission_classes=[HasModelPermission | HasObjectPermission, ])
    def index(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = CatalogIndexSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, url_path='export(/(?P<export_format>[a-z]+))?', permission_classes=[HasModelPermission  | HasObjectPermission, ])
    def export(self, request, export_format='xml'):
        queryset = self.filter_queryset(self.get_queryset())
        if export_format == 'xml':
            serializer = CatalogExportSerializer(queryset, many=True)
            xml = CatalogRenderer().render(serializer.data)
            return XMLResponse(xml, name='catalogs')
        else:
            return render_to_format(self.request, export_format, 'questions', 'questions/export/catalogs.html', {
                'catalogs': queryset
            })

    @action(detail=True, url_path='export(/(?P<export_format>[a-z]+))?', permission_classes=[HasModelPermission | HasObjectPermission, ])
    def detail_export(self, request, pk=None, export_format='xml'):
        if export_format == 'xml':
            serializer = CatalogExportSerializer(self.get_object())
            xml = CatalogRenderer().render([serializer.data])
            return XMLResponse(xml, name=self.get_object().uri_path)
        else:
            return render_to_format(self.request, export_format, self.get_object().uri_path, 'questions/export/catalogs.html', {
                'catalogs': [self.get_object()]
            })


class SectionViewSet(CopyModelMixin, ModelViewSet):
    permission_classes = (HasModelPermission | HasObjectPermission, )
    serializer_class = SectionSerializer

    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('uri', 'title')
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

    @action(detail=True, permission_classes=[HasModelPermission | HasObjectPermission, ])
    def nested(self, request, pk):
        serializer = SectionNestedSerializer(self.get_object(), context={'request': request})
        return Response(serializer.data)

    @action(detail=False, permission_classes=[HasModelPermission | HasObjectPermission, ])
    def index(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = SectionIndexSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path='export(/(?P<export_format>[a-z]+))?', permission_classes=[HasModelPermission | HasObjectPermission, ])
    def export(self, request, export_format='xml'):
        queryset = self.filter_queryset(self.get_queryset())
        if export_format == 'xml':
            serializer = SectionExportSerializer(queryset, many=True)
            xml = SectionRenderer().render(serializer.data)
            return XMLResponse(xml, name='sections')
        else:
            return render_to_format(self.request, export_format, 'questions', 'questions/export/sections.html', {
                'sections': queryset
            })

    @action(detail=True, url_path='export(/(?P<export_format>[a-z]+))?', permission_classes=[HasModelPermission | HasObjectPermission, ])
    def detail_export(self, request, pk=None, export_format='xml'):
        if export_format == 'xml':
            serializer = SectionExportSerializer(self.get_object())
            xml = SectionRenderer().render([serializer.data])
            return XMLResponse(xml, name=self.get_object().uri_path)
        else:
            return render_to_format(self.request, export_format, self.get_object().uri_path, 'questions/export/sections.html', {
                'sections': [self.get_object()]
            })


class PageViewSet(CopyModelMixin, ModelViewSet):
    permission_classes = (HasModelPermission | HasObjectPermission, )

    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('uri', 'title')
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

    @action(detail=True, permission_classes=[HasModelPermission | HasObjectPermission, ])
    def nested(self, request, pk):
        serializer = PageNestedSerializer(self.get_object(), context={'request': request})
        return Response(serializer.data)

    @action(detail=False, permission_classes=[HasModelPermission | HasObjectPermission, ])
    def index(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = PageIndexSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path='export(/(?P<export_format>[a-z]+))?', permission_classes=[HasModelPermission | HasObjectPermission, ])
    def export(self, request, export_format='xml'):
        queryset = self.filter_queryset(self.get_queryset())
        if export_format == 'xml':
            serializer = PageExportSerializer(queryset, many=True)
            xml = PageRenderer().render(serializer.data)
            return XMLResponse(xml, name='pages')
        else:
            return render_to_format(self.request, export_format, 'questions', 'questions/export/pages.html', {
                'pages': queryset
            })

    @action(detail=True, url_path='export(/(?P<export_format>[a-z]+))?', permission_classes=[HasModelPermission | HasObjectPermission, ])
    def detail_export(self, request, pk=None, export_format='xml'):
        if export_format == 'xml':
            serializer = PageExportSerializer(self.get_object())
            xml = PageRenderer().render([serializer.data])
            return XMLResponse(xml, name=self.get_object().uri_path)
        else:
            return render_to_format(self.request, export_format, self.get_object().uri_path, 'questions/export/pages.html', {
                'pages': [self.get_object()]
            })


class QuestionSetViewSet(CopyModelMixin, ModelViewSet):
    permission_classes = (HasModelPermission | HasObjectPermission, )
    serializer_class = QuestionSetSerializer

    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('uri', 'title')
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

    @action(detail=True, permission_classes=[HasModelPermission | HasObjectPermission, ])
    def nested(self, request, pk):
        serializer = QuestionSetNestedSerializer(self.get_object(), context={'request': request})
        return Response(serializer.data)

    @action(detail=False, permission_classes=[HasModelPermission | HasObjectPermission, ])
    def index(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = QuestionSetIndexSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, url_path='export(/(?P<export_format>[a-z]+))?', permission_classes=[HasModelPermission | HasObjectPermission, ])
    def export(self, request, export_format='xml'):
        queryset = self.filter_queryset(self.get_queryset())
        if export_format == 'xml':
            serializer = QuestionSetExportSerializer(queryset, many=True)
            xml = QuestionSetRenderer().render(serializer.data)
            return XMLResponse(xml, name='questionsets')
        else:
            return render_to_format(self.request, export_format, 'questionsets', 'questions/export/questionsets.html', {
                'questionsets': queryset
            })

    @action(detail=True, url_path='export(/(?P<export_format>[a-z]+))?', permission_classes=[HasModelPermission | HasObjectPermission, ])
    def detail_export(self, request, pk=None, export_format='xml'):
        if export_format == 'xml':
            serializer = QuestionSetExportSerializer(self.get_object())
            xml = QuestionSetRenderer().render([serializer.data])
            return XMLResponse(xml, name=self.get_object().uri_path)
        else:
            return render_to_format(self.request, export_format, self.get_object().uri_path, 'questions/export/questionsets.html', {
                'questionsets': [self.get_object()]
            })


class QuestionViewSet(CopyModelMixin, ModelViewSet):
    permission_classes = (HasModelPermission | HasObjectPermission, )
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('uri', 'text')
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

    @action(detail=False, permission_classes=[HasModelPermission | HasObjectPermission, ])
    def index(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = QuestionIndexSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path='export(/(?P<export_format>[a-z]+))?', permission_classes=[HasModelPermission | HasObjectPermission, ])
    def export(self, request, export_format='xml'):
        queryset = self.filter_queryset(self.get_queryset())
        if export_format == 'xml':
            serializer = QuestionExportSerializer(queryset, many=True)
            xml = QuestionRenderer().render(serializer.data)
            return XMLResponse(xml, name='questions')
        else:
            return render_to_format(self.request, export_format, 'questions', 'questions/export/questions.html', {
                'questions': queryset
            })

    @action(detail=True, url_path='export(/(?P<export_format>[a-z]+))?', permission_classes=[HasModelPermission | HasObjectPermission, ])
    def detail_export(self, request, pk=None, export_format='xml'):
        if export_format == 'xml':
            serializer = QuestionExportSerializer(self.get_object())
            xml = QuestionRenderer().render([serializer.data])
            return XMLResponse(xml, name=self.get_object().uri_path)
        else:
            return render_to_format(self.request, export_format, self.get_object().uri_path, 'questions/export/questions.html', {
                'questions': [self.get_object()]
            })


class WidgetTypeViewSet(ChoicesViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = get_widget_type_choices()


class ValueTypeViewSet(ChoicesViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = VALUE_TYPE_CHOICES
