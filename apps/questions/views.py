from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, DetailView

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import list_route, detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.core.views import ModelPermissionMixin, ChoicesViewSet
from apps.core.utils import render_to_format
from apps.core.permissions import HasModelPermission

from apps.domain.models import AttributeEntity, Attribute

from .models import Catalog, Section, Subsection, QuestionEntity, Question
from .serializers import (
    CatalogSerializer,
    CatalogIndexSerializer,
    CatalogNestedSerializer,
    SectionSerializer,
    SectionIndexSerializer,
    SubsectionSerializer,
    SubsectionIndexSerializer,
    QuestionSetSerializer,
    QuestionSetIndexSerializer,
    QuestionSerializer,
    AttributeEntitySerializer,
    AttributeSerializer,
    ExportSerializer
)
from .renderers import XMLRenderer


class CatalogsView(ModelPermissionMixin, TemplateView):
    template_name = 'questions/catalogs.html'
    permission_required = 'questions.view_catalog'

    def get_context_data(self, **kwargs):
        context = super(CatalogsView, self).get_context_data(**kwargs)
        context['export_formats'] = settings.EXPORT_FORMATS
        return context


class CatalogExportView(ModelPermissionMixin, DetailView):
    model = Catalog
    context_object_name = 'catalog'
    permission_required = 'options.view_option'

    def render_to_response(self, context, **response_kwargs):
        format = self.kwargs.get('format')
        if format == 'xml':
            serializer = ExportSerializer(context['catalog'])
            response = HttpResponse(XMLRenderer().render(serializer.data), content_type="application/xml")
            response['Content-Disposition'] = 'filename="%s.xml"' % context['catalog'].key
            return response
        else:
            return render_to_format(self.request, format, context['catalog'].title, 'questions/catalog_export.html', context)


class CatalogViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer

    @detail_route()
    def nested(self, request, pk):
        queryset = get_object_or_404(Catalog, pk=pk)
        serializer = CatalogNestedSerializer(queryset)
        return Response(serializer.data)

    @list_route()
    def index(self, request):
        serializer = CatalogIndexSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)


class SectionViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

    @list_route()
    def index(self, request):
        serializer = SectionIndexSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)


class SubsectionViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = Subsection.objects.all()
    serializer_class = SubsectionSerializer

    @list_route()
    def index(self, request):
        serializer = SubsectionIndexSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)


class QuestionSetViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = QuestionEntity.objects.filter(question=None)
    serializer_class = QuestionSetSerializer

    @list_route()
    def index(self, request):
        serializer = QuestionSetIndexSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)


class QuestionViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class WidgetTypeViewSet(ChoicesViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Question.WIDGET_TYPE_CHOICES


class AttributeEntityViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = AttributeEntity.objects.filter(attribute=None)
    serializer_class = AttributeEntitySerializer


class AttributeViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
