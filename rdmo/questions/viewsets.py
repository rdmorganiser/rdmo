from django.db import models

from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from django_filters.rest_framework import DjangoFilterBackend

from rdmo.core.constants import VALUE_TYPE_CHOICES
from rdmo.core.exports import XMLResponse
from rdmo.core.permissions import HasModelPermission, HasObjectPermission
from rdmo.core.utils import is_truthy, render_to_format
from rdmo.core.views import ChoicesViewSet

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
from .utils import get_widget_type_choices


class CatalogViewSet(ModelViewSet):
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
        if self.action in ['index']:
            return queryset
        elif self.action in ('nested', 'export', 'detail_export'):
            return queryset.prefetch_elements()
        else:
            return queryset.prefetch_related('sites', 'editors', 'groups', 'catalog_sections__section')

    @action(detail=True)
    def nested(self, request, pk):
        serializer = CatalogNestedSerializer(self.get_object(), context={'request': request})
        return Response(serializer.data)

    @action(detail=False)
    def index(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = CatalogIndexSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, url_path='export(/(?P<export_format>[a-z]+))?')
    def export(self, request, export_format='xml'):
        queryset = self.filter_queryset(self.get_queryset())
        if export_format == 'xml':
            serializer = CatalogExportSerializer(queryset, many=True)
            xml = CatalogRenderer().render(serializer.data, context=self.get_export_renderer_context(request))
            return XMLResponse(xml, name='catalogs')
        else:
            return render_to_format(
                self.request, export_format, 'questions', 'questions/export/catalogs.html', {
                    'catalogs': queryset
                }
            )

    @action(detail=True, url_path='export(/(?P<export_format>[a-z]+))?')
    def detail_export(self, request, pk=None, export_format='xml'):
        if export_format == 'xml':
            serializer = CatalogExportSerializer(self.get_object())
            xml = CatalogRenderer().render([serializer.data], context=self.get_export_renderer_context(request))
            return XMLResponse(xml, name=self.get_object().uri_path)
        else:
            return render_to_format(
                self.request, export_format, self.get_object().uri_path, 'questions/export/catalogs.html', {
                    'catalogs': [self.get_object()]
                }
            )

    def get_export_renderer_context(self, request):
        full = is_truthy(request.GET.get('full'))
        return {
            'sections': full or is_truthy(request.GET.get('sections', True)),
            'pages': full or is_truthy(request.GET.get('pages', True)),
            'questionsets': full or is_truthy(request.GET.get('questionsets', True)),
            'questions': full or is_truthy(request.GET.get('questions', True)),
            'attributes': full or is_truthy(request.GET.get('attributes')),
            'optionsets': full or is_truthy(request.GET.get('optionsets')),
            'options': full or is_truthy(request.GET.get('options')),
            'conditions': full or is_truthy(request.GET.get('conditions'))
        }


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
        elif self.action in ('nested', 'export', 'detail_export'):
            return queryset.prefetch_elements()
        else:
            return queryset.prefetch_related('catalogs', 'editors', 'section_pages__page')

    @action(detail=True)
    def nested(self, request, pk):
        serializer = SectionNestedSerializer(self.get_object(), context={'request': request})
        return Response(serializer.data)

    @action(detail=False)
    def index(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = SectionIndexSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path='export(/(?P<export_format>[a-z]+))?')
    def export(self, request, export_format='xml'):
        queryset = self.filter_queryset(self.get_queryset())
        if export_format == 'xml':
            serializer = SectionExportSerializer(queryset, many=True)
            xml = SectionRenderer().render(serializer.data, context=self.get_export_renderer_context(request))
            return XMLResponse(xml, name='sections')
        else:
            return render_to_format(
                self.request, export_format, 'questions', 'questions/export/sections.html', {
                    'sections': queryset
                }
            )

    @action(detail=True, url_path='export(/(?P<export_format>[a-z]+))?')
    def detail_export(self, request, pk=None, export_format='xml'):
        if export_format == 'xml':
            serializer = SectionExportSerializer(self.get_object())
            xml = SectionRenderer().render([serializer.data], context=self.get_export_renderer_context(request))
            return XMLResponse(xml, name=self.get_object().uri_path)
        else:
            return render_to_format(
                self.request, export_format, self.get_object().uri_path, 'questions/export/sections.html', {
                    'sections': [self.get_object()]
                }
            )

    def get_export_renderer_context(self, request):
        full = is_truthy(request.GET.get('full'))
        return {
            'pages': full or is_truthy(request.GET.get('pages', True)),
            'questionsets': full or is_truthy(request.GET.get('questionsets', True)),
            'questions': full or is_truthy(request.GET.get('questions', True)),
            'attributes': full or is_truthy(request.GET.get('attributes')),
            'optionsets': full or is_truthy(request.GET.get('optionsets')),
            'options': full or is_truthy(request.GET.get('options')),
            'conditions': full or is_truthy(request.GET.get('conditions'))
        }


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
        elif self.action in ['nested', 'export', 'detail_export']:
            return queryset.prefetch_elements().select_related('attribute')
        else:
            return queryset.prefetch_related(
                'conditions',
                'sections',
                'editors',
                'page_questionsets__questionset',
                'page_questions__question'
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

    @action(detail=False, url_path='export(/(?P<export_format>[a-z]+))?')
    def export(self, request, export_format='xml'):
        queryset = self.filter_queryset(self.get_queryset())
        if export_format == 'xml':
            serializer = PageExportSerializer(queryset, many=True)
            xml = PageRenderer().render(serializer.data, context=self.get_export_renderer_context(request))
            return XMLResponse(xml, name='pages')
        else:
            return render_to_format(
                self.request, export_format, 'questions', 'questions/export/pages.html', {
                    'pages': queryset
                }
            )

    @action(detail=True, url_path='export(/(?P<export_format>[a-z]+))?')
    def detail_export(self, request, pk=None, export_format='xml'):
        if export_format == 'xml':
            serializer = PageExportSerializer(self.get_object())
            xml = PageRenderer().render([serializer.data], context=self.get_export_renderer_context(request))
            return XMLResponse(xml, name=self.get_object().uri_path)
        else:
            return render_to_format(
                self.request, export_format, self.get_object().uri_path, 'questions/export/pages.html', {
                    'pages': [self.get_object()]
                }
            )

    def get_export_renderer_context(self, request):
        full = is_truthy(request.GET.get('full'))
        return {
            'questionsets': full or is_truthy(request.GET.get('questionsets', True)),
            'questions': full or is_truthy(request.GET.get('questions', True)),
            'attributes': full or is_truthy(request.GET.get('attributes')),
            'optionsets': full or is_truthy(request.GET.get('optionsets')),
            'options': full or is_truthy(request.GET.get('options')),
            'conditions': full or is_truthy(request.GET.get('conditions'))
        }


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
        elif self.action in ('nested', 'export', 'detail_export'):
            return queryset.prefetch_elements().select_related('attribute')
        else:
            return queryset.prefetch_related(
                'conditions',
                'pages',
                'parents',
                'editors',
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
        serializer = QuestionSetIndexSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, url_path='export(/(?P<export_format>[a-z]+))?')
    def export(self, request, export_format='xml'):
        queryset = self.filter_queryset(self.get_queryset())
        if export_format == 'xml':
            serializer = QuestionSetExportSerializer(queryset, many=True)
            xml = QuestionSetRenderer().render(serializer.data, context=self.get_export_renderer_context(request))
            return XMLResponse(xml, name='questionsets')
        else:
            return render_to_format(
                self.request, export_format, 'questionsets', 'questions/export/questionsets.html', {
                    'questionsets': queryset
                }
            )

    @action(detail=True, url_path='export(/(?P<export_format>[a-z]+))?')
    def detail_export(self, request, pk=None, export_format='xml'):
        if export_format == 'xml':
            serializer = QuestionSetExportSerializer(self.get_object())
            xml = QuestionSetRenderer().render([serializer.data], context=self.get_export_renderer_context(request))
            return XMLResponse(xml, name=self.get_object().uri_path)
        else:
            return render_to_format(
                self.request, export_format, self.get_object().uri_path, 'questions/export/questionsets.html', {
                    'questionsets': [self.get_object()]
                }
            )

    def get_export_renderer_context(self, request):
        full = is_truthy(request.GET.get('full'))
        return {
            'questionsets': full or is_truthy(request.GET.get('questionsets', True)),
            'questions': full or is_truthy(request.GET.get('questions', True)),
            'attributes': full or is_truthy(request.GET.get('attributes')),
            'optionsets': full or is_truthy(request.GET.get('optionsets')),
            'options': full or is_truthy(request.GET.get('options')),
            'conditions': full or is_truthy(request.GET.get('conditions'))
        }


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
        elif self.action in ('nested', 'export', 'detail_export'):
            return queryset.prefetch_elements().select_related('attribute')
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

    @action(detail=False, url_path='export(/(?P<export_format>[a-z]+))?')
    def export(self, request, export_format='xml'):
        queryset = self.filter_queryset(self.get_queryset())
        if export_format == 'xml':
            serializer = QuestionExportSerializer(queryset, many=True)
            xml = QuestionRenderer().render(serializer.data, context=self.get_export_renderer_context(request))
            return XMLResponse(xml, name='questions')
        else:
            return render_to_format(
                self.request, export_format, 'questions', 'questions/export/questions.html', {
                    'questions': queryset
                }
            )

    @action(detail=True, url_path='export(/(?P<export_format>[a-z]+))?')
    def detail_export(self, request, pk=None, export_format='xml'):
        if export_format == 'xml':
            serializer = QuestionExportSerializer(self.get_object())
            xml = QuestionRenderer().render([serializer.data], context=self.get_export_renderer_context(request))
            return XMLResponse(xml, name=self.get_object().uri_path)
        else:
            return render_to_format(
                self.request, export_format, self.get_object().uri_path, 'questions/export/questions.html', {
                    'questions': [self.get_object()]
                }
            )

    def get_export_renderer_context(self, request):
        full = is_truthy(request.GET.get('full'))
        return {
            'attributes': full or is_truthy(request.GET.get('attributes')),
            'optionsets': full or is_truthy(request.GET.get('optionsets')),
            'options': full or is_truthy(request.GET.get('options')),
            'conditions': full or is_truthy(request.GET.get('conditions'))
        }


class WidgetTypeViewSet(ChoicesViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = get_widget_type_choices()


class ValueTypeViewSet(ChoicesViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = VALUE_TYPE_CHOICES
