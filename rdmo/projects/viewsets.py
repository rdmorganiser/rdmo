from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework_extensions.cache.mixins import RetrieveCacheResponseMixin
from rest_framework_extensions.mixins import NestedViewSetMixin

from django_filters.rest_framework import DjangoFilterBackend

from rdmo.core.permissions import HasModelPermission, HasObjectPermission
from rdmo.conditions.models import Condition
from rdmo.questions.models import Catalog, QuestionSet
from rdmo.accounts.utils import is_site_manager

from .models import Project, Membership, Snapshot, Value
from .filters import ValueFilterBackend
from .serializers.v1 import (
    ProjectSerializer,
    ProjectMembershipSerializer,
    ProjectSnapshotSerializer,
    ProjectValueSerializer,
    MembershipSerializer,
    SnapshotSerializer,
    ValueSerializer
)
from .serializers.v1.questionset import QuestionSetSerializer
from .serializers.v1.catalog import CatalogSerializer


class ProjectViewSetMixin(object):

    def get_projects_for_user(self, user):
        if user.is_authenticated:
            if user.has_perm('projects.view_project'):
                return Project.objects.all()
            elif is_site_manager(user):
                return Project.on_site.all()
            else:
                return Project.objects.filter(user=user)
        else:
            return Project.objects.none()


class SnapshotViewSetMixin(object):

    def get_snapshots_for_user(self, user):
        if user.is_authenticated:
            if user.has_perm('projects.view_snapshot'):
                return Snapshot.objects.all()
            elif is_site_manager(user):
                return Snapshot.on_site.all()
            else:
                return Snapshot.objects.filter(project__user=self.request.user)
        else:
            return Snapshot.objects.none()


class ValueViewSetMixin(object):

    def get_values_for_user(self, user):
        if user.is_authenticated:
            if user.has_perm('projects.view_value'):
                return Value.objects.all()
            elif is_site_manager(user):
                return Value.on_site.all()
            else:
                return Value.objects.filter(project__user=self.request.user)
        else:
            return Value.objects.none()


class ProjectViewSet(ProjectViewSetMixin, ModelViewSet):
    permission_classes = (HasModelPermission | HasObjectPermission, )
    serializer_class = ProjectSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = (
        'title',
        'user',
        'user__username',
        'catalog',
        'catalog__uri',
        'catalog__key',
    )

    def get_queryset(self):
        return self.get_projects_for_user(self.request.user)

    @action(detail=True, permission_classes=(HasModelPermission | HasObjectPermission, ))
    def resolve(self, request, pk=None):
        try:
            condition = Condition.objects.get(pk=request.GET.get('condition'))
            return Response({'result': condition.resolve(self.get_object(), None)})
        except Condition.DoesNotExist:
            return Response({'result': False})

    @action(detail=True, permission_classes=(IsAuthenticated, ))
    def catalog(self, request, pk=None):
        project = self.get_object()
        serializer = CatalogSerializer(project.catalog)
        return Response(serializer.data)

    def perform_create(self, serializer):
        project = serializer.save(site=get_current_site(self.request))

        # add current user as owner
        membership = Membership(project=project, user=self.request.user, role='owner')
        membership.save()


class ProjectNestedViewSetMixin(ProjectViewSetMixin, NestedViewSetMixin):

    def initial(self, request, *args, **kwargs):
        self.project = self.get_project_from_parent_viewset()
        super().initial(request, *args, **kwargs)

    def get_project_from_parent_viewset(self):
        try:
            return self.get_projects_for_user(self.request.user).get(pk=self.get_parents_query_dict().get('project'))
        except Project.DoesNotExist:
            raise Http404

    def get_list_permission_object(self):
        return self.project

    def get_detail_permission_object(self, obj):
        return self.project

    def perform_create(self, serializer):
        serializer.save(project=self.project)


class ProjectMembershipViewSet(ProjectNestedViewSetMixin, ModelViewSet):
    permission_classes = (HasModelPermission | HasObjectPermission, )
    queryset = Membership.objects.all()
    serializer_class = ProjectMembershipSerializer

    filter_backends = (DjangoFilterBackend, )
    filter_fields = (
        'user',
        'user__username',
        'role'
    )

    # TODO
    # def get_queryset(self):
    #     return self.get_snapshots_for_user(self.request.user)


class ProjectSnapshotViewSet(ProjectNestedViewSetMixin, SnapshotViewSetMixin,
                             CreateModelMixin, RetrieveModelMixin,
                             UpdateModelMixin, ListModelMixin, GenericViewSet):
    permission_classes = (HasModelPermission | HasObjectPermission, )
    serializer_class = ProjectSnapshotSerializer

    def get_queryset(self):
        return self.project.snapshots.all()


class ProjectValueViewSet(ProjectNestedViewSetMixin, ValueViewSetMixin, ModelViewSet):
    permission_classes = (HasModelPermission | HasObjectPermission, )
    serializer_class = ProjectValueSerializer

    filter_backends = (ValueFilterBackend, DjangoFilterBackend)
    filter_fields = (
        'snapshot',
        'attribute',
        'attribute__path',
        'option',
        'option__path',
    )

    def get_queryset(self):
        return self.project.values.filter(snapshot=None)


class ProjectQuestionSetViewSet(ProjectNestedViewSetMixin, RetrieveCacheResponseMixin, ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = QuestionSetSerializer

    def get_queryset(self):
        return QuestionSet.objects.order_by_catalog(self.project.catalog)

    @action(detail=False, permission_classes=(IsAuthenticated, ))
    def first(self, request, pk=None, parent_lookup_project=None):
        questionset = self.get_queryset().first()
        serializer = self.get_serializer(questionset)
        return Response(serializer.data)


class MembershipViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = (
        'user',
        'user__username',
        'role'
    )

    # TODO
    # def get_queryset(self):
    #     return self.get_snapshots_for_user(self.request.user)
    #
    # def get_detail_permission_object(self, obj):
    #     return obj.project


class SnapshotViewSet(SnapshotViewSetMixin, ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = Snapshot.objects.all()
    serializer_class = SnapshotSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = (
        'title',
        'project'
    )

    def get_queryset(self):
        return self.get_snapshots_for_user(self.request.user)

    def get_detail_permission_object(self, obj):
        return obj.project


class ValueViewSet(ValueViewSetMixin, ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission | HasObjectPermission, )
    serializer_class = ValueSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = (
        'project',
        'snapshot',
        'attribute',
        'attribute__path',
        'option',
        'option__path',
    )

    def get_queryset(self):
        return self.get_values_for_user(self.request.user)

    def get_detail_permission_object(self, obj):
        return obj.project
