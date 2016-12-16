from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404

from rest_framework import viewsets, mixins, filters
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response

from apps.core.serializers import ChoicesSerializer
from apps.core.utils import render_to_format

from .models import *
from .serializers import *
from .renderers import *


@staff_member_required
def catalogs(request):
    return render(request, 'questions/catalogs.html', {
        'export_formats': settings.EXPORT_FORMATS
    })


@staff_member_required
def catalog_export(request, catalog_id, format):
    catalog = get_object_or_404(Catalog, pk=catalog_id)

    return render_to_format(request, format, catalog.title, 'questions/catalog_export.html', {
        'catalog': catalog
    })


@staff_member_required
def questions_catalog_export_xml(request):
    queryset = Catalog.objects.all()
    serializer = ExportSerializer(queryset, many=True)
    return HttpResponse(XMLRenderer().render(serializer.data), content_type="application/xml")


class CatalogViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

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


class SectionViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = Section.objects.all()
    serializer_class = SectionSerializer

    @list_route()
    def index(self, request):
        serializer = SectionIndexSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)


class SubsectionViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = Subsection.objects.all()
    serializer_class = SubsectionSerializer

    @list_route()
    def index(self, request):
        serializer = SubsectionIndexSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)


class QuestionSetViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = QuestionEntity.objects.filter(question=None)
    serializer_class = QuestionSetSerializer

    @list_route()
    def index(self, request):
        serializer = QuestionSetIndexSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)


class QuestionViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class WidgetTypeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )

    serializer_class = ChoicesSerializer

    def get_queryset(self):
        return Question.WIDGET_TYPE_CHOICES


class AttributeEntityViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = AttributeEntity.objects.filter(attribute=None)
    serializer_class = AttributeEntitySerializer


class AttributeViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
