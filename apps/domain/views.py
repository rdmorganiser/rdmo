from django.conf import settings
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, ListView

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.filters import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import list_route
from rest_framework.response import Response

from apps.core.views import ModelPermissionMixin, ChoicesViewSet
from apps.core.utils import render_to_format, render_to_csv
from apps.core.permissions import HasModelPermission

from apps.options.models import OptionSet
from apps.conditions.models import Condition

from .models import AttributeEntity, Attribute, VerboseName, Range
from .serializers import (
    AttributeEntitySerializer,
    AttributeEntityNestedSerializer,
    AttributeEntityIndexSerializer,
    AttributeSerializer,
    AttributeIndexSerializer,
    RangeSerializer,
    VerboseNameSerializer,
    OptionSetSerializer,
    ConditionSerializer,
    ExportSerializer
)
from .renderers import XMLRenderer


class DomainView(ModelPermissionMixin, TemplateView):
    template_name = 'domain/domain.html'
    permission_required = 'domain.view_attributeentity'

    def get_context_data(self, **kwargs):
        context = super(DomainView, self).get_context_data(**kwargs)
        context['export_formats'] = settings.EXPORT_FORMATS
        return context


class DomainExportView(ModelPermissionMixin, ListView):
    model = AttributeEntity
    context_object_name = 'entities'
    permission_required = 'domain.view_attributeentity'

    def get_queryset(self):
        if self.kwargs.get('format') == 'xml':
            return AttributeEntity.objects.filter(parent=None)
        else:
            return AttributeEntity.objects.all()

    def render_to_response(self, context, **response_kwargs):
        format = self.kwargs.get('format')
        if format == 'xml':
            serializer = ExportSerializer(context['entities'], many=True)
            response = HttpResponse(XMLRenderer().render(serializer.data), content_type="application/xml")
            response['Content-Disposition'] = 'filename="domain.xml"'
            return response
        elif format == 'csv':
            rows = []
            for entity in context['entities']:
                rows.append((
                    _('Attribute') if entity.is_attribute else _('Entity'),
                    _('collection') if entity.is_collection else '',
                    entity.key,
                    entity.comment,
                    entity.uri,
                    entity.attribute.value_type if entity.is_attribute else '',
                    entity.attribute.unit if entity.is_attribute else ''
                ))
            return render_to_csv(self.request, _('Domain'), rows)
        else:
            return render_to_format(self.request, format, _('Domain'), 'domain/domain_export.html', context)


class AttributeEntityViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )

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


class AttributeViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )

    queryset = Attribute.objects.order_by('path')
    serializer_class = AttributeSerializer

    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('path', 'parent_collection')

    @list_route()
    def index(self, request):
        queryset = Attribute.objects.all()
        serializer = AttributeIndexSerializer(queryset, many=True)
        return Response(serializer.data)


class RangeViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )

    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('attribute', )

    queryset = Range.objects.order_by('attribute__path')
    serializer_class = RangeSerializer


class VerboseNameViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )

    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('attribute_entity', )

    queryset = VerboseName.objects.all()
    serializer_class = VerboseNameSerializer


class ValueTypeViewSet(ChoicesViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Attribute.VALUE_TYPE_CHOICES


class OptionSetViewSet(ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission, )

    queryset = OptionSet.objects.all()
    serializer_class = OptionSetSerializer


class ConditionViewSet(ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission, )

    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer
