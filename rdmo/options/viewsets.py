from django_filters.rest_framework import DjangoFilterBackend
from rdmo.core.permissions import HasModelPermission
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Option, OptionSet
from .serializers.v1 import (OptionIndexSerializer, OptionSerializer,
                             OptionSetIndexSerializer,
                             OptionSetNestedSerializer, OptionSetSerializer)


class OptionSetViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = OptionSet.objects.order_by('order')
    serializer_class = OptionSetSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'uri',
        'key',
        'comment'
    )

    @action(detail=False)
    def nested(self, request):
        serializer = OptionSetNestedSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    @action(detail=False)
    def index(self, request):
        serializer = OptionSetIndexSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)


class OptionViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = Option.objects.order_by('optionset__order', 'order')
    serializer_class = OptionSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'uri',
        'key',
        'optionset',
        'comment'
    )

    @action(detail=False)
    def index(self, request):
        serializer = OptionIndexSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)
