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
def conditions(request):
    return render(request, 'conditions/conditions.html', {
        'export_formats': settings.EXPORT_FORMATS
    })


@staff_member_required
def conditions_export(request, catalog_id, format):
    return render(request, 'conditions/conditions.html', {
        'export_formats': settings.EXPORT_FORMATS
    })


class ConditionViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer

    @list_route()
    def index(self, request):
        queryset = Condition.objects.all()
        serializer = ConditionIndexSerializer(queryset, many=True)
        return Response(serializer.data)


class AttributeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer


class OptionViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = Option.objects.order_by('order')
    serializer_class = OptionSerializer


class RelationViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )

    serializer_class = ChoicesSerializer

    def get_queryset(self):
        return Condition.RELATION_CHOICES
