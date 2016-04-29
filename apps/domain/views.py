from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets, mixins, filters
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated

from .models import *
from .serializers import *


@login_required()
def domain(request):
    return render(request, 'domain/domain.html')


class AttributeEntityViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = AttributeEntity.objects.filter(attribute__attributeset=None).order_by('tag')
    serializer_class = AttributeEntitySerializer


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


class ValueTypeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )

    serializer_class = ValueTypeSerializer

    def get_queryset(self):
        return Attribute.VALUE_TYPE_CHOICES
