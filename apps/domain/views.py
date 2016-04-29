from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.xmlutils import SimplerXMLGenerator
from django.utils.six.moves import StringIO
from django.utils.encoding import smart_text

from rest_framework import viewsets, mixins, filters
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated

from .models import *
from .serializers import *


@login_required()
def domain(request):
    return render(request, 'domain/domain.html')


@login_required()
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


class AttributeViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    filter_fields = ('tag', )


class AttributeSetViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = AttributeSet.objects.all()
    serializer_class = AttributeSetSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    filter_fields = ('tag', )


class AttributeEntityViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = AttributeEntity.objects.filter(attribute__attributeset=None).order_by('tag')
    serializer_class = AttributeEntitySerializer


class ValueTypeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )

    serializer_class = ValueTypeSerializer

    def get_queryset(self):
        return Attribute.VALUE_TYPE_CHOICES
