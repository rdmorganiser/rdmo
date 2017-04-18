from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import list_route, detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.core.views import ChoicesViewSet
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
    AttributeSerializer
)


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
