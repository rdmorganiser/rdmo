from django.db import models

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from django_filters.rest_framework import DjangoFilterBackend

from rdmo.core.constants import VALUE_TYPE_CHOICES
from rdmo.core.exports import XMLResponse
from rdmo.core.filters import SearchFilter
from rdmo.core.permissions import HasModelPermission, HasObjectPermission
from rdmo.core.utils import render_to_format
from rdmo.core.views import ChoicesViewSet
from rdmo.management.viewsets import ElementToggleCurrentSiteViewSetMixin

from .constants import WIDGET_TYPE_CHOICES
from .models import Catalog, Page, Question, QuestionSet, Section
from .renderers import CatalogRenderer, PageRenderer, QuestionRenderer, QuestionSetRenderer, SectionRenderer
from .serializers.export import (
    CatalogExportSerializer,
    PageExportSerializer,
    QuestionExportSerializer,
    QuestionSetExportSerializer,
    SectionExportSerializer,
)
from .serializers.v1 import (
    CatalogIndexSerializer,
    CatalogNestedSerializer,
    CatalogSerializer,
    PageIndexSerializer,
    PageNestedSerializer,
    PageSerializer,
    QuestionIndexSerializer,
    QuestionSerializer,
    QuestionSetIndexSerializer,
    QuestionSetNestedSerializer,
    QuestionSetSerializer,
    SectionIndexSerializer,
    SectionNestedSerializer,
    SectionSerializer,
)
from .utils import get_export_flags, get_serializer_context


class CatalogViewSet(ElementToggleCurrentSiteViewSetMixin, ModelViewSet):
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
        queryset = Catalog.objects.all()
        if self.action in ['index']:
            return queryset

        queryset = Catalog.objects.annotate(projects_count=models.Count('projects'))
        if self.action in ['nested']:
            return queryset.prefetch_elements()
        elif self.action in ['export', 'detail_export']:
            return queryset.prefetch_elements(
                optionsets=True,
                optionsets_conditions=get_export_flags(self.request).get('conditions'),
                options=get_export_flags(self.request).get('options')
            )
        else:
            return queryset.prefetch_related(
                'sites',
                'editors',
                'groups',
                'catalog_sections__section',
            )

    @action(detail=True)
    def nested(self, request, pk):
        serializer = CatalogNestedSerializer(self.get_object(), context={'request': request})
        return Response(serializer.data)

    @action(detail=False)
    def index(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = CatalogIndexSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, url_path='export(?:/(?P<export_format>[a-z]+))?')
    def export(self, request, export_format='xml'):
        queryset = self.filter_queryset(self.get_queryset())
        if export_format == 'xml':
            export_flags = get_export_flags(self.request)
            serializer = CatalogExportSerializer(
                queryset,
                many=True,
                context=get_serializer_context(queryset, export_flags)
            )
            xml = CatalogRenderer().render(serializer.data, context=export_flags)
            return XMLResponse(xml, name='catalogs')
        else:
            return render_to_format(
                self.request, export_format, 'questions', 'questions/export/catalogs.html', {
                    'catalogs': queryset
                }
            )

    @action(detail=True, url_path='export(?:/(?P<export_format>[a-z]+))?')
    def detail_export(self, request, pk=None, export_format='xml'):
        instance = self.get_object()
        if export_format == 'xml':
            export_flags = get_export_flags(self.request)
            serializer = CatalogExportSerializer(
                instance,
                context=get_serializer_context([instance], export_flags)
            )
            xml = CatalogRenderer().render([serializer.data], context=export_flags)
            return XMLResponse(xml, name=instance.uri_path)
        else:
            return render_to_format(
                self.request, export_format, instance.uri_path, 'questions/export/catalogs.html', {
                    'catalogs': [instance]
                }
            )


class SectionViewSet(ModelViewSet):
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
        if self.action in ['index']:
            return queryset
        if self.action in ['nested']:
            return queryset.prefetch_elements()
        elif self.action in ['export', 'detail_export']:
            return queryset.prefetch_elements(
                optionsets=True,
                optionsets_conditions=get_export_flags(self.request).get('conditions'),
                options=get_export_flags(self.request).get('options')
            )
        else:
            return queryset.prefetch_related(
                'catalogs',
                'editors',
                'section_pages__page',
            )

    @action(detail=True)
    def nested(self, request, pk):
        serializer = SectionNestedSerializer(self.get_object(), context={'request': request})
        return Response(serializer.data)

    @action(detail=False)
    def index(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = SectionIndexSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path='export(?:/(?P<export_format>[a-z]+))?')
    def export(self, request, export_format='xml'):
        queryset = self.filter_queryset(self.get_queryset())
        if export_format == 'xml':
            export_flags = get_export_flags(self.request)
            serializer = SectionExportSerializer(
                queryset,
                many=True,
                context=get_serializer_context(queryset, export_flags)
            )
            xml = SectionRenderer().render(serializer.data, context=export_flags)
            return XMLResponse(xml, name='sections')
        else:
            return render_to_format(
                self.request, export_format, 'questions', 'questions/export/sections.html', {
                    'sections': queryset
                }
            )

    @action(detail=True, url_path='export(?:/(?P<export_format>[a-z]+))?')
    def detail_export(self, request, pk=None, export_format='xml'):
        instance = self.get_object()
        if export_format == 'xml':
            export_flags = get_export_flags(self.request)
            serializer = SectionExportSerializer(
                instance,
                context=get_serializer_context([instance], export_flags)
            )
            xml = SectionRenderer().render([serializer.data], context=export_flags)
            return XMLResponse(xml, name=instance.uri_path)
        else:
            return render_to_format(
                self.request, export_format, instance.uri_path, 'questions/export/sections.html', {
                    'sections': [instance]
                }
            )


class PageViewSet(ModelViewSet):
    permission_classes = (HasModelPermission | HasObjectPermission, )
    serializer_class = PageSerializer

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
        if self.action in ['index']:
            return queryset
        if self.action in ['nested']:
            return queryset.prefetch_elements()
        elif self.action in ['export', 'detail_export']:
            return queryset.prefetch_elements(
                optionsets=True,
                optionsets_conditions=get_export_flags(self.request).get('conditions'),
                options=get_export_flags(self.request).get('options')
            )
        else:
            return queryset.prefetch_related(
                'conditions',
                'sections',
                'editors',
                'page_questionsets__questionset',
                'page_questions__question',
            ).select_related('attribute')

    @action(detail=True)
    def nested(self, request, pk):
        serializer = PageNestedSerializer(self.get_object(), context={'request': request})
        return Response(serializer.data)

    @action(detail=False)
    def index(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = PageIndexSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path='export(?:/(?P<export_format>[a-z]+))?')
    def export(self, request, export_format='xml'):
        queryset = self.filter_queryset(self.get_queryset())
        if export_format == 'xml':
            export_flags = get_export_flags(self.request)
            serializer = PageExportSerializer(
                queryset,
                many=True,
                context=get_serializer_context(queryset, export_flags)
            )
            xml = PageRenderer().render(serializer.data, context=export_flags)
            return XMLResponse(xml, name='pages')
        else:
            return render_to_format(
                self.request, export_format, 'questions', 'questions/export/pages.html', {
                    'pages': queryset
                }
            )

    @action(detail=True, url_path='export(?:/(?P<export_format>[a-z]+))?')
    def detail_export(self, request, pk=None, export_format='xml'):
        instance = self.get_object()
        if export_format == 'xml':
            export_flags = get_export_flags(self.request)
            serializer = PageExportSerializer(
                instance,
                context=get_serializer_context([instance], export_flags)
            )
            xml = PageRenderer().render([serializer.data], context=export_flags)
            return XMLResponse(xml, name=instance.uri_path)
        else:
            return render_to_format(
                self.request, export_format, instance.uri_path, 'questions/export/pages.html', {
                    'pages': [instance]
                }
            )


class QuestionSetViewSet(ModelViewSet):
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

    def get_queryset(self):
        queryset = QuestionSet.objects.all()

        if self.action in ['index']:
            return queryset
        elif self.action in ['nested']:
            return queryset.prefetch_elements()
        elif self.action in ['export', 'detail_export']:
            return queryset.prefetch_elements(
                optionsets=True,
                optionsets_conditions=get_export_flags(self.request).get('conditions'),
                options=get_export_flags(self.request).get('options')
            )
        else:
            return queryset.prefetch_related(
                'conditions',
                'pages',
                'parents',
                'editors',
                'questionset_questionsets__questionset',
                'questionset_questions__question',
            ).select_related('attribute')

    @action(detail=True)
    def nested(self, request, pk):
        serializer = QuestionSetNestedSerializer(self.get_object(), context={'request': request})
        return Response(serializer.data)

    @action(detail=False)
    def index(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = QuestionSetIndexSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, url_path='export(?:/(?P<export_format>[a-z]+))?')
    def export(self, request, export_format='xml'):
        queryset = self.filter_queryset(self.get_queryset())
        if export_format == 'xml':
            export_flags = get_export_flags(self.request)
            serializer = QuestionSetExportSerializer(
                queryset,
                many=True,
                context=get_serializer_context(queryset, export_flags)
            )
            xml = QuestionSetRenderer().render(serializer.data, context=export_flags)
            return XMLResponse(xml, name='questionsets')
        else:
            return render_to_format(
                self.request, export_format, 'questionsets', 'questions/export/questionsets.html', {
                    'questionsets': queryset
                }
            )

    @action(detail=True, url_path='export(?:/(?P<export_format>[a-z]+))?')
    def detail_export(self, request, pk=None, export_format='xml'):
        instance = self.get_object()
        if export_format == 'xml':
            export_flags = get_export_flags(self.request)
            serializer = QuestionSetExportSerializer(
                instance,
                context=get_serializer_context([instance], export_flags)
            )
            xml = QuestionSetRenderer().render([serializer.data], context=export_flags)
            return XMLResponse(xml, name=instance.uri_path)
        else:
            return render_to_format(
                self.request, export_format, instance.uri_path, 'questions/export/questionsets.html', {
                    'questionsets': [instance]
                }
            )


class QuestionViewSet(ModelViewSet):
    permission_classes = (HasModelPermission | HasObjectPermission, )
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

    def get_queryset(self):
        queryset = Question.objects.all()

        if self.action in ['index']:
            return queryset
        elif self.action in ['nested']:
            return queryset.prefetch_elements()
        elif self.action in ['export', 'detail_export']:
            return queryset.prefetch_elements(
                optionsets=True,
                optionsets_conditions=get_export_flags(self.request).get('conditions'),
                options=get_export_flags(self.request).get('options')
            )
        else:
            return queryset.prefetch_related(
                'conditions',
                'optionsets',
                'pages',
                'questionsets',
                'editors'
            ).select_related('attribute')

    @action(detail=False)
    def index(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = QuestionIndexSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path='export(?:/(?P<export_format>[a-z]+))?')
    def export(self, request, export_format='xml'):
        queryset = self.filter_queryset(self.get_queryset())
        if export_format == 'xml':
            export_flags = get_export_flags(self.request)
            serializer = QuestionExportSerializer(
                queryset,
                many=True,
                context=get_serializer_context(queryset, export_flags)
            )
            xml = QuestionRenderer().render(serializer.data, context=export_flags)
            return XMLResponse(xml, name='questions')
        else:
            return render_to_format(
                self.request, export_format, 'questions', 'questions/export/questions.html', {
                    'questions': queryset
                }
            )

    @action(detail=True, url_path='export(?:/(?P<export_format>[a-z]+))?')
    def detail_export(self, request, pk=None, export_format='xml'):
        instance = self.get_object()
        if export_format == 'xml':
            export_flags = get_export_flags(self.request)
            serializer = QuestionExportSerializer(
                instance,
                context=get_serializer_context([instance], export_flags)
            )
            xml = QuestionRenderer().render([serializer.data], context=export_flags)
            return XMLResponse(xml, name=instance.uri_path)
        else:
            return render_to_format(
                self.request, export_format, instance.uri_path, 'questions/export/questions.html', {
                    'questions': [instance]
                }
            )


class WidgetTypeViewSet(ChoicesViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = WIDGET_TYPE_CHOICES


class ValueTypeViewSet(ChoicesViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = VALUE_TYPE_CHOICES
