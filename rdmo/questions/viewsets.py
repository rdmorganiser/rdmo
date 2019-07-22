from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from rdmo.core.views import ChoicesViewSet
from rdmo.core.permissions import HasModelPermission
from rdmo.core.constants import VALUE_TYPE_CHOICES

from .models import Catalog, Section, QuestionSet, Question
from .serializers.v1 import (
    CatalogSerializer,
    SectionSerializer,
    QuestionSetSerializer,
    QuestionSerializer,
    CatalogIndexSerializer,
    SectionIndexSerializer,
    QuestionSetIndexSerializer,
    QuestionIndexSerializer,
    CatalogNestedSerializer,
    SectionNestedSerializer,
    QuestionSetNestedSerializer,
    QuestionNestedSerializer
)


class CatalogViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = (
        'uri',
        'key'
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


class SectionViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = (
        'uri',
        'path',
        'key',
        'catalog'
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


class QuestionSetViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = QuestionSet.objects.all()
    serializer_class = QuestionSetSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = (
        'uri',
        'path',
        'key',
        'section'
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


class QuestionViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = (
        'uri',
        'path',
        'key',
        'questionset',
        'is_collection',
        'value_type',
        'widget_type'
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


class WidgetTypeViewSet(ChoicesViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Question.WIDGET_TYPE_CHOICES


class ValueTypeViewSet(ChoicesViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = VALUE_TYPE_CHOICES
