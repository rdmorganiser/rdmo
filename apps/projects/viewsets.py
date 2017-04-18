from django.utils.translation import ugettext_lazy as _

from rest_framework import viewsets, filters
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.exceptions import ValidationError

from rest_framework_extensions.cache.mixins import RetrieveCacheResponseMixin

from apps.core.permissions import HasObjectPermission
from apps.conditions.models import Condition
from apps.questions.models import Catalog, QuestionEntity

from .models import Project, Membership, Snapshot, Value
from .serializers import (
    ProjectSerializer,
    ValueSerializer,
    QuestionEntitySerializer,
    CatalogSerializer
)


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)


class ValueViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, HasObjectPermission)
    serializer_class = ValueSerializer

    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = (
        'attribute',
        'attribute__parent_collection',
        'set_index'
    )

    permission_required = {
        'view': 'projects.view_value',
        'add': 'projects.add_value',
        'change': 'projects.change_value',
        'delete': 'projects.delete_value'
    }

    def get_queryset(self):
        return Value.objects.filter(project=self.project, snapshot=self.snapshot) \
            .order_by('set_index', 'collection_index')

    def get_project(self, request):
        project_id = request.GET.get('project')

        if project_id is None:
            raise ValidationError({'project': [_('This field is required.')]})
        else:
            try:
                return Project.objects.get(pk=project_id)
            except Project.DoesNotExist as e:
                raise ValidationError({'project': [e.message]})

    def get_snapshot(self, request):
        snapshot_id = request.GET.get('snapshot')

        if snapshot_id is None:
            return None
        else:
            try:
                return self.project.snapshots.get(pk=snapshot_id)
            except Snapshot.DoesNotExist as e:
                raise ValidationError({'snapshot': [e.message]})

    def get_condition(self, request):
        condition_id = request.GET.get('condition')

        if condition_id is None:
            raise ValidationError({'condition': [_('This field is required.')]})
        else:
            try:
                return Condition.objects.get(pk=condition_id)
            except Condition.DoesNotExist as e:
                raise ValidationError({'condition': [e.message]})

    def get_permission_object(self):
        return self.project

    def dispatch(self, request, *args, **kwargs):
        self.project = self.get_project(request)
        self.snapshot = self.get_snapshot(request)

        return super(ValueViewSet, self).dispatch(request, *args, **kwargs)

    @list_route()
    def resolve(self, request):
        if not request.user.has_perm('projects.view_value', self.project):
            self.permission_denied(request)

        condition = self.get_condition(request)
        return Response({'result': condition.resolve(self.project, self.snapshot)})


class QuestionEntityViewSet(RetrieveCacheResponseMixin, viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated, DjangoModelPermissions)

    queryset = QuestionEntity.objects.filter(question__parent=None)
    serializer_class = QuestionEntitySerializer

    @list_route(methods=['get'], permission_classes=[DjangoModelPermissions])
    def first(self, request, pk=None):
        try:
            catalog = Catalog.objects.get(pk=request.GET.get('catalog'))
            entity = QuestionEntity.objects.order_by_catalog(catalog).first()
            serializer = self.get_serializer(entity)
            return Response(serializer.data)
        except Catalog.DoesNotExist as e:
            return Response({'message': e.message}, status=HTTP_404_NOT_FOUND)

    @detail_route(methods=['get'], permission_classes=[DjangoModelPermissions])
    def prev(self, request, pk=None):
        try:
            return Response({'id': QuestionEntity.objects.get_prev(pk).pk})
        except QuestionEntity.DoesNotExist as e:
            return Response({'message': e.message}, status=HTTP_404_NOT_FOUND)

    @detail_route(methods=['get'], permission_classes=[DjangoModelPermissions])
    def next(self, request, pk=None):
        try:
            return Response({'id': QuestionEntity.objects.get_next(pk).pk})
        except QuestionEntity.DoesNotExist as e:
            return Response({'message': e.message}, status=HTTP_404_NOT_FOUND)


class CatalogViewSet(RetrieveCacheResponseMixin, viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer
