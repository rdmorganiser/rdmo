from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.filters import DjangoFilterBackend
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from rdmo.core.permissions import HasModelPermission

from .models import View
from .serializers import ViewSerializer, ViewIndexSerializer
from .serializers.api import ViewSerializer as ViewApiSerializer


class ViewViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = View.objects.all()
    serializer_class = ViewSerializer

    @list_route()
    def index(self, request):
        queryset = View.objects.all()
        serializer = ViewIndexSerializer(queryset, many=True)
        return Response(serializer.data)


class ViewApiViewSet(ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission, )
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    queryset = View.objects.all()
    serializer_class = ViewApiSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = (
        'uri',
        'key'
    )
