from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from rest_framework import viewsets, mixins
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.decorators import list_route
from rest_framework.response import Response

from apps.core.utils import render_to_format

from .models import *
from .serializers import *


@staff_member_required
def tasks(request):
    return render(request, 'tasks/tasks.html', {
        'export_formats': settings.EXPORT_FORMATS
    })


@staff_member_required
def tasks_export(request, catalog_id, format):
    return render(request, 'tasks/tasks.html', {
        'export_formats': settings.EXPORT_FORMATS
    })


class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @list_route()
    def index(self, request):
        queryset = Task.objects.all()
        serializer = TaskIndexSerializer(queryset, many=True)
        return Response(serializer.data)
