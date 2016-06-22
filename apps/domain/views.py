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
