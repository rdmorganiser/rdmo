from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.filters import DjangoFilterBackend
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from rdmo.core.permissions import HasModelPermission

from rdmo.conditions.models import Condition

from .models import OptionSet, Option
from .serializers import (
    OptionSetIndexSerializer,
    OptionSetSerializer,
    OptionSerializer,
    ConditionSerializer
)
from .serializers.api import (
    OptionSetSerializer as OptionSetApiSerializer,
    OptionSerializer as OptionApiSerializer,
)


class OptionSetViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )

    queryset = OptionSet.objects.order_by('order')
    serializer_class = OptionSetSerializer

    @list_route()
    def index(self, request):
        queryset = OptionSet.objects.all()
        serializer = OptionSetIndexSerializer(queryset, many=True)
        return Response(serializer.data)


class OptionViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )

    queryset = Option.objects.order_by('order')
    serializer_class = OptionSerializer


class ConditionViewSet(ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission, )

    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer


class OptionSetApiViewSet(ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission, )
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    queryset = OptionSet.objects.all()
    serializer_class = OptionSetApiSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = (
        'uri',
        'key'
    )


class OptionApiViewSet(ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission, )
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    queryset = Option.objects.all()
    serializer_class = OptionApiSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = (
        'uri',
        'path',
        'key',
        'optionset'
    )
