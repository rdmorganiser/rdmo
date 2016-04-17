from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets, filters

from .models import *
from .serializers import *


@login_required()
def domain(request):
    return render(request, 'domain/domain.html')


class AttributeViewSet(viewsets.ModelViewSet):

    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('tag', )


class AttributeSetViewSet(viewsets.ModelViewSet):

    queryset = AttributeSet.objects.all()
    serializer_class = AttributeSetSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('tag', )


class AttributeEntityViewSet(viewsets.ModelViewSet):

    queryset = AttributeEntity.objects.filter(attribute__attributeset=None).order_by('tag')
    serializer_class = AttributeEntitySerializer
