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
from apps.core.utils import render_to_format, render_to_csv

from apps.conditions.models import Condition

from .models import *
from .serializers import *
from .renderers import *


@staff_member_required
def domain(request):
    return render(request, 'domain/domain.html', {
        'export_formats': settings.EXPORT_FORMATS
    })


@staff_member_required
def domain_export(request, format):
    return render_to_format(request, format, _('Domain'), 'domain/domain_export.html', {
        'entities': AttributeEntity.objects.order_by('label')
    })


@staff_member_required
def domain_export_csv(request):
    return render_to_csv(request, _('Domain'), AttributeEntity.objects.order_by('label').values_list())


@staff_member_required
def domain_export_xml(request):
    queryset = AttributeEntity.objects.filter(is_attribute=False)
    serializer = ExportSerializer(queryset, many=True)
    return HttpResponse(XMLRenderer().render(serializer.data), content_type="application/xml")


class AttributeEntityViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = AttributeEntity.objects.filter(is_attribute=False)
    serializer_class = AttributeEntitySerializer

    @list_route()
    def nested(self, request):
        queryset = AttributeEntity.objects.get_cached_trees()
        serializer = AttributeEntityNestedSerializer(queryset, many=True)
        return Response(serializer.data)

    @list_route()
    def index(self, request):
        queryset = AttributeEntity.objects.filter(is_attribute=False)
        serializer = AttributeEntityIndexSerializer(queryset, many=True)
        return Response(serializer.data)


class AttributeViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = Attribute.objects.order_by('label')
    serializer_class = AttributeSerializer

    filter_backends = (filters.DjangoFilterBackend, )
    filter_fields = ('label', 'parent_collection')

    @list_route()
    def index(self, request):
        queryset = Attribute.objects.all()
        serializer = AttributeIndexSerializer(queryset, many=True)
        return Response(serializer.data)


class OptionViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = Option.objects.order_by('order')
    serializer_class = OptionSerializer

    filter_backends = (filters.DjangoFilterBackend, )
    filter_fields = ('attribute', )

    @list_route()
    def index(self, request):
        queryset = Option.objects.all()
        serializer = OptionIndexSerializer(queryset, many=True)
        return Response(serializer.data)


class RangeViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    filter_backends = (filters.DjangoFilterBackend, )
    filter_fields = ('attribute', )

    queryset = Range.objects.order_by('attribute__label')
    serializer_class = RangeSerializer


class VerboseNameViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    filter_backends = (filters.DjangoFilterBackend, )
    filter_fields = ('attribute_entity', )

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
