import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


from rest_framework import viewsets, mixins
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND

from .models import *
from .serializers import *


@login_required()
def questions(request):
    return render(request, 'questions/questions.html', {
        'widget_types': json.dumps([{'id': id, 'text': text} for id, text in Question.WIDGET_TYPE_CHOICES])
    })


class CatalogViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = Catalog.objects.all().order_by('pk')

    def get_serializer_class(self):
        if self.action == 'list':
            return CatalogSerializer
        else:
            return NestedCatalogSerializer


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

    queryset = QuestionEntity.objects.filter(question__questionset=None)
    serializer_class = QuestionEntitySerializer

    @list_route(methods=['get'], permission_classes=[DjangoModelPermissions])
    def first(self, request, pk=None):
        try:
            catalog = Catalog.objects.get(pk=request.GET.get('catalog'))
            entity = QuestionEntity.objects.order_by_catalog(catalog).first()
            serializer = self.get_serializer(entity)
            return Response(serializer.data)
        except Catalog.DoesNotExist:
            return Response({'message': e.message}, status=HTTP_404_NOT_FOUND)

    @detail_route(methods=['get'], permission_classes=[DjangoModelPermissions])
    def prev(self, request, pk=None):
        try:
            return Response({'id': QuestionEntity.objects.get_prev(pk).pk})
        except QuestionEntity.DoesNotExist as e:
            return Response({'message': e.message}, status=HTTP_404_NOT_FOUND)

    @detail_route(methods=['get'], permission_classes=[DjangoModelPermissions])
    def next(self, request, pk=None):
        try:
            return Response({'id': QuestionEntity.objects.get_next(pk).pk})
        except QuestionEntity.DoesNotExist as e:
            return Response({'message': e.message}, status=HTTP_404_NOT_FOUND)


class QuestionSetViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = QuestionSet.objects.all()
    serializer_class = QuestionSetSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class OptionViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = Option.objects.all()
    serializer_class = OptionSerializer


class WidgetTypeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )

    serializer_class = WidgetTypeSerializer

    def get_queryset(self):
        return Question.WIDGET_TYPE_CHOICES
