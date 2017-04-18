from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import list_route
from rest_framework.response import Response

from apps.core.permissions import HasModelPermission

from .models import View
from .serializers import ViewSerializer, ViewIndexSerializer


class ViewViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = View.objects.all()
    serializer_class = ViewSerializer

    @list_route()
    def index(self, request):
        queryset = View.objects.all()
        serializer = ViewIndexSerializer(queryset, many=True)
        return Response(serializer.data)
