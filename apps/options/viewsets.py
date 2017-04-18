from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import list_route
from rest_framework.response import Response

from apps.core.permissions import HasModelPermission

from apps.conditions.models import Condition

from .models import OptionSet, Option
from .serializers import (
    OptionSetIndexSerializer,
    OptionSetSerializer,
    OptionSerializer,
    ConditionSerializer
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
