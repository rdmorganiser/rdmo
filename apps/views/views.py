from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.translation import ugettext_lazy as _

from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.decorators import list_route
from rest_framework.response import Response

from apps.core.utils import render_to_format

from .models import View
from .serializers import ViewSerializer, ViewIndexSerializer, ExportSerializer
from .renderers import XMLRenderer


@staff_member_required
def views(request):
    return render(request, 'views/views.html', {
        'export_formats': settings.EXPORT_FORMATS
    })


@staff_member_required
def views_export(request, format):
    return render_to_format(request, format, _('Views'), 'views/views_export.html', {
        'views': View.objects.all()
    })


@staff_member_required
def views_export_xml(request):
    queryset = View.objects.all()
    serializer = ExportSerializer(queryset, many=True)

    response = HttpResponse(XMLRenderer().render(serializer.data), content_type="application/xml")
    response['Content-Disposition'] = 'filename="views.xml"'
    return response


class ViewViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, IsAuthenticated)

    queryset = View.objects.all()
    serializer_class = ViewSerializer

    @list_route()
    def index(self, request):
        queryset = View.objects.all()
        serializer = ViewIndexSerializer(queryset, many=True)
        return Response(serializer.data)
