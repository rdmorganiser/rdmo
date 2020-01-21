from django_filters.rest_framework import DjangoFilterBackend
from rdmo.core.permissions import HasModelPermission
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import View
from .serializers.v1 import ViewIndexSerializer, ViewSerializer


class ViewViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = View.objects.all()
    serializer_class = ViewSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'uri',
        'key',
        'comment'
    )

    @action(detail=False)
    def index(self, request):
        serializer = ViewIndexSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)
