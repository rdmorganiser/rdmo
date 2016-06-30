from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.xmlutils import SimplerXMLGenerator
from django.utils.six.moves import StringIO
from django.utils.encoding import smart_text

from rest_framework import viewsets, mixins, filters
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer

from apps.core.serializers import ChoicesSerializer

from .models import *
from .serializers import *
from .renderers import *


@staff_member_required
def domain(request):
    return render(request, 'domain/domain.html')


@staff_member_required
def domain_export(request):
    attributes = Attribute.objects.all()

    stream = StringIO()
    xml = SimplerXMLGenerator(stream, "utf-8")
    xml.startDocument()
    xml.startElement('attributes', {})

    for attribute in attributes:
        xml.startElement('attribute', {
            'tag': attribute.tag,
            'is_collection': str(attribute.is_collection).lower()
        })
        xml.endElement('attribute')

    xml.endElement('attributes')
    xml.endDocument()

    return HttpResponse(stream.getvalue(), content_type="application/xml")


class AttributeEntityViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, XMLRenderer)

    def get_queryset(self):
        queryset = AttributeEntity.objects

        if self.request.GET.get('nested'):
            queryset = queryset.filter(parent_entity=None)

        attributes = self.request.GET.get('attributes')
        if attributes in ['0', 'false']:
            queryset = queryset.filter(attribute=None)

        return queryset

    def get_serializer_class(self):
        if self.request.GET.get('nested'):
            return NestedAttributeEntitySerializer
        else:
            return AttributeEntitySerializer


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


class RangeViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = Range.objects.order_by('attribute__full_title')
    serializer_class = RangeSerializer


class ConditionViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer


class VerboseNameViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = VerboseName.objects.all()
    serializer_class = VerboseNameSerializer


class ValueTypeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )

    serializer_class = ChoicesSerializer

    def get_queryset(self):
        return Attribute.VALUE_TYPE_CHOICES


class RelationViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )

    serializer_class = ChoicesSerializer

    def get_queryset(self):
        return Condition.RELATION_CHOICES
