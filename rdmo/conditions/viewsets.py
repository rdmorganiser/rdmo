from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.filters import DjangoFilterBackend
from rest_framework.decorators import list_route, detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from rdmo.core.views import ChoicesViewSet
from rdmo.core.permissions import HasModelPermission

from rdmo.domain.models import Attribute
from rdmo.options.models import OptionSet
from rdmo.projects.models import Snapshot

from .models import Condition
from .serializers import (
    ConditionSerializer,
    ConditionIndexSerializer,
    AttributeSerializer,
    OptionSetSerializer
)
from .serializers.api import (
    ConditionSerializer as ConditionApiSerializer,
)


class ConditionViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )

    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer

    @list_route()
    def index(self, request):
        queryset = Condition.objects.all()
        serializer = ConditionIndexSerializer(queryset, many=True)
        return Response(serializer.data)

    @detail_route()
    def resolve(self, request, pk):
        snapshot_id = request.GET.get('snapshot')

        if snapshot_id is None:
            return Response(status=HTTP_400_BAD_REQUEST)

        try:
            condition = Condition.objects.get(pk=pk)
        except Condition.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)

        snapshot = Snapshot.objects.filter(project__user=request.user).get(pk=snapshot_id)

        result = condition.resolve(snapshot)
        return Response({'result': result})


class AttributeViewSet(ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer


class OptionSetViewSet(ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = OptionSet.objects.order_by('order')
    serializer_class = OptionSetSerializer


class RelationViewSet(ChoicesViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Condition.RELATION_CHOICES


class ConditionApiViewSet(ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission, )
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    queryset = Condition.objects.all()
    serializer_class = ConditionApiSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = (
        'uri',
        'key',
        'source',
        'relation',
        'target_text',
        'target_option'
    )
