from django.db import models

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
from rdmo.management.viewsets import ElementToggleCurrentSiteViewSetMixin

from .constants import TaskAreas, TaskTypes
from .models import Task
from .renderers import TaskRenderer
from .serializers.export import TaskExportSerializer
from .serializers.v1 import TaskIndexSerializer, TaskSerializer


class TaskViewSet(ElementToggleCurrentSiteViewSetMixin, ModelViewSet):
    permission_classes = (HasModelPermission | HasObjectPermission, )
    serializer_class = TaskSerializer

    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('uri', 'title')
    filterset_fields = (
        'uri',
        'uri_prefix',
        'uri_path',
        'comment',
        'sites',
        'editors',
        'task_type'
    )

    def get_queryset(self):
        queryset = Task.objects.all().order_by('uri')
        if self.action in ['index']:
            return queryset
        elif self.action in ['export', 'detail_export']:
            return queryset.prefetch_related(
                'catalogs',
                'conditions',
            )
        else:
            return queryset.select_related(
                'start_attribute',
                'end_attribute'
            ).prefetch_related(
                'catalogs',
                'sites',
                'editors',
                'groups',
                'conditions'
            ).annotate(
                projects_count=models.Count('projects')
            )

    @action(detail=False)
    def index(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = TaskIndexSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path='export(?:/(?P<export_format>[a-z]+))?')
    def export(self, request, export_format='xml'):
        queryset = self.filter_queryset(self.get_queryset())
        if export_format == 'xml':
            serializer = TaskExportSerializer(
                queryset,
                many=True,
                context=self.get_export_serializer_context(queryset),
            )
            xml = TaskRenderer().render(serializer.data, context=self.get_export_flags())
            return XMLResponse(xml, name='tasks')
        else:
            return render_to_format(self.request, export_format, 'tasks', 'tasks/export/tasks.html', {
                'tasks': queryset
            })

    @action(detail=True, url_path='export(?:/(?P<export_format>[a-z]+))?')
    def detail_export(self, request, pk=None, export_format='xml'):
        instance = self.get_object()
        if export_format == 'xml':
            serializer = TaskExportSerializer(
                instance,
                context=self.get_export_serializer_context([instance]),
            )
            xml = TaskRenderer().render([serializer.data], context=self.get_export_flags())
            return XMLResponse(xml, name=instance.uri_path)
        else:
            return render_to_format(
                self.request, export_format, instance.uri_path, 'tasks/export/tasks.html', {
                    'tasks': [instance]
                }
            )

    def get_export_flags(self):
        full = is_truthy(self.request.GET.get('full'))
        return {
            'conditions': full or is_truthy(self.request.GET.get('conditions')),
            'attributes': full or is_truthy(self.request.GET.get('attributes')),
            'options': full or is_truthy(self.request.GET.get('options'))
        }

    def get_export_serializer_context(self, tasks):
        attribute_ids = set()
        for task in tasks:
            if task.start_attribute:
                attribute_ids.add(task.start_attribute_id)
            if task.end_attribute:
                attribute_ids.add(task.end_attribute_id)
            for condition in task.conditions.all():
                attribute_ids.add(condition.source_id)

        return {
            'attribute_map': Attribute.objects.get_queryset_ancestors(
                Attribute.objects.filter(id__in=attribute_ids),
                include_self=True
            ).in_bulk()
        }


class TaskTypeViewSet(ChoicesViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = TaskTypes.choices


class TaskAreaViewSet(ChoicesViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = TaskAreas.choices
