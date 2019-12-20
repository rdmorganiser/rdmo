from django_filters.rest_framework import DjangoFilterBackend
from rdmo.core.permissions import HasModelPermission
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Attribute
from .serializers.v1 import AttributeSerializer, NestedAttributeSerializer


class AttributeViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = Attribute.objects.order_by('path')
    serializer_class = AttributeSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'uri',
        'path',
        'key',
        'parent'
    )

    @action(detail=False)
    def nested(self, request):
        queryset = Attribute.objects.get_cached_trees()
        serializer = NestedAttributeSerializer(queryset, many=True)
        return Response(serializer.data)
