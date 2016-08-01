from django.conf import settings
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.translation import ugettext_lazy as _

from rest_framework import viewsets, mixins, filters
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.decorators import list_route
from rest_framework.response import Response

from apps.core.serializers import ChoicesSerializer
from apps.core.utils import render_to_format, render_to_csv

from apps.conditions.models import Condition

from .models import *
from .serializers import *


@staff_member_required
def domain(request):
    return render(request, 'domain/domain.html', {
        'export_formats': settings.EXPORT_FORMATS
    })


@staff_member_required
def domain_export(request, format):
    return render_to_format(request, 'domain/domain_export.html', {
        'format': format,
        'title': _('Domain'),
        'entities': AttributeEntity.objects.order_by('full_title')
    })


@staff_member_required
def domain_export_csv(request):
    return render_to_csv(request, _('Domain'), AttributeEntity.objects.order_by('full_title').values_list())


class AttributeEntityViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = AttributeEntity.objects.filter(attribute=None)
    serializer_class = AttributeEntitySerializer

    @list_route()
    def nested(self, request):
        queryset = AttributeEntity.objects.filter(parent_entity=None)
        serializer = AttributeEntityNestedSerializer(queryset, many=True)
        return Response(serializer.data)


class AttributeViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = Attribute.objects.order_by('full_title')
    serializer_class = AttributeSerializer

    filter_backends = (filters.DjangoFilterBackend, )
    filter_fields = ('full_title', 'parent_collection')


class OptionViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = Option.objects.order_by('order')
    serializer_class = OptionSerializer

    filter_backends = (filters.DjangoFilterBackend, )
    filter_fields = ('attribute', )


class RangeViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = Range.objects.order_by('attribute__full_title')
    serializer_class = RangeSerializer


class VerboseNameViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = VerboseName.objects.all()
    serializer_class = VerboseNameSerializer


class ValueTypeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )

    serializer_class = ChoicesSerializer

    def get_queryset(self):
        return Attribute.VALUE_TYPE_CHOICES


class ConditionViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer
