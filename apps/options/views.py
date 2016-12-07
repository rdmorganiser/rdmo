from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.translation import ugettext_lazy as _

from rest_framework import viewsets, mixins, filters
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.decorators import list_route
from rest_framework.response import Response

from apps.core.serializers import ChoicesSerializer
from apps.core.utils import render_to_format

from apps.options.models import OptionSet
from apps.conditions.models import Condition

from .models import *
from .serializers import *
from .renderers import *


@staff_member_required
def options(request):
    return render(request, 'options/options.html', {
        'export_formats': settings.EXPORT_FORMATS
    })


@staff_member_required
def options_export(request, format):
    return render_to_format(request, format, _('Options'), 'options/options_export.html', {
        'options': OptionSet.objects.all()
    })


@staff_member_required
def options_export_xml(request):
    queryset = OptionSet.objects.all()
    serializer = ExportSerializer(queryset, many=True)
    return HttpResponse(XMLRenderer().render(serializer.data), content_type="application/xml")


class OptionSetViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, IsAuthenticated)

    queryset = OptionSet.objects.order_by('order')
    serializer_class = OptionSetSerializer

    @list_route()
    def index(self, request):
        queryset = OptionSet.objects.all()
        serializer = OptionSetIndexSerializer(queryset, many=True)
        return Response(serializer.data)


class OptionViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, IsAuthenticated)

    queryset = Option.objects.order_by('order')
    serializer_class = OptionSerializer


class ConditionViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (DjangoModelPermissions, IsAuthenticated)

    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer
