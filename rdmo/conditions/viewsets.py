from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from django_filters.rest_framework import DjangoFilterBackend

from rdmo.core.exports import XMLResponse
from rdmo.core.filters import SearchFilter
from rdmo.core.permissions import HasModelPermission, HasObjectPermission
from rdmo.core.utils import is_truthy, render_to_format
from rdmo.core.views import ChoicesViewSet
from rdmo.domain.models import Attribute

from .models import Condition
from .renderers import ConditionRenderer
from .serializers.export import ConditionExportSerializer
from .serializers.v1 import ConditionIndexSerializer, ConditionSerializer


def get_attributes_by_id():
    attributes = list(Attribute.objects.all())
    return {attribute.pk: attribute for attribute in attributes}


class ConditionViewSet(ModelViewSet):
    permission_classes = (HasModelPermission | HasObjectPermission, )
    serializer_class = ConditionSerializer

    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('uri', )
    filterset_fields = (
        'uri',
        'uri_prefix',
        'uri_path',
        'source',
        'relation',
        'target_text',
        'target_option'
    )

    def get_queryset(self):
        queryset = Condition.objects.all()
        if self.action in ['index']:
            return queryset
        elif self.action in ['export', 'detail_export']:
            return queryset.select_related(
                'source',
                'source__parent',
                'target_option'
            ).prefetch_related(
                'optionsets',
                'pages',
                'questionsets',
                'questions',
                'tasks',
                'editors'
            )
        else:
            return queryset.select_related(
                'source',
                'target_option'
            ).prefetch_related(
                'optionsets',
                'pages',
                'questionsets',
                'questions',
                'tasks',
                'editors'
            )

    @action(detail=False)
    def index(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = ConditionIndexSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path='export(?:/(?P<export_format>[a-z]+))?')
    def export(self, request, export_format='xml'):
        queryset = self.filter_queryset(self.get_queryset())
        if export_format == 'xml':
            conditions = list(queryset)
            context = self.get_export_renderer_context(request, attributes_by_id=True)
            serializer = ConditionExportSerializer(conditions, many=True, context=context)
            xml = ConditionRenderer().render(serializer.data, context=context)
            return XMLResponse(xml, name='conditions')
        else:
            return render_to_format(self.request, export_format, 'conditions', 'conditions/export/conditions.html', {
                'conditions': queryset
            })

    @action(detail=True, url_path='export(?:/(?P<export_format>[a-z]+))?')
    def detail_export(self, request, pk=None, export_format='xml'):
        condition = self.get_object()
        if export_format == 'xml':
            context = self.get_export_renderer_context(request)
            serializer = ConditionExportSerializer(condition, context=context)
            xml = ConditionRenderer().render([serializer.data], context=context)
            return XMLResponse(xml, name=condition.uri_path)
        else:
            return render_to_format(
                self.request, export_format, condition.uri_path, 'conditions/export/conditions.html', {
                    'conditions': [condition]
                }
            )

    def get_export_renderer_context(self, request, attributes_by_id=False):
        full = is_truthy(request.GET.get('full'))
        context = {
            'attributes': full or is_truthy(request.GET.get('attributes')),
            'options': full or is_truthy(request.GET.get('options')),
        }
        if attributes_by_id:
            context['attributes_by_id'] = get_attributes_by_id()
        return context


class RelationViewSet(ChoicesViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Condition.RELATION_CHOICES
