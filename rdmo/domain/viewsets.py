from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from django_filters.rest_framework import DjangoFilterBackend

from rdmo.core.permissions import HasModelPermission

from .models import Attribute
from .serializers import (
    AttributeSerializer,
    AttributeNestedSerializer,
    AttributeIndexSerializer
)
from .serializers.api import (
    AttributeSerializer as AttributeApiSerializer
)


class AttributeViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )

    queryset = Attribute.objects.order_by('path')
    serializer_class = AttributeSerializer

    @list_route()
    def nested(self, request):
        queryset = Attribute.objects.get_cached_trees()
        serializer = AttributeNestedSerializer(queryset, many=True)
        return Response(serializer.data)

    @list_route()
    def index(self, request):
        queryset = Attribute.objects.order_by('path')
        serializer = AttributeIndexSerializer(queryset, many=True)
        return Response(serializer.data)


class AttributeApiViewSet(ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission, )
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    queryset = Attribute.objects.order_by('path')
    serializer_class = AttributeApiSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = (
        'uri',
        'path',
        'key',
        'parent'
    )
