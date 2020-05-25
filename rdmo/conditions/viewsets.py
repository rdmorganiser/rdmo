from django_filters.rest_framework import DjangoFilterBackend
from rdmo.core.permissions import HasModelPermission
from rdmo.core.views import ChoicesViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Condition
from .serializers.v1 import ConditionIndexSerializer, ConditionSerializer


class ConditionViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'uri',
        'key',
        'source',
        'relation',
        'target_text',
        'target_option'
    )

    @action(detail=False)
    def index(self, request):
        queryset = self.get_queryset()
        serializer = ConditionIndexSerializer(queryset, many=True)
        return Response(serializer.data)


class RelationViewSet(ChoicesViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Condition.RELATION_CHOICES
