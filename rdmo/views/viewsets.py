from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from rdmo.core.exports import XMLResponse
from rdmo.core.permissions import HasModelPermission
from rdmo.core.viewsets import CopyModelMixin

from .models import View
from .renderers import ViewRenderer
from .serializers.export import ViewExportSerializer
from .serializers.v1 import ViewIndexSerializer, ViewSerializer


class ViewViewSet(CopyModelMixin, ModelViewSet):
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

    @action(detail=False, permission_classes=[HasModelPermission])
    def export(self, request):
        serializer = ViewExportSerializer(self.get_queryset(), many=True)
        xml = ViewRenderer().render(serializer.data)
        return XMLResponse(xml, name='views')

    @action(detail=True, url_path='export', permission_classes=[HasModelPermission])
    def detail_export(self, request, pk=None):
        serializer = ViewExportSerializer(self.get_object())
        xml = ViewRenderer().render([serializer.data])
        return XMLResponse(xml, name=self.get_object().key)
