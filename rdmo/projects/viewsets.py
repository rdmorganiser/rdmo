from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rdmo.conditions.models import Condition
from rdmo.core.permissions import HasModelPermission, HasObjectPermission
from rdmo.questions.models import Catalog, QuestionSet
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.mixins import (CreateModelMixin, ListModelMixin,
                                   RetrieveModelMixin, UpdateModelMixin)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import (GenericViewSet, ModelViewSet,
                                     ReadOnlyModelViewSet)
from rest_framework_extensions.cache.mixins import RetrieveCacheResponseMixin
from rest_framework_extensions.mixins import NestedViewSetMixin

from .filters import ValueFilterBackend
from .models import Membership, Project, Snapshot, Value
from .serializers.v1 import (MembershipSerializer, ProjectMembershipSerializer,
                             ProjectSerializer, ProjectSnapshotSerializer,
                             ProjectValueSerializer, SnapshotSerializer,
                             ValueSerializer)
from .serializers.v1.catalog import CatalogSerializer
from .serializers.v1.questionset import QuestionSetSerializer


class ProjectViewSet(ModelViewSet):
    permission_classes = (HasModelPermission | HasObjectPermission, )
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'title',
        'user',
        'user__username',
        'catalog',
        'catalog__uri',
        'catalog__key',
    )

    @action(detail=True, permission_classes=(HasModelPermission | HasObjectPermission, ))
    def resolve(self, request, pk=None):
        try:
            condition = Condition.objects.get(pk=request.GET.get('condition'))
            return Response({'result': condition.resolve(self.get_object(), None)})
        except Condition.DoesNotExist:
            return Response({'result': False})


class ProjectNestedViewSetMixin(NestedViewSetMixin):

    def initial(self, request, *args, **kwargs):
        self.project = self.get_project_from_parent_viewset()
        super().initial(request, *args, **kwargs)

    def get_project_from_parent_viewset(self):
        try:
            return Project.objects.get(pk=self.get_parents_query_dict().get('project'))
        except Project.DoesNotExist:
            raise Http404

    def get_permission_object(self):
        return self.project

    def perform_create(self, serializer):
        serializer.save(project=self.project)


class ProjectMembershipViewSet(ProjectNestedViewSetMixin, ModelViewSet):
    permission_classes = (HasModelPermission | HasObjectPermission, )
    queryset = Membership.objects.all()
    serializer_class = ProjectMembershipSerializer

    filter_backends = (DjangoFilterBackend, )
    filterset_fields = (
        'user',
        'user__username',
        'role'
    )


class ProjectSnapshotViewSet(ProjectNestedViewSetMixin, CreateModelMixin, RetrieveModelMixin,
                             UpdateModelMixin, ListModelMixin, GenericViewSet):
    permission_classes = (HasModelPermission | HasObjectPermission, )
    queryset = Snapshot.objects.all()
    serializer_class = ProjectSnapshotSerializer


class ProjectValueViewSet(ProjectNestedViewSetMixin, ModelViewSet):
    permission_classes = (HasModelPermission | HasObjectPermission, )
    queryset = Value.objects.filter(snapshot=None)
    serializer_class = ProjectValueSerializer

    filter_backends = (ValueFilterBackend, DjangoFilterBackend)
    filterset_fields = (
        'snapshot',
        'attribute',
        'attribute__path',
        'option',
        'option__path',
    )


class MembershipViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'user',
        'user__username',
        'role'
    )


class SnapshotViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin,
                      ListModelMixin, GenericViewSet):
    permission_classes = (HasModelPermission, )
    queryset = Snapshot.objects.all()
    serializer_class = SnapshotSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'title',
        'project'
    )


class ValueViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = Value.objects.all()
    serializer_class = ValueSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'project',
        'snapshot',
        'attribute',
        'attribute__path',
        'option',
        'option__path',
    )


class QuestionSetViewSet(RetrieveCacheResponseMixin, ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated, )

    queryset = QuestionSet.objects.all()
    serializer_class = QuestionSetSerializer

    @action(detail=False, permission_classes=(IsAuthenticated, ))
    def first(self, request, pk=None):
        try:
            catalog = Catalog.objects.get(pk=request.GET.get('catalog'))
            questionset = QuestionSet.objects.order_by_catalog(catalog).first()
            serializer = self.get_serializer(questionset)
            return Response(serializer.data)
        except Catalog.DoesNotExist:
            raise NotFound()

    @action(detail=True, permission_classes=(IsAuthenticated, ))
    def prev(self, request, pk=None):
        try:
            return Response({'id': QuestionSet.objects.get_prev(pk).pk})
        except QuestionSet.DoesNotExist:
            raise NotFound()

    @action(detail=True, permission_classes=(IsAuthenticated, ))
    def next(self, request, pk=None):
        try:
            return Response({'id': QuestionSet.objects.get_next(pk).pk})
        except QuestionSet.DoesNotExist:
            raise NotFound()


class CatalogViewSet(RetrieveCacheResponseMixin, ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer
