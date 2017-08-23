from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.filters import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from rdmo.core.views import ChoicesViewSet
from rdmo.core.permissions import HasModelPermission

from rdmo.options.models import OptionSet
from rdmo.conditions.models import Condition

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
from .serializers.api import (
    AttributeEntitySerializer as AttributeEntityApiSerializer,
    AttributeSerializer as AttributeApiSerializer
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


class AttributeEntityApiViewSet(ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission, )
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    queryset = AttributeEntity.objects.filter(is_attribute=False)
    serializer_class = AttributeEntityApiSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = (
        'uri',
        'path',
        'key',
        'parent'
    )


class AttributeApiViewSet(ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission, )
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    queryset = Attribute.objects.all()
    serializer_class = AttributeApiSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = (
        'uri',
        'path',
        'key',
        'parent'
    )
