from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _

from rest_framework import viewsets, mixins
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND

from apps.core.serializers import ChoicesSerializer
from apps.core.utils import render_to_format

from .models import *
from .serializers import *


@staff_member_required
def questions(request):
    return render(request, 'questions/questions.html', {
        'export_formats': settings.EXPORT_FORMATS
    })


@staff_member_required
def questions_catalog_export(request, catalog_id, format):
    catalog = get_object_or_404(Catalog, pk=catalog_id)
    title = '%s %s' % (_('Catalog'), catalog.title)

    return render_to_format(request, 'questions/catalog_pdf.html', {
        'pagesize': 'A4',
        'title': title,
        'catalog': catalog,
    }, title, format)


class CatalogViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = Catalog.objects.all()

    def get_serializer_class(self):
        if self.request.GET.get('nested'):
            return NestedCatalogSerializer
        else:
            return CatalogSerializer


class SectionViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = Section.objects.all()
    serializer_class = SectionSerializer


class SubsectionViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = Subsection.objects.all()
    serializer_class = SubsectionSerializer


class QuestionEntityViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = QuestionEntity.objects.filter(question__parent_entity=None)
    serializer_class = QuestionEntitySerializer

    def get_queryset(self):
        queryset = QuestionEntity.objects

        if self.request.GET.get('nested'):
            queryset = queryset.filter(question__parent_entity=None)

        questions = self.request.GET.get('questions')
        if questions in ['0', 'false']:
            queryset = queryset.filter(question=None)

        return queryset

    def get_serializer_class(self):
        if self.request.GET.get('nested'):
            return NestedQuestionEntitySerializer
        else:
            return QuestionEntitySerializer


class QuestionViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class WidgetTypeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )

    serializer_class = ChoicesSerializer

    def get_queryset(self):
        return Question.WIDGET_TYPE_CHOICES
