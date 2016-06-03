from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

from rest_framework import viewsets, mixins, filters
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated

from apps.core.serializers import ChoicesSerializer

from .models import *
from .serializers import *


@staff_member_required
def domain(request):
    return render(request, 'domain/domain.html')


class AttributeEntityViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = AttributeEntity.objects.filter(parent_entity=None)
    serializer_class = AttributeEntitySerializer


class AttributeViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = Attribute.objects.order_by('full_title')
    serializer_class = AttributeSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    filter_fields = ('full_title', )


class OptionViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = Option.objects.all()
    serializer_class = OptionSerializer


class ConditionViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer


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
