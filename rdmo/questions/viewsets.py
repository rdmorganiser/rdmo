from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from django_filters.rest_framework import DjangoFilterBackend

from rdmo.core.views import ChoicesViewSet
from rdmo.core.permissions import HasModelPermission
from rdmo.core.constants import VALUE_TYPE_CHOICES
from rdmo.domain.models import AttributeEntity, Attribute
from rdmo.options.models import OptionSet
from rdmo.conditions.models import Condition

from .models import Catalog, Section, Subsection, QuestionSet, Question
from .serializers import (
    CatalogSerializer,
    CatalogIndexSerializer,
    SectionSerializer,
    SectionIndexSerializer,
    SubsectionSerializer,
    SubsectionIndexSerializer,
    QuestionSetSerializer,
    QuestionSetIndexSerializer,
    QuestionSerializer,
    AttributeEntitySerializer,
    AttributeSerializer,
    OptionSetSerializer,
    ConditionSerializer
)
from .serializers.nested import CatalogSerializer as NestedCatalogSerializer
from .serializers.api import (
    CatalogSerializer as CatalogApiSerializer,
    SectionSerializer as SectionApiSerializer,
    SubsectionSerializer as SubsectionApiSerializer,
    QuestionSetSerializer as QuestionSetApiSerializer,
    QuestionSerializer as QuestionApiSerializer,
)


class CatalogViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer

    @detail_route()
    def nested(self, request, pk):
        queryset = get_object_or_404(Catalog, pk=pk)
        serializer = NestedCatalogSerializer(queryset)
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
    queryset = QuestionSet.objects.all()
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


class ValueTypeViewSet(ChoicesViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = VALUE_TYPE_CHOICES


class AttributeEntityViewSet(ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = AttributeEntity.objects.all()
    serializer_class = AttributeEntitySerializer


class AttributeViewSet(ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer


class OptionSetViewSet(ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = OptionSet.objects.all()
    serializer_class = OptionSetSerializer


class ConditionViewSet(ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer


class CatalogApiViewSet(ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission, )
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    queryset = Catalog.objects.all()
    serializer_class = CatalogApiSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = (
        'uri',
        'key'
    )


class SectionApiViewSet(ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission, )
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    queryset = Section.objects.all()
    serializer_class = SectionApiSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = (
        'uri',
        'path',
        'key',
        'catalog'
    )


class SubsectionApiViewSet(ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission, )
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    queryset = Subsection.objects.all()
    serializer_class = SubsectionApiSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = (
        'uri',
        'path',
        'key',
        'section'
    )


class QuestionSetApiViewSet(ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission, )
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    queryset = QuestionSet.objects.all()
    serializer_class = QuestionSetApiSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = (
        'uri',
        'path',
        'key',
        'subsection'
    )


class QuestionApiViewSet(ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission, )
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    queryset = Question.objects.all()
    serializer_class = QuestionApiSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = (
        'uri',
        'path',
        'key',
        'questionset'
    )
