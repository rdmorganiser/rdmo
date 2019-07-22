from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from rdmo.core.permissions import HasModelPermission

from .models import View
from .serializers.v1 import ViewSerializer, ViewIndexSerializer


class ViewViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = View.objects.all()
    serializer_class = ViewSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = (
        'uri',
        'key'
    )

    @action(detail=False)
    def index(self, request):
        serializer = ViewIndexSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)
