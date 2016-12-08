from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.translation import ugettext_lazy as _

from rest_framework import viewsets, mixins, filters
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from apps.core.utils import render_to_format

from apps.core.serializers import ChoicesSerializer
from apps.domain.models import Attribute
from apps.options.models import OptionSet
from apps.conditions.models import Condition
from apps.projects.models import Snapshot

from .models import *
from .serializers import *
from .renderers import *


@staff_member_required
def conditions(request):
    return render(request, 'conditions/conditions.html', {
        'export_formats': settings.EXPORT_FORMATS
    })


@staff_member_required
def conditions_export(request, format):
    return render_to_format(request, format, _('Conditions'), 'conditions/conditions_export.html', {
        'conditions': Condition.objects.all()
    })


@staff_member_required
def conditions_export_xml(request):
    queryset = Condition.objects.all()
    serializer = ExportSerializer(queryset, many=True)
    return HttpResponse(XMLRenderer().render(serializer.data), content_type="application/xml")


class ConditionViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer

    @list_route()
    def index(self, request):
        queryset = Condition.objects.all()
        serializer = ConditionIndexSerializer(queryset, many=True)
        return Response(serializer.data)

    @detail_route()
    def resolve(self, request, pk):
        snapshot_id = request.GET.get('snapshot')

        if snapshot_id is None:
            return Response(status=HTTP_400_BAD_REQUEST)

        try:
            condition = Condition.objects.get(pk=pk)
        except Condition.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)

        snapshot = Snapshot.objects.filter(project__owner=request.user).get(pk=snapshot_id)

        result = condition.resolve(snapshot)
        return Response({'result': result})


class AttributeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer


class OptionSetViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = OptionSet.objects.order_by('order')
    serializer_class = OptionSetSerializer


class RelationViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )

    serializer_class = ChoicesSerializer

    def get_queryset(self):
        return Condition.RELATION_CHOICES
