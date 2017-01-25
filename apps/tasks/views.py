from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.translation import ugettext_lazy as _

from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.decorators import list_route
from rest_framework.response import Response

from apps.core.serializers import ChoicesSerializer
from apps.core.utils import render_to_format

from apps.conditions.models import Condition
from apps.domain.models import Attribute

from .models import *
from .serializers import *
from .renderers import *


@staff_member_required
def tasks(request):
    return render(request, 'tasks/tasks.html', {
        'export_formats': settings.EXPORT_FORMATS
    })


@staff_member_required
def tasks_export(request, format):
    return render_to_format(request, format, _('Tasks'), 'tasks/tasks_export.html', {
        'tasks': Task.objects.all()
    })


@staff_member_required
def tasks_export_xml(request):
    queryset = Task.objects.all()
    serializer = ExportSerializer(queryset, many=True)

    response = HttpResponse(XMLRenderer().render(serializer.data), content_type="application/xml")
    response['Content-Disposition'] = 'attachment; filename="tasks.xml"'
    return response


class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @list_route()
    def index(self, request):
        queryset = Task.objects.all()
        serializer = TaskIndexSerializer(queryset, many=True)
        return Response(serializer.data)


class AttributeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = Attribute.objects.filter(value_type='datetime')
    serializer_class = AttributeSerializer


class ConditionViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer
