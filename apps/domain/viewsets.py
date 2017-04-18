from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.filters import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import list_route
from rest_framework.response import Response

from apps.core.views import ChoicesViewSet
from apps.core.permissions import HasModelPermission

from apps.options.models import OptionSet
from apps.conditions.models import Condition

from .models import AttributeEntity, Attribute, VerboseName, Range
from .serializers import (
    AttributeEntitySerializer,
    AttributeEntityNestedSerializer,
    AttributeEntityIndexSerializer,
    AttributeSerializer,
    AttributeIndexSerializer,
    RangeSerializer,
    VerboseNameSerializer,
    OptionSetSerializer,
    ConditionSerializer
)


class AttributeEntityViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )

    queryset = AttributeEntity.objects.filter(is_attribute=False)
    serializer_class = AttributeEntitySerializer

    @list_route()
    def nested(self, request):
        queryset = AttributeEntity.objects.get_cached_trees()
        serializer = AttributeEntityNestedSerializer(queryset, many=True)
        return Response(serializer.data)

    @list_route()
    def index(self, request):
        queryset = AttributeEntity.objects.filter(is_attribute=False)
        serializer = AttributeEntityIndexSerializer(queryset, many=True)
        return Response(serializer.data)


class AttributeViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )

    queryset = Attribute.objects.order_by('path')
    serializer_class = AttributeSerializer

    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('path', 'parent_collection')

    @list_route()
    def index(self, request):
        queryset = Attribute.objects.all()
        serializer = AttributeIndexSerializer(queryset, many=True)
        return Response(serializer.data)


class RangeViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )

    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('attribute', )

    queryset = Range.objects.order_by('attribute__path')
    serializer_class = RangeSerializer


class VerboseNameViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )

    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('attribute_entity', )

    queryset = VerboseName.objects.all()
    serializer_class = VerboseNameSerializer


class ValueTypeViewSet(ChoicesViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Attribute.VALUE_TYPE_CHOICES


class OptionSetViewSet(ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission, )

    queryset = OptionSet.objects.all()
    serializer_class = OptionSetSerializer


class ConditionViewSet(ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission, )

    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer
