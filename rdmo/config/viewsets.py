
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from django_filters.rest_framework import DjangoFilterBackend

from rdmo.core.filters import SearchFilter
from rdmo.core.permissions import HasModelPermission, HasObjectPermission
from rdmo.management.viewsets import ElementToggleCurrentSiteViewSetMixin

from .models import Plugin
from .serializers.v1 import PluginIndexSerializer, PluginSerializer


class PluginViewSet(ElementToggleCurrentSiteViewSetMixin, ModelViewSet):
    permission_classes = (HasModelPermission | HasObjectPermission, )
    serializer_class = PluginSerializer
    queryset = (
        Plugin
            .objects
            .prefetch_related('catalogs', 'sites', 'editors', 'groups')
            .order_by('uri')
    )

    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('uri', 'title')
    filterset_fields = (
        'uri',
        'uri_prefix',
        'uri_path',
        'comment',
        'sites',
        'editors'
    )

    @action(detail=False)
    def index(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = PluginIndexSerializer(queryset, many=True)
        return Response(serializer.data)
