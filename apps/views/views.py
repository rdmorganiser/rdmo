from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from rest_framework import viewsets, mixins
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.decorators import list_route
from rest_framework.response import Response

from apps.core.utils import render_to_format

from apps.core.serializers import ChoicesSerializer
from apps.domain.models import Attribute, Option

from .models import *
from .serializers import *


@staff_member_required
def views(request):
    return render(request, 'views/views.html', {
        'export_formats': settings.EXPORT_FORMATS
    })


class ViewViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = View.objects.all()
    serializer_class = ViewSerializer

    @list_route()
    def index(self, request):
        queryset = View.objects.all()
        serializer = ViewIndexSerializer(queryset, many=True)
        return Response(serializer.data)
